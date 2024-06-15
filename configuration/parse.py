from collections import defaultdict
import os
import subprocess
from .restart import restart_containers
from webNUT.settings import NUT_CONFIG_DIRECTORY, UPSMON_FILE_HANDLER


class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


def parse_ups(ups=False, general=False):
    ups_info = {}
    found = False

    ini_file = NUT_CONFIG_DIRECTORY+"ups.conf"

    with open(ini_file, "r") as f:
        data = f.readlines()
        if not general:
            for line in data:
                if line == "\n":
                    continue

                if not found:
                    if line.find(f"[{ups}]") != -1:
                        found = True
                        line = line.replace("\n", "")
                        line = line.replace("\t", "")
                        line = line.replace("[", "")
                        line = line.replace("]", "")
                        ups_info['name'] = line

                else:
                    if line.find("[") != -1:
                        found = False

                    else:
                        line = line.replace("\n", "")
                        line = line.replace("\t", "")
                        try:
                            info = line.split(" = ")
                            ups_info[info[0]] = info[1]
                        except IndexError:
                            ups_info['flag'] = line
        else:
            for line in data:
                if line == "\n":
                    continue
                if line.find("["):
                    line = line.replace("\n", "")
                    line = line.replace("\t", "")
                    try:
                        info = line.split(" = ")
                        ups_info[info[0]] = info[1]
                    except IndexError:
                        ups_info['flag'] = line
                else:
                    break 
        return ups_info


def save_ups(request=None, general=False, ups=False):
    if request is None:
        return "Failure"

    found = False

    ups_info = {}

    for key, value in request.items():
        if key.startswith('key_'):
            ups_info[value] = request['value_' + key[4:]]

    ini_file = NUT_CONFIG_DIRECTORY+"ups.conf"

    return_code = 0

    with open(ini_file, "r") as f:
        data = f.readlines()

    current = 1
    if general:
        current = 0

    for i, line in enumerate(data):
        if not general:
            if line == "\n":
                data[i] = line
                continue

            if not found:
                if line.find(f"[{ups}]") != -1:
                    found = True
                    if ups != ups_info['name']:
                        data[i] = line.replace(ups, ups_info['name'])
                        return_code = 1
                    else:
                        data[i] = line
                else:
                    data[i] = line

            else:
                if line.find("[") != -1:
                    data[i] = line
                    found = False

                else:
                    if list(ups_info)[current] == 'flag':
                        data[i] = f"{list(ups_info.values())[current]}\n"
                    else:
                        data[i] = f"{list(ups_info)[current]} = {list(ups_info.values())[current]}\n"
                    current += 1

        else:
            return_code = 2
            if line == "\n":
                data[i] = line
                continue

            if not found:
                if line.find(f"[{ups}]") != -1:
                    found = True
                    data[i] = line
                elif line.find(f"[{ups}]") == -1 and current < len(ups_info):
                    data[i] = f"{list(ups_info)[current]} = {list(ups_info.values())[current]}\n"
                    current += 1
            else:
                data[i] = line


    text = ''.join(data)
    text = text.replace('"', '\\"')
    command = f"sh -c 'echo \"{text}\" > {ini_file}'"
    subprocess.call(command, shell=True)
    container_list = ['upsdrvctl', 'upsd']
    restart_containers(container_list)
    command = f"sh -c 'echo \"\" > {UPSMON_FILE_HANDLER}'"
    subprocess.call(command, shell=True)

    if return_code == 1:
        return ups_info['name'], return_code
    elif return_code == 2:
        return return_code
    else:
        return ups, return_code


def parse_upsd():
    upsd_info = defaultdict(list)
    ini_file = NUT_CONFIG_DIRECTORY+"upsd.conf"

    with open(ini_file, "r") as f:
        data = f.readlines()
        for line in data:
            if line == "\n":
                continue
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            try:
                info = line.split(" ")
                upsd_info[info[0]].append(' '.join(info[1:]))
            except IndexError:
                upsd_info['flag'] = line

        return upsd_info
    
def save_upsd(request=None):
    if request is None:
        return "Failure"
    
    upsd_info = defaultdict(list)
    ini_file = NUT_CONFIG_DIRECTORY+"upsd.conf"
    return_code = 0

    for key, value in request.items():
        if key.startswith('key_'):
            upsd_info[value] = request['value_' + key[4:]]

    data = upsd_info.items();
    text = ''
    for key, value in data:
        text += key.split('_')[0] + ' ' + value + '\n'

    text = text.replace('"', '\\"')
    command = f"sh -c 'echo \"{text}\" > {ini_file}'"
    subprocess.call(command, shell=True)

    container_list = ['upsd']
    restart_containers(container_list)
    command = f"sh -c 'echo \"\" > {UPSMON_FILE_HANDLER}'"
    subprocess.call(command, shell=True)

    return return_code


def parse_upsmon():
    upsmon_info = defaultdict(list)
    ini_file = NUT_CONFIG_DIRECTORY+"upsmon.conf"

    with open(ini_file, "r") as f:
        data = f.readlines()
        for line in data:
            if line == "\n":
                continue
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            try:
                info = line.split(" ")
                upsmon_info[info[0]].append(' '.join(info[1:]))
            except IndexError:
                upsmon_info['flag'] = line

        return upsmon_info

def save_upsmon(request=None):
    if request is None:
        return "Failure"
    
    upsmon_info = defaultdict(list)
    ini_file = NUT_CONFIG_DIRECTORY+"upsmon.conf"
    return_code = 0

    for key, value in request.items():
        if key.startswith('key_'):
            upsmon_info[value] = request['value_' + key[4:]]

    data = upsmon_info.items()
    text = ''
    for key, value in data:
        text += key.split('_')[0] + ' ' + value + '\n'

    text = text.replace('"', '\\"')
    command = f"sh -c 'echo \"{text}\" > {ini_file}'"
    subprocess.call(command, shell=True)

    command = f"sh -c 'echo \"\" > {UPSMON_FILE_HANDLER}'"
    subprocess.call(command, shell=True)

    return return_code