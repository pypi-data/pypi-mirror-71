import amitools.util.ByteSize as ByteSize


class DiskGeometry:
    def __init__(self, cyls=0, heads=0, secs=0, block_bytes=512):
        self.cyls = cyls
        self.heads = heads
        self.secs = secs
        self.block_bytes = block_bytes

    def __str__(self):
        size = self.get_num_bytes()
        return "chs=%d,%d,%d bs=%d size=%d/%s" % (
            self.cyls,
            self.heads,
            self.secs,
            self.block_bytes,
            size,
            ByteSize.to_byte_size_str(size),
        )

    def get_num_blocks(self):
        """return the number of block allocated by geometry"""
        return self.cyls * self.heads * self.secs

    def get_num_bytes(self):
        """return the number of bytes allocated by geometry"""
        return self.get_num_blocks() * self.block_bytes

    def _update_block_size(self, options):
        if options and "bs" in options:
            bs = int(options["bs"])
            if bs % 512 != 0 or bs < 512:
                raise ValueError("invalid block size given: %d" % bs)
            self.block_bytes = bs

    def detect(self, byte_size, options=None):
        """detect a geometry from a given image size and optional options.
       return bytes required by geometry or None if geomtry is invalid
    """
        c = None
        h = None
        s = None
        self._update_block_size(options)
        num_blocks = byte_size // self.block_bytes
        algo = None
        if options != None:
            (c, h, s) = self._parse_chs(options)
            if "algo" in options:
                algo = int(options["algo"])
        # chs if fully specified then take this one
        if c != None and h != None and s != None:
            self.cyls = c
            self.heads = h
            self.secs = s
            size = self.get_num_bytes()
            if size == byte_size:
                return size
            else:
                return None
        else:
            return self._guess_for_size(byte_size, algo=algo, secs=s, heads=h)

    def setup(self, options):
        """setup a new geometry by giving options
       return bytes required by geometry or None if geometry is invalid
    """
        if options == None:
            return False
        c = None
        h = None
        s = None
        (c, h, s) = self._parse_chs(options)
        self._update_block_size(options)
        # chs is fully specified
        if c != None and h != None and s != None:
            self.cyls = c
            self.heads = h
            self.secs = s
            return self.get_num_bytes()
        else:
            # we require a size
            if "size" not in options:
                return None
            # parse size
            size = options["size"]
            if type(size) != int:
                size = ByteSize.parse_byte_size_str(size)
                if size == None:
                    return None
            # select guess algo
            algo = None
            if "algo" in options:
                algo = int(options["algo"])
            # guess size
            return self._guess_for_size(size, approx=True, algo=algo, secs=s, heads=h)

    def _parse_chs(self, options):
        c = None
        h = None
        s = None
        # chs=<n>,<n>,<n>
        if "chs" in options:
            comp = options["chs"].split(",")
            if len(comp) == 3:
                return [int(x) for x in comp]
        else:
            if "s" in options:
                s = int(options["s"])
            if "h" in options:
                h = int(options["h"])
            if "c" in options:
                c = int(options["c"])
        return (c, h, s)

    def _guess_for_size1(self, size, approx=True, secs=None, heads=None):
        mb = size // 1024
        if secs == None:
            secs = 63
        if heads == None:
            if mb <= 504 * 1024:
                heads = 16
            elif mb <= 1008 * 1024:
                heads = 32
            elif mb <= 2016 * 1024:
                heads = 64
            elif mb <= 4032 * 1024:
                heads = 128
            else:
                heads = 256
        cyls = (size // self.block_bytes) // (secs * heads)
        geo_size = cyls * secs * heads * self.block_bytes
        # keep approx values or match
        if approx or geo_size == size:
            self.cyls = cyls
            self.heads = heads
            self.secs = secs
            return geo_size
        else:
            return None

    def _guess_for_size2(self, size, approx=True, secs=None, heads=None):
        if heads == None:
            heads = 1
        if secs == None:
            secs = 32
        cyls = (size // self.block_bytes) // (secs * heads)
        # keep cyls low
        while cyls > 65535:
            cyls //= 2
            heads *= 2
        # keep approx values or match
        geo_size = cyls * secs * heads * self.block_bytes
        if approx or geo_size == size:
            self.cyls = cyls
            self.heads = heads
            self.secs = secs
            return geo_size
        else:
            return None

    def _guess_for_size(self, size, approx=True, algo=None, secs=None, heads=None):
        if algo == 1:
            return self._guess_for_size1(size, approx, secs, heads)
        elif algo == 2:
            return self._guess_for_size2(size, approx, secs, heads)
        else:
            algos = [self._guess_for_size1, self._guess_for_size2]
            if approx:
                # find min diff to real size
                min_diff = size
                min_algo = None
                for a in algos:
                    s = a(size, True, secs, heads)
                    if s != None:
                        delta = abs(size - s)
                        if delta < min_diff:
                            min_diff = delta
                            min_algo = a
                if min_algo != None:
                    return min_algo(size, True, secs, heads)
                else:
                    return None
            else:  # exact match
                for a in algos:
                    s = a(size, True, secs, heads)
                    if s == size:
                        return size
                return None
