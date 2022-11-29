# 웹 크롤링과 정규표현식을 위한 모듈
import requests
from bs4 import BeautifulSoup

# 디스코드 문법을 위한 디스코드 모듈
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def GetBus(ctx):
    embed = discord.Embed(description="셔틀버스 시간표", color=0x20BEF1)
    embed.set_image(url="https://contents.kpu.ac.kr/contents/E/EWZ/EWZXESWY72X1/images/scale1/YUGJAO4Y2Q27.jpg")
    await ctx.channel.send(embed=embed)
