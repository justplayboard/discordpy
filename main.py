import discord
from token_0 import *
import youtube_dl
from dice import *
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from discord_buttons_plugin import *

bot = commands.Bot(command_prefix="!")

def chrome_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)
    driver.get(url)

    page = driver.page_source
    driver.quit()

    return page

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="명령어", color=0xFFE400)
    embed.add_field(name="1. 스포츠 순위", value="!kbo : 크보 순위 제공\n!mlb [NL or AL] : 내셔널리그 or 아메리칸리그 순위 제공\n!k1 : k리그 순위 제공\n!football [epl or primera or bundesliga or seria or ligue1] : 해축 순위 제공\n!kbl : kbl 순위 제공\n!nba [EAST or WEST] : nba 각 컨퍼런스 순위 제공\n!배구 [kovo or wkovo] : 남자배구, 여자배구 순위 제공", inline=False)
    embed.add_field(name="2. 가위바위보", value="!가위바위보 : 봇과 유저와의 가위바위보 대결 버튼을 클릭하면 봇과의 승패무 결과나 나옴", inline=False)
    embed.add_field(name="3. 주사위", value="!주사위 : 봇과 유저와의 주사위 대결 더 큰 수가 나온 이가 승리", inline=False)
    embed.add_field(name="4. 음악", value="!play [youtube URL] : 음악 재생\n!leave : 봇 음성채널 퇴장\n!pause : 음악 일시정지\n!resume : 음악 일시재생\n!stop : 음악 중지", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 배구(ctx, category):
    url = f"https://sports.news.naver.com/volleyball/record/index?category={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = discord.Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수/승점/승/패/세트득실률/점수득실률/세트수/공격성공률/블로킹(세트당)/서브(세트당)/득점", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        w_0 = team.select('span')[1].text
        w_1 = team.select('strong')[1].text
        w_1 = w_1.strip()
        w_2 = team.select('span')[2].text
        w_3 = team.select('span')[3].text
        w_4 = team.select('span')[4].text
        w_5 = team.select('span')[5].text
        w_6 = team.select('span')[6].text
        w_7 = team.select('span')[7].text
        w_8 = team.select('span')[8].text
        w_9 = team.select('span')[9].text
        w_10 = team.select('span')[10].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{w_0}/{w_1}/{w_2}/{w_3}/{w_4}/{w_5}/{w_6}/{w_7}/{w_8}/{w_9}/{w_10}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def nba(ctx, category):
    url = f"https://sports.news.naver.com/basketball/record/index?category=nba&conference={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = discord.Embed(title=f"nba {category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀 [디비전]", value="경기수/승/패/승률/승차/홈승/홈패/원정승/원정패/디비전승/디비전패/연속", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        w_0 = team.select('span')[1].text
        w_1 = team.select('span')[2].text
        w_2 = team.select('span')[3].text
        w_3 = team.select('span')[4].text
        w_4 = team.select('strong')[1].text
        w_5 = team.select('span')[5].text
        w_6 = team.select('span')[6].text
        w_7 = team.select('span')[7].text
        w_8 = team.select('span')[8].text
        w_9 = team.select('span')[9].text
        w_10 = team.select('span')[10].text
        w_11 = team.select('span')[11].text
        w_12 = team.select('span')[12].text

        embed_name = f"{num}위 : {name} [{w_0}]"
        embed_value = f"{w_1}/{w_2}/{w_3}/{w_4}/{w_5}/{w_6}/{w_7}/{w_8}/{w_9}/{w_10}/{w_11}/{w_12}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def kbl(ctx):
    url = f"https://sports.news.naver.com/basketball/record/index?category=kbl"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = discord.Embed(title=f"kbl 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수/승률/승/패/승차/득점/AS/리바운드/스틸/블록/3점슛/자유투/자유투성공", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        w_0 = team.select('span')[1].text
        w_1 = team.select('strong')[1].text
        w_2 = team.select('span')[2].text
        w_3 = team.select('span')[3].text
        w_4 = team.select('span')[4].text
        w_5 = team.select('span')[5].text
        w_6 = team.select('span')[6].text
        w_7 = team.select('span')[7].text
        w_8 = team.select('span')[8].text
        w_9 = team.select('span')[9].text
        w_10 = team.select('span')[10].text
        w_11 = team.select('span')[11].text
        w_12 = team.select('span')[12].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{w_0}/{w_1}/{w_2}/{w_3}/{w_4}/{w_5}/{w_6}/{w_7}/{w_8}/{w_9}/{w_10}/{w_11}/{w_12}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def football(ctx, category):
    url = f"https://sports.news.naver.com/wfootball/record/index?category={category}&tab=team"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#wfootballTeamRecordBody>table>tbody>tr')

    embed = discord.Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀 [진출 여부]", value="경기수/승점/승/무/패/득점/실점/득실차", inline=False)

    for team in team_rank_list:
        number = len(team.select('div.inner > span'))
        num = team.select('.num > div.inner > strong')[0].text
        w_0 = team.select('div.inner > span')[0].text
        w_1 = team.select('div.inner > span')[1].text
        w_2 = team.select('div.inner > span')[2].text
        w_3 = team.select('div.inner > span')[3].text
        w_4 = team.select('div.inner > span')[4].text
        w_5 = team.select('div.inner > span')[5].text
        w_6 = team.select('div.inner > span')[6].text
        w_7 = team.select('div.inner > span')[7].text
        w_8 = team.select('div.inner > span')[8].text

        if number == 10:
            w_9 = team.select('div.inner > span')[9].text
            embed_name = f"{num}위 : {w_1} [{w_0}]"
            embed_value = f"{w_2}/{w_3}/{w_4}/{w_5}/{w_6}/{w_7}/{w_8}/{w_9}"

        else:
            embed_name = f"{num}위 : {w_0}"
            embed_value = f"{w_1}/{w_2}/{w_3}/{w_4}/{w_5}/{w_6}/{w_7}/{w_8}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def k1(ctx):
    url = f"https://sports.news.naver.com/kfootball/record/index?category=kleague"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")

    embed = discord.Embed(title="K리그 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수/승점/승/무/패/득점/실점/득실차/도움/파울", inline=False)

    team_rank_list = team_rank.select('#splitGroupA_table>tr')

    for team in team_rank_list:
        num = team.select('th > strong')[0].text
        name = team.select('span')[0].text
        games = team.select('td')[1].text
        points = team.select('td')[2].text
        wins = team.select('td')[3].text
        draws = team.select('td')[4].text
        loses = team.select('td')[5].text
        gf = team.select('td')[6].text
        ga = team.select('td')[7].text
        gd = team.select('td')[8].text
        assists = team.select('td')[9].text
        fouls = team.select('td')[10].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{points}/{wins}/{draws}/{loses}/{gf}/{ga}/{gd}/{assists}/{fouls}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    team_rank_list = team_rank.select('#splitGroupB_table>tr')

    for team in team_rank_list:
        num = team.select('th > strong')[0].text
        name = team.select('span')[0].text
        games = team.select('td')[1].text
        points = team.select('td')[2].text
        wins = team.select('td')[3].text
        draws = team.select('td')[4].text
        loses = team.select('td')[5].text
        gf = team.select('td')[6].text
        ga = team.select('td')[7].text
        gd = team.select('td')[8].text
        assists = team.select('td')[9].text
        fouls = team.select('td')[10].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{points}/{wins}/{draws}/{loses}/{gf}/{ga}/{gd}/{assists}/{fouls}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def mlb(ctx, category):
    url = f"https://sports.news.naver.com/wbaseball/record/index?category=mlb&league={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")

    embed = discord.Embed(title="메이저리그 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수/승/패/승률/게임차/연속/타율/평균자책/최근10경기", inline=False)

    team_rank_list = team_rank.select('#eastDivisionTeamRecordList_table>tr')
    embed.add_field(name="동부지구", value=f"{category}", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        games = team.select('span')[1].text
        wins = team.select('span')[2].text
        loses = team.select('span')[3].text
        win_rate = team.select('span')[4].text
        g_b = team.select('span')[5].text
        sequences = team.select('span')[6].text
        on_base_per = team.select('span')[7].text
        s_a = team.select('span')[8].text
        last_ten_games = team.select('span')[9].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{wins}/{loses}/{win_rate}/{g_b}/{sequences}/{on_base_per}/{s_a}/{last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    team_rank_list = team_rank.select('#centerDivisionTeamRecordList_table>tr')
    embed.add_field(name="중부지구", value=f"{category}", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        games = team.select('span')[1].text
        wins = team.select('span')[2].text
        loses = team.select('span')[3].text
        win_rate = team.select('span')[4].text
        g_b = team.select('span')[5].text
        sequences = team.select('span')[6].text
        on_base_per = team.select('span')[7].text
        s_a = team.select('span')[8].text
        last_ten_games = team.select('span')[9].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{wins}/{loses}/{win_rate}/{g_b}/{sequences}/{on_base_per}/{s_a}/{last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    team_rank_list = team_rank.select('#westDivisionTeamRecordList_table>tr')
    embed.add_field(name="서부지구", value=f"{category}", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        games = team.select('span')[1].text
        wins = team.select('span')[2].text
        loses = team.select('span')[3].text
        win_rate = team.select('span')[4].text
        g_b = team.select('span')[5].text
        sequences = team.select('span')[6].text
        on_base_per = team.select('span')[7].text
        s_a = team.select('span')[8].text
        last_ten_games = team.select('span')[9].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{wins}/{loses}/{win_rate}/{g_b}/{sequences}/{on_base_per}/{s_a}/{last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    team_rank_list = team_rank.select('#wildCardTeamRecordList_table>tr')
    embed.add_field(name="와일드카드", value=f"{category}", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[0].text
        games = team.select('span')[1].text
        wins = team.select('span')[2].text
        loses = team.select('span')[3].text
        win_rate = team.select('span')[4].text
        g_b = team.select('span')[5].text
        sequences = team.select('span')[6].text
        on_base_per = team.select('span')[7].text
        s_a = team.select('span')[8].text
        last_ten_games = team.select('span')[9].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{wins}/{loses}/{win_rate}/{g_b}/{sequences}/{on_base_per}/{s_a}/{last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def kbo(ctx):
    url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = discord.Embed(title="kbo리그 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수/승/패/무/승률/게임차/연속/출루율/장타율/최근10경기", inline=False)

    for team in team_rank_list:
        num = team.select('th > strong')[0].text
        name = team.select('span')[0].text
        games = team.select('span')[1].text
        wins = team.select('span')[2].text
        loses = team.select('span')[3].text
        draws = team.select('span')[4].text
        win_rate = team.select('strong')[1].text
        g_b = team.select('span')[5].text
        sequences = team.select('span')[6].text
        on_base_per = team.select('span')[7].text
        s_a = team.select('span')[8].text
        last_ten_games = team.select('span')[9].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games}/{wins}/{loses}/{draws}/{win_rate}/{g_b}/{sequences}/{on_base_per}/{s_a}/{last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

buttons = ButtonsClient(bot)

@bot.command()
async def 가위바위보(ctx):
    await buttons.send(
        content="가위, 바위, 보 중 하나를 선택하세요.",
        channel=ctx.channel.id,
        components=[
            ActionRow([
                Button(
                    label="가위",
                    style=ButtonType().Danger,
                    custom_id="button_가위"
                ),
                Button(
                    label="바위",
                    style=ButtonType().Primary,
                    custom_id="button_바위"
                ),
                Button(
                    label="보",
                    style=ButtonType().Success,
                    custom_id="button_보"
                )
            ])
        ]
    )

@buttons.click
async def button_가위(ctx):
    computer = random.choice(['가위', '바위', '보'])

    if computer == '가위':
        await ctx.reply(f'무승부 ({bot.user.name} : {computer}, user : 가위)')
    elif computer == '바위':
        await ctx.reply(f'패배 ({bot.user.name} : {computer}, user : 가위)')
    elif computer == '보':
        await ctx.reply(f'승리 ({bot.user.name} : {computer}, user : 가위)')

@buttons.click
async def button_바위(ctx):
    computer = random.choice(['가위', '바위', '보'])

    if computer == '가위':
        await ctx.reply(f'승리 ({bot.user.name} : {computer}, user : 바위)')
    elif computer == '바위':
        await ctx.reply(f'무승부 ({bot.user.name} : {computer}, user : 바위)')
    elif computer == '보':
        await ctx.reply(f'패배 ({bot.user.name} : {computer}, user : 바위)')

@buttons.click
async def button_보(ctx):
    computer = random.choice(['가위', '바위', '보'])

    if computer == '가위':
        await ctx.reply(f'패배 ({bot.user.name} : {computer}, user : 보)')
    elif computer == '바위':
        await ctx.reply(f'승리 ({bot.user.name} : {computer}, user : 보)')
    elif computer == '보':
        await ctx.reply(f'무승부 ({bot.user.name} : {computer}, user : 보)')

@bot.command()
async def 주사위(ctx):
    result, _color, bot_dice, user = dice()
    embed = discord.Embed(title="주사위 게임 결과", color=_color)
    embed.add_field(name=f"{bot.user.name}의 숫자", value=":game_die: " + bot_dice, inline=True)
    embed.add_field(name=f"{ctx.author.name}의 숫자", value=":game_die: " + user, inline=True)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send(str(bot.voice_clients[0].channel)+" 음성채널에 접속하였습니다.")

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()

@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("중지되어 있습니다.")

@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("재생되어 있습니다.")

@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("재생되지 않았습니다.")

@bot.event
async def on_ready():
    print(f"{bot.user.name}이 작동되었습니다.")

@bot.command()
async def hello(ctx):
    await ctx.send("hello")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다")

bot.run(token)  # 토큰
