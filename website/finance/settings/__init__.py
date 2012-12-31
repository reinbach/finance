try:
    from .currentenv import *
except ImportError:
    print ('Error importing settings/currentenv.py. Did you forget to symlink your '
           'local settings?')

    import traceback
    print traceback.print_exc()