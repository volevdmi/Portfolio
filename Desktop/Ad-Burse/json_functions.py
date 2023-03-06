import json


def write_json(json_str, name):
    file = open(f"{name}.json", 'w')
    file.write(json_str)
    file.close()


def convert_to_json(data, name):
    json_str = json.dumps(data)
    write_json(json_str, name)


def read_json(name):
    res = json.loads(open(f"{name}.json", "r").read())
    print(res)
    return res
