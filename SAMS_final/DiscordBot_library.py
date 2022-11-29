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

# 동적 웹크롤링을 위한 디스코드 모듈
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


async def SearchBook(ctx, command):
    keyword = command[5:] #"!도서관 책이름" 이니까 5번째 인덱스부터가 책이름

    if ' ' in keyword: #공백 다루지 않기로 약속
        await ctx.channel.send("키워드에는 공백이 들어가면 안됩니다. 다시 검색해주십시오.")
        return

    # https://thomass.tistory.com/43 에서 셀레니움 headless 방법 찾음
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--start-maximized") # add
    options.add_argument("--window-size=1920,1080") # add

    #도서관 url을 분석해보니 다른 부분은 같고 검색하는 책 이름 부분만 바뀜
    book = "?ALL=k%7Ca%7C" + keyword + "&offset=0"          
    url="https://library.tukorea.ac.kr/search/i-discovery" + book
         
    
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    driver.get(url=url)
    driver.implicitly_wait(3)    

    html = driver.page_source #
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser') 
    #책 이름 부분
    books = soup.find_all('a',attrs={"class":"ikc-biblio-title"})
    #대출 여부 부분
    lend=soup.find_all('span',attrs={"class":"ikc-item-status"})
    book_list=[]
    book_lend=[]
    
    #존재하지 않는 책을 검색하면 리스트는 빈 상태를 이용
    if len(books) ==0: 
      await ctx.channel.send("해당 도서는 존재하지 않습니다.")
      return
     
    #lend의 개수가 최대 5개라는 특성으 이용
    #lend가 존재하면 책은 무조건 존재
    for i in range(len(lend)): #
      book_list.append(books[i].get_text())
      book_lend.append(lend[i].get_text())
      
    #이미지 가져오기
    img=soup.find('img',attrs={"class":"ikc-biblio-thumbnail ng-star-inserted"})
    
     
    embed = discord.Embed(description="도서관에 환영합니다!.", color=0x20BEF1)
    embed.set_image(url=f"{img['src']}")
    for i in range(len(book_list)): #책의 개수만큼 반복
      embed.add_field(name=book_list[i], value = book_lend[i], inline=False)
    await ctx.channel.send(embed=embed)