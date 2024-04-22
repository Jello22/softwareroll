#Installation UI for forklift setup
#This could be used for any other software rollout on any platform that supports .exe

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import subprocess
import shutil
import glob

#Setup your configurations to be called down later.  Add more as needed this one sets up Wireless on a windows device via NETSH using XML files, copies some files, and then installs some software or not
configurations = {
    "Configuration Name 1": {"wireless_batch_file": "bat1.bat", "shortcuts_subfolder": "foldername", "install_software": True},
    "Configuration Name 2": {"wireless_batch_file": "bat2.bat", "shortcuts_subfolder": "foldername", "install_software": false},
    }

#add wireless 
def setup_wireless(wireless_batch_file):
    # Path to the directory containing the batch files
    batch_file_path = r'\\networkpath\to\wirelessprofile\xml'

    # Complete path to the batch file
    full_path = f"{batch_file_path}\\{wireless_batch_file}"

    # Execute the batch file
    try:
        result = subprocess.run([full_path], capture_output=True, text=True, check=True)
        print(f"Wireless setup successful. Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Wireless setup failed. Error:\n{e.stderr}")
    except Exception as ex:
        print(f"An error occurred setting up wireless: {ex}")

def install_software():
    # Software installation path from UNC
    exe_path = r'\\networkpath\to\some\softwareinstall\someexe.exe'
    install_command = [exe_path, '/silent']

    # Execute the executable
    try:
        result = subprocess.run(install_command, capture_output=True, text=True, check=True)
        print("Installation successful. Output:\n", result.stdout)

        # Path of the file you want to copy say a license file
        source_file = r'\\networkpath\bla\bla\licensefile.lic'
        
        # Destination path where you want to copy the file
        destination_path = r'C:\Program Files (x86)\softwareinstall'
        
        # Copy the file
        shutil.copy(source_file, destination_path)
        print(f"File copied successfully to {destination_path}")

    except subprocess.CalledProcessError as e:
        print("Installation failed. Error:\n", e.stderr)
    except shutil.Error as copy_error:
        print("Failed to copy file. Error:\n", copy_error)
    except Exception as ex:
        print("An error occurred:", ex)

# Function to update the Public Desktop with shortcuts
def update_public_desktop(shortcuts_subfolder):
    public_desktop_path = r'C:\Users\Public\Desktop'
    shortcuts_source = os.path.join(r'\\networkpath\towhereyouhave\yourshortcut\folders\Shortcuts', shortcuts_subfolder)
    
    # Clear everything on the Public Desktop
    for item in os.listdir(public_desktop_path):
        item_path = os.path.join(public_desktop_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)  # Remove all the existing icons on public desktop
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directories

    # Copy all .lnk files from the specified subfolder to the Public Desktop
    pattern = os.path.join(shortcuts_source, '*.lnk')
    for shortcut_path in glob.glob(pattern):
        shutil.copy(shortcut_path, public_desktop_path)
        print(f"Copied {os.path.basename(shortcut_path)} to Public Desktop.")

#call another program in this example say you want to auto logon for a kiosk or maybe you want to do something else I don know?
def launch_autologon():
    autologon_path = r'\\uncpath\setupautologoin\powertoy\Autologon.exe'
    
    # Execute the Autologon application
    try:
        subprocess.Popen([autologon_path])
        print("Autologon launched successfully.")
    except Exception as ex:
        print(f"An error occurred while launching Autologon: {ex}")

#Define task actions
#when the user clicks the button what actions are going to fire off ?
def execute_setup(profile_name):
    status_label.config(text=f"Starting setup for: {profile_name}")
    root.update_idletasks()  # Update GUI

    profile = configurations[profile_name]

    if 'wireless_batch_file' in profile:
        status_label.config(text="Setting up wireless...")
        root.update_idletasks()
        setup_wireless(profile['wireless_batch_file'])

    if profile.get('install_software', False):
        status_label.config(text="Installing Software...")
        root.update_idletasks()
        install_anita()

    status_label.config(text="Updating Public Desktop with shortcuts...")
    root.update_idletasks()
    update_public_desktop(profile['shortcuts_subfolder'])  
    
    status_label.config(text=f"Setup completed for {profile_name}.")
    root.update_idletasks()

     # Launch Autologon at the end of the setup
    launch_autologon()

    print(f"Setup completed for {profile_name}.")

#Make a super not generic UI
def create_gui():
    global root, status_label
    root = tk.Tk()
    root.title("Configuration Setup")

    for profile_name in configurations:
        action = lambda name=profile_name: execute_setup(name)  # Ensure the correct profile is used
        ttk.Button(root, text=profile_name, command=action).pack(pady=5, padx=10, fill='x')

    status_label = ttk.Label(root, text="Ready. Select a configuration to begin setup.")
    status_label.pack(pady=20)

    root.mainloop()

    root.mainloop()

create_gui()



