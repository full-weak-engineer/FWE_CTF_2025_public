import json
import tarfile
import zipfile
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import urllib.parse

URL = "http://localhost:8000/"
API = f"{URL}api/v1/"
token = os.environ.get("CTFD_TOKEN", "")

s = requests.session()
s.headers.update({"Authorization": f"Token {token}", "Content-Type": "application/json"})

r = s.get(f"{API}configs")
configs_arr = r.json()["data"]

config = {}
for config_entry in configs_arr:
    config[config_entry["key"]] = config_entry["value"]

if os.path.exists("cache.json"):
    with open("cache.json", "r", encoding="utf-8") as f:
        challenges = json.load(f)
else:
    r = s.get(f"{API}challenges")
    challenges = r.json()["data"]

    for challenge in challenges:
        r = s.get(f"{API}challenges/{challenge["id"]}")
        c = r.json()["data"]
        challenge["attribution"] = c["attribution"]
        challenge["description"] = c["description"]
        r = s.get(f"{API}challenges/{challenge["id"]}/flags")
        challenge["flags"] = []
        for flag in r.json()["data"]:
            if flag["type"] == "static":
                challenge["flags"].append(flag["content"])
    with open("cache.json", "w", encoding="utf-8") as f:
        json.dump(challenges, f)



    
table = "|ジャンル|問題名|作問者|タグ|最終スコア|Solve数|Writeup|\n"
table += f"|{"---|"*7}\n"

for c in challenges:
    tags = ", ".join([tag["value"] for tag in c["tags"]]) if len(c["tags"]) > 0 else ""
    path = urllib.parse.quote(f"{c["category"].replace("/", "_")}/{c["name"].replace("/", "_")}")
    table += f"|{c["category"]}|[{c["name"]}]({path})|{c["attribution"]}|{tags}|{c["value"]}|{c["solves"]}||\n"


markdown = (
    f"#{config["ctf_name"]}\n\n"
    f"## Event dates\n\n"
    f"{datetime.fromtimestamp(int(config['start']), ZoneInfo("Asia/Tokyo")).strftime("%Y.%m.%d %-H:%M")} ~ {datetime.fromtimestamp(int(config['end']), ZoneInfo("Asia/Tokyo")).strftime("%Y.%m.%d %-H:%M")} (JST)\n\n"
    f"## Challenges\n\n"
    f"{table}"
)
with open(f"index.md", "w") as f:
    f.write(markdown)

for c in challenges:
    dir_name = f"{c["category"].replace("/", "_")}/{c["name"].replace("/", "_")}"
    os.makedirs(f"{dir_name}/attachment/", exist_ok=True)
    markdown = (
        f"# {c["name"]}\n\n" + 
        f"|ジャンル|問題名|作問者|タグ|最終スコア|Solve数|\n" + 
        f"|{"---|"*6}\n" +
        f"|{c["category"]}|{c["name"]}|{c["attribution"]}|{tags}|{c["value"]}|{c["solves"]}|\n" + 
        f"## Description(問題文)\n\n" + 
        f"{c["description"]}\n\n" +
        f"## Flag\n\n" + 
        f"{"\n".join([f"`{flag}`" for flag in c["flags"]])}\n\n"
    )
    with open(f"{dir_name}/README.md", "w") as f:
        f.write(markdown)

    r = s.get(f"{API}challenges/{c["id"]}/files")
    file_data = r.json()["data"]
    for fd in file_data:
        loc = fd["location"]
        filename = os.path.basename(loc)
        filepath = f"{dir_name}/attachment/{filename}"
        root, ext = os.path.splitext(filename)
        r = s.get(f"{URL}files/{loc}")
        with open(filepath, "wb") as f:
            f.write(r.content)
        if ext == ".zip":
            with zipfile.ZipFile(filepath, 'r') as z:
                z.extractall(path=f"{dir_name}/attachment")
        elif ext == ".gz" and os.path.splitext(root)[1] == ".tar":
            with tarfile.open(filepath, 'r') as t:
                t.extractall(path=f"{dir_name}/attachment", filter='data')

# Export pages

os.makedirs("./pages", exist_ok=True)

r = s.get(f"{API}pages")
for page_info in r.json()["data"]:
    r = s.get(f"{API}pages/{page_info["id"]}")
    page_content = r.json()["data"]
    filename = page_content["route"]
    filename += ".html" if page_content["format"] == "html" else ".md"
    with open(f"pages/{filename}", "w") as f:
        f.write(page_content["content"])

# Export logos

os.makedirs("./files", exist_ok=True)

root, ext = os.path.splitext(config["ctf_logo"])

r = s.get(f"{URL}files/{config["ctf_logo"]}")
with open(f"files/ctf_logo{ext}", "wb") as f:
    f.write(r.content)
    
root, ext = os.path.splitext(config["ctf_small_icon"])

r = s.get(f"{URL}files/{config["ctf_small_icon"]}")
with open(f"files/ctf_small_icon{ext}", "wb") as f:
    f.write(r.content)