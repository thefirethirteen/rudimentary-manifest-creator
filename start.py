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
import json
import subprocess
import sys

# Get options
parser = argparse.ArgumentParser()
parser.add_argument("options_file_name")
args = parser.parse_args()

with open(args.options_file_name, 'rt') as options_file:
    options = json.loads(options_file.read())

# Choose the appropriate manifest creator based on what data was given

if options["manual_manifest_creation"] is True:
    print("Manual manifest creation not available. Exiting") # TODO
elif options["modrinth_id"] is not None and options["modrinth_version_id"] is not None:
    subprocess.Popen([sys.executable, "modrinth_manifest_creator.py", args.options_file_name])

else:
    print("Bad option combo. Exiting.")
