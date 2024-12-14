import ctypes
import sys
import winreg as reg


def run_as_admin():
    """Re-run the script with admin privileges."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def disable_task_manager():
    """Disable Task Manager by modifying the Windows Registry."""
    run_as_admin()

    try:
        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, reg.KEY_SET_VALUE)
    except FileNotFoundError:
        # Create the key if it doesn't exist
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")

    # Set the value to disable Task Manager
    reg.SetValueEx(key, "DisableTaskMgr", 0, reg.REG_DWORD, 1)
    reg.CloseKey(key)
    print("Task Manager disabled.")


def enable_task_manager():
    """Re-enable Task Manager by modifying the Windows Registry."""
    run_as_admin()

    try:
        # Open the registry key
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, reg.KEY_SET_VALUE)
        reg.DeleteValue(key, "DisableTaskMgr")
        reg.CloseKey(key)
        print("Task Manager enabled.")
    except FileNotFoundError:
        print("Task Manager is already enabled or the key does not exist.")
    except OSError as e:
        print(f"Error while enabling Task Manager: {e}")
