import os
import subprocess

CLOUD_LIST = ["onedrive", "dropbox", "mega", "gdrive"]
CLOUD_STRING = ["OneDrive", "Dropbox", "Mega", "Google Drive"]
SEL_CLOUD = 0
MOUNT_DIR = os.path.expanduser(f"~/{CLOUD_STRING[SEL_CLOUD].replace(' ', '')}")

def create_mount_dir():
    if not os.path.isdir(MOUNT_DIR):
        print(f"Creating mount directory: {MOUNT_DIR}")
        os.makedirs(MOUNT_DIR)

def mount_drive():
    print(f"Mounting {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.Popen(["rclone", "mount", f"{CLOUD_LIST[SEL_CLOUD]}:", MOUNT_DIR, "--vfs-cache-mode", "writes"])
    print(f"{CLOUD_STRING[SEL_CLOUD]} mounted to {MOUNT_DIR}")

if __name__ == "__main__":
    create_mount_dir()
    mount_drive()