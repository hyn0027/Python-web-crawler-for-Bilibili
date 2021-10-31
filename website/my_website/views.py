from django.shortcuts import render
import os
import django
import orjson as json
import time
import numba

os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()

def run_video_information(request, idx):
    idx = str(idx)
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    item = load_dict["av" + idx]
    comment_num = item["comment_num"]
    comments = item["comments"]
    if len(comments) > 0:
        comment_0 = comments[0]
    else:
        comment_0 = "-"
    if len(comments) > 1:
        comment_1 = comments[1]
    else:
        comment_1 = "-"
    if len(comments) > 2:
        comment_2 = comments[2]
    else:
        comment_2 = "-"
    if len(comments) > 3:
        comment_3 = comments[3]
    else:
        comment_3 = "-"
    if len(comments) > 4:
        comment_4 = comments[4]
    else:
        comment_4 = "-"
    item["comment_0"] = comment_0
    item["comment_1"] = comment_1
    item["comment_2"] = comment_2
    item["comment_3"] = comment_3
    item["comment_4"] = comment_4
    item["up_url"] = "http://127.0.0.1:8000/up/" + item["uid"] + "/"
    return render(request, 'video_information.html', item)

def run_up_information(request, idx):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    idx = str(idx)
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    list = [];
    for x in load_dict:
        if load_dict[x]["uid"] == idx:
            list.append(load_dict[x])
    item = {}
    my_len = len(list)
    item["uid"] = list[0]["uid"]
    if page > (my_len + 7) // 8:
        page = 1
    page_right = min((my_len + 7) // 8, page + 6)
    page_left = max(1, page - 6)
    item["my_pages_goto"] = []
    for x in range(page_left, page_right + 1):
        tmp_list = []
        tmp_list.append(str(x))
        m_str = "http://127.0.0.1:8000/up/" + str(idx) + "/?page=" + str(x)
        tmp_list.append(m_str)
        vv = 0
        if x == page:
            vv = 1
        tmp_list.append(str(vv))
        item["my_pages_goto"].append(tmp_list)
    page_start = (page - 1) * 8;
    page_end = min(page * 8, my_len)
    my_title = []
    for x in range(page_start, page_end):
        tmp_list = []
        m_str = "/static/pic/" + str(list[x]["avid"]) + ".jpg"
        tmp_list.append(m_str)
        tmp_list.append(list[x]["title"])
        m_str = "http://127.0.0.1:8000/video/" + str(list[x]["avid"]) + "/"
        tmp_list.append(m_str)
        my_title.append(tmp_list)
    item["title"] = my_title
    item["name"] = list[0]["creator_ID"]
    item["introduce"] = list[0]["creator_introduce"]
    item["followers"] = list[0]["followers"]
    item["page"] = page;
    return render(request, 'up_information.html', item)

def run_homepage(request, sth = ""):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    one_page_num = 60;
    item = {}
    item["mm_total"] = len(load_dict) 
    item["page_total"] = (len(load_dict) + one_page_num - 1) // one_page_num
    if page > item["page_total"]:
        page = 1
    start_num = one_page_num * (page - 1) + 1; #1
    end_num = min(one_page_num * page, len(load_dict)) #60
    visited = 0;
    list = []
    for x in load_dict:
        visited += 1
        if visited >= start_num:
            list.append(load_dict[x])
        if visited == end_num:
            break
    item["my_video"] = []
    for x in list:
        tmp_list = []
        m_str = "/static/pic/" + str(x["avid"]) + ".jpg"
        tmp_list.append(m_str)
        tmp_list.append(x["title"])
        m_str = "http://127.0.0.1:8000/video/" + str(x["avid"]) + "/"
        tmp_list.append(m_str)
        item["my_video"].append(tmp_list)
    page_right = min((len(load_dict) + one_page_num - 1) // one_page_num, page + 2)
    page_left = max(1, page - 2)
    if page == 4:
        page_left = 1
    item["left_url"] = "http://127.0.0.1:8000/home/?page=1"
    item["right_url"] = "http://127.0.0.1:8000/home/?page=" + str(item["page_total"])
    if page > 4:
        item["left_pass"] = 1
    else:
        item["left_pass"] = 0
    if page == item["page_total"] - 3:
        page_right = item["page_total"]
    if page < item["page_total"] - 3:
        item["right_pass"] = 1
    else:
        item["right_pass"] = 0
    item["before_url"] = "orz"
    if page == 1:
        item["page_before"] = 0
    else:
        item["page_before"] = 1
        item["before_url"] = "http://127.0.0.1:8000/home/?page=" + str(page - 1)
    item["next_url"] = "orz"
    if page == item["page_total"]:
        item["page_next"] = 0
    else:
        item["page_next"] = 1
        item["next_url"] = "http://127.0.0.1:8000/home/?page=" + str(page + 1)
    item["my_pages_goto"] = []
    for x in range(page_left, page_right + 1):
        tmp_list = []
        tmp_list.append(str(x))
        m_str = "http://127.0.0.1:8000/home/?page=" + str(x)
        tmp_list.append(m_str)
        vv = 0
        if x == page:
            vv = 1
        tmp_list.append(str(vv))
        item["my_pages_goto"].append(tmp_list)
    item["page"] = page
    return render(request, 'homepage.html', item)
    
def run_creator(request):
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    creator = {}
    for x in load_dict:
        creator[load_dict[x]["uid"]] = load_dict[x]["creator_ID"]
    one_page_num = 70;
    item = {}
    item["mm_total"] = len(creator)
    item["page_total"] = (len(creator) + one_page_num - 1) // one_page_num
    if page > item["page_total"]:
        page = 1
    start_num = one_page_num * (page - 1) + 1; #1
    end_num = min(one_page_num * page, len(load_dict)) #60
    visited = 0;
    list = []
    for x in creator:
        visited += 1
        if visited >= start_num:
            tmp = []
            tmp.append(x)#0
            tmp.append(creator[x])#1
            m_str = "http://127.0.0.1:8000/up/" + str(x) + "/"
            tmp.append(m_str)#2
            m_str = "/static/creator/" + str(x) + ".jpg"
            tmp.append(m_str)#3
            list.append(tmp)
        if visited == end_num:
            break
    item["list"] = list
    page_right = min(item["page_total"], page + 2)
    page_left = max(1, page - 2)
    if page == 4:
        page_left = 1
    item["left_url"] = "http://127.0.0.1:8000/creator/?page=1"
    item["right_url"] = "http://127.0.0.1:8000/creator/?page=" + str(item["page_total"])
    if page > 4:
        item["left_pass"] = 1
    else:
        item["left_pass"] = 0
    if page == item["page_total"] - 3:
        page_right = item["page_total"]
    if page < item["page_total"] - 3:
        item["right_pass"] = 1
    else:
        item["right_pass"] = 0
    item["before_url"] = "orz"
    if page == 1:
        item["page_before"] = 0
    else:
        item["page_before"] = 1
        item["before_url"] = "http://127.0.0.1:8000/creator/?page=" + str(page - 1)
    item["next_url"] = "orz"
    if page == item["page_total"]:
        item["page_next"] = 0
    else:
        item["page_next"] = 1
        item["next_url"] = "http://127.0.0.1:8000/creator/?page=" + str(page + 1)
    item["my_pages_goto"] = []
    for x in range(page_left, page_right + 1):
        tmp_list = []
        tmp_list.append(str(x))
        m_str = "http://127.0.0.1:8000/creator/?page=" + str(x)
        tmp_list.append(m_str)
        vv = 0
        if x == page:
            vv = 1
        tmp_list.append(str(vv))
        item["my_pages_goto"].append(tmp_list)
    item["page"] = page
    return render(request, 'creators.html', item)

def run_search(request):
    return render(request, 'search.html')

def get_item_video(page, choose, key):
    time_start=time.time()
    str_base = "http://127.0.0.1:8000/search_result/?key=" + key + "&choose=" + choose + "&page="
    item = {}
    m_list = []
    seq = []
    '''
    load_f = open("data.json",'r', encoding = 'utf-8')
    load_dict = json.load(load_f)'''
    
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    append1 = m_list.append
    for x in load_dict:
        if (load_dict.get(x).get("title").find(key) != -1) or (load_dict[x]["introduce"].find(key) != -1):
            append1(x)
    one_page_num = 28
    item["page_total"] = (len(m_list) + one_page_num - 1) // one_page_num
    if page > item["page_total"]:
        page = 1
    item["total_result"] = len(m_list)
    st = (page - 1) * one_page_num
    ed = min(st + one_page_num, item["total_result"])
    item["my_video"] = []
    appendi = item["my_video"].append
    for i in range(st, ed):
        x = m_list[i]
        tmp_list = []
        tappend = tmp_list.append
        seq = ("/static/pic/", str(load_dict[x]["avid"]), ".jpg")
        tappend(''.join(seq))
        tappend(load_dict[x]["title"])
        seq = ("http://127.0.0.1:8000/video/", str(load_dict[x]["avid"]), "/")
        tappend(''.join(seq))
        appendi(tmp_list)
    page_right = min(item["page_total"], page + 2)
    page_left = max(1, page - 2)
    if page == 4:
        page_left = 1
    seq = (str_base, "1")
    item["left_url"] = ''.join(seq)
    seq = (str_base, str(item["page_total"]))
    item["right_url"] = ''.join(seq)
    if page > 4:
        item["left_pass"] = 1
    else:
        item["left_pass"] = 0
    if page == item["page_total"] - 3:
        page_right = item["page_total"]
    if page < item["page_total"] - 3:
        item["right_pass"] = 1
    else:
        item["right_pass"] = 0
    item["before_url"] = ""
    if page == 1:
        item["page_before"] = 0
    else:
        item["page_before"] = 1
        seq = (str_base, str(page - 1))
        item["before_url"] = ''.join(seq)
    item["next_url"] = "orz"
    if page == item["page_total"]:
        item["page_next"] = 0
    else:
        item["page_next"] = 1
        seq = (str_base, str(page + 1))
        item["next_url"] = ''.join(seq)
    item["my_pages_goto"] = []
    appendp = item["my_pages_goto"].append
    for x in range(page_left, page_right + 1):
        tmp_list = []
        tappend = tmp_list.append
        tappend(str(x))
        seq = (str_base, str(x))
        tappend(''.join(seq))
        if x == page:
            tappend("1")
        else:
            tappend("0")
        appendp(tmp_list)
    item["page"] = page
    time_end=time.time()
    item["time"] = str(int(round(time_end - time_start, 4) * 1000))
    return item

def get_item_up(page, choose, key):
    time_start=time.time()
    str_base = "http://127.0.0.1:8000/search_result/?key=" + key + "&choose=" + choose + "&page="
    item = {}
    m_list = []
    seq = []
    append1 = m_list.append
    with open("data.json", "rb") as f:
        load_dict = json.loads(f.read())
    m_list_2 = []
    m_dict = {}
    append2 = m_list_2.append
    one_page_num = 28
    for x in load_dict:
        if m_dict.get(str(load_dict.get(x).get("uid")), False):
            continue
        if (load_dict.get(x).get("creator_ID").find(key) != -1) or (load_dict[x]["creator_introduce"].find(key) != -1):
            append1(load_dict[x]["uid"])
            append2(load_dict[x]["creator_ID"])
            m_dict[str(load_dict[x]["uid"])] = "1";
    item["page_total"] = (len(m_list) + one_page_num - 1) // one_page_num
    if page > item["page_total"]:
        page = 1
    item["total_result"] = len(m_list)
    st = (page - 1) * one_page_num
    ed = min(st +  one_page_num, item["total_result"])
    item["list"] = []
    appendi = item["list"].append
    for i in range(st, ed):
        x = m_list[i]
        tmp = []
        t_append = tmp.append
        t_append(x)#0
        t_append(m_list_2[i])#1
        seq = ("http://127.0.0.1:8000/up/", str(x), "/")
        t_append(''.join(seq))#2
        seq = ("/static/creator/", str(x), ".jpg")
        t_append(''.join(seq))#3
        appendi(tmp)
    item["page"] = page
    page_right = min(item["page_total"], page + 2)
    page_left = max(1, page - 2)
    if page == 4:
        page_left = 1
    seq = (str_base, "1")
    item["left_url"] = ''.join(seq)
    seq = (str_base, str(item["page_total"]))
    item["right_url"] = ''.join(seq)
    if page > 4:
        item["left_pass"] = 1
    else:
        item["left_pass"] = 0
    if page == item["page_total"] - 3:
        page_right = item["page_total"]
    if page < item["page_total"] - 3:
        item["right_pass"] = 1
    else:
        item["right_pass"] = 0
    item["before_url"] = ""
    if page == 1:
        item["page_before"] = 0
    else:
        item["page_before"] = 1
        seq = (str_base, str(page - 1))
        item["before_url"] = ''.join(seq)
    item["next_url"] = "orz"
    if page == item["page_total"]:
        item["page_next"] = 0
    else:
        item["page_next"] = 1
        seq = (str_base, str(page + 1))
        item["next_url"] = ''.join(seq)
    item["my_pages_goto"] = []
    appendp = item["my_pages_goto"].append
    for x in range(page_left, page_right + 1):
        tmp_list = []
        t_append = tmp_list.append
        t_append(str(x))
        seq = (str_base, str(x))
        t_append(''.join(seq))
        if x == page:
            t_append("1")
        else:
            t_append("0")
        appendp(tmp_list)
    time_end=time.time()   
    item["time"] = str(int(round(time_end - time_start, 4) * 1000))
    return item

def run_search_result(request):
    key = str(request.GET.get("key"))
    choose = str(request.GET.get("choose"))
    try:
        page = int(request.GET.get("page"))
    except:
        page = 1
    
    if choose == "video":
        item = get_item_video(page, choose, key)
        item["key"] = key
        return render(request, 'search_result_video.html', item)
    else:
        item = get_item_up(page, choose, key)
        item["key"] = key
        return render(request, 'search_result_up.html', item)