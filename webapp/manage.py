#!/usr/bin/python
import os
import sys
# import subprocess
# subprocess.Popen('ipconfig getifaddr en0'.split())

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
