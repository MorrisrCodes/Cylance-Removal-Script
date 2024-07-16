import winreg

# Cylance Registry Key Information
CYLANCE_REGISTRY_KEY = r"SOFTWARE\Cylance"

def check_cylance_installed():
    """Check if Cylance is installed by querying the registry."""
    try:
        # Connect to the local registry
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, CYLANCE_REGISTRY_KEY)
        # If we can open the key, Cylance is installed
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False

def remove_cylance():
    """Remove Cylance by deleting the registry key."""
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        # Attempt to delete the registry key
        winreg.DeleteKey(registry, CYLANCE_REGISTRY_KEY)
    except FileNotFoundError:
        pass  # Cylance was not found in the registry
    except Exception:
        pass  # Handle other potential exceptions silently

def main():
    if check_cylance_installed():
        remove_cylance()

if __name__ == "__main__":
    main()