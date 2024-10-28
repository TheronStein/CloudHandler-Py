import os
import subprocess
import time

CLOUD_LIST = ["onedrive", "dropbox", "mega", "gdrive"]
CLOUD_STRING = ["OneDrive", "Dropbox", "Mega", "Google Drive"]
SEL_CLOUD = 0
LOCAL_SYNC_DIR = os.path.expanduser("~/LocalSync")
REMOTE_DIR = "/path/to/onedrive/folder"  # Adjust the remote path as needed
SYNC_INTERVAL = 1300  # Sync interval in seconds

def check_sync():
    print(f"Checking for differences between local directory and {CLOUD_STRING[SEL_CLOUD]}...")
    result = subprocess.run(["rclone", "check", LOCAL_SYNC_DIR, f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}"], capture_output=True, text=True)
    differences = result.stdout
    if differences:
        handle_differences(differences)

def handle_differences(differences):
    for line in differences.split('\n'):
        if 'ERROR' in line:
            parts = line.split()
            if len(parts) > 1:
                file_path = parts[-1]
                print(f"Handling difference for file: {file_path}")
                # Determine if the local file is newer or older than the cloud file
                # Use rclone lsl to get file modification times and sizes
                local_info = subprocess.run(["rclone", "lsl", os.path.join(LOCAL_SYNC_DIR, file_path)], capture_output=True, text=True).stdout.strip()
                remote_info = subprocess.run(["rclone", "lsl", f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}/{file_path}"], capture_output=True, text=True).stdout.strip()
                
                if local_info and remote_info:
                    local_time = int(local_info.split()[0])
                    remote_time = int(remote_info.split()[0])
                    if local_time > remote_time:
                        print(f"Local file {file_path} is newer, copying to cloud.")
                        subprocess.run(["rclone", "copy", os.path.join(LOCAL_SYNC_DIR, file_path), f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}"])
                    else:
                        print(f"Cloud file {file_path} is newer, copying to local.")
                        subprocess.run(["rclone", "copy", f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}/{file_path}", LOCAL_SYNC_DIR])