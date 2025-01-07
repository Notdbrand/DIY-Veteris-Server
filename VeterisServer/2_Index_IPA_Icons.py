import os
import zipfile
from PIL import Image
import shutil
from io import BytesIO
import re
import json

ipa_directory = 'static/ipas'
icon_directory = 'static/icons'
default_icon_path = 'data/default.png'
scanned_file_path = 'data/scanned.json'

def load_scanned_files():
    if os.path.exists(scanned_file_path):
        with open(scanned_file_path, 'r') as file:
            data = json.load(file)
            return data.get("scanned_ipas", [])
    return []

def save_scanned_files(scanned_files):
    with open(scanned_file_path, 'w') as file:
        json.dump({"scanned_ipas": scanned_files}, file, indent=4)

def extract_icon_from_ipa(ipa_path, bundle_id):
    with zipfile.ZipFile(ipa_path, 'r') as ipa:
        for file in ipa.namelist():
            if 'itunesartwork' in file.lower():
                image_data = ipa.read(file)
                return image_data, file

        app_icons = []
        for file in ipa.namelist():
            if 'appicon' in file.lower():
                app_icons.append(file)

        if app_icons:
            largest_icon = max(app_icons, key=lambda x: len(x))
            image_data = ipa.read(largest_icon)
            return image_data, largest_icon
        
    return None, None

def save_icon(icon_data, bundle_id):
    clean_bundleID = bundle_id[1:-1]
    
    if not os.path.exists(icon_directory):
        os.makedirs(icon_directory)

    try:
        icon_image = Image.open(BytesIO(icon_data))
        icon_image.verify()
        icon_image = Image.open(BytesIO(icon_data))
        output_path = os.path.join(icon_directory, f"{clean_bundleID}.png")
        icon_image.save(output_path)
        print(f"Icon saved for {clean_bundleID} at {output_path}")
    except (OSError, Image.UnidentifiedImageError) as e:
        print(f"Failed to save icon for {clean_bundleID}: {e}")
        shutil.copy(default_icon_path, os.path.join(icon_directory, f"{clean_bundleID}.png"))

def process_ipas():
    bundle_ids = {}
    pattern = re.compile(r'^(.*?)\-(.*?)\-(.*?)\-(.*?)\-(.*?)\.ipa$')
    scanned_files = load_scanned_files()
    new_icons_found = False

    for root, _, files in os.walk(ipa_directory):
        for file in files:
            if file.endswith('.ipa') and file not in scanned_files:
                match = pattern.match(file)
                if match:
                    name, bundle_id, ipa_version, required_os, md5 = match.groups()
                    ipa_path = os.path.join(root, file)
                    ipa_size = os.path.getsize(ipa_path)

                    if bundle_id in bundle_ids:
                        existing_ipa_path = bundle_ids[bundle_id]['path']
                        existing_ipa_size = bundle_ids[bundle_id]['size']

                        if ipa_size > existing_ipa_size:
                            os.remove(existing_ipa_path)
                            bundle_ids[bundle_id] = {'path': ipa_path, 'size': ipa_size}
                        elif ipa_size == existing_ipa_size:
                            os.remove(existing_ipa_path)
                            bundle_ids[bundle_id] = {'path': ipa_path, 'size': ipa_size}
                    else:
                        bundle_ids[bundle_id] = {'path': ipa_path, 'size': ipa_size}

    for bundle_id, ipa_info in bundle_ids.items():
        ipa_path = ipa_info['path']
        
        icon_data, icon_name = extract_icon_from_ipa(ipa_path, bundle_id)

        if icon_data:
            save_icon(icon_data, bundle_id)
            new_icons_found = True
        else:
            shutil.copy(default_icon_path, os.path.join(icon_directory, f"{bundle_id}.png"))
            print(f"No icon found for {bundle_id}, using default.")

        scanned_files.append(os.path.basename(ipa_path))

    save_scanned_files(scanned_files)

    if not new_icons_found:
        print("No new icons")

if __name__ == '__main__':
    process_ipas()

# You reviewed the code :O
# -NDB