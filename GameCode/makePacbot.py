class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def getPacbot(pacbot_pos, pacbot_direction):
    pacbot = {}
    pacbot["pos"] = pacbot_pos
    pacbot["direction"] = pacbot_direction
    return dotdict(pacbot)