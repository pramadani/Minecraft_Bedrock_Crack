import os
import subprocess
import shutil

def take_ownership(filepath):
    subprocess.run(['takeown', '/f', filepath], shell=True)
    subprocess.run(['icacls', filepath, '/grant', f"{os.getlogin()}:F"], shell=True)

def delete_file(filepath):
    try:
        subprocess.run(["cmd", "/c", f"del {filepath}"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Gagal menghapus file {filepath}")


def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        print(f"File berhasil disalin dari {source} ke {destination}.")
    except Exception as e:
        print(f"Gagal menyalin file: {e}")


file_path = "C:\\Windows\\System32\\Windows.ApplicationModel.Store.dll"
source_file = "Files/System32/Windows.ApplicationModel.Store.dll"

take_ownership(file_path)
delete_file(file_path)
copy_file(source_file, file_path)

file_path = "C:\\Windows\\SysWOW64\\Windows.ApplicationModel.Store.dll"
source_file = "Files/SysWOW64/Windows.ApplicationModel.Store.dll"

take_ownership(file_path)
delete_file(file_path)
copy_file(source_file, file_path)