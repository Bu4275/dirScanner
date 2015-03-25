import os
import sys
import urllib
import argparse

File_Name = 'worldlist.txt'
SRC_URL = 'http://ucgjhe.github.io/note/misc/dict/worldlist.txt'
VER_URL = 'http://ucgjhe.github.io/note/misc/dict/version'


def ask(content):
    ans = (raw_input(content +  ' (Y or N) => ')).lower()
    return True if ans in ('y', 'yes') else False

def dict_update():
    try:
        urllib.urlretrieve(SRC_URL, File_Name)
        print '[Download completed]'
        print '[Now moving forward]'
    except err:
        print '[Unexpected Error : %s]' % sys.exc_info[0]

def dict_version_check():
    with open(File_Name) as f:
        locver = f.readline().strip('\n')
    remver = urllib.urlopen(VER_URL).readline().strip('\n')
    if remver > locver:
        print '[Remote version : %s]' % remver
        print '[Local  version : %s]' % locver
        update = ask('[Your worldlist file is out of date, wanna update it ?]')
        if update:
            dict_update()
            return True
    else:
        print '[Everything is up to date ...]'
    return False

parser = argparse.ArgumentParser(description='Kinda directory buster')
parser.add_argument('URL', help='The target which you want to play with')
parser.add_argument('-src', '--source', help='It will be downloaded automatically if you did not have one')
parser.add_argument('-p','--port', help='The port of your target , [80]')
parser.add_argument('-t', '--thread', help='How many thread do you want , [100]')

args = parser.parse_args()

target =  args.URL
port = args.port or 80
THREAD_COUNT = int(args.thread or 100)
source = args.source


if not source:
    if os.path.exists(File_Name):
        print '[Detected worldlist.txt]'
        print '[Checking version]'
        if dict_version_check():
            if not ask('[Progress with outdated worldlist file ?]'):
                print '[Please set source option OR use --help get some help]'
                sys.exit(0)
    elif ask('[Prefer to donwload the latest version of worldlist file ?]'):
        dict_update()
    else:    
        print '[Please set --source option OR use --help get some help]'
        sys.exit(0)
    source = File_Name
