#coding:utf8
import urllib2
import lxml.html as HTML
import time
import random
import sys
import re
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
sys.setdefaultencoding('utf-8')

proxyfile = open("./src/proxy.txt")
lines = proxyfile.readlines()
def proxy():
    i = random.randint(1, len(lines))
    ip = lines[i].strip("\n").split("\t")
    proxy_host =  ip[0] + ":" + ip[1]
    return proxy_host

def baidu(num):
    url = 'https://www.baidu.com/s?ie=utf-8&wd=%s'%num
    try:
        headers = {'Accept':'text/html, application/xhtml+xml, */*',
                   'Accept-Language':'zh-CN',
                   'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0) QQBrowser/8.2.4257.400'
                   }
        requ = urllib2.Request(url,headers=headers)
        proxy_get = proxy()
        print proxy_get
        requ.set_proxy(proxy_get,'http')
        req = urllib2.urlopen(requ,timeout=30)
        res = req.read()
        doc = HTML.document_fromstring(res)
        c = doc.xpath("//*[@id='1']/div[1]/div[1]/div[2]/div[2]/span[2]")
        if len(c)>0:
            #正常号码只获取归属地
            guishudi = c[0].text.strip()
            #print guishudi
            nvalue = num + "\t" + guishudi
            #print(revalue)
            print num+"--------"+"00"
            return str(nvalue)
        else:
            #其他号码获取 类型和被标记的数量
            c1 = doc.xpath("//*[@id='1']/div[1]/div/div[2]/div[2]/strong")
            leixing = c1[0].text_content().strip('\" ')
            c2 = doc.xpath("//*[@id='1']/div[1]/div/div[2]/div[2]")
            shuliang = c2[0].text.strip()[1:-1]
            #print shuliang,leixing
            wvalue = num + "\t" + leixing + "\t" + shuliang
            print num+"--------"+"11"
            return str(wvalue)
    except:
        pass
        print num +"----------except"
        return ''

inFile = open("./input/20160607.txt",'r')
outFile = open("./output/baidu-output.txt",'w')
errFile = open("./output/baidu-error.txt",'w')

print(time.ctime())
outFile.write(time.ctime() + '\n')
for line in inFile.readlines():
    line = line.replace('\n','')
    rdom = random.randint(1,5)
    time.sleep(rdom)
    tv = baidu(line)
    if len(tv)>0:
        outFile.write(str(tv) + '\n')
    else:
        errFile.write(line + '\n')
print(time.ctime())
outFile.write(time.ctime() + '\n')
inFile.close()
outFile.close()
errFile.close()
