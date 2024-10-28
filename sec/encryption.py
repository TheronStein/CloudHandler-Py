import os
import sys
import time
import subprocess

def program_init(arg1, arg2, arg3):
    #invalid initializating parameters
    if arg1 is None:
        invalid_init()
        if arg2 is None:
            invalid_init()

    #lock handler
    if arg1 is 0:
        if arg2 is None or arg3 is None:
            invalid_param(0)


    #access handler
    if arg1 is 1 and arg2 is None:
        invalid_param(1)
    
    program_start()

def invalid_param(arg1):
        if arg1 is 0:
            case = "Lock Failure"
        if arg1 is 1:
            case = "Access Failure"
        else:
            case = "Invalid Failure"

def invalid_init()
    print(f"Encryption Handler/n")
    print(f"/n")
    print(f"Requires parameters:/n")
    print(f"Examples:/n
    /n
    Locking your folder:/n
    print ./mycrypt.py 0 /path/to/vis_dir /n
    /n
    Accessing your folder:/n
    print ./mycrypt.py 1 /path/to/hid_dir /desired_path/vis_dir")
    print(f"/n/nUse ./mycrypt.py help for more information/n")
    sys.exit()

def program_start():
    print(f"Input Eligble for Program./n")


def encrypt_file(unencrypted_filepath, encrypted_filepath):
    password = os.getenv('ENCRYPT_RCLONE_PASSWORD', get_password("Password: "))
    result = subprocess.run(['gpg', '-q', '--symmetric', '--passphrase', password, '-o', encrypted_filepath, unencrypted_filepath], check=True)
    if result.returncode != 0:
        print("Error: could not encrypt archive.")
        sys.exit(1)
    print(f"Created encrypted archive: {encrypted_filepath}")

def decrypt_file(encrypted_filepath, archive_filepath):
    password = get_password("Password: ")
    result = subprocess.run(['gpg', '-d', '-q', '--passphrase', password, '-o', archive_filepath, encrypted_filepath], check=True)
    if result.returncode != 0:
        print("Error: could not decrypt archive.")
        sys.exit(1)
    print(f"Decrypted file available: {archive_filepath}")
