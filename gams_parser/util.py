
def get_path(obj,path):
    keys = path.split('.')
    for k in keys:
        try:
            obj = obj[k]
        except KeyError:
            return None
    return obj

def set_path(obj,path,value):
	keys = path.split('.')
	for k in keys[:-1]:
		if k not in obj.keys():
			obj[k] = {}
		obj = obj[k]
	obj[keys[-1]] = value