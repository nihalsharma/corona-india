import os
import sys


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ENV = os.environ.get('ENV')
print("Using ENV: " + str(ENV))


def import_settings(name):
    try:
        mod = __import__(name, fromlist=[name])
        thismod = sys.modules[__name__]
        for attr in dir(mod):
            if (attr.isupper()) and (not attr.startswith('__')):
                print(getattr(mod, attr))
                setattr(thismod, attr, getattr(mod, attr))
    except ImportError as e:
        print(BColors.FAIL + "Unable to import " + name + BColors.ENDC)
        print(e)

import_settings("settings." + str(ENV))
