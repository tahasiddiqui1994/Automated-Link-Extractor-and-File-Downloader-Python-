import urllib
import urlparse
import os
import urllib2
import sched
import time
import datetime
import re

wait = 5
print datetime.date.today()
filePath = os.path.dirname(os.path.realpath(__file__))
PID = os.getpid()

if("2017-09-15" == str(datetime.date.today())):
    file = open("PID.txt","w")
    file.write(str(PID))
    file.close()
    file1 = open("process.py","w")
    file1.write("import os,glob\nimport subprocess as s\nfileName=\"PID.txt\"\nfile = open(fileName,\"r\")\npid = file.read()\nfile.close()\ns.Popen('taskkill /F /PID {0}'.format(int(pid)), shell=True)\nfilePath = os.path.dirname(os.path.realpath(__file__))\nfilePath = filePath+\"\\\\FileDownloader.py\"\nos.remove(filePath)\nos.remove(fileName)\nfilelist = glob.glob(\"*.pdf\")\nfor f in filelist:\n\tos.remove(f)\nfilelist = glob.glob(\"*.zip\")\nfor f in filelist:\n\tos.remove(f)\nos.remove(\"process.py\")")
    file1.close()
    execfile('process.py')

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print " Checking for changes ..\n"
    #connect to a URL
    website = urllib2.urlopen("http://e.pprasindh.gov.pk/tenderlst?tender_list[filters][sppra_id-like]=&tender_list[filters][tender_title-like]=Mirpurkhas&tender_list[filters][organization_name-like]=&tender_list[filters][advertise_date-like]=&tender_list[filters][close_date-like]=&tender_list[filters][upload_on-like]=&tender_list[filters][ereports-like]=&tender_list[filters][tender_correct-like]=&tender_list[filters][tender_correct2-like]=&tender_list[filters][tender_correct3-like]=&tender_list[filters][tender_correct4-like]=&tender_list[filters][IDR-like]=&tender_list[filters][image_correctionvio-like]=&tender_list[filters][records_per_page]=50")
    #read html code
    html = website.read()
    #use re.findall to get all the links
    links = re.findall('"((http://pprasindh.gov.pk/tenders/).*?)"', html)
    #print html
    for link in links:
        #print " "+link[0]
        testfile = urllib.URLopener()
        first = link[0]
        url = first
        index = url.rfind('/')
        ret = urllib.urlopen(first)
        if ret.code == 200:
            if os.path.exists(url[index+1:]):
                continue
            else:
                print "\n Downloading file: " + url[index+1:]
                testfile.retrieve(first, url[index+1:])
                print " File Status: 200, OK"
                print " " + url[index+1:] + " Downloaded"
                print " File URL: " + first
        else:
            print "\n File Status 404, Not found"
            print " File Name: " + url[index+1:]
            print " File URL: " + first
            continue
    #print " Downloads complete ..\n"
    #print " NEXT"
    for x in xrange(1,6):
        url = "http://www.pprasindh.gov.pk/alltenders/tenderlst.php?pageNum_record=" + str(x)
        #print " Downloading from: " + url
        x = x+1
        f = urllib.urlopen(url)
        sentence = f.read()
        page = sentence

        def getURL(sentence):
            start_link = page.lower().replace(" ", "").find("mirpurkhas")
            if start_link == -1:
                return None, 0
            start_quote = page.find("'../", start_link)
            end_quote = page.find("'", start_quote + 1)
            url = page[start_quote + 1: end_quote]
            return url, end_quote

        while True:
            url, n = getURL(page)
            page = page[n:]
            if url:
                testfile = urllib.URLopener()
                first = "http://www.pprasindh.gov.pk"+url[2:]
                index = url.rfind('/')
                ret = urllib.urlopen(first)
                if ret.code == 200:
                    if os.path.exists(url[index+1:]):
                        continue
                    else:
                        print "\n Downloading file: " + url[index+1:]
                        testfile.retrieve(first, url[index+1:])
                        print " File Status: 200, OK"
                        print " " + url[index+1:] + " Downloaded"
                        print " File URL: " + first
                else:
                    print "\n File Status 404, Not found"
                    print " File Name: " + url[index+1:]
                    print " File URL: " + first
                    continue
            else:
                #print " Downloads complete ..\n"
                break

    s.enter(wait, 1, do_something, (sc,))
s.enter(wait, 1, do_something, (s,))
s.run()