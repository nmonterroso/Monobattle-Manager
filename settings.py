# loads local settings in local/ subdirectory. local/ should *not* be committed to source control

import os, sys, imp
try:
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent+"/local")
    imp.find_module("local_settings")
except:
    sys.stderr.write("Missing local settings file\n")
    sys.exit(1)
    
import local_settings