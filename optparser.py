import argparse
import urllib
import sys
import os

File_Name = 'wordlist.txt'
SRC_URL = 'http://ucgjhe.github.io/note/misc/dict/%s' % File_Name
VER_URL = 'http://ucgjhe.github.io/note/misc/dict/version'


def ask(content):
    ans = (raw_input(content +  ' (Y or N) => ')).lower()
    return True if ans in ('y', 'yes') else False

def dict_update():
    try:
        urllib.urlretrieve(SRC_URL, File_Name)
        print '[Download completed]'
    except err:
        print '[Unexpected Error : %s]' % sys.exc_info[0]

def dict_version_check():
    print '[Checking version]'
    with open(File_Name) as f:
        locver = f.readline().strip('\n')
    remver = urllib.urlopen(VER_URL).readline().strip('\n')
    if remver > locver:
        print '[Remote version : %s]' % remver
        print '[Local  version : %s]' % locver
        if ask('[Your wordlist file is out of date, wanna update it ?]'):
            dict_update()
            return True
    else:
        print '[Everything is up to date ...]'
    return False

parser = argparse.ArgumentParser(description='Kinda directory buster')
parser.add_argument('URL', help='The target which you want to play with')
parser.add_argument('-src', '--source', help='It will be downloaded automatically if you did not have one')
parser.add_argument('-p','--port', help='The port of your target')
parser.add_argument('-t', '--thread', help='How many thread do you want , [100]', default=100)
parser.add_argument('-v', '--verbose',action="store_true" , help='Show more detail message even Not Found', default=False)

args = parser.parse_args()

source = args.source

if not source:
    if os.path.exists(File_Name):
        print '[Detected wordlist.txt]'
        if dict_version_check():
          if not ask('[Progress with existed wordlist file ?]'):
                print '[Then You should specify a wordlist]'
                sys.exit(0)

    elif ask('[Wanna donwload the latest version of wordlist file ?]'):
        dict_update()

    else:
        print '[Please set --source option OR use --help to get some help]'
        sys.exit(0)
    source = File_Name

def main():
    pass

if __name__ == '__name__':
    main()
