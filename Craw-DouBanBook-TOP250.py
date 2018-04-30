import requests
from lxml import etree
import time
import re
AllList=[]#储存所有信息
AllList.append(['书名','作者','评分','评价人数','出版社','出版年月','页数','定价','地址'])#表头
def GetAllPageUrl():#获取每一页的地址
    AllUrl=[]
    for i in range(0,226,25):
        AllUrl.append('https://book.douban.com/top250?start={}'.format(i))
    return AllUrl
def GetAllBookUrl(selector):#获得每本书的地址
    AllUrl=[]
    book_url=selector.xpath('//*[@id="content"]/div/div[1]/div/table')
    for url in book_url:
        AllUrl.append(url.xpath('tr/td[2]/div[1]/a/@href')[0])
    return AllUrl
def GetSelector(url):#获取网页文档
    time.sleep(1)
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()#若连接网页错误则抛出异常
        r.encoding='utf-8'
        return r.text,etree.HTML(r.text)
    except:
        print("获取错误!")
        return 0,0
def GetList(selector,num,text,book_url):#爬取信息
    try:
        name=selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]#书籍名字
        author1=selector.xpath('//*[@id="info"]/a[1]/text()')[0]#作者
        author2=author1.replace(' ','')
        author=author2.replace('\n','')
        score=selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
        score_number=selector.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()')[0]
        press=re.findall('<span class="pl">出版社:</span> (.*?)<br/>',text)[0]
        time=re.findall('<span class="pl">出版年:</span> (.*?)<br/>',text)[0]
        pages=re.findall('<span class="pl">页数:</span> (.*?)<br/>',text)[0]
        price=re.findall('<span class="pl">定价:</span> (.*?)<br/>',text)[0]
    except:
        return num-1
    AllList.append([name,author,score,score_number,press,time,pages,price,book_url])
    print('{}'.format(AllList[num]))
    return num+1
def SaveCSV():#储存为CSV文件保存到本地
    fw = open("豆瓣图书TOP250.csv", 'w')
    for i in AllList:
        fw.write(",".join(i) + '\n')#用“，”分割数据，每行以“\n”结束
    fw.close()
def main():
    num=1
    AllPageUrl=GetAllPageUrl()
    for page in AllPageUrl:
        text1,selector1=GetSelector(page)
        AllBookUrl=GetAllBookUrl(selector1)
        for book in AllBookUrl:
            text2,selector2=GetSelector(book)
            if text2==0:
                continue
            num=GetList(selector2,num,text2,book)
    SaveCSV()
main()