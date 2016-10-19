import json
import urllib2
import threading
import time

URL = 'http://api.miaopai.com/m/ad_hot.json?version=6.6.1.0&require=0'
TOTAL = 0
SUCC = 0
FAIL = 0
TIMES = 1000
MAX_TIME = 0
ST1 = 0
LT1 = 0


def visit():
    global TOTAL
    global SUCC
    global FAIL
    global MAX_TIME
    global ST1
    global LT1

    st = time.time()
    response = urllib2.urlopen(URL)
    api_content = response.read()
    json_object = json.loads(api_content)
    time_span = time.time()-st

    if json_object['status'] == 200:
        TOTAL += 1
        SUCC += 1
        if time_span > MAX_TIME:
            MAX_TIME = time_span
        if time_span < 1:
            ST1 += 1
        if time_span > 1:
            LT1 += 1
    else:
        TOTAL += 1
        FAIL += 1
        if time_span > MAX_TIME:
            MAX_TIME = time_span


def main():
    print "====Test start===="
    threads = []

    for i in range(0, TIMES):
        t = threading.Thread(target=visit)
        threads.append(t)

    for i in range(0, TIMES):
        threads[i].start()

    for i in range(0, TIMES):
        threads[i].join()

    print "Total: %s" % TOTAL
    print "Success: %s" % SUCC
    print "Fail: %s" % FAIL
    print "Max time: %s" % MAX_TIME
    print "Small than 1s: %s, percent: %0.2f" % (ST1, float(ST1) / TOTAL)
    print "Large than 1s: %s, percent: %0.2f" % (LT1, float(LT1) / TOTAL)

if __name__ == '__main__':
    main()
