import copy

def equalsEnough(a, b):
    a, b = copy.copy(a), copy.copy(b)
    if type(a) != type(b):
        return False
    elif type(a) == dict:
        if len(a) != len(b):
            return False
        for k, v in a.items():
            if not equalsEnough(b[k], v):
                return False
        return True
    elif type(a) == list:
        if len(a) != len(b):
            return False
        for i in range(len(a)-1, -1, -1):
            matched = False
            for j in range(len(b)-1, -1, -1):
                if equalsEnough(a[i], b[j]):
                    del a[i]
                    del b[j]
                    matched = True
                    break
            if not matched:
                return False
        return True
    else:
        return a == b