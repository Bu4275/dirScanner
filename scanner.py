#!/usr/bin/python2
import multiThread as mthread
import optparser as opt
import sys

target =  opt.args.URL
port = opt.args.port
THREAD_COUNT = int(opt.args.thread)
verbose = opt.args.verbose

if target.endswith('/'):
    target = target.strip('/')

def isOnline(url, port):
    if port:
        aim = '%s:%s/' % (url, port)
    else:
        aim = url + '/'
    try:
        res = mthread.requests.head(aim)

    except mthread.requests.ConnectionError as err:
        return False

    return True

def main():
    if not isOnline(target, port):
        print 'Target is down.'
        sys.exit(0)

    with open(opt.source, 'r') as f:
        txt = f.readlines()

    txt = [each.strip('\n') for each in txt if '\n' in each]

    map(mthread.jobq.put, txt)

    for _ in xrange(THREAD_COUNT):
        T = mthread.JThread(mthread.condition, target, port, verbose)
        T.setDaemon(True)
        T.start()

    mthread.jobq.join()

    print 'Tried : ', len(txt)

if __name__ == '__main__':
    main()
    '''
    print "%s:%s" % (target, port)
    print THREAD_COUNT
    print verbose
    print opt.source
    '''
