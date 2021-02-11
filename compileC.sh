# https://www.journaldev.com/31907/calling-c-functions-from-python
# also for more reference https://realpython.com/python-bindings-overview/
cc -fPIC -shared -o ./build/myFunctions.so ./serinda/plugin/OpenCVPlugin/CFilters/myFunctions.c