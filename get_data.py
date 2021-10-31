#get_data.py
#hyn0027

import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
import random
import string
import requests
import re
import json
import os
import time
from bs4 import BeautifulSoup # import包

import sys 
from importlib import reload
reload(sys)
        
def main(): 
    #fileObject = open('data.json', 'a', encoding = 'utf-8')  
    #fileObject.write('{\n')
    #fileObject.close()  
    cnt = 0
    for av_idx in range(30020000, 30021000):
        try:
            print("start" + str(av_idx))
            #1 m_title 视频标题
            #2 introduce 简介
            #3 url 视频播放页url
            #4 E:\hyn_new\summer\python\code\pic\xxxxxxxx.jpg 封面图片
            #5 played_time 播放量
            #6 barrage_num 弹幕数
            #7 upload_time 上传时间
            #8 liked_num 点赞数
            #9 coin_num 投币数
            #10 collect_num 收藏数
            #11 share_num 转发数
            #12 comment_num 评论数
            #13 comments[] 评论
            #14 creator_ID 作者ID
            #15 creator_introduce 作者简介
            #16 E:\hyn_new\summer\python\code\creator\ID.jpg 作者头像图片
            #17 followers 粉丝数
            #18 type 联合投稿(1)
            #19 uid B站编号
            
            #确定地址
            url = 'https://www.bilibili.com/video/av' + str(av_idx)
            html = requests.get(url)
            html.encoding = 'utf8'
            
            #获取soup
            soup = BeautifulSoup(html.text, 'lxml')
            do_not_exist = soup.find_all(string = "视频去哪了呢？_哔哩哔哩_bilibili")
            
            #判断是否存在
            if len(do_not_exist) != 0:
                continue
            
            #计数
            cnt += 1
            
            #视频标题
            m_title = str(soup.title.string[:-14])
            
            #视频简介
            get_introduce = soup.find_all(class_ = "desc-info desc-v2 open")
            if len(get_introduce) == 0:
                continue
            introduce = str(get_introduce[0])
            introduce = introduce[42 : -13]
            
            #封面图片
            target = soup.find("meta", itemprop = "thumbnailUrl")
            target = str(target["content"])
            path = 'E:\\hyn_new\\summer\\python\\code\\pic'
            if not os.path.isdir(path):
                os.makedirs(path)
            path += '\\'
            urllib.request.urlretrieve(target, path + str(av_idx) + '.jpg')
            
            #播放量
            my_played = soup.find(class_ = "view")
            played_time = str(my_played.string)[:-5]
            
            #弹幕数
            my_barrage = soup.find(class_ = "dm")
            barrage_num = str(my_barrage.string)[:-2]
            
            #上传时间
            my_upload_time = soup.find(class_  = "dm").find_next_sibling()
            upload_time = str(my_upload_time.string)
            
            #点赞数
            my_like = soup.find_all(class_ = "like")
            liked_num = my_like[0]['title'][3:]
            if len(liked_num) == 0:
                liked_num = "0"
            
            #投币数
            my_coin_num = soup.find_all(class_ = "coin")
            coin_num = my_coin_num[0]['title'][5:]
            if len(coin_num) == 0:
                coin_num = "0"
            
            #收藏数
            my_collect_num = soup.find_all(class_ = "collect")
            collect_num = my_collect_num[0]['title'][4:]
            if len(collect_num) == 0:
                collect_num = "0"
            
            #转发数
            my_share_num = soup.find_all(class_ = "share")
            share_num = str(my_share_num[0])
            left_num = share_num.find('</i>') + 4
            right_num = share_num.find('\n')
            share_num = share_num[left_num : right_num]
            if share_num == "分享":
                share_num = "0"
            
            #评论数
            titles = soup.select("script") # CSS 选择器
            i = 1
            comment_num = "0"
            for title in titles:
                m_str = str(title)
                tmp = m_str.find("reply")
                if tmp != -1:
                    comment_num = m_str[tmp + 7 : tmp + 30]
                    right_tmp = comment_num.find(",")
                    comment_num = comment_num[: right_tmp]
                    break
            
            #5条评论
            driver = webdriver.Chrome(executable_path = "D:\python\chromedriver.exe")
            driver.get(url)
            time.sleep(3.2)
            
            driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(1)
            driver.execute_script('window.scrollBy(0,7000)')
            time.sleep(1)
        
            time.sleep(1)
            
            comments = []
            my_comments = driver.find_elements_by_css_selector('#comment > div > div.comment > div.bb-comment > div.comment-list > div > div.con > p')
            cur_cnt = 0
            for i in my_comments:
                comments.append(i.text)
                cur_cnt += 1
                if cur_cnt == 5:
                    break
            driver.close()
            
            #作者ID
            creator_ID = str(soup.find(attrs = {"name": "author"})['content'])
            
            #作者简介
            my_creator_introduce = soup.find_all(class_ = "up-info_right")
            creator_introduce = ""
            if len(my_creator_introduce) != 0:
                type = 0
                my_creator_introduce = my_creator_introduce[0]
                creator_introduce = my_creator_introduce.find(class_ = "desc")
                if creator_introduce == None:
                    creator_introduce = ""
                else:
                    creator_introduce = creator_introduce['title']
            else:
                type = 1
                my_creator_introduce = soup.find_all(class_ = "up-card")
                my_creator_introduce = my_creator_introduce[0]
                tmp = my_creator_introduce.find_all(class_ = "avatar")
                user_space = tmp[0]['href']
                tmp_url = "https:" + user_space;
                tmp_html = requests.get(tmp_url)
                tmp_html.encoding = "utf-8"
                tmp_soup = BeautifulSoup(tmp_html.text, 'lxml')
                my_creator_introduce = tmp_soup.find(attrs = {"name": "description"})
                creator_introduce = my_creator_introduce['content']
                right_num = creator_introduce.find(creator_ID + "的主页、动态、视频、专栏")
                creator_introduce = creator_introduce[len(creator_ID) + 1: right_num - 1]
            
            #作者头像&uid
            if type == 0:
                user_space = soup.find_all(class_ = "fa")[0]['href']
                tmp_url = "https:" + user_space;
                tmp_html = requests.get(tmp_url)
                tmp_html.encoding = "utf-8"
                tmp_soup = BeautifulSoup(tmp_html.text, 'lxml')
            uid = tmp_url[27:]
            my_img = tmp_soup.find(rel = "apple-touch-icon")['href']
            path = 'E:\\hyn_new\\summer\\python\\code\\creator'
            if not os.path.isdir(path):
                os.makedirs(path)
            path += '\\'
            if my_img == "":
                continue
            #用户已注销
            urllib.request.urlretrieve(my_img, path + str(uid) + '.jpg')
            
            #粉丝数
            driver = webdriver.Chrome(executable_path = "D:\python\chromedriver.exe")
            driver.get("https://space.bilibili.com/" + str(uid) + "/")
            time.sleep(2)
            content = driver.find_element_by_xpath('//*[@id="n-fs"]')
            followers = content.text
            driver.close()
            
            #转dict
            thisdict = {
                "title": m_title,
                "introduce": introduce,
                "url": url,
                "avid": av_idx,
                "view_cnt": played_time,
                "barrage_cnt": barrage_num,
                "upload_time": upload_time,
                "liked_num": liked_num,
                "coin_num": coin_num,
                "collect_num": collect_num,
                "share_num": share_num,
                "comment_num": comment_num,
                "comments": comments,
                "creator_ID": creator_ID,
                "creator_introduce": creator_introduce,
                "uid": uid,
                "followers": followers,
                "type": type
            }
            #print(thisdict)
            js_Obj = json.dumps(thisdict, ensure_ascii = False, indent = 1)  
            fileObject = open('data.json', 'a', encoding = 'utf-8')  
            fileObject.write("\"av" + str(av_idx)  + "\": ")
            fileObject.write(js_Obj)  
            fileObject.write(',\n')
            fileObject.close()
        except:
            av_idx -= 1
            print("oops")
            continue
    print(cnt)
    fileObject = open('data.json', 'a', encoding = 'utf-8')  
    fileObject.write('}\n')
    fileObject.close()  
    
main()