#-*-coding:utf-8-*-
import urllib,urllib2,re,os,time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#phantomjs设置user_agent参数
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
)
#定义浏览器1
driver = webdriver.PhantomJS()
driver = webdriver.PhantomJS(desired_capabilities=dcap)
#定义浏览器2  防止抓取图片链接时出错
driver1 = webdriver.PhantomJS()
driver1 = webdriver.PhantomJS(desired_capabilities=dcap)

#文件路径
comName = "MMSpider\\"

# 入口url  淘女郎首页
url = "https://mm.taobao.com/?spm=719.7763510.1998606017.1.ecsHes"
# 相册url 还不会抓 只能拼接
url2= "https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20="

#模拟浏览器滑动条下滑
def winScroll():
    js1 = 'return document.body.scrollHeight'
    js2 = 'window.scrollTo(0, document.body.scrollHeight)'
    old_scroll_height = 0
    while (driver.execute_script(js1) > old_scroll_height):
        old_scroll_height = driver.execute_script(js1)
        driver.execute_script(js2)
        time.sleep(3)

# 普通获取html
def getHtml(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    return response.read()

# 获取相册内全部图片的链接
def driverHtml(url):
    driver.get(url)
    winScroll()
    return driver.find_elements_by_xpath('//div[@class="mm-photoimg-area"]/a')

# 获取图片的链接
def driverHtml1(url):
    driver1.get(url)
    time.sleep(3)
    return driver1.find_element_by_xpath('//div[@class="mm-p-img-panel"]/img')

# 正则匹配
def match(html,reg):
    pattern = re.compile(reg,re.S)
    return re.findall(pattern,html)
# 匹配数字
def matchNum(html):
    pattern = re.compile(r'pic_id=(\d+)', re.S)
    return re.findall(pattern,html)

# 创建目录
def mkdir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

#下载图片
def getImg(path,url):
    try:
        url123 = path +".jpg"
        print url123
        urllib.urlretrieve(url, url123)
    except Exception as e:
        print e
# 获取入口链接的页面
html1 = getHtml(url).decode("utf-8")
content = match(html1,"<p class=\"currentLady-name\">(.*?)</p>.*?<div class=\"currentLady-pic\">.*?<a href=\"(.*?)\".*?<img src=\"(.*?)\".*?</a>.*?</div>")
# print content
# 对每个mm进行抓取其
for item in content:
    purl = "https:"+str(item[1])
    html2 = getHtml(purl).decode("gbk")
    content1 = match(html2,"<li class=\"currentTab mm-add-red\">.*?<a href=\"(.*?)\".*?</a>.*?</li>")
    num = match(content1[0],"\d+")
    # print num
    for item1 in range(1,2):
        print item1
        try:
            mzurl = url2 + str(num[0]) + "&page=" + str(item1)
            html3 = getHtml(mzurl).decode("gbk")
            content3 = match(html3,"<h4>.*?<a href=\"(.*?)\" target=\"_blank\">(.*?)</a>.*?</h4>")
            q=1
            for mz in content3:
                # 添加文件目录
                path = comName + item[0] + "\\" + mz[1].strip()
                mkdir(path)
                url34 = "https:" + str(mz[0])
                imagesUrl = driverHtml(url34)
                # print imagesUrl
                for x in imagesUrl:
                    durl =  x.get_attribute('href')+"#"+str(matchNum(x.get_attribute('href'))[0].encode("utf-8"))
                    images = driverHtml1(durl).get_attribute("src")
                    getImg(path+"\\"+str(q), images)
                    q+=1
                break
        except Exception as e:
            print "错误"
            break

