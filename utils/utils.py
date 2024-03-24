import requests
from utils.model import * 
#import utils.vuln
import utils.keys as keys
from utils.vuln import get_vuln_data

#print(vuln.get_vuln_data("esphome", "2023.12.9", "PyPI"))

# Error Codes: 
# 1 - Not an Error
# 2 - Ratelimit Exceeded for All Keys
# 3 - Im not going to fix this
# 4 - Not Found
complete = []
deps = []
api_key = keys.keylist
current_index = 0
current_recursive = 0
def get_dep_tree(library, version, pkgmngr="pypi"):
    print("[LOG] RUNNING GET_DEP_TREE ON " + library + "@" + version)
    global current_index
    global complete
    # TODO: Check if in db, if yes then dont run, if no then run (main pkg)
    requrl = f"https://libraries.io/api/{pkgmngr}/{library}/{version}/dependencies?api_key={api_key[current_index]}"
    resp = requests.get(requrl)
    if resp.status_code == 429:
        if current_index >= (len(api_key)-1):
            return 2
        else:
            current_index += 1
            return get_dep_tree(library, version)
    if version == "latest":
        check = Dblk.select().where(Dblk.package == library, Dblk.version == resp.json()["latest_release_number"])
    else:
        check = Dblk.select().where(Dblk.package == library, Dblk.version == version)
    print(len(check))
    try:
        rejs = resp.json()["dependencies"]
        if version == "latest":
            vers_behind = 0
        else:
            try:
                vers = resp.json()["versions"][::-1]
                vers_behind = 0
                for items in vers:
                    if items["number"] == version:
                        break
                    vers_behind+=1
            except:
                vers_behind = 0
                print("failed")
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
                except:
                    pages = None
                    rejs_list.append([items["project_name"], str(items["latest_stable"]), str(pages), str(None)])
        if len(check) == 0:
            if version != "latest":
                Dblk.create(package=library, subdeps=rejs_list, version=version, v_behind=vers_behind)
            else:
                Dblk.create(package=library, subdeps=rejs_list, version=new_call["latest_stable_release_number"], v_behind=vers_behind)
        else:
            print("Already in DB")
        complete.append(library)
        for items in rejs_list:
            if items[0] in complete:
                pass
            else:
                get_dep_tree(items[0], items[1])
        return 1
    except:
        pass
def get_flat_tree(library):
    global deps
    global current_recursive
    if current_recursive == 0:
        deps = []
    get_mod = list(Dblk.select().where(Dblk.package == library).dicts())
    if len(list(get_mod)) > 0:
        for items in list(get_mod[0]["subdeps"]):
            if items not in deps:
                deps.append(items)
            current_recursive+=1
            get_flat_tree(items[0])
        current_recursive = 0
        return deps
    else:
        pass
def get_tree_rec(library):
    global deps
    global current_recursive
    global contscore
    rcv = {} # Initialize rcv as a dictionary to hold the entire tree
    if current_recursive == 0:
        deps = []
    get_mod = list(Dblk.select().where(Dblk.package == library).dicts())
    if len(get_mod) > 0:
        v_behind = get_mod[0]["v_behind"]
        print(v_behind)
        for items in get_mod[0]["subdeps"]:
            # Assuming items[0] is the library name and the rest are details
            print(items)
            library_name, version, contributors, date = items[0], items[1], items[2], items[3]
            # Recursive call to get the dependencies of each sub-dependency
            results = get_tree_rec(library_name)
            # Integrate the results into the rcv dictionary
            if library not in rcv:
                rcv[library] = {"v_behind": v_behind, "dependencies": {}}
            rcv[library]["dependencies"][library_name] = {
                "version": version,
                "contributors": contributors,
                "date": date,
                "dependencies": results
            }
            #start making scores
            # Calculate the score based on the number of contributors

        return rcv
    else:
        return {} # Return an empty dictionary if no dependencies are found
    
def createscore(library, version):
    global contscore
    cnt_score = 0
    amt = 0
    rcv = list(get_flat_tree(library))
    for items in rcv:
        try:
            contributors = int(items[2])
            print(contributors)
            if contributors <= 10:
                cnt_score += 10
            elif contributors <= 20:
                cnt_score += 9
            elif contributors <= 30:
                cnt_score += 8
            elif contributors <= 40:
                cnt_score += 7
            elif contributors <= 50:
                cnt_score += 6
            elif contributors <= 60:
                cnt_score += 5
            elif contributors <= 70:
                cnt_score += 4
            elif contributors <= 80:
                cnt_score += 3
            elif contributors <= 90:
                cnt_score += 2
            elif contributors >= 100:
                cnt_score += 1
            amt += 1
        except:
            pass

    vulndict = get_vuln_data(library, version, "PyPI")
    if vulndict == []:
        vuln_score = 0
    else:
        vuln_score = vulndict[0]["CVSS Score"]
    return {"community_score": round(cnt_score/amt, 1), "vulnerability_score": vuln_score}

        
    
createscore("beautifulsoup4", "4.11.1")
print(get_tree_rec("beautifulsoup4"))


def get_reqs_github(github):
    url = github.split("/")
    resp1 = requests.get(f"https://api.github.com/repos/{url[3]}/{url[4]}/contents", headers=keys.headers).json()
    reqs_url = ""
    for items in resp1:
        if items['name'] == "requirements.txt":
            reqs_url = items['download_url']
            break
    if reqs_url == "":
        return 4
    else:
        fsgh = requests.get(reqs_url, headers=keys.headers).text.replace(" ", "").split("\n")
        fsgh = fsgh[0:len(fsgh)-1]
        fsgh_imp = []
        for items in fsgh:
            items = items.split("==")
            if len(items) < 2:
                fsgh_imp.append([items[0], "latest"])
            else:
                fsgh_imp.append([items[0], items[1]])
        return fsgh_imp
