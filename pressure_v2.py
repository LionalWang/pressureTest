# coding=utf-8
import json
import urllib2
import time
import xlrd
import xlwt

TOTAL = 0
SUCC = 0
FAIL = 0
TIMEOUT = 0
MAX_TIME = 0
MIN_TIME = 1
ST1 = 0
LT1 = 0
TOTAL_TIME = 0


def visit(number, url):
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
        response = urllib2.urlopen(url)
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


def read():
    global TOTAL
    global SUCC
    global FAIL
    global MAX_TIME
    global MIN_TIME
    global ST1
    global LT1
    global TOTAL_TIME
    global TIMEOUT

    data = xlrd.open_workbook("interface.xlsx")

    for table in data.sheets():
        new_data = xlwt.Workbook()
        sheet = new_data.add_sheet(table.name, cell_overwrite_ok=True)

        sheet.write(0, 0, "URL")
        sheet.write(0, 1, "Description")
        sheet.write(0, 2, "Success count")
        sheet.write(0, 3, "Fail count")
        sheet.write(0, 4, "Timeout count")
        sheet.write(0, 5, "Largest time")
        sheet.write(0, 6, "Shortest time")
        sheet.write(0, 7, "Average time")
        sheet.write(0, 8, "Lager than 1 second")

        for i in range(1, table.nrows):
            TOTAL = 0
            SUCC = 0
            FAIL = 0
            TIMEOUT = 0
            MAX_TIME = 0
            MIN_TIME = 1
            ST1 = 0
            LT1 = 0
            TOTAL_TIME = 0

            times = table.col_values(2)[i]
            url = table.col_values(0)[i]

            print "====Test start===="

            for j in range(0, int(times)):
                visit(j, url)
                time.sleep(1)

            print url
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
                print "Average time: %f" % (TOTAL_TIME / SUCC)
            print "Small than 1s: %s, percent: %0.2f" % (ST1, float(ST1) / TOTAL)
            print "Large than 1s: %s, percent: %0.2f\n\n\n\n" % (LT1, float(LT1) / TOTAL)

            sheet.write(i, 0, url)
            sheet.write(i, 1, table.col_values(1)[i])
            sheet.write(i, 2, SUCC)
            sheet.write(i, 3, FAIL)
            sheet.write(i, 4, TIMEOUT)
            sheet.write(i, 5, MIN_TIME)
            sheet.write(i, 6, MAX_TIME)
            sheet.write(i, 7, TOTAL_TIME/SUCC)
            sheet.write(i, 8, float(LT1)/TOTAL)

        new_data.save('result.xls')


if __name__ == '__main__':
    read()
