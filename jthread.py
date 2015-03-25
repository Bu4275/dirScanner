from threading import *


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

def main():
    pass

if __name__ == '__main__':
    main()
