import json


def read_json(list_name):
    res = json.loads(open(f"{list_name}.json", "r").read())
    print(res)
    return res

def write_json(json_str, list_name):
    file = open(f"{list_name}.json", 'w')
    file.write(json_str)
    file.close()


def list_to_json(data, list_name):
    json_str = json.dumps(data)
    write_json(json_str, list_name)
