#!/usr/bin/python2

from jargparse import *
import urllib2
import Queue


if target.endswith('/'):
    target = target.strip('/')
    
threadPool = Queue.Queue(0)
condition = Condition()
cnt = 0



def main():    
    with open(source, 'r') as f:
        txt = f.readlines()

    txt = [each.strip('\n') for each in txt if '\n' in each]

    for each in txt:
        threadPool.put(each)

    for i in xrange(THREAD_COUNT):
        T = JThread(condition)
        T.setDaemon(True)
        T.start()
    
    threadPool.join()
    
    print 'Total :',cnt

if __name__ == '__main__':
    main()
