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

# start.py
# TODO

import argparse
import subprocess
import sys

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("modrinth_id")
parser.add_argument("modrinth_version_id")
parser.add_argument("curseforge_project_id")
parser.add_argument("curseforge_version_page_link")
parser.add_argument("source_control_version_link")
parser.add_argument("manual_manifest_creation")

args = parser.parse_args()

# Choose the appropriate manifest creator based on what data was given
# subprocess.Popen([sys.executable])

if args.manual_manifest_creation == "yes":
    print("Manual manifest creation not available. Exiting") # TODO
elif args.modrinth_id != "none" and args.modrinth_version_id != "none":
    subprocess.Popen([sys.executable, "modrinth_manifest_creator.py", args.modrinth_id, args.modrinth_version_id,
                      args.curseforge_project_id,args.curseforge_version_page_link , args.source_control_version_link])

else:
    print("Bad argument combo. Exiting.")
