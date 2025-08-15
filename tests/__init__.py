# import imp
# import importlib
# import os.path
# import sys
#
# modname = 'tests.create_new.example'
#
# i = modname.rfind(".")
# modname = modname[i + 1:]
# paths = [os.path.normpath('create_new/'), '.']
#
# print(os.path.abspath('create_new'))
# print(sys.path)
# (stream, filename, (suffix, mode, kind)) = imp.find_module(modname, paths)
