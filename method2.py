import os
import shutil
import subprocess
import winreg

# Paths and registry keys
CYLANCE_REGISTRY_KEY = r"folder with(\Cylance\Desktop)"
CYLANCE_SERVICES = ["cylancesvc", "cylanceui", "cyoptics"]
CYLANCE_DRIVERS_PATH = r"C:\Windows\System32\drivers\\"
CYLANCE_DRIVER_FILES = [
    "CylanceDrv64.sys",
    "CyOpticsDrv.sys",
    "CyProtectDrv64.sys"
]

def stop_services():
    """Stop Cylance services."""
    for service in CYLANCE_SERVICES:
        try:
            subprocess.run(['sc', 'stop', service], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass  # Service might already be stopped or other issue

def delete_registry_key(key_path):
    """Delete a registry key if it exists."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        winreg.DeleteKey(registry, key_path)
    except FileNotFoundError:
        pass  # Key does not exist
    except Exception:
        pass  # Handle other potential exceptions silently

def set_registry_value(key_path, value_name, value, value_type):
    """Set a registry value."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, value)
        winreg.CloseKey(key)
    except Exception:
        pass  # Handle exceptions silently

def delete_files(path, files):
    """Delete specified files from a directory."""
    for file in files:
        try:
            os.remove(os.path.join(path, file))
        except FileNotFoundError:
            pass  # File does not exist
        except Exception:
            pass  # Handle other potential exceptions silently

def main():
    # Stop Cylance services
    stop_services()
    
    # Delete registry keys/values
    delete_registry_key(CYLANCE_REGISTRY_KEY)
    
    # Set registry value
    set_registry_value(CYLANCE_REGISTRY_KEY, 'SelfProtectionLevel', 1, winreg.REG_DWORD)
    
    # Delete Cylance driver files
    delete_files(CYLANCE_DRIVERS_PATH, CYLANCE_DRIVER_FILES)
    
    # Optionally, delete the Cylance registry folder (if any other paths are involved)
    delete_registry_key(r"folder with cylance")

if __name__ == "__main__":
    main()