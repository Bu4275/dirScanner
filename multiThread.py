import threading
import requests
import socket
import Queue
import sys


jobq = Queue.Queue(0)

condition = threading.Condition()

# found = []

# errlist = []

class JThread(threading.Thread):
    def __init__(self, condition, target, port, verbose):
        threading.Thread.__init__(self)
        self.cond = condition
        self.target = target
        self.port = port
        self.verbose = verbose

    def wget(self, url):

        res = requests.head(url, timeout=5)

        if res.ok:
            msg = '[+][%s] %s\n' % (res.status_code, url)

            if res.history:
                msg = '[-][%s] %s\n' % (res.history[0].status_code, url)

            print msg

        elif not res.ok:
            msg = '[-][%s] %s\n' % (res.status_code, url)

            if self.verbose or res.status_code != 404:
                print msg

    def run(self):
        while True:
            # global found, errlist

            each = jobq.get()

            if self.port:
                url = '%s:%s/%s' % (self.target, self.port, each)
            else:
                url = '%s/%s' % (self.target, each)

            self.cond.acquire()

            try:
                self.wget(url)

            except requests.exceptions.Timeout as err:
                print 'requests Timeout for %s\n' % url
                # errlist.append('Timeout ' + each)

            except socket.timeout as err:
                print 'socket Timeout for %s\n' % url
                # errlist.append('Socket Timeout ' + each)

            except requests.exceptions.RequestException as err:
                print 'Unexpected exeception'
                # errlist.append('Unexpect Exception ' + str(err))

            self.cond.release()
            jobq.task_done()

def main():
    pass

if __name__ == '__main__':
    main()
