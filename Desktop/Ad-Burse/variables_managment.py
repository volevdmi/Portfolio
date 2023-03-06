import os

import json_functions

# -------------------------------------------

if os.stat("users_id.json").st_size != 0:
    users_id = json_functions.read_json("users_id")
else:
    users_id = []
    json_functions.convert_to_json(users_id, "users_id")

# --------------------------------------------
# users_role = {user_id: status}
# status : 0 - not registered 1 - seller 2 - buyer 3 - seller and buyer

if os.stat("users_role.json").st_size != 0:
    users_role = json_functions.read_json("users_role")
else:
    users_role = {}
    for user_id in users_id:
        users_role[user_id] = 0
    json_functions.convert_to_json(users_role, "users_role")


# ---------------------------------------------
networks = ["telegram", "youtube", "instagram", "facebook"]


if os.stat("users_registration_form.json").st_size != 0:
    users_registration_form = json_functions.read_json("users_registration_form.json")
else:
    users_registration_form = {}
    for user_id in users_id:
        users_registration_form[user_id] = []
    json_functions.convert_to_json(users_registration_form, "users_registration_form")


