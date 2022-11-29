# 디스코드 문법을 위한 디스코드 모듈
import discord
from discord.ext import commands
intents = discord.Intents.default()					
intents.message_content = True
client = discord.Client(intents=intents)

# 동적 웹크롤링을 위한 디스코드 모듈
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request

# 정적 웹 크롤링을 위한 디스코드 모듈
import requests
from bs4 import BeautifulSoup
import re

# 가상환경을 위한 모듈
import asyncio

async def Getmenu(ctx):
    await ctx.channel.send("잠시 기다려 주십시오...")
    

    driver = webdriver.Chrome("chromedriver.exe")#, options=options)
    driver.implicitly_wait(5)
    driver.get("https://ibook.kpu.ac.kr/Viewer/menu02")

    req1 = driver.page_source
    soup1 = BeautifulSoup(req1, 'html.parser')  

    next_button = driver.find_element(By.CSS_SELECTOR, '#go-next') #다음 페이지 버튼 누르게함
    next_button.click() #버튼클릭
    driver.implicitly_wait(1)

    req2 = driver.page_source
    soup2 = BeautifulSoup(req2, 'html.parser')  

    http = "https:"
    image1 = soup1.select_one("#viewer > div:nth-child(2) > div:nth-child(1) > div > img")["src"]
    image2 = soup2.select_one("#viewer > div:nth-child(3) > div:nth-child(1) > div > img")["src"]
    await ctx.channel.send(http+image1)
    await ctx.channel.send(http+image2)

    driver.quit()
