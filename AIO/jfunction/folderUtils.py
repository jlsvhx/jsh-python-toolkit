import os
import shutil
import datetime
import re


def delBlankDir(maindir):
    for root, dirs, files in os.walk(maindir, topdown=False):
        for seconder in dirs:
            wholePath = os.path.join(root, seconder)
            if len(os.listdir(wholePath)) == 0:
                shutil.rmtree(wholePath)
                print(wholePath)
