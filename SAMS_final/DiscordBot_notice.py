# 웹 크롤링과 정규표현식을 위한 모듈
import requests
from bs4 import BeautifulSoup
import re

# 디스코드 문법을 위한 디스코드 모듈
import discord
from discord.ext import commands
intents = discord.Intents.default()					
intents.message_content = True
client = discord.Client(intents=intents)

# 디스코드 파이썬 가상환경을 위한 디스코드 모듈
import asyncio

# 동적 웹크롤링을 위한 디스코드 모듈
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# list를 DataFrame(엑셀)로 바꿔주고 전송하기 위한 모듈
import openpyxl
import pandas as pd
import os



async def helpNotice(ctx):
    embed=discord.Embed(title=":desktop: 도움말 목록", color=0x20BEF1)
    embed.add_field(name=":small_blue_diamond: !공지 (학사, 장학, 취업, 일반) - ex) !공지 일반", value="각 공지사항 1페이지의 내용을 출력합니다.", inline=False)
    embed.add_field(name=":small_blue_diamond: !공지 (학사, 장학, 취업, 일반) 제목검색 (keyword) - ex) !공지 일반 제목검색 장학금", value="각 게시판에서 입력한 키워드로 제목을 검색해 공지사항 1페이지의 내용을 출력합니다.", inline=False)
    embed.add_field(name=":small_blue_diamond: !공지 (학사, 장학, 취업, 일반) 작성자검색 (keyword) - ex) !공지 학사 작성자검색 기계공학과", value="각 게시판에서 입력한 키워드로 작성자를 검색해 공지사항 1페이지의 내용을 출력합니다.", inline=False)
    embed.add_field(name=":small_blue_diamond: !공지 통합 (작성자검색 OR 제목검색) (keyword) - ex) !공지 통합 작성자검색 기계공학과", value="학사, 장학, 취업, 일반 게시판에서 입력한 키워드로 작성자 또는 제목을 검색해 공지사항 1페이지의 내용을 검색합니다. 검색결과를 엑셀파일로 만들어 전송합니다.", inline=False)
    await ctx.channel.send(embed=embed)

async def GetNotice(ctx, kind):
    if kind == "학사":
        url = "https://www.tukorea.ac.kr/tukorea/1096/subview.do"
        embed = discord.Embed(title="학사공지", url=url, description="학사공지 1페이지 검색 결과입니다.",color=0x20BEF1)
        embed.set_footer(text="이상입니다.")
    elif kind == "장학":
        url = "https://www.tukorea.ac.kr/tukorea/1097/subview.do"
        embed = discord.Embed(title="장학공지", url=url, description="장학공지 1페이지 검색 결과입니다.",color=0x20BEF1)
        embed.set_footer(text="이상입니다.")
    elif kind == "취업":
        url = "https://www.tukorea.ac.kr/tukorea/1098/subview.do"
        embed = discord.Embed(title="취업공지", url=url, description="취업공지 1페이지 검색 결과입니다.",color=0x20BEF1)
        embed.set_footer(text="이상입니다.")
    elif kind == "일반":
        url = "https://www.tukorea.ac.kr/tukorea/1099/subview.do"
        embed = discord.Embed(title="일반공지", url=url, description="일반공지 1페이지 검색 결과입니다.",color=0x20BEF1)
        embed.set_footer(text="이상입니다.")
    else:
        await ctx.channel.send("유효한 명령어가 아닙니다. '!공지 도움말' 을 입력하여 도움말을 살펴보세요!")
        return

    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    #soup.find는 가장 먼저 만나는 태그 하나만을 뽑지만,
    #soup.find_all은 전체 태그에서 찾는다.
    #또한 find 함수에서 첫번째 요소는 태그, 두번째 요소는 클래스를 입력한다.

    titles = [] # 공지의 제목을 저장하는 리스트
    links = [] # 공지의 링크를 저장하는 리스트
    writers = [] # 공지의 작성자를 저장하는 리스트
    dates = [] # 공지의 작성일자를 저장하는 리스트

    # 공지 제목을 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})

    if temp == []:
        embed.add_field(name="이런...", value="검색결과가 없습니다.", inline=False)
        await ctx.channel.send(embed=embed)
        return

    for temp in temp:
        title = temp.find("strong").get_text() #strong 태그만 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+", "", title) #re.sub() 정규표현식을 사용하여 좌측공백제거
        titles.append(revised_text)

    # 공지 링크를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})
    for temp in temp:
        link = temp.find("a")["href"] #a href만 텍스트로 바꿔 저장한다.
        links.append(link)

    # 공지 작성자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-write"})
    for temp in temp:
        writer = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+|\s+$", "", writer) #re.sub() 정규표현식을 사용하여 양측공백제거
        writers.append(revised_text)

    # 공지 작성일자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-date"})
    for temp in temp:
        date = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        dates.append(date)

    for i in range(len(titles)):
        real_title = '{0} : {1}'.format(i,titles[i])
        real_link = '''https://www.tukorea.ac.kr{0},
        작성자 : {1}, 작성일자 : {2}\n'''.format(links[i], writers[i], dates[i])
        embed.add_field(name=real_title, value = real_link, inline=False)
    url =""
    await ctx.channel.send(embed=embed)

async def keyWordSearchNotice(ctx, command):
    tempParam = command.split()
    keyword = command[12:]
    noticeType = ['학사', '장학', '일반', '취업']

    if tempParam[1] not in noticeType :
        await ctx.channel.send("유효한 명령어가 아닙니다. '!공지 도움말' 을 입력하여 도움말을 살펴보세요!")
        return

    if tempParam[1] == '학사':
        url = 'https://www.tukorea.ac.kr/tukorea/1096/subview.do'
        css_selector = '#menu1096_obj1098'
    if tempParam[1] == '장학':
        url = 'https://www.tukorea.ac.kr/tukorea/1097/subview.do'
        css_selector = '#menu1097_obj1099'
    if tempParam[1] == '취업':
        url = 'https://www.tukorea.ac.kr/tukorea/1098/subview.do'   
        css_selector = '#menu1098_obj1100'     
    if tempParam[1] == '일반':
        url = 'https://www.tukorea.ac.kr/tukorea/1099/subview.do'
        css_selector = '#menu1099_obj1101'



    # https://thomass.tistory.com/43 에서 셀레니움 headless 방법 찾음
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--start-maximized") # add
    options.add_argument("--window-size=1920,1080") # add

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    driver.get(url)
    driver.implicitly_wait(3) 

    
    driver.find_element(By.ID,'srchWrd').click()
    element = driver.find_element(By.ID,'srchWrd')
    element.send_keys(keyword)
    driver.implicitly_wait(3) 

    driver.find_element(By.CSS_SELECTOR,'{0} > div._fnctWrap > form:nth-child(2) > div.board-search > div > fieldset > div > div.box-search > input[type=submit]:nth-child(2)'.format(css_selector)).click()

    html = driver.page_source
    newurl = driver.current_url
    driver.implicitly_wait(3) 
    soup = BeautifulSoup(html, 'html.parser')

    titles = [] # 공지의 제목을 저장하는 리스트
    links = [] # 공지의 링크를 저장하는 리스트
    writers = [] # 공지의 작성자를 저장하는 리스트
    dates = [] # 공지의 작성일자를 저장하는 리스트
    
    embed = discord.Embed(title="{0}공지에서 '{1}' 제목검색결과 ".format(tempParam[1], keyword), url = newurl, color=0x20BEF1)
    # 공지 제목을 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})

    if temp == []:
        embed.add_field(name="이런...", value="검색결과가 없습니다.", inline=False)
        await ctx.channel.send(embed=embed)
        driver.quit()
        return

    for temp in temp:
        title = temp.find("strong").get_text() #strong 태그만 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+", "", title) #re.sub() 정규표현식을 사용하여 좌측공백제거
        titles.append(revised_text)

    # 공지 링크를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})
    for temp in temp:
        link = temp.find("a")["href"] #a href만 텍스트로 바꿔 저장한다.
        links.append(link)

    # 공지 작성자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-write"})
    for temp in temp:
        writer = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+|\s+$", "", writer) #re.sub() 정규표현식을 사용하여 양측공백제거
        writers.append(revised_text)

    # 공지 작성일자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-date"})
    for temp in temp:
        date = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        dates.append(date)

    for i in range(len(titles)):
        real_title = '{0} : {1}'.format(i,titles[i])
        real_link = '''http://www.tukorea.ac.kr{0},
        작성자 : {1}, 작성일자 : {2}\n'''.format(links[i], writers[i], dates[i])
        embed.add_field(name=real_title, value = real_link, inline=False)
        embed.set_footer(text="안이 텅 비었다면? 검색결과가 존재하지 않습니다...")
    url =""
    await ctx.channel.send(embed=embed)
    driver.quit()

async def writerSearchNotice(ctx, command):
    tempParam = command.split()
    keyword = command[13:]
    noticeType = ['학사', '장학', '일반', '취업']

    if tempParam[1] not in noticeType :
        await ctx.channel.send("유효한 명령어가 아닙니다. '!공지 도움말' 을 입력하여 도움말을 살펴보세요!")
        return

    if tempParam[1] == '학사':
        url = 'https://www.tukorea.ac.kr/tukorea/1096/subview.do'
        css_selector = '#menu1096_obj1098'
    if tempParam[1] == '장학':
        url = 'https://www.tukorea.ac.kr/tukorea/1097/subview.do'
        css_selector = '#menu1097_obj1099'
    if tempParam[1] == '취업':
        url = 'https://www.tukorea.ac.kr/tukorea/1098/subview.do'   
        css_selector = '#menu1098_obj1100'     
    if tempParam[1] == '일반':
        url = 'https://www.tukorea.ac.kr/tukorea/1099/subview.do'
        css_selector = '#menu1099_obj1101'


    # https://thomass.tistory.com/43 에서 셀레니움 headless 방법 찾음
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--start-maximized") # add
    options.add_argument("--window-size=1920,1080") # add

    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    driver.get(url)
    driver.implicitly_wait(3) 

    dropdown = Select(driver.find_element(By.CSS_SELECTOR,'#srchColumn'))
    dropdown.select_by_index(1)
    driver.implicitly_wait(3) 
    
    driver.find_element(By.ID,'srchWrd').click()
    element = driver.find_element(By.ID,'srchWrd')
    element.send_keys(keyword)
    driver.implicitly_wait(3) 

    driver.find_element(By.CSS_SELECTOR,'{0} > div._fnctWrap > form:nth-child(2) > div.board-search > div > fieldset > div > div.box-search > input[type=submit]:nth-child(2)'.format(css_selector)).click()

    html = driver.page_source
    newurl = driver.current_url
    driver.implicitly_wait(3) 
    soup = BeautifulSoup(html, 'html.parser')

    titles = [] # 공지의 제목을 저장하는 리스트
    links = [] # 공지의 링크를 저장하는 리스트
    writers = [] # 공지의 작성자를 저장하는 리스트
    dates = [] # 공지의 작성일자를 저장하는 리스트
    
    embed = discord.Embed(title="{0}공지에서 '{1}' 작성자 검색결과 ".format(tempParam[1], keyword), url = newurl, color=0x20BEF1)
    # 공지 제목을 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})

    if temp == []:
        embed.add_field(name="이런...", value="검색결과가 없습니다.", inline=False)
        await ctx.channel.send(embed=embed)
        driver.quit()
        return

    for temp in temp:
        title = temp.find("strong").get_text() #strong 태그만 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+", "", title) #re.sub() 정규표현식을 사용하여 좌측공백제거
        titles.append(revised_text)

    # 공지 링크를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-subject"})
    for temp in temp:
        link = temp.find("a")["href"] #a href만 텍스트로 바꿔 저장한다.
        links.append(link)

    # 공지 작성자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-write"})
    for temp in temp:
        writer = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        revised_text = re.sub(r"^\s+|\s+$", "", writer) #re.sub() 정규표현식을 사용하여 양측공백제거
        writers.append(revised_text)

    # 공지 작성일자를 읽어오기
    temp = soup.find_all("td", attrs={"class":"td-date"})
    for temp in temp:
        date = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
        dates.append(date)

    for i in range(len(titles)):
        real_title = '{0} : {1}'.format(i,titles[i])
        real_link = '''http://www.tukorea.ac.kr{0},
        작성자 : {1}, 작성일자 : {2}\n'''.format(links[i], writers[i], dates[i])
        embed.add_field(name=real_title, value = real_link, inline=False)
        embed.set_footer(text="안이 텅 비었다면? 검색결과가 존재하지 않습니다...")
    url =""
    await ctx.channel.send(embed=embed)
    driver.quit()

async def powerSearchNotice(ctx, command):
    tempParam = command.split()
    searchType = ['제목검색', '작성자검색']

    if tempParam[2] not in searchType :
        await ctx.channel.send("유효한 명령어가 아닙니다. '!공지 도움말' 을 입력하여 도움말을 살펴보세요!")
        return
    
    if tempParam[2] == '작성자검색' :
        keyword = command[13:]
        await ctx.channel.send("작업이 진행중입니다. (예상대기시간 : 30sec)")
        searchProcessWriter(keyword)
        await ctx.channel.send(file=discord.File('searchResults.xlsx'))
        await ctx.channel.send("작업이 완료되었습니다. 기다려줘서 감사합니다!")

    elif tempParam[2] == '제목검색' :
        keyword = command[12:]
        await ctx.channel.send("작업이 진행중입니다. (예상대기시간 : 30sec)")
        searchProcessTitle(keyword)
        await ctx.channel.send(file=discord.File('searchResults.xlsx'))
        await ctx.channel.send("작업이 완료되었습니다. 기다려줘서 감사합니다!")        

def searchProcessWriter(keyword):
    raw_data0 = {} # pandas를 이용해 엑셀로 변환할 딕셔너리 자료형
    raw_data1 = {}
    raw_data2 = {}
    raw_data3 = {}

    urls = ['https://www.tukorea.ac.kr/tukorea/1096/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1097/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1098/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1099/subview.do']

    css_selectors = ['#menu1096_obj1098', '#menu1097_obj1099', '#menu1098_obj1100', '#menu1099_obj1101']
    
    for i in range(4):       
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--start-maximized") # add
        options.add_argument("--window-size=1920,1080") # add

        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(3)

        driver.get(urls[i])
        driver.implicitly_wait(3) 

        dropdown = Select(driver.find_element(By.CSS_SELECTOR,'#srchColumn'))
        dropdown.select_by_index(1)
        driver.implicitly_wait(3) 
        
        driver.find_element(By.ID,'srchWrd').click()
        element = driver.find_element(By.ID,'srchWrd')
        element.send_keys(keyword)
        driver.implicitly_wait(3) 

        driver.find_element(By.CSS_SELECTOR,'{0} > div._fnctWrap > form:nth-child(2) > div.board-search > div > fieldset > div > div.box-search > input[type=submit]:nth-child(2)'.format(css_selectors[i])).click()

        html = driver.page_source
        newurl = driver.current_url
        driver.implicitly_wait(3) 
        soup = BeautifulSoup(html, 'html.parser')

        titles = [] # 공지의 제목을 저장하는 리스트
        links = [] # 공지의 링크를 저장하는 리스트
        writers = [] # 공지의 작성자를 저장하는 리스트
        dates = [] # 공지의 작성일자를 저장하는 리스트
        
        # 공지 제목을 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-subject"})
        for temp in temp:
            title = temp.find("strong").get_text() #strong 태그만 텍스트로 바꿔 저장한다.
            revised_text = re.sub(r"^\s+", "", title) #re.sub() 정규표현식을 사용하여 좌측공백제거
            titles.append(revised_text)

        # 공지 링크를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-subject"})
        for temp in temp:
            link = temp.find("a")["href"] #a href만 텍스트로 바꿔 저장한다.
            real_link = "https://www.tukorea.ac.kr{0}".format(link)
            links.append(real_link)

        # 공지 작성자를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-write"})
        for temp in temp:
            writer = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
            revised_text = re.sub(r"^\s+|\s+$", "", writer) #re.sub() 정규표현식을 사용하여 양측공백제거
            writers.append(revised_text)

        # 공지 작성일자를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-date"})
        for temp in temp:
            date = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
            dates.append(date)

        # 공지가 텅 비어 있을 경우 리스트에 다음과 같이 값을 추가해준다.
        if temp == []:
            titles.append('None')
            links.append('None')
            writers.append('None')
            dates.append('None')

        if i == 0:
            raw_data0['제목'] = titles
            raw_data0['링크'] = links
            raw_data0['글쓴이'] = writers
            raw_data0['작성일자'] = dates

        elif i == 1:
            raw_data1['제목'] = titles
            raw_data1['링크'] = links
            raw_data1['글쓴이'] = writers
            raw_data1['작성일자'] = dates

        elif i == 2:
            raw_data2['제목'] = titles
            raw_data2['링크'] = links
            raw_data2['글쓴이'] = writers
            raw_data2['작성일자'] = dates

        elif i == 3:
            raw_data3['제목'] = titles
            raw_data3['링크'] = links
            raw_data3['글쓴이'] = writers
            raw_data3['작성일자'] = dates
        driver.quit()

    page1 = pd.DataFrame(raw_data0)
    page2 = pd.DataFrame(raw_data1)
    page3 = pd.DataFrame(raw_data2)
    page4 = pd.DataFrame(raw_data3)

    writer=pd.ExcelWriter('searchResults.xlsx', engine='openpyxl')

    page1.to_excel(writer, sheet_name = '학사공지') #raw_data0 시트
    page2.to_excel(writer, sheet_name = '장학공지') #raw_data1 시트
    page3.to_excel(writer, sheet_name = '취업공지') #raw_data2 시트
    page4.to_excel(writer, sheet_name = '일반공지') #raw_data3 시트

    writer.save()
    
def searchProcessTitle(keyword):
    raw_data0 = {} # pandas를 이용해 엑셀로 변환할 딕셔너리 자료형
    raw_data1 = {}
    raw_data2 = {}
    raw_data3 = {}

    urls = ['https://www.tukorea.ac.kr/tukorea/1096/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1097/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1098/subview.do',
            'https://www.tukorea.ac.kr/tukorea/1099/subview.do']

    css_selectors = ['#menu1096_obj1098', '#menu1097_obj1099', '#menu1098_obj1100', '#menu1099_obj1101']
    
    for i in range(4):       
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("--start-maximized") # add
        options.add_argument("--window-size=1920,1080") # add

        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(3)

        driver.get(urls[i])
        driver.implicitly_wait(3) 
        
        driver.find_element(By.ID,'srchWrd').click()
        element = driver.find_element(By.ID,'srchWrd')
        element.send_keys(keyword)
        driver.implicitly_wait(3) 

        driver.find_element(By.CSS_SELECTOR,'{0} > div._fnctWrap > form:nth-child(2) > div.board-search > div > fieldset > div > div.box-search > input[type=submit]:nth-child(2)'.format(css_selectors[i])).click()

        html = driver.page_source
        newurl = driver.current_url
        driver.implicitly_wait(3) 
        soup = BeautifulSoup(html, 'html.parser')

        titles = [] # 공지의 제목을 저장하는 리스트
        links = [] # 공지의 링크를 저장하는 리스트
        writers = [] # 공지의 작성자를 저장하는 리스트
        dates = [] # 공지의 작성일자를 저장하는 리스트
        
        # 공지 제목을 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-subject"})
        for temp in temp:
            title = temp.find("strong").get_text() #strong 태그만 텍스트로 바꿔 저장한다.
            revised_text = re.sub(r"^\s+", "", title) #re.sub() 정규표현식을 사용하여 좌측공백제거
            titles.append(revised_text)

        # 공지 링크를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-subject"})
        for temp in temp:
            link = temp.find("a")["href"] #a href만 텍스트로 바꿔 저장한다.
            real_link = "https://www.tukorea.ac.kr{0}".format(link)
            links.append(real_link)

        # 공지 작성자를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-write"})
        for temp in temp:
            writer = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
            revised_text = re.sub(r"^\s+|\s+$", "", writer) #re.sub() 정규표현식을 사용하여 양측공백제거
            writers.append(revised_text)

        # 공지 작성일자를 읽어오기
        temp = soup.find_all("td", attrs={"class":"td-date"})
        for temp in temp:
            date = temp.get_text() #저자 정보를 텍스트로 바꿔 저장한다.
            dates.append(date)

        # 공지가 텅 비어 있을 경우 리스트에 다음과 같이 값을 추가해준다.
        if temp == []:
            titles.append('None')
            links.append('None')
            writers.append('None')
            dates.append('None')

        if i == 0:
            raw_data0['제목'] = titles
            raw_data0['링크'] = links
            raw_data0['글쓴이'] = writers
            raw_data0['작성일자'] = dates

        elif i == 1:
            raw_data1['제목'] = titles
            raw_data1['링크'] = links
            raw_data1['글쓴이'] = writers
            raw_data1['작성일자'] = dates

        elif i == 2:
            raw_data2['제목'] = titles
            raw_data2['링크'] = links
            raw_data2['글쓴이'] = writers
            raw_data2['작성일자'] = dates

        elif i == 3:
            raw_data3['제목'] = titles
            raw_data3['링크'] = links
            raw_data3['글쓴이'] = writers
            raw_data3['작성일자'] = dates
        driver.quit()

    page1 = pd.DataFrame(raw_data0)
    page2 = pd.DataFrame(raw_data1)
    page3 = pd.DataFrame(raw_data2)
    page4 = pd.DataFrame(raw_data3)

    writer=pd.ExcelWriter('searchResults.xlsx', engine='openpyxl')

    page1.to_excel(writer, sheet_name = '학사공지') #raw_data0 시트
    page2.to_excel(writer, sheet_name = '장학공지') #raw_data1 시트
    page3.to_excel(writer, sheet_name = '취업공지') #raw_data2 시트
    page4.to_excel(writer, sheet_name = '일반공지') #raw_data3 시트

    writer.save()
