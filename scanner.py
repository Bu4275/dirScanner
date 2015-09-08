#!/usr/bin/python2
import optparser as opt
import multiThread

target =  opt.args.URL
port = opt.args.port or 80
THREAD_COUNT = int(opt.args.thread or 100)
verbose = opt.args.verbose or False

if target.endswith('/'):
    target = target.strip('/')

def main():
    with open(opt.source, 'r') as f:
        txt = f.readlines()

    txt = [each.strip('\n') for each in txt if '\n' in each]

    map(multiThread.jobq.put, txt)

    for _ in xrange(THREAD_COUNT):
        T = multiThread.JThread(multiThread.condition, target, port)
        T.setDaemon(True)
        T.start()

    multiThread.jobq.join()

    print 'Tried : ',len(txt)

if __name__ == '__main__':
    main()
