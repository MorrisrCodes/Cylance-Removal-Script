import os
import subprocess
import winreg

# Paths and registry keys
CYLANCE_REGISTRY_KEY = r" folder with(\Cylance\Desktop)"
CYLANCE_SERVICES = ["cylancesvc", "cylanceui", "cyoptics"]
CYLANCE_DRIVERS_PATH = r"C:\Windows\System32\drivers\\"
CYLANCE_DRIVER_FILES = [
    "CylanceDrv64.sys",
    "CyOpticsDrv.sys",
    "CyProtectDrv64.sys"
]

def is_cylance_installed():
    """Check if Cylance is installed by verifying the presence of the registry key."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        winreg.OpenKey(registry, CYLANCE_REGISTRY_KEY)
        return True
    except FileNotFoundError:
        return False

def stop_services():
    """Stop Cylance services."""
    for service in CYLANCE_SERVICES:
        try:
            subprocess.run(['sc', 'stop', service], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass  # Service might already be stopped or other issue

def set_registry_value(key_path, value_name, value, value_type):
    """Set a registry value."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, value)
        winreg.CloseKey(key)
    except Exception:
        pass  # Handle exceptions silently

def delete_registry_value(key_path, value_name):
    """Delete a registry value if it exists."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
    except FileNotFoundError:
        pass  # Key or value does not exist
    except Exception:
        pass  # Handle other potential exceptions silently

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
    # Check if Cylance is installed
    if is_cylance_installed():
        # Stop Cylance services
        stop_services()
        
        # Set SelfProtectionLevel to 1
        set_registry_value(CYLANCE_REGISTRY_KEY, 'SelfProtectionLevel', 1, winreg.REG_DWORD)
        
        # Delete LastStateRestorePoint
        delete_registry_value(CYLANCE_REGISTRY_KEY, 'LastStateRestorePoint')
        
        # Delete Cylance driver files
        delete_files(CYLANCE_DRIVERS_PATH, CYLANCE_DRIVER_FILES)

if __name__ == "__main__":
    main()