import json
import urllib2
import time

URL = 'http://m.miaopai.com/m/cate2_channel.json?cateid=136&columns=1&extend=1&os=ios&page=1&per=20&timestamp=1478226673552&token=gfOAJQhSpSw0NPRF9U9JegIlegdAVfvi&type=news&unique_id=cc59c089d5e720454a56260558620002520823219&uuid=cc59c089d5e720454a56260558620002520823219&vend=miaopai&version=6.6.1'
TOTAL = 0
SUCC = 0
FAIL = 0
TIMEOUT = 0
TIMES = 15
MAX_TIME = 0
MIN_TIME = 1
ST1 = 0
LT1 = 0
TOTAL_TIME = 0


def visit(number):
    global TOTAL
    global SUCC
    global FAIL
    global MAX_TIME
    global MIN_TIME
    global ST1
    global LT1
    global TOTAL_TIME
    global TIMEOUT

    st = time.time()
    try:
        response = urllib2.urlopen(URL)
    except Exception:
        print "timeout"
        TIMEOUT += 1
        TOTAL += 1
    else:
        api_content = response.read()
        json_object = json.loads(api_content)
        time_span = time.time()-st
        print "%s time is: %s" % (number+1, time_span)

        if json_object['status'] == 200:
            TOTAL += 1
            SUCC += 1
            TOTAL_TIME += time_span
            if time_span > MAX_TIME:
                MAX_TIME = time_span
            if time_span < MIN_TIME:
                MIN_TIME = time_span
            if time_span < 1:
                ST1 += 1
            if time_span > 1:
                LT1 += 1
        else:
            TOTAL += 1
            FAIL += 1
            if time_span > MAX_TIME:
                MAX_TIME = time_span
            if time_span < MIN_TIME:
                MIN_TIME = time_span


def main():
    print "====Test start===="

    for i in range(0, TIMES):
        visit(i)
        time.sleep(2)

    print "====Test Result===="
    print "Total: %s" % TOTAL
    print "Success: %s" % SUCC
    print "Fail: %s" % FAIL
    print "Timeout: %s" % TIMEOUT
    print "Max time: %s" % MAX_TIME
    print "Min time: %s" % MIN_TIME
    if SUCC == 0:
        print "No average time because SUCC=0"
    else:
        print "Average time: %f" % (TOTAL_TIME/SUCC)
    print "Small than 1s: %s, percent: %0.2f" % (ST1, float(ST1) / TOTAL)
    print "Large than 1s: %s, percent: %0.2f" % (LT1, float(LT1) / TOTAL)

if __name__ == '__main__':
    main()
