import threading
import requests
import socket
import Queue
import sys


jobq = Queue.Queue(0)

condition = threading.Condition()

found = []

errlist = []

class JThread(threading.Thread):
    def __init__(self, condition, target, port, verbose=False):
        threading.Thread.__init__(self)
        self.cond = condition
        if target.endswith('/'):
            target = target.strip('/')
        self.target = target
        self.port = port
        self.verbose = verbose
        
    def run(self):
        while True:
            global found, errlist
            
            each = jobq.get()

            if each.endswith('/'):
                each = each.strip('/') + '/'
            elif each.startswith('.'):
                each = each + '/'
            elif '.' not in each:
                each = each + '/'
                
            url = '%s:%s/%s' % (self.target, self.port, each)

            self.cond.acquire()
            
            try:
                res = requests.get(url, timeout=5)

                if res.ok:
                    msg = '[+][%s] %s\n' % (res.status_code, url)
                    if res.history:
                        msg = '[-][%s] %s\n' % (res.history[0].status_code, url)
                    
                elif not res.ok:
                    msg = '[-][%s] %s\n' % (res.status_code, url)
                    
                if res.status_code != 404:
                    found.append(each)
                    print msg
                    
            except requests.exceptions.Timeout as err:
                print 'Timeout'
                errlist.append('Timeout ' + each)
                
            except socket.timeout as err:
                errlist.append('Socket Timeout ' + each)

            except requests.exceptions.RequestException as err:
                errlist.append('Unexpect Exception ' + str(err))

            
            self.cond.release()
            jobq.task_done()
            
def main():
    pass

if __name__ == '__main__':
    main()
