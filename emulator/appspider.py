# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 9:11
# @Author  : GLY
# @FileName: appspider.py
# @Software: PyCharm

import requests
import re
import json
import os
import io
def get_categorylist(index_url):
    response = requests.get(index_url)
    response.encoding = 'utf-8'
    data = re.findall("应用分类(.*?)</ul></div> <div class=".decode('utf-8'), response.text)
    data = data[0].split("实用工具".decode('utf-8'))
  #  data = re.findall("应用分类(.*?)</ul></div> <div class=", requests.get(index_url).text)
  #  data = data[0].split("游戏应用")
    list1 = re.findall("<a  href=\"/category/(.*?)</a></li>", data[0])
    list2 = re.findall("<a  href=\"/category/(.*?)</a></li>", data[1])
    list = []
    for l in list1:
        l = l.split("\">")
        list.append(l)
    for l in list2:
        l = l.split("\">")
        list.append(l)
    for i in list:
	print(i[0])
        print(i[1])
    return list
def unicode_convert(input):
    if isinstance(input, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicode_convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
            
def get_category(selected_url_category,page_begin, page_end):
    app_details_list = []
    for page in range(int(page_begin)-1, int(page_end)):
        print("正在爬取第"+str(page)+"页, 共"+str(page_end)+"页")
        url = selected_url_category+"&page="+str(page)
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.text
       # print(data)
        data1 = json.loads(data,encoding="utf-8")
        for datas in data1["data"]:
            app_details_list.append([datas["displayName"], datas["packageName"]])
            #print(data["displayName"], data["packageName"])
   # print(app_details_list)
    return app_details_list

def get_download_link(url_details, app_details_list):
    download_link_list = []
    for app in app_details_list:
        url = url_details+app[1]
        data = re.findall("<div class=\"app-info-down\"> <a href=\"(.*?)\" class=\"download\">", requests.get(url).text)
        download_link_list.append("https://app.mi.com"+data[0])
        print(app[0]+" https://app.mi.com/details?id="+app[1])
    return download_link_list


if __name__ == '__main__':
    url = "https://app.mi.com/"
    url_category_api ="https://app.mi.com/categotyAllListApi?"
    # https://app.mi.com/categotyAllListApi?page=0&categoryId=20
    url_details = "https://app.mi.com/details?id="
    # https: // app.mi.com / details?id = com.joym.legendhero.mi


    category_list = get_categorylist(url) 
    #get all category
    print("==========================================")
    category_selected = input("请输入要爬取的app类型编号：")
    print("请输入要爬取的页码")
    page_begin = input("开始页码：")
    page_end = input("结束页码：")

    download_num = input("本次共爬取"+str((int(page_end)-int(page_begin)+1)*20)+"个，请输入要下载的数量：")

    print(">>>>>>>开始爬取>>>>>>>>>>>>>>>>")
    app_details_list = get_category(url_category_api+"categoryId="+str(category_selected), page_begin, page_end)
    download_link_list = get_download_link(url_details, app_details_list)

    category_dict = {}
    for category in category_list:
        category_dict[category[0]] = category[1]
    # number - category

   
    print("===============爬取=======================\n")
    file_name = category_dict[unicode(str(category_selected),"utf-8")] + "--" + str(page_begin)+"--" + str(page_end) + ".txt"
    with io.open(file_name, 'w', encoding='utf-8') as f:
        for (m, n) in zip(app_details_list, download_link_list):
            f.write(m[0]+ " "+m[1]+" "+"https://app.mi.com/details?id="+m[1] + " " + n + "\n")
    print("===============爬取完毕=======================\n")
    print("本次爬取"+str(len(app_details_list))+"个\n")

    # 下载模块
    print(">>>>>>>开始下载>>>>>>>>>>>>>>>>")
    download = []
    for line in io.open(file_name, encoding='utf-8'):
        download.append(line.split(' '))

    print((category_dict[unicode(str(category_selected),"utf-8")]))
    print(">>>>>>>开始下载>>>>>>>>>>>>>>>>")
    try:
        os.mkdir(category_dict[unicode(str(category_selected),"utf-8")])
    except:
        print("目录已存在，直接进入目录")
        pass
    os.chdir(category_dict[unicode(str(category_selected),"utf-8")])
    num = 0
    for d in download:
    	
        if (download_num == 0):
            break
        down_url = d[3][0:-2]

        apk_name = d[1]
        try:
        	down_res = requests.get(url=down_url)
        	with io.open(apk_name + '.apk', "wb") as code:
            		code.write(down_res.content)
            		download_num = int(download_num) - 1
            		num = num + 1

            		print("Downloading "+str(num)+"th Filename:"+(apk_name))
            		code.close()
        except:
        	print("Downlaod APK Error:"+(apk_name))
        	continue
    print("下载完成")



