import os
import json
import re
import random
import shutil
from packaging import version

source_folder = "New_IPAs"
output_apps_file = "data/apps.json"
output_categories_file = "data/categories.json"
static_ipas_folder = "static/ipas"

os.makedirs(os.path.dirname(output_apps_file), exist_ok=True)

filename_pattern = re.compile(
    r"^(?P<name>.+)-\((?P<bundleid>.+)\)-\((?P<version>.+)\)-\((?P<required_os>.+)\)-\((?P<md5>[a-f0-9]{32})\)\.ipa$"
)

# Load categories data
if os.path.exists(output_categories_file):
    with open(output_categories_file, "r") as f:
        categories_data = json.load(f)
else:
    categories_data = {"categories": []}

def get_category_id(category_name):
    for category in categories_data["categories"]:
        if category["name"].lower() == category_name.lower():
            return category["id"]
    return generate_unique_id()

def generate_unique_id():
    used_ids = {int(category["id"]) for category in categories_data["categories"]}
    while True:
        new_id = random.randint(1, 1000)
        if new_id not in used_ids:
            used_ids.add(new_id)
            return new_id

# Ensure there are IPA files in the source folder
ipa_files_found = False
ipa_files_matching = False

for root, _, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".ipa"):
            ipa_files_found = True
            if filename_pattern.match(file):
                ipa_files_matching = True
                break
    if ipa_files_matching:
        break

if not ipa_files_found:
    print("No new IPAs found.")
    exit()

if not ipa_files_matching:
    print("No IPAs matching the required filename format found.")
    exit()

# Get category name and ID
category_name = input("Enter the category name: ").strip()
category_id = get_category_id(category_name)

if category_id not in [category["id"] for category in categories_data["categories"]]:
    categories_data["categories"].append({"id": str(category_id), "name": category_name})
    with open(output_categories_file, "w") as f:
        json.dump(categories_data, f, indent=4)

# Load apps data
if os.path.exists(output_apps_file):
    with open(output_apps_file, "r") as f:
        apps_data = json.load(f)
else:
    apps_data = {"applications": []}

def parse_filename(filename):
    match = filename_pattern.match(filename)
    if match:
        data = match.groupdict()
        ipa_version = data["version"]
        required_os = data["required_os"].replace("iOS_", "")  #  Can't be bothered to re-compile IPA_Sorter to remove iOS_ from filename.
        clean_name = data["name"][1:-1]
        return {
            "name": clean_name,
            "developer": "Unknown",
            "bundleid": data["bundleid"],
            "requiredOS": required_os,
            "ipadApp": "ipad" in data["name"].lower(),
            "description": f"It's {clean_name}. What more is there to know?",
            "fileName": filename,
            "category": int(category_id),
            "iconurl": f"static/icons/{data['bundleid']}.png",
            "version_data": {ipa_version: f"static/ipas/{category_name}/{filename}"}
        }
    return None

def add_or_update_application(apps_data, app_data):
    for app in apps_data["applications"]:
        if app["bundleid"] == app_data["bundleid"]:
            app["versions"].append(app_data["version_data"])
            app["versions"] = sorted(
                app["versions"], key=lambda v: version.parse(next(iter(v.keys())))
            )
            return

    apps_data["applications"].append({
        "name": app_data["name"],
        "developer": app_data["developer"],
        "bundleid": app_data["bundleid"],
        "requiredOS": app_data["requiredOS"],
        "ipadApp": app_data["ipadApp"],
        "description": app_data["description"],
        "fileName": app_data["fileName"],
        "category": app_data["category"],
        "iconurl": app_data["iconurl"],
        "versions": [app_data["version_data"]]
    })

def scan_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipa"):
                yield parse_filename(file), os.path.join(root, file)

ipa_files = []
for app_data, file_path in scan_directory(source_folder):
    if app_data:
        add_or_update_application(apps_data, app_data)
        ipa_files.append((file_path, app_data["fileName"]))

with open(output_apps_file, "w") as f:
    json.dump(apps_data, f, indent=4)

print(f"Scan complete. Data written to {output_apps_file}")
print(f"Category '{category_name}' with ID {category_id} added to {output_categories_file}")

move_files = input(f"Do you want to move all IPAs to static/ipas/{category_name}? (Y/N): ").strip().lower()
if move_files == "y":
    category_folder = os.path.join(static_ipas_folder, category_name)
    os.makedirs(category_folder, exist_ok=True)
    for src_path, filename in ipa_files:
        dest_path = os.path.join(category_folder, filename)
        shutil.move(src_path, dest_path)
    print(f"All IPAs have been moved to {category_folder}")
else:
    print("No files were moved. Now you have to move it manually. ._.")

# You reviewed the code :D
# -NDB