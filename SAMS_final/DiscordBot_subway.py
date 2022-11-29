import requests
import json
import pandas as pd

import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

trainCodeExcel = pd.read_csv('TrainCode.csv', encoding='MS949') #열차 코드 csv파일
url = 'http://apis.data.go.kr/B553766/smt-path/path'
params ={'serviceKey' : 's08ZW0EAgYlgdsLFJNkcL2YGGLtczytGfqAjxKqgvWI+/QkyUIy21Ydkn6TSPdDj00C8DVsJesJzNVT6md0iDg==',
        'pageNo' : '1',
        'numOfRows' : '1',
        'dept_station_code' : '',
        'dest_station_code' : '1761', #해당 인자는 정왕역 코드 1761로 고정
        'week' : 'DAY',
        'search_type' : 'FASTEST',
        'first_last' : '',
        'dept_time' : '',
        'train_seq' : '' }

async def SubwayHelp(ctx):
    embed=discord.Embed(title=":desktop: 도움말 목록", color=0x20BEF1)
    embed.add_field(name=":small_blue_diamond: !지하철 도움말", value="지하철 명령어 사용법을 출력합니다.", inline=False)
    embed.add_field(name=":small_blue_diamond: !지하철 출발역 출발시간(HHMM)", value="입력된 출발시간에 맞는 가장 빠른 시간을 출력합니다.", inline=False)
    embed.add_field(name=":small_blue_diamond: !지하철 출발역 출발시간(HHMM) 도착시간(HHMM)", value="1번 기능에 더해 도착시간 내로 도착 가능한지 알려줍니다.", inline=False)
    await ctx.channel.send(embed=embed)

async def GetFastestTime(ctx, command):
    tempParam = command.split()

    if (len(tempParam[2]) != 4 or int(tempParam[2][0:2]) > 12 or int(tempParam[2][2:4]) > 60):
        embed=discord.Embed(title=":warning: 오류가 발생했습니다!", description='출발시간 인자가 명령어 형식에 맞지 않습니다..', color=0x20bef1)
        embed.set_footer(text="*출발시간 인자는 HHMM 으로 입력해야합니다. 헷갈리신다면 도움말을 참고해주세요.")
        await ctx.channel.send(embed=embed)
        return
    
    if (len(tempParam) == 4):
        if (len(tempParam[3]) != 4 or int(tempParam[3][0:2]) > 12 or int(tempParam[3][2:4]) > 60):
            embed=discord.Embed(title=":warning: 오류가 발생했습니다!", description='도착시간 인자가 명령어 형식에 맞지 않습니다..', color=0x20bef1)
            embed.set_footer(text="*도착시간 인자는 HHMM 으로 입력해야합니다. 헷갈리신다면 도움말을 참고해주세요.")
            await ctx.channel.send(embed=embed)
            return
        
        elif (int(tempParam[2]) >= int(tempParam[3])):
            embed=discord.Embed(title=":warning: 오류가 발생했습니다!", description='도착시간이 출발시간보다 빠릅니다..', color=0x20bef1)
            embed.set_footer(text="*두 시간의 위치가 바뀌지 않도록 주의해주세요.")
            await ctx.channel.send(embed=embed)
            return

    try:
        params['dept_station_code'] = trainCodeExcel[trainCodeExcel['station_name'] == tempParam[1]]['station_code'].values[0]
    except:
        embed=discord.Embed(title=":warning: 오류가 발생했습니다!", description='\'' + tempParam[1] + '\' 에 해당하는 역이름을 찾을 수 없습니다..', color=0x20bef1)
        embed.set_footer(text="*계속해서 문제가 발생한다면 개발자에게 문의해주세요")
        await ctx.channel.send(embed=embed)
        return
    
    params['dept_time'] = tempParam[2] + '00'

    try:
        response = json.loads(requests.get(url, params=params).text)
    except:
        embed=discord.Embed(title=":warning: 오류가 발생했습니다!", description='API JSON 파일 로드에 문제가 발생했습니다..', color=0x20bef1)
        embed.set_footer(text="*계속해서 문제가 발생한다면 개발자에게 문의해주세요")
        await ctx.channel.send(embed=embed)
        return


    #필요 정보 저장
    startSt = response['data']['route'][0]['station_nm'] #출발역 이름

    startTime = response['data']['route'][0]['timestamp'] #출발 기차시간
    startMin = int(startTime[0:2]) * 60 + int(startTime[2:4]) #출발 기차시간 분으로 환산

    arrvTime = response['data']['arrv_time'] #최종도착시간
    arrvMin = int(arrvTime[0:2]) * 60 + int(arrvTime[2:4])#도착시간 분으로 환산

    totalTime = [str(int((arrvMin - startMin) / 60)), str((arrvMin - startMin) % 60)] #소요시간

    #embed형식 메세지 생성
    embed=discord.Embed(title=":train: 지하철 시간 정보", description=tempParam[2][0:2] + "시" + tempParam[2][2:4] + "분 기준", color=0x20bef1)
    embed.add_field(name=":station: 출발역", value=startSt, inline=True)
    embed.add_field(name=":fire: 가장 빠른 출발시간", value=startTime[0:2] + "시" + startTime[2:4] + "분", inline=True)
    embed.add_field(name=":stopwatch: 도착 예정시간", value=arrvTime[0:2] + "시" + arrvTime[2:4] + "분", inline=True)

    #도착 시간 포함 명령어인 경우
    if (len(tempParam) == 4):
        limitTime = int(tempParam[3][0:2]) * 60 + int(tempParam[3][2:4])
        diff = limitTime - arrvMin
        diffS = [str(int(abs(diff) / 60)), str(abs(diff) % 60)]
        resultMsg = ''

        if (diff > 0):
            if (totalTime[0] != '0'):
                resultMsg += totalTime[0] + "시간 " + totalTime[1] + "분 소요될 예정이며, 도착 후 "
            else:
                resultMsg += totalTime[1] + "분 소요될 예정이며, 도착 후 "
            
            if (diffS[0] != '0'):
                resultMsg += diffS[0] + "시간 " + diffS[1] + "분 정도 여유가 있어요!"
            else:
                resultMsg += diffS[1] + "분 정도 여유가 있어요!"

            embed.add_field(name=":raised_hands: 제시간에 정왕역에 도착할 수 있어요!", value=resultMsg, inline=False)
            embed.set_footer(text="*지하철 시간은 상황에 따라 달라질 수 있습니다.")
            await ctx.channel.send(embed=embed)
        
        else:
            if (totalTime[0] != '0'):
                resultMsg += totalTime[0] + "시간 " + totalTime[1] + "분 소요될 예정이며, "
            else:
                resultMsg += totalTime[1] + "분 소요될 예정이며,  "
            
            if (diffS[0] != '0'):
                resultMsg += diffS[0] + "시간 " + diffS[1] + "분 정도 늦을 것 같아요.."
            else:
                resultMsg += diffS[1] + "분 정도 늦을 것 같아요.."

            embed.add_field(name=":fearful: 늦게 도착할지도 모르겠어요",
                            value=resultMsg, inline=False)
            embed.set_footer(text="*지하철 시간은 상황에 따라 달라질 수 있습니다.")
            await ctx.channel.send(embed=embed)


def test(command):
    tempParam = command.split()
    params['dept_station_code'] = trainCodeExcel[trainCodeExcel['station_name'] == tempParam[1]]['station_code'].values[0]
    params['numOfRows'] = '10'
    params['dept_time'] = tempParam[2] + '00'
    print(params)
    print(requests.get(url, params=params).text)
    response = json.loads(requests.get(url, params=params).text)
    start_st = response['data']['route'][0]['station_nm'] #출발역 이름
    start_time = response['data']['route'][0]['timestamp'] #출발 기차시간
    arrv_time = response['data']['arrv_time'] #최종도착시간
    totalTime =response['data']['time'] #소요시간

    print(response)
    print(start_st + " " + start_time + " " + arrv_time)

#test('!지하철 보라매 0500')