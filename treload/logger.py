import sys


class LEVEL(object):
    NO_DEBUG = 0
    TRACE = 1
    DEBUG = 2
    INFO = 3


_DEBUG = LEVEL.NO_DEBUG


def write(*args):
    msgList = []
    for a in args:
        msgList.append(str(a))

    msg = ' '.join(msgList)
    sys.stdout.write('\n%s' % (msg,))


def writeErr(*args):
    newLst = []
    for a in args:
        newLst.append(str(a))

    msg = ' '.join(newLst)
    sys.stderr.write('\npydev debugger: %s' % (msg,))


def logInfo(*args):
    if _DEBUG >= LEVEL.TRACE:
        write(*args)


def logDebug(*args):
    if _DEBUG >= LEVEL.DEBUG:
        write(*args)


def logTrace(*args):
    if _DEBUG >= LEVEL.TRACE:
        write(*args)


def logError(*args):
    writeErr(*args)
