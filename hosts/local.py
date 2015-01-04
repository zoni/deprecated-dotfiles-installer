#!/usr/bin/env python

import json
import os
import sys
import yaml
from getpass import getpass
from shutil import move
from tempfile import mkstemp


SUDO_PASS_FILE = os.path.join(os.path.dirname(__file__), "..", ".sudo_pass")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.yml")


def load_sudo_pass():
    if os.getuid() == 0:
        # Root should always be able to sudo, no need to ask for
        # password then.
        return None

    try:
        with open(SUDO_PASS_FILE, 'r') as f:
            password = f.readline()[:-1]
    except IOError:
        password = ask_sudo_pass()

    return password


def ask_sudo_pass():
    password = getpass("sudo password: ")

    fd, fpath = mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write("{}\n".format(password))
    move(fpath, SUDO_PASS_FILE)

    return password


def inventory(sudo_pass=None):
    groups = {
        'all': ["localhost"],
        'local': ["localhost"],
        '_meta': {
            'hostvars': {
                'localhost': {
                    "ENV": dict(os.environ),
                    "ansible_connection": "local",
                }
            }
        }
    }

    if os.getuid() == 0:
        groups['_meta']['hostvars']['localhost']['sudo_available'] = True
    elif sudo_pass is not None:
        groups['_meta']['hostvars']['localhost']['sudo_available'] = True
        groups['_meta']['hostvars']['localhost']['ansible_sudo_pass'] = sudo_pass
    else:
        groups['_meta']['hostvars']['localhost']['sudo_available'] = False

    return groups


if __name__ == '__main__':
    if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
        config = yaml.safe_load(open(CONFIG_FILE, 'r'))
        sudo_pass = load_sudo_pass() if config.get('SUDO', False) else None
        print(json.dumps(inventory(sudo_pass=sudo_pass)))
    else:
        sys.stderr.write("Usage: {} --list\n".format(sys.argv[0]))
        sys.exit(1)
