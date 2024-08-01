###############################################################################
# Copyright (c) by Z3R0-CDS and Zer0-Industries.com
# All rights reserved.
#
# This script is created by Z3R0-CDS and will be distributed by Z3R0-CDS
# via Github and or Zer0-Industries.com Modifying the code to use it for
# profit is forbidden and will be punished.
# Questions? Contact copyright@zer0-industries.com
###############################################################################

import json
import os
import sys
import time
import requests
from packaging.version import Version

from colorama import init, Fore, Back
import getpass
if sys.platform == 'win64' or sys.platform == 'win32':
    print("OS currently not supported. The software will not work.")
    time.sleep(500)
    os._exit(1)
else:
    import readline


class Cli():

    def __init__(self, appname="AutoPenguin"):
        init()
        self.softname = appname
        self.__version__ = "0.1"
        self.dev_ver = "0.1.0"
        self.project = "Z3R0-CDS/AutoPenguin"
        self.privacyMode = False
        self.simpleMode = False

        self._setConsoleTItle(f"{self.softname} ~ {self.dev_ver}")
        self.clear([])

        self.console = True
        self.shellname = f"[{Fore.RED}{getpass.getuser()}{Fore.BLUE}@{Fore.GREEN}{os.getcwd()}{Fore.RESET}]:"
        self.shortShellname = f"[{Fore.RED}{getpass.getuser()}{Fore.BLUE}@{Fore.GREEN}{os.path.basename(os.getcwd())}{Fore.RESET}]:"
        self.username = getpass.getuser()
        self.privateShellname = f"[Privateshell]:"

        self.loadConfig()

        self.commands = [
            {'name': 'help', "alias": ["h"], 'params': '(command)', 'func': self.help, "description": "Help"},
            {'name': 'update', "alias": ["up"], 'params': 'None', 'func': self.getUpdate, "description": "Checks for an update"},
            {'name': 'privacy', "alias": ['pm'], 'params': 'None', 'func': self.privacy, "description": "Toggle privacy mode to hide name and path"},
            {'name': 'simple', "alias": ['sm'], 'params': 'None', 'func': self.setSimpleMode,
             "description": "Toggle simple mode to shorten path"},
            {'name': 'exit', "alias": ["ex"], 'params': 'None', 'func': self.quit, "description": f"Exit {self.softname}"},
            {'name': 'about', "alias": ["ab"], 'params': 'None', 'func': self.info, "description": f"Info for {self.softname}"},
            {'name': 'cls', "alias": ["clear", "clr"], 'params': 'None', 'func': self.clear, "description": "Clear Terminal"},
            {'name': 'cd', "alias": ["chdir", "changedir"], 'params': '[path]', 'func': self.changedir, "description": "Change working directory"},
            {'name': 'sp', "alias": ["scd"], 'params': 'None', 'func': self.showpath, "description": "Show working directory"},
            {'name': 'sys', "alias": ["system"], 'params': '[System Command]', 'func': self.system, "description": "Run system commands that are blocked because of similar names"}
            ]

        self.output(f"---\nWelcome to {self.softname} {self.dev_ver} ~ {len(self.commands)} commands at your fingertip\n---", True)
        self.getUpdate()

    def _setConsoleTItle(self, title):
        if sys.platform == "win64":
            os.system(f"title {title}")
        else:
            os.system(f"echo -n -e '\033]0;{title}\a'")

    def path_completer(self,text, state):
        # Get the current directory and the input text
        current_dir = os.getcwd()
        expanded_text = os.path.expanduser(text)

        # Join the current directory and the expanded input text to get the base path
        base_path = os.path.join(current_dir, expanded_text)

        # Use os.path.dirname to get the directory part and os.path.basename to get the base part
        directory, base_part = os.path.dirname(base_path), os.path.basename(base_path)

        # List all files/directories in the directory part that start with the base part
        matches = [os.path.join(directory, file) for file in os.listdir(directory) if file.startswith(base_part)]

        # Filter out directories/files that are not under the current directory
        matches = [os.path.relpath(match, current_dir) for match in matches if match.startswith(current_dir)]

        # If the match is a directory and doesn't end with '/', add a '/'
        for i, match in enumerate(matches):
            if os.path.isdir(os.path.join(current_dir, match)) and not match.endswith('/'):
                matches[i] = match + '/'
            if ' ' in match:
                matches[i] = f"'{match}'"

        return matches[state] if state < len(matches) else None


    # Processsing

    def run(self):
        def get_input(inpReq):
            data= input(inpReq)
            if data != "":
                readline.add_history(data)
            return data.split(" ")
        readline.set_completer_delims(' \t\n')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.path_completer)
        try:
            while self.console:
                self.processCommands(get_input(self.getShellName()))
                self.saveConfig()
        except EOFError:
            self.output('\nUser forced exit via ctrl+d', True)
        except KeyboardInterrupt:
            self.output('\nUser forced exit via ctrl+c', True)
        except Exception as x:
            self.output(f'\nCrash exit\nException: {x}', True)


    def isInCommands(self, name):
        cnt = 0
        for command in self.commands:
            if name == command['name']:
                return (cnt, True)
            elif name in command['alias']:
                return (cnt, True)
            cnt += 1
        return (None, False)

    def processCommands(self, cmd):
        point, isThere = self.isInCommands(cmd[0])
        if isThere:
            if len(cmd)>1:
                self.commands[point]['func'](cmd[1:len(cmd)])
            else:
                self.commands[point]['func'](['empty'])
        else:
            osCommand = ""
            for part in cmd:
                osCommand += f"{part} "
            os.system(osCommand)

    def output(self, txt, pureText=False):
        if pureText:
            print(txt)
        else:
            print(f"{self.getShellName()} {txt}")

    def getShellName(self):
        if self.privacyMode:
            return f"{self.privateShellname} "
        elif self.simpleMode:
            return f"{self.shortShellname} "
        else:
            return f"{self.shellname} "

    def updateShellName(self):
        self.shellname = f"[{Fore.RED}{os.getlogin()}{Fore.BLUE}@{Fore.GREEN}{os.getcwd()}{Fore.RESET}]:"
        self.privateShellname = f"[Privateshell]:"
        self.shortShellname = f"[{Fore.RED}{getpass.getuser()}{Fore.BLUE}@{Fore.GREEN}{os.path.basename(os.getcwd())}{Fore.RESET}]:"

    def saveConfig(self):
        config = {
            "private": self.privacyMode,
            "simple": self.simpleMode
        }
        with open("config.json", "w") as configFile:
            json.dump(config, configFile, indent=4)

    def loadConfig(self):
        try:
            with open("config.json", "r") as configFile:
                config = json.load(configFile)
                self.privacyMode = config["private"]
                self.simpleMode = config["simple"]
        except:
            # No config console hasn't ran yet
            pass

    def getLatest(self):
        latest = {
            "success": False
        }
        try:
            rsp = requests.get(f"https://api.github.com/repos/{self.project}/releases/latest", timeout=5)
            if rsp.ok:
                data = rsp.json()
                latest["success"] = True
                latest["version"] = data["tag_name"]
                latest["downloads"] = [{"name": asset["name"], "url": asset["browser_download_url"]} for asset in data["assets"]]
            else:
                if rsp.status_code == 404:
                    latest["exception"] = "No Release found / No Release available"
                else:
                    latest["exception"] = rsp
        except Exception as e:
            latest["exception"] = e

        return latest

    # Internal commands

    def getUpdate(self, args=None):
        self.output("Checking for updates...", True)
        latest = self.getLatest()
        if latest["success"]:
            self.output(f"Fetched latest release: {latest['version']}", True)
            onlineVersion = Version(latest['version'])
            selfVersion = Version(self.__version__)
            if onlineVersion > selfVersion:
                self.output(f"Update is available. You have ({self.__version__}) but could have ({latest['version']})", True)
                self.output("Run the install.sh as sudo to update.")
            else:
                self.output("No new version :)", True)
        else:
            self.output(f"Failed to get latest release: {latest['exception']}", True)

    def privacy(self, args):
        if self.simpleMode and not self.privacyMode:
            self.simpleMode = False
        self.privacyMode = not self.privacyMode

    def setSimpleMode(self, args):
        if self.privacyMode and not self.simpleMode:
            self.privacyMode = False
        self.simpleMode = not self.simpleMode

    def quit(self, args):
        self.output('Logging off! Bye...')
        self.console = False
        os._exit(0)

    def info(self, args):
        data = f"""
Name...: {self.softname}
Version: {self.__version__}
Int Ver: {self.dev_ver}
"""
        self.output(data, True)

    def help(self, args):
        if args[0]!="empty" and args[0]!="":
            point, exists = self.isInCommands(args[0])
            if exists:
                command = self.commands[point]
                self.output(f"Details for {args[0]}", True)
                self.output(f"------------------------------------------------------------", True)
                self.output(f" Aliases: {command['alias']}", True)
                self.output(f" Name: {command['name']}", True)
                if 'params' in command:
                    self.output(f" Params: {command['params']}", True)
                    if command['params']!="None":
                        self.output(f" Command Struct: {command['name']} {command['params']}", True)
                else:
                    self.output(f" Params: No documentation available", True)
                self.output(f" Description: {command['description']}", True)
                self.output(f"------------------------------------------------------------", True)
            else:
                self.output(f"The command does not exist.")
        else:
            self.info([])
            maxLen = 0
            for cmd in self.commands:
                if len(cmd['name'])>maxLen:
                    maxLen = len(cmd['name'])
            for cmd in self.commands:
                if len(cmd['name'])<maxLen:
                    cmdText = f"{cmd['name']}"
                    for i in range(maxLen-len(cmd['name'])):
                        cmdText+=" "
                    self.output(f"{cmdText} -> {cmd['description']}", True)
                else:
                    self.output(f"{cmd['name']} -> {cmd['description']}", True)
            self.output("\n", True)

    def clear(self, args):
        if sys.platform == "win64":
            os.system("cls")
        else:
            os.system("clear")

    def changedir(self, args):
        try:
            os.chdir(' '.join(args).replace("'", ""))

            self.updateShellName()
        except Exception as x:
            self.output(f"{x}")

    def showpath(self, args):
        if self.privacyMode:
            self.output(f"You are working in ->{os.getcwd().replace(self.username, 'HIDDEN')}")
        else:
            self.output(f"You are working in ->{os.getcwd()}")

    def spoofUser(self, args):
        try:
            self.output("NYI")
        except Exception as x:
            self.output(f"Error on [spoof] -> {x}")

    def system(self, args):
        try:
            command=""
            if len(args)>1:
                for part in args:
                    command += f"{part} "
            elif len(args)==1:
                command = args[0]
            os.system(command)
        except Exception as x:
            self.output(f"Error on [system] -> {x}")
