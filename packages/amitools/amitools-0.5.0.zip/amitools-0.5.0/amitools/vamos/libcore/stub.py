from types import MethodType
import time
import traceback

from amitools.vamos.machine.regs import REG_D0, REG_D1, REG_A7


class LibStub(object):
    """a lib stub is a frontend object instance that wraps all calls into
     a library implementation.

     It is suitable for binding these functions to traps of the machine
     emulation.

     A wrapped call return value processing or optional profiling features.
  """

    def __init__(self, name, fd, impl=None, profile=None):
        """create a stub for a given implementation and
       associated fd description"""
        self.name = name
        self.impl = impl
        self.fd = fd
        # a table with all methods mapped via index
        self.func_tab = [None] * fd.get_num_indices()
        # (optional) attach profile object
        self.profile = profile
        self.log_exc = None

    def get_func_tab(self):
        return self.func_tab

    def _get_callee_pc(self, ctx):
        """a call stub log helper to extract the callee's pc"""
        sp = ctx.cpu.r_reg(REG_A7)
        return ctx.mem.r32(sp)

    def _gen_arg_dump(self, args, ctx):
        """a call stub helper to dump the registers of a call"""
        if args == None or len(args) == 0:
            return ""
        result = []
        for a in args:
            name = a[0]
            reg = a[1]
            reg_num = int(reg[1])
            if reg[0] == "a":
                reg_num += 8
            val = ctx.cpu.r_reg(reg_num)
            result.append("%s[%s]=%08x" % (name, reg, val))
        return ", ".join(result)

    def _handle_exc(self):
        """default exception handler"""
        traceback.print_exc()
        raise


class LibStubGen(object):
    """the lib stub generator scans a lib impl and creates stubs for all
     methods found there"""

    def __init__(self, log_missing=None, log_valid=None, ignore_invalid=True):
        self.log_missing = log_missing
        self.log_valid = log_valid
        self.ignore_invalid = ignore_invalid

    def gen_fake_stub(self, name, fd, ctx, profile=None):
        """a fake stub exists without an implementation and only contains
       "missing" functions
    """
        # create stub object
        stub = LibStub(name, fd, profile=profile)

        # iterate all functions in fd
        for fd_func in fd.get_funcs():
            stub_func = self.wrap_missing_func(fd_func, ctx, profile)
            self._set_method(fd_func, stub, stub_func)

        return stub

    def gen_stub(self, impl_scan, ctx, profile=None):
        # create stub object
        name = impl_scan.get_name()
        fd = impl_scan.get_fd()
        impl = impl_scan.get_impl()
        stub = LibStub(name, fd, impl, profile)

        # generate valid funcs
        valid_funcs = list(impl_scan.get_valid_funcs().values())
        for fd_func, impl_method in valid_funcs:
            stub_func = self.wrap_func(fd_func, impl_method, ctx, profile)
            self._set_method(fd_func, stub, stub_func)

        # generate missing funcs
        missing_funcs = list(impl_scan.get_missing_funcs().values())
        for fd_func in missing_funcs:
            stub_func = self.wrap_missing_func(fd_func, ctx, profile)
            self._set_method(fd_func, stub, stub_func)

        # return final stub
        return stub

    def _set_method(self, fd_func, stub, stub_func):
        # bind method to stub instance
        stub_method = MethodType(stub_func, stub)
        # store in stub
        setattr(stub, fd_func.get_name(), stub_method)
        # add to func tab
        index = fd_func.get_index()
        stub.func_tab[index] = stub_method

    def wrap_missing_func(self, fd_func, ctx, profile):
        """create a stub func for a missing function in impl
       returns an unbound method for the stub instance
    """
        log = self.log_missing
        if log is None:
            # without tracing
            def stub_func(this, *args, **kwargs):
                # return d0=0
                ctx.cpu.w_reg(REG_D0, 0)

        else:
            name = fd_func.get_name()
            func_args = fd_func.get_args()
            bias = fd_func.get_bias()
            # with tracing

            def stub_func(this, *args, **kwargs):
                callee_pc = this._get_callee_pc(ctx)
                call_info = "%4d %s( %s ) from PC=%06x" % (
                    bias,
                    name,
                    this._gen_arg_dump(func_args, ctx),
                    callee_pc,
                )
                log.warning("? CALL: %s -> d0=0 (default)", call_info)
                ctx.cpu.w_reg(REG_D0, 0)

        func = stub_func

        # wrap profiling?
        if profile:
            index = fd_func.get_index()
            prof = profile.get_func_by_index(index)

            def profile_func(this, *args, **kwargs):
                stub_func(this, *args, **kwargs)
                prof.count(0.0)

            func = profile_func

        # return created func
        return func

    def wrap_func(self, fd_func, impl_method, ctx, profile):
        """create a stub func for a valid impl func
       returns an unbound method for the stub instaance
    """

        def base_func(this, *args, **kwargs):
            """the base function to call the impl,
         set return vals, and catch exceptions"""
            res = impl_method(ctx)
            if res is not None:
                if type(res) in (list, tuple):
                    ctx.cpu.w_reg(REG_D0, res[0] & 0xFFFFFFFF)
                    ctx.cpu.w_reg(REG_D1, res[1] & 0xFFFFFFFF)
                else:
                    ctx.cpu.w_reg(REG_D0, res & 0xFFFFFFFF)
            return res

        func = base_func

        # wrap around logging method?
        log = self.log_valid
        if log:
            name = fd_func.get_name()
            func_args = fd_func.get_args()
            bias = fd_func.get_bias()

            def log_func(this, *args, **kwargs):
                callee_pc = this._get_callee_pc(ctx)
                call_info = "%4d %s( %s ) from PC=%06x" % (
                    bias,
                    name,
                    this._gen_arg_dump(func_args, ctx),
                    callee_pc,
                )
                log.info("{ CALL: %s" % call_info)
                res = base_func(this, *args, **kwargs)
                if res is not None:
                    if type(res) in (list, tuple):
                        res_str = "d0=%08x, d1=%08x" % tuple(res)
                    else:
                        res_str = "d0=%08x" % res
                else:
                    res_str = "n/a"
                log.info("} CALL: -> %s" % res_str)

            func = log_func

        # wrap profiling?
        if profile:
            index = fd_func.get_index()
            prof = profile.get_func_by_index(index)
            if log:
                call = log_func
            else:
                call = base_func

            def profile_func(this, *args, **kwargs):
                start = time.perf_counter()
                call(this, *args, **kwargs)
                end = time.perf_counter()
                delta = end - start
                prof.count(delta)

            func = profile_func

        return func
