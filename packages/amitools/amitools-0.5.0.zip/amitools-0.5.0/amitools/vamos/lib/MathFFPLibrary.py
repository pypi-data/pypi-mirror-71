from amitools.vamos.machine.regs import *
from amitools.vamos.libcore import LibImpl
from amitools.vamos.log import log_math
from amitools.util.Math import *


class MathFFPLibrary(LibImpl):
    def SPFix(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        if arg > Amiga_INT_MAX:
            arg = Amiga_INT_MAX
        elif arg < Amiga_INT_MIN:
            arg = Amiga_INT_MIN
        res = int(arg)
        log_math.info("SPFix(%s) = %s", arg, res)
        return res

    def SPFlt(self, ctx):
        i = int32(ctx.cpu.r_reg(REG_D0))
        d = float(i)
        log_math.info("SPFlt(%s) = %s", i, d)
        return float_to_ffp_reg(d)

    def SPCmp(self, ctx):
        arg1 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        arg2 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        if arg1 < arg2:
            res = -1
        elif arg1 > arg2:
            res = +1
        else:
            res = 0
        log_math.info("SPCmp(%s, %s) = %s", arg1, arg2, res)
        return res

    def SPTst(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        if arg < 0.0:
            res = -1
        elif arg > 0.0:
            res = +1
        else:
            res = 0
        log_math.info("SPTst(%s) = %s", arg, res)
        return res

    def SPAbs(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        if arg < 0.0:
            res = -arg
        else:
            res = arg
        log_math.info("SPAbs(%s) = %s", arg, res)
        return float_to_ffp_reg(res)

    def SPAdd(self, ctx):
        arg1 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        arg2 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        res = arg1 + arg2
        log_math.info("SPAdd(%s, %s) = %s", arg1, arg2, res)
        return float_to_ffp_reg(res)

    def SPSub(self, ctx):
        arg1 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        arg2 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        res = arg1 - arg2
        log_math.info("SPSub(%s, %s) = %s", arg1, arg2, res)
        return float_to_ffp_reg(res)

    def SPMul(self, ctx):
        arg1 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        arg2 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        res = arg1 * arg2
        log_math.info("SPMul(%s, %s) = %s", arg1, arg2, res)
        return float_to_ffp_reg(res)

    def SPDiv(self, ctx):
        arg1 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        arg2 = ffp_reg_to_float(ctx.cpu.r_reg(REG_D1))
        if arg2 == 0.0:
            if arg1 == 0.0:
                # Amiga returns sign bit set on nan...
                res = float("-nan")
            elif arg1 > 0.0:
                res = float("inf")
            else:
                res = float("-inf")
        else:
            res = arg1 / arg2
        log_math.info("SPDiv(%s, %s) = %s", arg1, arg2, res)
        return float_to_ffp_reg(res)

    def SPFloor(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        res = math.floor(arg)
        log_math.info("SPFloor(%s) = %s", arg, res)
        return float_to_ffp_reg(res)

    def SPCeil(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        res = math.ceil(arg)
        log_math.info("SPCeil(%s) = %s", arg, res)
        return float_to_ffp_reg(res)

    def SPNeg(self, ctx):
        arg = ffp_reg_to_float(ctx.cpu.r_reg(REG_D0))
        res = -arg
        log_math.info("SPNeg(%s) = %s", arg, res)
        return float_to_ffp_reg(res)
