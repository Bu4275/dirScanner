#!/usr/bin/python2
from jargparse import *
from jthread import *


target =  args.URL
port = args.port or 80
THREAD_COUNT = int(args.thread or 100)


if target.endswith('/'):
    target = target.strip('/')
    
def main():
    with open(source, 'r') as f:
        txt = f.readlines()

    txt = [each.strip('\n') for each in txt if '\n' in each]

    map(threadPool.put, txt)

    for _ in xrange(THREAD_COUNT):
        T = JThread(condition, target, port)
        T.setDaemon(True)
        T.start()
    
    threadPool.join()
    
    print 'Total :',len(txt)

if __name__ == '__main__':
    main()
