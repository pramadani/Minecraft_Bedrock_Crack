import os
import subprocess
import shutil
import ctypes
import sys
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        script = sys.argv[0]
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1)
            sys.exit(0)
        except Exception as e:
            print(f"Elevated permissions required. Error: {e}")
            sys.exit(1)

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

def kill_process(process_name):
    try:
        subprocess.run(["taskkill", "/F", "/IM", process_name], shell=True, check=True)
        print(f"Proses {process_name} telah dihentikan.")
    except subprocess.CalledProcessError:
        print(f"Tidak dapat menghentikan proses {process_name}. Proses mungkin sudah tidak berjalan.")

def get_file_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(".")
    return os.path.join(bundle_dir, relative_path)

run_as_admin()

kill_process("XboxPcAppFT.exe")
kill_process("XboxPcApp.exe")

file_path_32 = "C:\\Windows\\System32\\Windows.ApplicationModel.Store.dll"
source_file_32 = get_file_path("files/System32/Windows.ApplicationModel.Store.dll")

take_ownership(file_path_32)
delete_file(file_path_32)
copy_file(source_file_32, file_path_32)

file_path_64 = "C:\\Windows\\SysWOW64\\Windows.ApplicationModel.Store.dll"
source_file_64 = get_file_path("files/SysWOW64/Windows.ApplicationModel.Store.dll")

take_ownership(file_path_64)
delete_file(file_path_64)
copy_file(source_file_64, file_path_64)

print("Operasi selesai. Menutup dalam 5 detik...")
time.sleep(5)