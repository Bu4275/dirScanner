#!/usr/bin/python2
import optparser as opt
import multiThread

target =  opt.args.URL
port = opt.args.port
THREAD_COUNT = int(opt.args.thread)
verbose = opt.args.verbose

if target.endswith('/'):
    target = target.strip('/')

def probe(url, port):
    aim = '%s:%s/' % (url, port)
    try:
        res = multiThread.requests.head(aim)

    except multiThread.requests.ConnectionError as err:
        return False

    return True

def main():
    if not probe(target, port):
        print 'Target is down.'
        multiThread.sys.exit(0)

    with open(opt.source, 'r') as f:
        txt = f.readlines()

    txt = [each.strip('\n') for each in txt if '\n' in each]

    map(multiThread.jobq.put, txt)

    for _ in xrange(THREAD_COUNT):
        T = multiThread.JThread(multiThread.condition, target, port, verbose)
        T.setDaemon(True)
        T.start()

    multiThread.jobq.join()

    print 'Tried : ',len(txt)

if __name__ == '__main__':
    main()
    '''
    print "%s:%s" % (target, port)
    print THREAD_COUNT
    print verbose
    '''
