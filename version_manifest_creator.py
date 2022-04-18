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

# version_manifest_creator.py
# Creates a version manifest

import sys
import subprocess
import json
import time
import yaml
import shutil

# Get file to process
file = sys.argv[1]

# Process file using the fabric extractor
subprocess.Popen([sys.executable, "fabric_extractor.py", file])
time.sleep(1)

# Make the manifest
json_filename = file + ".json"
path_prefix = "./extracted/"

with open(path_prefix + json_filename, 'r') as json_file:
    json_data = json.load(json_file)

loader_data = {'loaders': ["fabric"]}
minecraft_version_data = {'minecraftVersions': json_data["depends"]["minecraft"]}

manifest_data = [loader_data, minecraft_version_data]

with open(json_data["version"] + ".yaml", 'w') as version_manifest:
    yaml.dump(manifest_data, version_manifest)

# Cleanup
shutil.rmtree("./extracted")
