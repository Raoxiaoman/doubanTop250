# coding:utf-8
import requests
from lxml import html
import sys 
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 

def downLoad(title):
    print(title)
    return

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

cur = open("./current.txt","r")
curnum = cur.readline().split()
if(is_number(curnum[0])):
    num = int(curnum[0])
    page = num / 25
    k = page*25 + 1
    url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25) 
    con = requests.get(url).content 
    sel = html.fromstring(con) 

    # 所有的信息都在class属性为info的div标签里，可以先把这个节点取出来 
    for i in sel.xpath('//div[@class="info"]'): 

        # 影片名称 
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0] 
        info = i.xpath('div[@class="bd"]/p[1]/text()') 
        # 导演演员信息 
        info_1 = info[0].replace(" ", "").replace("\n", "") 
        # 上映日期 
        date = info[1].replace(" ", "").replace("\n", "").split("/")[0] 
        # 制片国家 
        country = info[1].replace(" ", "").replace("\n", "").split("/")[1] 
        # 影片类型 
        geners = info[1].replace(" ", "").replace("\n", "").split("/")[2] 
        # 评分 
        rate = i.xpath('//span[@class="rating_num"]/text()')[0] 
        # 评论人数 
        comCount = i.xpath('//div[@class="star"]/span[4]/text()')[0] 

        # 打印结果看看 
        # print "TOP%s" % str(k) 
        # print title, info_1, rate, date, country, geners, comCount 

        # 写入文件 
        with open("movieInfo.txt", "w") as f: 
            f.write("TOP%s\n影片名称：%s\n评分：%s %s\n上映日期：%s\n上映国家：%s\n%s\n" % (k, title, rate, comCount, date, country, info_1)) 
            f.write("==========================\n") 

        if(k == num):
            downLoad(title)
            num += 1
            cur.close
            cur = open("./current.txt","w")
            cur.write(str(num))
            cur.close
            tag = 1
            break

        k += 1;


