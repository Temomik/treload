import sys

MSG_MAX_LEN = 150


class LEVEL(object):
    NO_DEBUG = 0
    DEBUG = 2
    TRACE = 1
    INFO = 3


_DEBUG = LEVEL.TRACE


def write(*args):
    msgList = []
    for a in args:
        s = str(a)
        if len(s) > MSG_MAX_LEN:
            s = s[:MSG_MAX_LEN] + '...'
        msgList.append(s)

    msg = ' '.join(msgList)
    sys.stdout.write('\n%s' % (msg,))


def writeErr(*args):
    newLst = []
    for a in args:
        newLst.append(str(a))

    msg = ' '.join(newLst)
    sys.stderr.write('\n[ERROR]: %s' % (msg,))


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
