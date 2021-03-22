import os

def get_current_branch():
    return os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
