import os
import time
import subprocess

CLOUD_LIST = ["onedrive", "dropbox", "mega", "gdrive"]
CLOUD_STRING = ["OneDrive", "Dropbox", "Mega", "Google Drive"]
SEL_CLOUD = 0
MOUNT_DIR = os.path.expanduser(f"~/{CLOUD_STRING[SEL_CLOUD].replace(' ', '')}")
SYNC_INTERVAL = 1300  # Check every half hour

def check_mount():
    if not os.path.ismount(MOUNT_DIR):
        print(f"{CLOUD_STRING[SEL_CLOUD]} is not mounted, attempting to mount...")
        subprocess.run(["python3", "mount.py"])
    else:
        print(f"{CLOUD_STRING[SEL_CLOUD]} is already mounted.")

def check_size():
    print(f"Checking size of {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.run(["rclone", "size", f"{CLOUD_LIST[SEL_CLOUD]}:"])

def check_quota():
    print(f"Checking quota of {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.run(["rclone", "about", f"{CLOUD_LIST[SEL_CLOUD]}:"])

if __name__ == "__main__":
    while True:
        check_mount()
        check_size()
        check_quota()
        time.sleep(SYNC_INTERVAL)