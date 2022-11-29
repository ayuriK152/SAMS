# 디스코드 문법을 위한 디스코드 모듈
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def GetMap(ctx):
      embed = discord.Embed(description="학교 지도", color=0x20BEF1)
      embed.add_field(name="자세한 사항", value="https://www.tukorea.ac.kr/tukorea/1085/subview.do", inline=False)
      embed.set_image(url="https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver."
                            "net%2F20141201_256%2Flinc2012_1417411358821I8TwJ_JPEG%2F%25C7%25D0%25B1%25B3_%25B5%25F0%25"
                            "C0%25DA%25C0%25CE.jpg&type=sc960_832")
      await ctx.channel.send(embed=embed)