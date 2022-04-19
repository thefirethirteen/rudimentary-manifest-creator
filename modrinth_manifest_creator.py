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
# Creates a manifest

import argparse
import subprocess
import sys
import time
import json
import requests
# import hashlib
import os

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("modrinth_id")
parser.add_argument("curseforge_id")
parser.add_argument("modrinth_version_id")

args = parser.parse_args()

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

# Get modrinth version info, if it exists
if args.modrinth_version_id != "null":
    modrinth_link = MODRINTH_API_VERSION_PREFIX + args.modrinth_version_id
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

# Get modrinth project info, if it exists
if args.modrinth_id != "null":
    modrinth_link = MODRINTH_API_PROJECT_PREFIX + args.modrinth_id
    modrinth_api_response = requests.get(modrinth_link)
    with open("./modrinth_project_json.json", 'wb') as modrinth_json:
        modrinth_json.write(modrinth_api_response.content)
    with open("./modrinth_project_json.json", 'r') as modrinth_json:
        modrinth_project_data = json.load(modrinth_json)

    # Cleanup
    modrinth_api_response.close()
    os.remove("./modrinth_project_json.json")

if args.modrinth_id != "null":
    python_manifest_data.update({"fancyName": modrinth_project_data["title"]})
    python_manifest_data.update({"author": "TODO"})  # TODO

    if modrinth_project_data["license"]["id"] != "custom":
        python_manifest_data.update({"license": modrinth_project_data["license"]["id"]})
    else:
        python_manifest_data.update({"license": modrinth_project_data["license"]["url"]})

if args.curseforge_id != "null":
    python_manifest_data.update({"curseForgeId": args.curseforge_id})
else:
    python_manifest_data.update({"curseForgeId": None})

if args.modrinth_id != "null":
    python_manifest_data.update({"modrinthId": args.modrinth_id})
else:
    python_manifest_data.update({"modrinthId": None})

if args.modrinth_id != "null":
    python_manifest_data.update({"links": {"issue": modrinth_project_data["issues_url"]}})
    python_manifest_data["links"].update({"sourceControl": modrinth_project_data["source_url"]})

    python_manifest_data["links"].update({"others": []})
    if modrinth_project_data["wiki_url"] is not None:
        python_manifest_data["links"]["others"].append({"linkName": "Discord",
                                                        "url": modrinth_project_data["wiki_url"]})
    if modrinth_project_data["discord_url"] is not None:
        python_manifest_data["links"]["others"].append({"linkName": "Discord",
                                                        "url": modrinth_project_data["discord_url"]})

    if len(python_manifest_data["links"]["others"]) == 0:
        python_manifest_data["links"].update({"others": None})

python_manifest_data.update({"files": []})

"""
hasher = hashlib.sha1()
with open(args.mod_file, 'rb') as hfile:
    buffer = hfile.read(BLOCKSIZE)
    while len(buffer) > 0:
        hasher.update(buffer)
        buffer = hfile.read(BLOCKSIZE)
"""

python_manifest_data["files"].append({"fileName": modfile_name, "mcVersions": modrinth_version_data["game_versions"],
                                      "sha1Hash": modrinth_version_data["files"][0]["hashes"]["sha1"],
                                      "downloadUrls": ["TODO"]}) # TODO

manifest_json_file_name = fabric_json_data["id"] + ".json"

# Write the manifest
with open(manifest_json_file_name, 'w') as manifest_json_file:
    manifest_json_file.write(json.dumps(python_manifest_data, indent=4))
