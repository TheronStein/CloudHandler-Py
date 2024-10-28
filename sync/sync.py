import os
import subprocess
import time

CLOUD_LIST = ["onedrive", "dropbox", "mega", "gdrive"]
CLOUD_STRING = ["OneDrive", "Dropbox", "Mega", "Google Drive"]
SEL_CLOUD = 0
LOCAL_SYNC_DIR = os.path.expanduser("~/LocalSync")
REMOTE_DIR = "/path/to/onedrive/folder"  # Adjust the remote path as needed
SYNC_INTERVAL = 1300  # Sync interval in seconds

def sync_drive():
    print(f"Syncing local directory with {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.run(["rclone", "sync", LOCAL_SYNC_DIR, f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}"])
    print("Sync complete.")

def bisync_drive():
    print(f"Bi-directionally syncing {CLOUD_STRING[SEL_CLOUD]} with local directory...")
    subprocess.run(["rclone", "bisync", LOCAL_SYNC_DIR, f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}"])
    print("Bi-directional sync complete.")

def verify_sync():
    print(f"Verifying sync with {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.run(["rclone", "check", LOCAL_SYNC_DIR, f"{CLOUD_LIST[SEL_CLOUD]}:{REMOTE_DIR}"])

def dedupe_drive():
    print(f"Deduplicating {CLOUD_STRING[SEL_CLOUD]}...")
    subprocess.run(["rclone", "dedupe", f"{CLOUD_LIST[SEL_CLOUD]}:"])

if __name__ == "__main__":
    while True:
        sync_drive()
        verify_sync()
        dedupe_drive()
        time.sleep(SYNC_INTERVAL)