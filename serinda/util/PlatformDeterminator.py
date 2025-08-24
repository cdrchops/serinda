from sys import platform
from enum import Enum #to do enum work in this file - overkill? maybe, but I want to do it this way... for now 9Mar24 wink

class Platform(Enum):
    UNDEFINED = 0
    LINUX = 1
    MAC = 2
    WINDOWS = 3

class PlatformDeterminator:
    PLATFORM = Platform.UNDEFINED

    def __init__(self):
        if platform == "linux" or platform == "linux2":
            self.PLATFORM = Platform.LINUX
        elif platform == "darwin":
            self.PLATFORM = Platform.MAC
        elif platform == "win32":
            self.PLATFORM = Platform.WINDOWS

    def isWindows(self):
        return self.PLATFORM == Platform.WINDOWS

    def isLinux(self):
        return self.PLATFORM == Platform.LINUX

    def isMac(self):
        return self.PLATFORM == Platform.MAC