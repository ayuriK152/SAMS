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

@client.event
async def GetWeather(ctx):
    url1 = "https://weather.naver.com/today/02390591" # 기온, 날씨, 강수량 데이터를 가져올 url

    embed = discord.Embed(title=":sun_with_face: 정왕동 날씨", description='현재 시간 기준' ,color=0x20BEF1)
    res1 = requests.get(url1)
    res1.raise_for_status()

    url2 = "https://weather.naver.com/air/02390591" # 미세먼지, 초미세먼지 데이터를 가져올 url
    res2 = requests.get(url2)
    res2.raise_for_status()

    soup1 = BeautifulSoup(res1.text, "html.parser")
    soup2 = BeautifulSoup(res2.text, "html.parser")

    # 기온
    temp = soup1.find('strong', {'class' : 'current'}).text
    temp_float = re.findall("\d+.\d+", temp)[0] # 실수만 추출하기 위한 정규식
    # 날씨
    weather = soup1.select_one('#now > div > div.weather_area > div.weather_now > p > span.weather').get_text()
    if weather == '맑음' : # 맑음일 경우 :sunny: 이모티콘
        icorn = ':sunny:'
    elif weather == '비' : # 비일 경우 :cloud_rain: 이모티콘
        icorn = ':cloud_rain:'
    elif weather == '흐림' : # 흐림일 경우 :cloud: 이모티콘
        icorn = ':cloud:' 
    else : # 그 외의 경우 아무것도 출력하지 않는다
        icorn = None
    # 어제 날씨
    yesterday_up = soup1.select_one('#now > div > div.weather_area > div.weather_now > p > span.temperature.up') # 기온 상승
    yesterday_down = soup1.select_one('#now > div > div.weather_area > div.weather_now > p > span.temperature.down') # 기온 하강
    if yesterday_up == None : # 기온 상승 값이 none일 경우
        yesterday_data = yesterday_down.get_text()
    elif yesterday_down == None : # 기온 하강 값이 none일 경우
        yesterday_data = yesterday_up.get_text()
    # 비
    rain_am = soup1.select_one('#weekly > ul > li:nth-child(1) > div > div.cell_weather > span:nth-child(1) > strong > span.rainfall').get_text() # 오전 강수확률
    rain_amz = re.findall('\d+', rain_am)[0] # 정수만 추출하기 위한 정규식
    
    rain_pm = soup1.select_one('#weekly > ul > li:nth-child(1) > div > div.cell_weather > span:nth-child(2) > strong > span.rainfall').get_text() # 오후 강수확률
    rain_pmz = re.findall('\d+', rain_pm)[0] # 정수만 추출하기 위한 정규식

    if int(rain_amz) > 50 : # 오전 강수 확률이 50보다 클 경우
        umbrella = '오전에 우산을 챙기셔야 겠어요!:umbrella2: '
    elif int(rain_pmz) > 50 : # 오후 강수확률이 50보다 클 경우
        umbrella = '오후에 우산을 챙기셔야 겠어요!:umbrella2: '
    elif int(rain_amz) > 50 and int(rain_pmz) > 50 : # 오전 강수확률과 오후 강수확률 모두 50보다 클 경우
        umbrella = '나갈 때 꼭 우산 챙기기!:umbrella2: '
    else :
        umbrella = '우산을 챙길 필요는 없겠네요!:thumbsup:'
    #미세먼지
    dust = soup2.select_one('#content > div > div.section_right > div.card.card_dust > div.top_area > div:nth-child(1) > em > span.grade._cnPm10Grade').get_text() # 미세먼지 정도
    supdust = soup2.select_one('#content > div > div.section_right > div.card.card_dust > div.top_area > div:nth-child(1) > em > span.grade._cnPm10Grade').get_text() # 초미세먼지 정도
    dust_z = soup2.select_one('#content > div > div.section_right > div.card.card_dust > div.top_area > div:nth-child(1) > em > span.value._cnPm10Value').get_text() # 미세먼지 수치
    supdust_z = soup2.select_one('#content > div > div.section_right > div.card.card_dust > div.top_area > div:nth-child(2) > em > span.value._cnPm25Value').get_text() # 초미세먼지 수치
    if int(dust_z) >= 150 or int(supdust_z) >= 75: # 미세먼지 수치가 150 보다 크거나 초미세먼지 수치가 75보다 클 경우
        mask = '마스크를 쓰셔야 겠어요!:mask: ' 
    else :
        mask = '상쾌한 공기를 만끽하세요!:triumph:'
   # 포멧
    temp_data = '오늘의 기온은 {0}° 에요 현재 날씨는 {1} 이에요{2}\n어제보다 {3}'.format(temp_float, weather, icorn, yesterday_data) # 기온
    drain = '오늘 오전에 비가올 확률은 {0}% 이고, 오후에 비가 올 확률은 {1}% 에요'.format(rain_amz, rain_pmz) # 비소식의 첫 줄에 들어갈 강수확률
    rain_data = '{0}\n{1}'.format(drain, umbrella) # 비소식
    air_data = '미세먼지는 {0} 초미세먼지는 {1} 이에요\n{2}'.format(dust, supdust, mask) # 미세먼지
    
    embed.add_field(name = ":thermometer: 기온", value = temp_data, inline = False)
    embed.add_field(name = ":sweat_drops: 비소식", value = rain_data, inline = False)
    embed.add_field(name = ":fog: 미세먼지", value = air_data, inline = False)
    embed.add_field(name = ":point_right: 네이버 날씨 바로가기", value = url1, inline = False)

    url1 =""
    await ctx.channel.send(embed=embed)