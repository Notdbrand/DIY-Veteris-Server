# Difteris  
This github repo contains the code for a custom server that was built for veteris 1.7.2, as well as the code and deb for a redirect tweak that can change veteris to use any url.  
This server was not made by or related to Electimon or InvoxiPlayGames, so if there is a problem with anything on this github repo, don't bug them. Instead email me or open an issue in this github repo.  

## Part 1: Difteris Server Setup  
### Requirements:  
Python 3  
And these other libraries; Flask, Pillow, packaging.
<pre> pip install Flask Pillow packaging </pre>  
  
Minimum of .NET Core 3.1 (Just for IPA sorter)  
    
### Step 1: Download Difteris Server  
Download the server files and place it where ever you want.  
  
### Step 2: Prepare IPA files  
- a. Place all the IPAs that you want for your first category into the folder called "New_IPAs".  
- b. Now run IPASorter.exe from the command line (The time it takes will depend of your computers specs and the amount of ipas you are scanning). You can just run it by double clicking it, but commandline will show you any errors, if any happen.  
- c. All the processed ipas should be in folders that are named with their minimum os. Any failed apps will be moved to "incomplete".  
Example of folders:  
![image](https://github.com/user-attachments/assets/8139b949-cfed-48d0-a34d-d5bd9979baa2)  
Example of processed ipa:  
![image](https://github.com/user-attachments/assets/80b3f204-0f00-47f8-a488-1f8499c250e0)  

### Step 3: Scanning IPAs  
Run 1_Index_New_IPAS.py  
It will prompt you to enter the name you want for the category of the apps you are about to scan.  
Next, it will ask you if want the ipas moved automatically. This will (if it doesn't exist already) the folder structue static/ipas/(The Category name entered).  
Select no if you don't want them moved.  

### Step 4: Scanning IPAs Icons  
Run 2_Index_IPA_Icons.py  
This will scan all new ipas, and get their icon. If an ipas icon isn't found, a placeholder is used.  
All icons are located in static/icons, and the images are named with their ipas bundle ID.  

### Step 5: Starting Difteris  
Run 3_Difteris_Server.py  
The server will be running on port 5010. You can not change this, this is because my tweak only changes the IP address, not the port number. (Might fix this in the future)  

### Adding more ipas:  
To add more ipas to either new categories or existing ones, follow steps 2, 3 and 4 again.  
You can add ipas to existing categories by typing the exact name the category you want to add to. 
  
  
## Part 2: Veteris client setup  
### Step 1: Downgrade Veteris  
There is two methods to downgrading  
- 1: Downgrade using cydia's downgrade option  
- 2: Uninstall Veteris and download the deb archive.org (https://web.archive.org/web/20231119205614/https://yzu.moe/dev/packs/Veteris-v1.7.2.deb)  
  
### Step 2: Download Veteris Redirect  
Install Veteris redirect either from within this github or install it from my repo at https://notdbrand.com/repo  
Or if you want to complie it yourself, use theos to compile the tweak.
  
### Step 3: Configure the tweak  
To configure the tweak go to setting a scroll down to Veteris Redirect then go into the setting.  
In the Veteris Redirect page enter just the ip address or url for your server. Don't include http:// or the port number.  
  
### Step 4: Apply the tweak  
Now to apply the redirect click the back button then go back into the tweak page.  
This is because if you just hit respring it won't save the address.  
  
  
## Enjoy  
Now you should be able to start veteris and it should connect to your server.  
  
Feel free to submit an issue or pull request for feature suggestions or bug reports.

## Other Projects used  
IPA Sorter - Made by kawaiizenbo  
https://github.com/kawaiizenbo/IPASorter
