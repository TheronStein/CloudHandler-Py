import os
import subprocess
import sys
import time
from getpass import getpass

RCLONE_CONFIG_DIRPATH = os.getenv('RCLONE_CONFIG_DIRPATH', os.path.expanduser('~/.config/rclone'))

def check_dependency(dependency):
    if not shutil.which(dependency):
        print(f"Error: {dependency} is required to run backup")
        sys.exit(3)

def get_password(prompt):
    while True:
        password = getpass(prompt)
        if password:
            return password
        else:
            print(f"{prompt} cannot be blank")

def create_archive(archive_filepath, backup_dirs):
    dirs_to_tar = ' '.join(backup_dirs.split(':'))
    result = subprocess.run(['tar', '-czf', archive_filepath, *dirs_to_tar.split()], check=True)
    if result.returncode != 0:
        print("Error: could not create archive.")
        sys.exit(1)
    print(f"Created archive: {archive_filepath}")

def encrypt_file(unencrypted_filepath, encrypted_filepath):
    password = os.getenv('ENCRYPT_RCLONE_PASSWORD', get_password("Password: "))
    result = subprocess.run(['gpg', '-q', '--symmetric', '--passphrase', password, '-o', encrypted_filepath, unencrypted_filepath], check=True)
    if result.returncode != 0:
        print("Error: could not encrypt archive.")
        sys.exit(1)
    print(f"Created encrypted archive: {encrypted_filepath}")

def transfer_file(encrypted_filepath, remote):
    docker_backup_filepath = f"/workspace/backup-{time.strftime('%Y%m%d-%H%M%S')}.gpg"
    if not os.path.isdir(RCLONE_CONFIG_DIRPATH):
        print(f"Error: could not find rclone config directory at: {RCLONE_CONFIG_DIRPATH}")
        sys.exit(1)
    result = subprocess.run([
        'docker', 'run', '--rm', '-it',
        '-v', f"{RCLONE_CONFIG_DIRPATH}:/config/rclone",
        '-v', f"{encrypted_filepath}:{docker_backup_filepath}",
        'rclone/rclone:latest',
        'copy', docker_backup_filepath, remote
    ], check=True)
    if result.returncode != 0:
        print("Error: failed to transfer archive to target host")
        sys.exit(1)
    print("Completed transfer")

def cleanup_files(*filepaths):
    for filepath in filepaths:
        if os.path.isfile(filepath):
            os.remove(filepath)
    print("Cleaned up.")

def decrypt_file(encrypted_filepath, archive_filepath):
    password = get_password("Password: ")
    result = subprocess.run(['gpg', '-d', '-q', '--passphrase', password, '-o', archive_filepath, encrypted_filepath], check=True)
    if result.returncode != 0:
        print("Error: could not decrypt archive.")
        sys.exit(1)
    print(f"Decrypted file available: {archive_filepath}")

def backup_put(remote, backup_dirs):
    if not remote:
        print("Error: no remote host and path details specified")
        sys.exit(1)
    now = time.strftime("%Y%m%d%H%M%S")
    archive_filepath = f"/tmp/backup_{now}.tar.gz"
    encrypted_filepath = f"/tmp/backup_{now}.gpg"
    create_archive(archive_filepath, backup_dirs)
    encrypt_file(archive_filepath, encrypted_filepath)
    transfer_file(encrypted_filepath, remote)
    cleanup_files(archive_filepath, encrypted_filepath)

def backup_extract(encrypted_filepath):
    if not encrypted_filepath:
        print("Error: no encrypted file specified")
        sys.exit(1)
    archive_dir = os.path.dirname(encrypted_filepath)
    archive_filename = os.path.basename(encrypted_filepath)
    archive_filename_noext = os.path.splitext(archive_filename)[0]
    now = time.strftime("%Y%m%d%H%M%S")
    archive_filepath = os.path.join(archive_dir, f"decrypted_{archive_filename_noext}.tar.gz")
    decrypt_file(encrypted_filepath, archive_filepath)

def backup_help():
    print("description: Encrypts and stores backups using gpg, tar and rclone")
    print("\nusage: backup.py [FUNCTION] [ARGUMENTS]")
    print("\tFUNCTIONS")
    print("\t\tput")
    print("\t\t\targ1: remote - the rclone address of the backup store, e.g. remote:backup-dir")
    print("\t\t\targ2: dirs - directories to backup (colon-separated)")
    print("\t\textract")
    print("\t\t\targ1: filepath - the filepath of the encrypted archive to extract")
    print("")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        backup_help()
        sys.exit()
    operation = sys.argv[1]
    check_dependency('gpg')
    if operation == "put":
        if len(sys.argv) != 4:
            backup_help()
            sys.exit(1)
        remote = sys.argv[2]
        backup_dirs = sys.argv[3]
        backup_put(remote, backup_dirs)
    elif operation == "extract":
        if len(sys.argv) != 3:
            backup_help()
            sys.exit(1)
        encrypted_filepath = sys.argv[2]
        backup_extract(encrypted_filepath)
    else:
        backup_help()
        sys.exit(1)