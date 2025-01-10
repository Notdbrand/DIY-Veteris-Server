# Difteris

This GitHub repository contains the code for a custom server built for Veteris 1.7.2, as well as the code and .deb file for a redirect tweak that enables Veteris to use any URL.

This server is not affiliated with or endorsed by Electimon or InvoxiPlayGames. If you encounter issues, please email me or open an issue in this repository instead of contacting them.


## Part 1: Difteris Server Setup

### Requirements
- **Python 3**
- Libraries: Flask, Pillow, packaging
  ```bash
  pip install Flask Pillow packaging
  ```
- **.NET Core 3.1 or higher** (required for IPA Sorter)

### Step 1: Download the Difteris Server
Download the server files and place them in your desired directory.

### Step 2: Prepare IPA Files
1. Place all the IPAs for your first category into the `New_IPAs` folder.
2. Run `IPASorter.exe` from the command line. (Running via command line will display any errors.)
    - You can also double-click it to run, but errors won't be visible.
3. Processed IPAs will be categorised into folders based on their minimum iOS requirements. Any failed apps will be moved to the `incomplete` folder.

**Example of folder structure:**  
![Folder Example](https://github.com/user-attachments/assets/8139b949-cfed-48d0-a34d-d5bd9979baa2)

**Example of a processed IPA:**  
![Processed IPA Example](https://github.com/user-attachments/assets/80b3f204-0f00-47f8-a488-1f8499c250e0)

### Step 3: Index IPAs
Run `1_Index_New_IPAS.py`:
- Enter the name for the category you want the apps you are scanning to be put under.
- Specify whether you want the IPAs moved automatically. If selected, the folder structure `static/ipas/(Category Name)` will be created if it doesn’t already exist and the ipas will be moved.

### Step 4: Index IPA Icons
Run `2_Index_IPA_Icons.py`:
- This script scans all new IPAs and retrieves their icons. If an icon isn’t found, a placeholder image is used.
- Icons are stored in `static/icons` and named using the IPA’s bundle ID.

### Step 5: Start the Difteris Server
Run `3_Difteris_Server.py`:
- The server will run on port **5010** (this cannot currently be changed, as the tweak only modifies the IP).

### Adding More IPAs
To add additional IPAs to new or existing categories, repeat Steps 2, 3, and 4. For existing categories, ensure you type the category name exactly.


## Part 2: Veteris Client Setup

### Step 1: Downgrade Veteris
There are two methods to downgrade:
1. Use Cydia’s downgrade option.
2. Uninstall Veteris. Then download and install the .deb file from [Archive.org](https://web.archive.org/web/20231119205614/https://yzu.moe/dev/packs/Veteris-v1.7.2.deb).

### Step 2: Download Veteris Redirect
Install Veteris Redirect:
- From this repository `VeterisRedirect/packages/com.notdbrand.veterisredirect_1.7.2-4+debug_iphoneos-arm.deb`.
- Or from my repo at [https://notdbrand.com/repo](https://notdbrand.com/repo).
- Alternatively, compile it yourself using Theos.

### Step 3: Configure the Tweak
1. Open **Settings** and navigate to **Veteris Redirect**.
2. Enter the IP address or URL of your server. (Do **not** include `http://` or the port number.)

### Step 4: Apply the Tweak
1. Click the back button.
2. Re-enter the tweak page to ensure the address is saved.
   - Simply hitting respring won’t save the address (most of the time).
3. Now hit the respring button.


## Enjoy
You should now be able to start Veteris, which will connect to your server.

Feel free to submit issues or pull requests for feature suggestions or bug reports.


## Other Projects Used
- [**IPA Sorter**](https://github.com/kawaiizenbo/IPASorter) - Made by kawaiizenbo - I slightly modified the processed ipa's filename. [Version used in this project](https://github.com/Notdbrand/IPASorter)

