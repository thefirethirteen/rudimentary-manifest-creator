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

# options_creator.py
# Creates an `options.json` file

import argparse
import json

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("modrinth_id")
parser.add_argument("modrinth_version_id")
parser.add_argument("curseforge_project_id")
parser.add_argument("curseforge_version_page_link")
parser.add_argument("source_control_version_link")
parser.add_argument("manual_manifest_creation")

args = parser.parse_args()

processed_args = {}

if args.modrinth_id != "None":
    processed_args.update({"modrinth_id": args.modrinth_id})
else:
    processed_args.update({"modrinth_id": None})

if args.modrinth_version_id != "None":
    processed_args.update({"modrinth_version_id": args.modrinth_version_id})
else:
    processed_args.update({"modrinth_version_id": None})

if args.curseforge_project_id != "None":
    processed_args.update({"curseforge_project_id": args.curseforge_project_id})
else:
    processed_args.update({"curseforge_project_id": None})

if args.curseforge_version_page_link != "None":
    processed_args.update({"curseforge_version_page_link": args.curseforge_version_page_link})
else:
    processed_args.update({"curseforge_version_page_link": None})

if args.source_control_version_link != "None":
    processed_args.update({"source_control_version_link": args.source_control_version_link})
else:
    processed_args.update({"source_control_version_link": None})

if args.manual_manifest_creation == "True":
    processed_args.update({"manual_manifest_creation": True})
else:
    processed_args.update({"manual_manifest_creation": False})

with open("options.json", 'w') as options_file:
    options_file.write(json.dumps(processed_args, indent=4))
