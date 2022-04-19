"""
MIT License

Copyright (c) 2022 thefirethirteen

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# modrinth_manifest_creator.py
# Creates a manifest using modrinth

import argparse
import subprocess
import sys
import time
import json
import urllib.parse
import requests
# import hashlib
import os

# Get options
parser = argparse.ArgumentParser()
parser.add_argument("options_file_name")
args = parser.parse_args()

with open(args.options_file_name, 'rt') as options_file:
    options = json.loads(options_file.read())

# "Constants"
BLOCKSIZE = 65536
MODRINTH_API_PROJECT_PREFIX = "https://api.modrinth.com/v2/project/"
MODRINTH_API_VERSION_PREFIX = "https://api.modrinth.com/v2/version/"
FABRIC_EXTRACTOR_LINK = "https://raw.githubusercontent.com/thefirethirteen/modinfo-file-extractor/main/" \
                        "fabric_extractor_main.py"
CHUNK_SIZE = 1024

# Get required scripts
fabric_extractor_response = requests.get(FABRIC_EXTRACTOR_LINK)

with open("fabric_extractor.py", 'wb') as fabric_extractor_file:
    fabric_extractor_file.write(fabric_extractor_response.content)

fabric_extractor_response.close()

# Get modrinth version info
modrinth_link = MODRINTH_API_VERSION_PREFIX + options["modrinth_version_id"]
modrinth_api_response = requests.get(modrinth_link)
with open("./modrinth_version_json.json", 'wb') as modrinth_json:
    modrinth_json.write(modrinth_api_response.content)
with open("./modrinth_version_json.json", 'r') as modrinth_json:
    modrinth_version_data = json.load(modrinth_json)

# Cleanup
modrinth_api_response.close()
os.remove("./modrinth_version_json.json")

# Get the modfile
modfile_url = modrinth_version_data["files"][0]["url"]
modfile_name = modrinth_version_data["files"][0]["filename"]

modfile_response = requests.get(modfile_url, stream=True)
with open(modfile_name, "wb") as modfile_file:
    for chunk in modfile_response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            modfile_file.write(chunk)

modfile_response.close()

"""
# Process file using the fabric extractor
subprocess.Popen([sys.executable, "fabric_extractor.py", args.mod_file])
time.sleep(1)

# Move the file to the working directory and cleanup
os.rename("./extracted/" + args.mod_file + ".json", args.mod_file + ".json")
fabric_json_filename = args.mod_file + ".json"

os.removedirs("./extracted")
os.remove("fabric_extractor.py")
"""

# Process file using the fabric extractor and cleanup
subprocess.Popen([sys.executable, "fabric_extractor.py", modfile_name])
time.sleep(1)

os.remove(modfile_name)

# Move the file to the working directory and cleanup
os.rename("./extracted/" + modfile_name + ".json", modfile_name + ".json")
fabric_json_filename = modfile_name + ".json"

os.removedirs("./extracted")
os.remove("fabric_extractor.py")

# Load the fabric data and cleanup
with open(fabric_json_filename, 'r') as fabric_json_file:
    fabric_json_data = json.load(fabric_json_file)

os.remove(fabric_json_filename)

# Make the manifest
python_manifest_data = {"schemaVersion": "1.0.0"}

# Get modrinth project info
modrinth_link = MODRINTH_API_PROJECT_PREFIX + options["modrinth_id"]
modrinth_api_response = requests.get(modrinth_link)
with open("./modrinth_project_json.json", 'wb') as modrinth_json:
    modrinth_json.write(modrinth_api_response.content)
with open("./modrinth_project_json.json", 'r') as modrinth_json:
    modrinth_project_data = json.load(modrinth_json)

# Cleanup
modrinth_api_response.close()
os.remove("./modrinth_project_json.json")

python_manifest_data.update({"fancyName": modrinth_project_data["title"]})

if modrinth_project_data["source_url"] is not None:
    source_control_url = modrinth_project_data["source_url"]
    if "github.com" in source_control_url:
        github_api_base_url = "https://api.github.com/repos"
        github_path = urllib.parse.urlparse(source_control_url).path
        github_link = github_api_base_url + github_path

        github_api_response = requests.get(github_link)
        with open("./github_repo_json.json", 'wb') as github_json:
            github_json.write(github_api_response.content)
        with open("./github_repo_json.json", 'r') as github_json:
            github_repo_data = json.load(github_json)

        github_api_response.close()
        os.remove("./github_repo_json.json")

        python_manifest_data.update({"author": github_repo_data["owner"]["login"]})
    else:
        modrinth_api_response = requests.get(modrinth_link + "/members")
        with open("./modrinth_team_json.json", 'wb') as modrinth_json:
            modrinth_json.write(modrinth_api_response.content)
        with open("./modrinth_team_json.json", 'r') as modrinth_json:
            modrinth_team_data = json.load(modrinth_json)

        modrinth_api_response.close()
        os.remove("./modrinth_team_json.json")

        for i in range(len(modrinth_team_data)):
            if modrinth_team_data[i]["role"] == "Owner":
                python_manifest_data.update({"author": modrinth_team_data[i]["username"]})

if modrinth_project_data["license"]["id"] != "custom":
    python_manifest_data.update({"license": modrinth_project_data["license"]["id"]})
else:
    python_manifest_data.update({"license": modrinth_project_data["license"]["url"]})

if options["curseforge_project_id"] is not None:
    python_manifest_data.update({"curseForgeId": options["curseforge_project_id"]})
else:
    python_manifest_data.update({"curseForgeId": None})

python_manifest_data.update({"modrinthId": modrinth_project_data["id"]})

python_manifest_data.update({"links": {"issue": modrinth_project_data["issues_url"]}})
python_manifest_data["links"].update({"sourceControl": modrinth_project_data["source_url"]})

python_manifest_data["links"].update({"others": []})
if modrinth_project_data["wiki_url"] is not None:
    python_manifest_data["links"]["others"].append({"linkName": "Wiki",
                                                    "url": modrinth_project_data["wiki_url"]})
if modrinth_project_data["discord_url"] is not None:
    python_manifest_data["links"]["others"].append({"linkName": "Discord",
                                                    "url": modrinth_project_data["discord_url"]})
for i in range(len(modrinth_project_data["donation_urls"])):
    python_manifest_data["links"]["others"].append({"linkName": modrinth_project_data["donation_urls"][i]["platform"],
                                                    "url": modrinth_project_data["donation_urls"][i]["url"]})

python_manifest_data.update({"files": []})

"""
hasher = hashlib.sha1()
with open(args.mod_file, 'rb') as hfile:
    buffer = hfile.read(BLOCKSIZE)
    while len(buffer) > 0:
        hasher.update(buffer)
        buffer = hfile.read(BLOCKSIZE)
"""

mod_download_links = [modrinth_version_data["files"][0]["url"]]
if options["source_control_version_link"] is not None:
    mod_download_links.append(options["source_control_version_link"])
if options["curseforge_version_page_link"] is not None:
    curseforge_download_link = options["curseforge_version_page_link"].replace("files", "download") + "/file"
    mod_download_links.append(curseforge_download_link)


python_manifest_data["files"].append({"fileName": modfile_name,
                                      "mcVersions": modrinth_version_data["game_versions"],
                                      "sha1Hash": modrinth_version_data["files"][0]["hashes"]["sha1"],
                                      "downloadUrls": mod_download_links})

# Write the manifest
manifest_file_name = fabric_json_data["id"] + ".json"
with open(manifest_file_name, 'w') as manifest_file:
    manifest_file.write(json.dumps(python_manifest_data, indent=4))
