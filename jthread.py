from threading import *
import urllib2
import socket
import Queue
import sys

threadPool = Queue.Queue(0)

condition = Condition()



class JThread(Thread):
    def __init__(self, condition, target, port):
        Thread.__init__(self)
        self.cond = condition
        self.target = target
        self.port = port
    def run(self):
        while True:
            global target

            each = threadPool.get()
            
            if each.startswith('.'):
                each = each + '/'
            elif '.' not in each:
                each = each + '/'
                
            url = '%s:%s/%s' % (self.target, self.port, each)
            
            try:
                res = urllib2.urlopen(url, timeout=3)
                print '[+][%s] %s\n' % (res.code, url),
            except urllib2.HTTPError as err:
                if err.code != 404:
                    print '[-][%s] %s\n' % (err.code, url),
            except (socket.timeout, urllib2.URLError) as err:
                print '[Timeout][%s]' % (url)
            finally:
                self.cond.acquire()
                self.cond.release()
                threadPool.task_done()

def main():
    pass

if __name__ == '__main__':
    main()
