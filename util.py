
def equalsEnough(a, b):
    if type(a) == dict:
        if len(a) != len(b):
            return False
        for k, v in a.items():
            if b[k] != v:
                return False
        return True
    if type(a) == list:
        return sorted(a) == sorted(b)