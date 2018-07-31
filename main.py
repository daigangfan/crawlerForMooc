import requests
import threading
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from time import sleep
from collections import OrderedDict
import re
i=0
driver=webdriver.Chrome("chromedriver.exe")
driver.get("http://tsinghua.xuetangx.com/newcloud/login/#/login")

nodes=driver.find_elements_by_tag_name("input")
nodes[0].send_keys("2015012502")
nodes[1].send_keys("********")
node=driver.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div/form/div[4]/button")
node.click()
WebDriverWait(driver,1000).until(expected_conditions.url_contains("mycredit"))
driver.get("http://tsinghua.xuetangx.com/courses/course-v1:TsinghuaX+40510293X+2017_T3/courseware/f441582f8bbf4e50bd8dba0e89f4dc3e/1f3575cea2ee48c18592b033aceab2b0/")
chapter_nodes=driver.find_elements_by_class_name("chapter")
href_list=[]
for temp_node in chapter_nodes:
    li_nodes=temp_node.find_elements_by_tag_name("li")
    for temp_li_node in li_nodes:
        temp_a_node=temp_li_node.find_element_by_tag_name("a")
        href_list.append(temp_a_node.get_attribute("href"))
video_list=OrderedDict()
for href in href_list:
    driver.get(href)
    try:
        WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.TAG_NAME,"video")))
    except Exception as e:
        continue
    try:
        newNode=driver.find_element_by_tag_name("video")

        video_list[driver.title]=newNode.get_attribute("src")
        print({driver.title:newNode.get_attribute("src")})
    except Exception  as e:
        continue
driver.close()
def getVideo(name,url):
    name=name.replace(" | ","_")
    global i
    i=i+1
    name=str(i)+name
    response=requests.get(url)
    if(response.status_code==200):
        with open(name+".mp4","wb") as f:
            f.write(response.content)

for key in video_list.keys():
    sleep(5)
    print("downloading"+key.replace(" | ","_"))
    t=threading.Thread(target=getVideo,args=(key,video_list[key]))
    t.start()
