import os
import sys


def macos_flag():
    cmd = "/usr/sbin/system_profiler SPHardwareDataType | fgrep 'Serial' | awk '{print $NF}'"
    output = os.popen(cmd)
    return output.read()


def windows_flag():
    return "win flag"


def get_flag():
    if sys.platform == 'darwin':
        return macos_flag().replace('\n', '').replace('\r', '').strip()
    elif sys.platform == 'win32':
        return ""


if __name__ == '__main__':
    print(macos_flag())
