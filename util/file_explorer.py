import os
import subprocess
import psutil

def is_explorer_running():
    """Check if explorer.exe is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'explorer.exe':
            return True
    return False

def disable_explorer():
    """Stop the File Explorer if it's running."""
    if is_explorer_running():
        os.system("taskkill /F /IM explorer.exe")

def enable_explorer():
    """Start the File Explorer if it's not already running."""
    if not is_explorer_running():
        subprocess.Popen("explorer.exe")
