# https://www.journaldev.com/31907/calling-c-functions-from-python
# also for more reference https://realpython.com/python-bindings-overview/

# The purpose of this file is so that
from ctypes import *
so_file = "../../build/myFunctions.so"
my_functions = CDLL(so_file)
print(type(my_functions))
print(my_functions.square(12))
print(my_functions.square(8))
