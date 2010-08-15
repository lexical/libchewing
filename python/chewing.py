from ctypes import *
from functools import partial

_libchewing = CDLL('libchewing.so.3')
_libchewing.chewing_handle_Default.argtypes = [c_void_p, c_char]
_libchewing.chewing_commit_String.restype = c_char_p
_libchewing.chewing_buffer_String.restype = c_char_p

def Init(datadir, userdir):
    return _libchewing.chewing_Init(datadir, userdir)

class ChewingContext:
    def __init__(self):
        self.ctx = _libchewing.chewing_new()
    def __del__(self):
        _libchewing.chewing_free(self.ctx)
    def __getattr__(self, name):
        func = 'chewing_' + name
        if func in _libchewing.__dict__:
            wrap = partial(_libchewing.__dict__[func], self.ctx)
            setattr(self, name, wrap)
            return wrap
        elif hasattr(_libchewing, func):
            wrap = partial(_libchewing.__getattr__(func), self.ctx)
            setattr(self, name, wrap)
            return wrap
        else:
            raise AttributeError, name
    def Configure(self, cpp, maxlen, direction, space, kbtype):
        self.set_candPerPage(cpp)
        self.set_maxChiSymbolLen(maxlen)
        self.set_addPhraseDirection(direction)
        self.set_spaceAsSelection(space)
        self.set_KBType(kbtype)
