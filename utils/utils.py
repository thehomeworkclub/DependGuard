import requests
import keys
from model import *


# Error Codes: 
# 1 - Not an Error
# 2 - Ratelimit Exceeded for All Keys
# 3 - Im not going to fix this
complete = []
api_key = keys.keylist
current_index = 0
def get_dep_tree(library, version):
    global current_index
    global complete
    requrl = f"https://libraries.io/api/pypi/{library}/{version}/dependencies?api_key={api_key[current_index]}"
    resp = requests.get(requrl)
    if resp.status_code == 429:
        if current_index >= (len(api_key)-1):
            return 2
        else:
            current_index += 1
            return get_dep_tree(library, version)
    try:
        rejs = resp.json()["dependencies"]
        rejs_list = []
        for items in rejs:
            if items in complete or items["kind"] != "runtime":
                pass
            else:
                resp1 = requests.get()
                rejs_list.append([items["project_name"], str(items["latest_stable"])])
        Dblk.create(package=library, subdeps=rejs_list)
        complete.append(library)
        for items in rejs_list:
            if items[0] in complete:
                pass
            else:
                get_dep_tree(items[0], items[1])
        return 1
    except:
        pass