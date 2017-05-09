from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import os
from functools import partial

# default path to xnat pass file
def path():
    return os.getenv('USERPROFILE') or os.getenv('HOME') + "/.xnatPass"

# str ->  {'host': ..., 'u': ..., 'p': ..., 'port': ...} | None
def read_xnat_pass(f):
    if os.path.exists(f) and os.path.isfile(f):
        infile = open(f)
        return parse_xnat_pass(infile.readlines())
    else:
        # raise IOError('XNAT Pass file :' + f + " does not exist")
        return None

# [str] -> {'host': ..., 'u': ..., 'p': ..., 'port':...} | None
def parse_xnat_pass(lines):
    empty = {'host': None,  'u': None, 'p': None}
    line = find_plus_line(lines)
    u = ('u',partial(find_token,'@'),True)
    host = ('host',partial(find_token,'='),True)
    p = ('p',partial(lambda x : (x,x)),True)
    
    def update_state(x,k,state):
        state[k] = x
        return state
    if line == None:
        return None
    else:
        return chain([u,host,p],line,empty,update_state)

# [(str, str -> str, bool)] ->
#  str ->
#  dict
#  dict -> dict
#  dict | None
def chain(ops, initEnv, initState, update_statef):
    env = initEnv
    state = initState
    for op in ops:
        (k,_op,mandatory) = op
        tmp = _op(env)
        if tmp == None:
            if mandatory:
                return None
        else:
            (v,rest) = tmp
            env = rest
            state = update_statef(v,k,state)
    return state
        
# [str] -> str | None
def find_plus_line(lines):
    plusLines = [x for x in lines if x.startswith('+')]
    if len(plusLines) == 0:
        return None
    else:
        return plusLines[0][1:]

# char -> str -> (str,str) | None
def find_token(tok,line):
    splitString = [x.strip() for x in line.split(tok)]
    if len(splitString) == 0 or len(splitString) == 1 or splitString[0] == '':
        return None
    else:
        return (splitString[0],splitString[1])

