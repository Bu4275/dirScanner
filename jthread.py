from threading import *
import urllib2
import socket
import Queue
import sys

threadPool = Queue.Queue(0)

condition = Condition()

found = []

PUSHBACK = []

class JThread(Thread):
    def __init__(self, condition, target, port, verbose=False):
        Thread.__init__(self)
        self.cond = condition
        self.target = target
        self.port = port
        self.counter = 3
        self.verbose = verbose
    def run(self):
        while True:
            global found, PUSHBACK
            
            each = threadPool.get()

            if each.endswith('/'):
                each = each.strip('/') + '/'
            elif each.startswith('.'):
                each = each + '/'
            elif '.' not in each:
                each = each + '/'
                
            url = '%s:%s/%s' % (self.target, self.port, each)

            
            try:
                res = urllib2.urlopen(url, timeout=10)
                print '[+][%s] %s\n' % (res.code, url),
                found.append(url)
            except urllib2.HTTPError as err:
                if self.verbose is True:
                    print '[-][%s] %s\n' % (err.code, url),
                elif err.code != 404:
                    print '[-][%s] %s\n' % (err.code, url),
                    found.append(url)
            except (socket.timeout, urllib2.URLError) as err:
                print 'PUSHBACK %s\n' % (each),
                PUSHBACK.append(each)
            self.cond.acquire()
            self.cond.release()
            threadPool.task_done()
            
def main():
    pass

if __name__ == '__main__':
    main()
