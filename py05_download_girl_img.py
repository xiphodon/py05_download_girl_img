import urllib.request
import os
import random


def url_open(url):
    "链接url，并返回二进制数据"
    
    request = urllib.request.Request(url)
    request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")

    #  添加代理ip
    #proxy_list = ["121.40.108.76:80","120.76.243.40:80","122.96.59.99:80","124.88.67.17:82"]
    #proxy = random.choice(proxy_list)
    #proxy_support = urllib.request.ProxyHandler({"http":proxy})
    #opener = urllib.request.build_opener(proxy_support)
    #urllib.request.install_opener(opener)

    response = urllib.request.urlopen(url)
    html = response.read()

    return html



def get_page(url):
    "获取html中指定位置上的字符串，此处获得的是当前页面（即最后一页）的页码页数"
    
    html = url_open(url).decode("utf-8")
    
    #  找到解码为 utf-8 的 html 中 "current-comment-page" 的起始位置，并向后偏移23个字符，定位到页码处
    #  <span class="current-comment-page">[2196]</span>
    a = html.find("current-comment-page") + 23
    #  从 a 处向后寻找到"]"
    b = html.find("]",a)

    #  返回html中 a 到 b 之间的字符串（此处为页码）
    return html[a:b]



def find_imgs(url):
    "在当前html中获取所有图片的地址，并返回图片地址列表"
    
    html = url_open(url).decode("utf-8")
    img_addrs = []

    #  查找到html中"img src="起始位置为a
    a = html.find("img src=")

    #  a = -1即"img src="不再存在则跳出循环
    while a != -1:
        #  在html中，a为起始位置，a+255个偏移量为终点位置，找取中间包换".jpg"字符串的起始位置为b
        b = html.find(".jpg", a, a + 255)
        if b != -1:
            #  取得该图片的地址
            #  <img src="http://ww2.sinaimg.cn/mw600/66b3de17jw1f9fe8ym7iij20dw0k7wfp.jpg" style="max-width: 480px; max-height: none;">
            each_img_addrs = html[a + 9 : b + 4]

            #  筛选出需要图片地址并加入列表中
            if each_img_addrs.startswith("http://") and each_img_addrs.endswith(".jpg") and not " " in each_img_addrs:
                img_addrs.append(each_img_addrs)
        else :
            #  若b不存在即找不到，则增大b位置，可以在b后找新的a点
            b = a + 9

        #  在b后找新的a点
        a = html.find("img src=", b)

    #  输出图片地址列表
    for each in img_addrs:
        print(each)
        
    return img_addrs



def save_imgs(folder,img_addrs):
    "把图片地址列表中的图片全部存入指定目录中"
    
    for each in img_addrs:
        # 取拆分后的最后一部分作为图片的文件名
        filename = each.split("/")[-1]
        with open(filename,"wb") as f:
            img = url_open(each)
            f.write(img)

            

def download_main(folder = "girl_imgs",pages = 10):
    "主方法"
    "参数1：图片所放的文件夹目录"
    "参数2：想要爬取的页面数量"

    #  建立文件夹
    if not os.path.exists(folder):
        os.mkdir(folder)

    #  进入文件目录
    os.chdir(folder)

    url = "http://jiandan.net/ooxx/"
    #  页码由str转型为int
    page_num = int(get_page(url))

    for i in range(pages):
        page_num_copy = page_num - i

        #  拼接要爬取的页码的url
        #  http://jandan.net/ooxx/page-2195#comments
        page_url = url + "page-" + str(page_num_copy) + "#comments"
        
        #  在当前html中获取所有图片的地址，并返回图片地址列表
        img_addrs = find_imgs(page_url)
        
        #  把图片地址列表中的图片全部存入指定目录中
        save_imgs(folder, img_addrs)


#测试方法
if __name__ == "__main__":
    try:
        download_main("test30pages",30)
    except:
        pass
