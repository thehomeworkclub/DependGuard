import requests
import keys
from model import *
import vuln
import keys

#print(vuln.get_vuln_data("esphome", "2023.12.9", "PyPI"))

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
                requrl_newcall = f"https://libraries.io/api/pypi/{items['project_name']}/{items['latest_stable']}/dependencies?api_key={api_key[current_index]}"
                new_call = requests.get(requrl_newcall).json()
                try:
                    github_repo = new_call["repository_url"]
                    gb_parsed = github_repo.split("/")
                    resp1 = requests.get(f"https://api.github.com/repos/{gb_parsed[3]}/{gb_parsed[4]}/contributors?per_page=1&anon=true", headers=keys.headers).headers
                    dels = [",", ";"]
                    for dela in dels:
                        pages = " ".join(resp1["Link"].split(dela))
                    pages = pages.split()[2].strip(">").strip("<").split("&")[2].split("=")[1]
                    rejs_list.append([items["project_name"], str(items["latest_stable"]), str(pages), str(new_call["latest_release_published_at"])])
                    print(pages)
                except:
                    pages = None
                rejs_list.append([items["project_name"], str(items["latest_stable"]), str(pages), str(None)])
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
print(get_dep_tree("matplotlib", "3.7.5"))