#!/usr/bin/python2

from threading import *
import argparse
import urllib2
import Queue



parser = argparse.ArgumentParser(description='Kinda directory buster')
parser.add_argument('-t', '--thread', help='How many thread do you want , [100]')
parser.add_argument('URL', help='The target which you want to play with')
parser.add_argument('-p','--port', help='The port of your target , [80]')
args = parser.parse_args()


target =  args.URL
port = args.port or 80
THREAD_COUNT = int(args.thread) or 100

if target.endswith('/'):
    target = target.strip('/')
    
threadPool = Queue.Queue(0)
condition = Condition()
cnt = 0


class JThread(Thread):
    def __init__(self, condition):
        Thread.__init__(self)
        self.cond = condition

    def run(self):
        while True:
            global target, cnt

            each = threadPool.get()
            
            if each.startswith('.'):
                each = each + '/'
            elif '.' not in each:
                each = each + '/'
                
            url = '%s/%s' % (target, each)
            
            try:
                res = urllib2.urlopen(url)
                print '[+][%s] %s\n' % (res.code, url),
            except urllib2.HTTPError, err:
                if err.code != 404:
                    print '[-][%s] %s\n' % (err.code, url),

            self.cond.acquire()
            cnt += 1
            self.cond.release()
            threadPool.task_done()

if __name__ == '__main__':
    with open('path', 'r') as f:
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
