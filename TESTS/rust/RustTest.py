# https://erambler.co.uk/blog/extending-python-rust-1/
# http://jakegoulding.com/rust-ffi-omnibus/string_arguments/
import sys
from ctypes import cdll
# from ctypes import c_uint32, c_char_p

extension = {'darwin': '.dylib', 'win32': '.dll'}.get(sys.platform, '.so')
lib = cdll.LoadLibrary('../../build/serindalib' + extension)

# superfluous - leaving just in case they're needed later
# lib.how_many_characters.argtypes = (c_char_p,)
# lib.how_many_characters.restype = c_uint32

# lib.print_something.argtypes = (c_char_p,)

assert(lib.how_many_characters("göes to élevên".encode('utf-8')) == 14)

# def test_rust_add():
assert(lib.add(27, 15) == 42)

lib.print_something("something goes here".encode('utf-8'))