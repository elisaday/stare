# -*- coding: utf_8 -*-
"""
    created: 2007-11-5
    author: Zeb
    e-mail: zebbey@gmail.com
"""

__builtins__['MESSAGE_SEPERATOR'] = '$'

def __show_trace():
    import traceback
    import StringIO
    import sys
    
    excinfo = sys.exc_info()
    sio = StringIO.StringIO()
    traceback.print_exception(excinfo[0], excinfo[1], excinfo[2], None, sio)
    s = sio.getvalue()
    print traceback.format_exc()
    sio.close()
    
__builtins__['SHOW_TRACE'] = __show_trace

__id = 0
def __getId():
    __id += 1
    return __id
    
__builtins__['GET_ID'] = __getId

__builtins__['USER_ROOT'] = './data/user/'