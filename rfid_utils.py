__author__ = 'amaurial'

def is_integer(s):
    try:
        int(s) # for int, long and float
    except ValueError:
        return False

    return True
