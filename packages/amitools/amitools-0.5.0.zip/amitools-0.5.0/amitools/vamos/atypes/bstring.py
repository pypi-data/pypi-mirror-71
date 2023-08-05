class BString(object):
    """Manage BCPL-Strings in Amiga memory.

  The string is immutable as changing strings typically requires
  re-allocating memory for it.
  """

    def __init__(self, mem, addr, alloc=None, mem_obj=None, max_size=None):
        self.mem = mem
        self.addr = addr
        self.alloc = alloc
        self.mem_obj = mem_obj
        self.baddr = addr >> 2
        self.max_size = max_size
        assert self.addr & 3 == 0

    def __str__(self):
        return self.get_string()

    def __int__(self):
        return self.addr

    def __repr__(self):
        return "BString(@%06x:%s)" % (self.addr, self.get_string())

    def __eq__(self, other):
        if type(other) is int:
            return self.addr == other
        elif type(other) is str:
            return self.get_string() == other
        elif isinstance(other, BString):
            return self.addr == other.addr
        else:
            return NotImplemented

    def get_mem(self):
        return self.mem

    def get_addr(self):
        return self.addr

    def get_baddr(self):
        return self.baddr

    def get_max_size(self):
        return self.max_size

    def get_size(self):
        return len(self.get_string())

    def get_string(self):
        if self.addr == 0:
            return None
        else:
            return self.mem.r_bstr(self.addr)

    def set_string(self, txt):
        if self.max_size:
            if len(txt) > self.max_size:
                raise ValueError("new string too long!")
        if self.addr == 0:
            raise ValueError("bstr is NULL")
        else:
            return self.mem.w_bstr(self.addr, txt)

    def free(self):
        if self.alloc:
            self.alloc.free_bstr(self.mem_obj)
            self.mem_obj = None
            self.alloc = None
            self.addr = 0
            self.max_size = 0

    @staticmethod
    def alloc(alloc, txt, tag=None):
        """allocate memory for the given txt with the allocator

    Returns a BString object with allocation info.
    You can free() the object later on
    """
        if type(txt) is BString:
            return txt
        if tag is None:
            tag = "BString('%s')" % txt
        mem = alloc.get_mem()
        # NULL ptr
        if txt is None:
            mem_obj = None
            alloc = None
            addr = 0
            n = 0
        # valid string
        else:
            mem_obj = alloc.alloc_bstr(tag, txt)
            addr = mem_obj.addr
            n = len(txt)
        return BString(mem, addr, alloc, mem_obj, n)
