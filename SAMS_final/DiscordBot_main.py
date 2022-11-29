# https://nstgic3.tistory.com/26 참고함.
# bot은 client 의 하위 클래스로 실제로 discord.py API의 extention으로 존재
import discord
from discord.ext import commands

intents = discord.Intents.default()					
intents.message_content = True
client = discord.Client(intents=intents)

# 김동현 팀원 부분 파일
from DiscordBot_notice import *
from DiscordBot_menu import *

# 이원섭 팀원 부분 파일
from DiscordBot_subway import *

# 이지민 팀원 부분 파일
from DiscordBot_weather import * # 내일 안돼면 추가적으로 손본다고 하심. 

# 김상원 팀원 부분 파일
from DiscordBot_map import *
from DiscordBot_bus import *
from DiscordBot_library import *


# 봇이 접속하면 아래의 함수를 실행하게 된다
@client.event
async def on_ready():
    print(f'{client.user} online!') 
#위 문장은 f-string 으로 파이썬의 포멧팅 방법 중 하나이다.


# https://luran.me/547 사이트 참고
@client.event
async def on_message(ctx):
    if ctx.content.startswith("!도움말"):
        embed = discord.Embed(description="도움말 목록", color=0x20BEF1)
        embed.set_author(name="도움말")
        embed.add_field(name="0. !식당메뉴", value="입력 시 금일 학교 식당 메뉴를 보여줍니다.", inline=False)
        embed.add_field(name="1. !셔틀", value="입력 시 셔틀버스 시간을 알려줍니다.", inline=False)
        embed.add_field(name="2. !날씨", value="입력 시 정왕동 날씨를 알려줍니다.", inline=False)
        embed.add_field(name="3. !건물위치", value="입력 시 학교 내 건물위치를 알려줍니다.", inline=False)
        embed.add_field(name="4. !공지", value="입력 시 학교 공지사항 게시판을 검색하는 다양한 기능을 제공합니다. 도움말을 참고해주세요!", inline=False)
        embed.add_field(name="5. !지하철", value="입력 시 열차시간 안내 및 출발역과 도착시간을 입력하면 마지막으로 탈 수 있는열차를 알려줍니다. 도움말을 참고해주세요!", inline=False)
        embed.add_field(name="6. !도서관", value="입력 시 학교 도서관 내 소장도서란에 검색한 도서가 있는지 알아봅니다.", inline=False)
        embed.set_footer(text="이상입니다.")
        await ctx.channel.send(embed=embed)

    if ctx.content.startswith("!공지"):
        sentence = ctx.content.split()
        if(len(sentence) == 1):
            await helpNotice(ctx)

        elif(len(sentence) == 2 and sentence[1] == "도움말"):
            await helpNotice(ctx)

        elif(len(sentence) == 2):
            await GetNotice(ctx, sentence[1])

        elif(sentence[1] == "통합" and (sentence[2] == "제목검색" or sentence[2] == "작성자검색")):
            await powerSearchNotice(ctx, ctx.content)

        elif(sentence[2] == "제목검색" and sentence[1] != '통합'):
            await keyWordSearchNotice(ctx, ctx.content) 
        
        elif(sentence[2] == "작성자검색" and sentence[1] != '통합'):
            await writerSearchNotice(ctx, ctx.content)
 
    if ctx.content.startswith("!식당메뉴"):
        await Getmenu(ctx)

    if ctx.content.startswith("!지하철"):
        sentence = ctx.content.split()
        if (len(sentence) == 2 and sentence[1] == "도움말"):
            await SubwayHelp(ctx)
        
        elif (len(sentence) == 3 or len(sentence) == 4):
            await GetFastestTime(ctx, ctx.content)

    if ctx.content.startswith("!날씨"):
        await GetWeather(ctx)

    if ctx.content.startswith("!셔틀"):
        await GetBus(ctx)
        
    if ctx.content.startswith("!건물위치"):
        await GetMap(ctx)
    
    if ctx.content.startswith("!도서관"):
        await SearchBook(ctx, ctx.content) 
        
# 개발자 페이지에서 봇에 대한 토큰 텍스트를 가져온 뒤, TOKEN에 대입하자
f = open("token.txt", "r")
client.run(f.readline())
f.close()