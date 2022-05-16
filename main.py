from discord import Embed
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from config import *
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

bot = Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="0_명령어", description="명령어 설명", guild_ids=guild_ids)
async def command(ctx):
    embed = Embed(title="명령어", color=0xFFE400)
    embed.add_field(name="1_프로야구", value="kbo", inline=False)
    embed.add_field(name="2_해외야구", value="내셔널 | 아메리칸", inline=False)
    embed.add_field(name="3_프로축구", value="K1 | K2", inline=False)
    embed.add_field(name="4_해외축구", value="5대 리그", inline=False)
    embed.add_field(name="5_프로농구", value="남자 | 여자", inline=False)
    embed.add_field(name="6_해외농구", value="동부 | 서부", inline=False)
    embed.add_field(name="7_프로배구", value="남자부 | 여자부", inline=False)
    embed.add_field(name="8_뉴스검색", value="검색어를 입력하세요.", inline=False)
    embed.add_field(name="9_일정검색", value="팀이름을 입력하세요.", inline=False)

    await ctx.send(embed=embed)

def chrome_driver(url):
    options = ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)
    driver.get(url)

    page = driver.page_source
    driver.quit()

    return page

@slash.slash(name="1_프로야구", description="kbo", guild_ids=guild_ids)
async def baseball(ctx):
    await ctx.defer()
    url = f"https://sports.news.naver.com/kbaseball/record/index?category=kbo"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")

    embed = Embed(title="kbo리그 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수 | 승 | 패 | 무 | **__승률__** | 게임차 | 연속 | 출루율 | 장타율 | 최근10경기", inline=False)

    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')
    for team in team_rank_list:
        num = team.select('th > strong')[0].text
        name = team.select('span')[1].text
        games = team.select('span')[2].text
        wins = team.select('span')[3].text
        loses = team.select('span')[4].text
        draws = team.select('span')[5].text
        win_rate = team.select('strong')[1].text
        g_b = team.select('span')[6].text
        sequences = team.select('span')[7].text
        on_base_per = team.select('span')[8].text
        s_a = team.select('span')[9].text
        last_ten_games = team.select('span')[10].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games} | {wins} | {loses} | {draws} | **__{win_rate}__** | {g_b} | {sequences} | {on_base_per} | {s_a} | {last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

def mlb_team(embed, team_rank_list):
    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[1].text
        games = team.select('span')[2].text
        wins = team.select('span')[3].text
        loses = team.select('span')[4].text
        win_rate = team.select('span')[5].text
        g_b = team.select('span')[6].text
        sequences = team.select('span')[7].text
        on_base_per = team.select('span')[8].text
        s_a = team.select('span')[9].text
        last_ten_games = team.select('span')[10].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{games} | {wins} | {loses} | **__{win_rate}__** | {g_b} | {sequences} | {on_base_per} | {s_a} | {last_ten_games}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

@slash.slash(name="2_해외야구", description="MLB", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="리그",
                     description="리그를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="내셔널리그",
                             value="NL"
                         ),
                         create_choice(
                             name="아메리칸리그",
                             value="AL"
                         )
                     ]
                 )
             ],
             connector={
                 "리그": "category"
             })
async def mlb(ctx, category: str = "NL"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/wbaseball/record/index?category=mlb&league={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")

    embed = Embed(title="메이저리그 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수 | 승 | 패 | **__승률__** | 게임차 | 연속 | 타율 | 평균자책 | 최근10경기", inline=False)

    team_rank_list = team_rank.select('#eastDivisionTeamRecordList_table>tr')
    embed.add_field(name="동부지구", value=f"{category}", inline=False)
    mlb_team(embed, team_rank_list)

    team_rank_list = team_rank.select('#centerDivisionTeamRecordList_table>tr')
    embed.add_field(name="중부지구", value=f"{category}", inline=False)
    mlb_team(embed, team_rank_list)

    team_rank_list = team_rank.select('#westDivisionTeamRecordList_table>tr')
    embed.add_field(name="서부지구", value=f"{category}", inline=False)
    mlb_team(embed, team_rank_list)

    team_rank_list = team_rank.select('#wildCardTeamRecordList_table>tr')
    embed.add_field(name="와일드카드", value=f"{category}", inline=False)
    mlb_team(embed, team_rank_list)

    await ctx.send(embed=embed)

def soccer_team(embed, team_rank_list):
    for team in team_rank_list:
        num = team.select('th > strong')[0].text
        name = team.select('span')[1].text
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
        embed_value = f"{games} | **__{points}__** | {wins} | {draws} | {loses} | {gf} | {ga} | {gd} | {assists} | {fouls}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

@slash.slash(name="3_프로축구", description="k리그", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="리그",
                     description="리그를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="k1리그",
                             value="kleague"
                         ),
                         create_choice(
                             name="k2리그",
                             value="kleague2"
                         )
                     ]
                 )
             ],
             connector={
                 "리그": "category"
             })
async def soccer(ctx, category: str = "kleague"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/kfootball/record/index?category={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")

    embed = Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수 | **__승점__** | 승 | 무 | 패 | 득점 | 실점 | 득실차 | 도움 | 파울", inline=False)

    team_rank_list = team_rank.select('#regularGroup_table>tr')

    if team_rank_list:
        soccer_team(embed, team_rank_list)

    else:
        team_rank_list = team_rank.select('#splitGroupA_table>tr')
        soccer_team(embed, team_rank_list)

        team_rank_list = team_rank.select('#splitGroupB_table>tr')
        soccer_team(embed, team_rank_list)

    await ctx.send(embed=embed)

@slash.slash(name="4_해외축구", description="유럽축구", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="리그",
                     description="리그를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="프리미어리그",
                             value="epl"
                         ),
                         create_choice(
                             name="라리가",
                             value="primera"
                         ),
                         create_choice(
                             name="분데스리가",
                             value="bundesliga"
                         ),
                         create_choice(
                             name="세리에 A",
                             value="seria"
                         ),
                         create_choice(
                             name="리그 1",
                             value="ligue1"
                         )
                     ]
                 )
             ],
             connector={
                 "리그": "category"
             })
async def football(ctx, category: str = "epl"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/wfootball/record/index?category={category}&tab=team"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#wfootballTeamRecordBody>table>tbody>tr')

    embed = Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀 [진출 여부]", value="경기수 | **__승점__** | 승 | 무 | 패 | 득점 | 실점 | 득실차", inline=False)

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
        w_9 = team.select('div.inner > span')[9].text

        if number == 11:
            w_10 = team.select('div.inner > span')[10].text
            embed_name = f"{num}위 : {w_2} [{w_0}]"
            embed_value = f"{w_3} | **__{w_4}__** | {w_5} | {w_6} | {w_7} | {w_8} | {w_9} | {w_10}"

        else:
            embed_name = f"{num}위 : {w_1}"
            embed_value = f"{w_2} | **__{w_3}__** | {w_4} | {w_5} | {w_6} | {w_7} | {w_8} | {w_9}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@slash.slash(name="5_프로농구", description="남자 | 여자", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="리그",
                     description="리그를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="KBL",
                             value="kbl"
                         ),
                         create_choice(
                             name="WKBL",
                             value="wkbl"
                         )
                     ]
                 )
             ],
             connector={
                 "리그": "category"
             })
async def basketball(ctx, category: str = "kbl"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/basketball/record/index?category={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수 | **__승률__** | 승 | 패 | 승차 | 득점 | AS | 리바운드 | 스틸 | 블록 | 3점슛 | 자유투 | 자유투성공", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[1].text
        w_0 = team.select('span')[2].text
        w_1 = team.select('strong')[1].text
        w_2 = team.select('span')[3].text
        w_3 = team.select('span')[4].text
        w_4 = team.select('span')[5].text
        w_5 = team.select('span')[6].text
        w_6 = team.select('span')[7].text
        w_7 = team.select('span')[8].text
        w_8 = team.select('span')[9].text
        w_9 = team.select('span')[10].text
        w_10 = team.select('span')[11].text
        w_11 = team.select('span')[12].text
        w_12 = team.select('span')[13].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{w_0} | **__{w_1}__** | {w_2} | {w_3} | {w_4} | {w_5} | {w_6} | {w_7} | {w_8} | {w_9} | {w_10} | {w_11} | {w_12}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@slash.slash(name="6_해외농구", description="NBA", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="컨퍼런스",
                     description="컨퍼런스를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="동부",
                             value="EAST"
                         ),
                         create_choice(
                             name="서부",
                             value="WEST"
                         )
                     ]
                 )
             ],
             connector={
                 "컨퍼런스": "category"
             })
async def nba(ctx, category: str = "EAST"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/basketball/record/index?category=nba&conference={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = Embed(title=f"nba {category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀 [디비전]", value="경기수 | 승 | 패 | **__승률__** | 승차 | 홈승 | 홈패 | 원정승 | 원정패 | 디비전승 | 디비전패 | 연속", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[1].text
        w_0 = team.select('span')[2].text
        w_1 = team.select('span')[3].text
        w_2 = team.select('span')[4].text
        w_3 = team.select('span')[5].text
        w_4 = team.select('strong')[1].text
        w_5 = team.select('span')[6].text
        w_6 = team.select('span')[7].text
        w_7 = team.select('span')[8].text
        w_8 = team.select('span')[9].text
        w_9 = team.select('span')[10].text
        w_10 = team.select('span')[11].text
        w_11 = team.select('span')[12].text
        w_12 = team.select('span')[13].text

        embed_name = f"{num}위 : {name} [{w_0}]"
        embed_value = f"{w_1} | {w_2} | {w_3} | **__{w_4}__** | {w_5} | {w_6} | {w_7} | {w_8} | {w_9} | {w_10} | {w_11} | {w_12}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@slash.slash(name="7_프로배구", description="남자부 | 여자부", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="리그",
                     description="리그를 선택해주세요.",
                     option_type=3,
                     required=False,
                     choices=[
                         create_choice(
                             name="남자부",
                             value="kovo"
                         ),
                         create_choice(
                             name="여자부",
                             value="wkovo"
                         )
                     ]
                 )
             ],
             connector={
                 "리그": "category"
             })
async def volleyball(ctx, category: str = "kovo"):
    await ctx.defer()
    url = f"https://sports.news.naver.com/volleyball/record/index?category={category}"
    page = chrome_driver(url)
    team_rank = BeautifulSoup(page, "html.parser")
    team_rank_list = team_rank.select('#regularTeamRecordList_table>tr')

    embed = Embed(title=f"{category} 팀순위", color=0xFFE400)
    embed.add_field(name="순위 : 팀", value="경기수 | **__승점__** | 승 | 패 | 세트득실률 | 점수득실률 | 세트수 | 공격성공률 | 블로킹(세트당) | 서브(세트당) | 득점", inline=False)

    for team in team_rank_list:
        num = team.select('strong')[0].text
        name = team.select('span')[1].text
        w_0 = team.select('span')[2].text
        w_1 = team.select('strong')[1].text
        w_1 = w_1.strip()
        w_2 = team.select('span')[3].text
        w_3 = team.select('span')[4].text
        w_4 = team.select('span')[5].text
        w_5 = team.select('span')[6].text
        w_6 = team.select('span')[7].text
        w_7 = team.select('span')[8].text
        w_8 = team.select('span')[9].text
        w_9 = team.select('span')[10].text
        w_10 = team.select('span')[11].text

        embed_name = f"{num}위 : {name}"
        embed_value = f"{w_0} | **__{w_1}__** | {w_2} | {w_3} | {w_4} | {w_5} | {w_6} | {w_7} | {w_8} | {w_9} | {w_10}"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@slash.slash(name="8_뉴스검색", description="검색어 입력", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="검색어",
                     description="검색어를 입력해주세요.",
                     option_type=3,
                     required=True
                 )
             ],
             connector={
                 "검색어": "category"
             })
async def news(ctx, category):
    await ctx.defer()
    url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={category}"
    page = chrome_driver(url)
    news_html = BeautifulSoup(page, "html.parser")

    embed = Embed(title="뉴스", description=f"검색어 : {category}", color=0xFFE400)

    news_title = news_html.select("ul.list_news > li div.news_area")

    for a in news_title:
        press = a.select("a.info.press")[0].text
        before = a.select("span.info")[0].text
        tit = a.select("a.news_tit")[0]
        href = tit.attrs['href']
        title = tit.attrs['title']

        embed_name = f"> {press} - `{before}`"
        embed_value = f"[{title}]({href})"

        embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@slash.slash(name="9_일정검색", description="팀이름 입력", guild_ids=guild_ids,
             options=[
                 create_option(
                     name="종목",
                     description="종목을 선택해주세요.",
                     option_type=4,
                     required=True,
                     choices=[
                         create_choice(
                             name="프로야구",
                             value=1
                         ),
                         create_choice(
                             name="해외야구",
                             value=2
                         ),
                         create_choice(
                             name="프로축구",
                             value=3
                         ),
                         create_choice(
                             name="해외축구",
                             value=4
                         ),
                         create_choice(
                             name="프로농구",
                             value=5
                         ),
                         create_choice(
                             name="해외농구",
                             value=6
                         )
                     ]
                 ),
                 create_option(
                     name="팀이름",
                     description="풀네임을 입력해주세요.",
                     option_type=3,
                     required=True
                 )
             ],
             connector={
                 "종목": "choice",
                 "팀이름": "category"
             })
async def diary(ctx, choice, category):
    await ctx.defer()
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query={category}"
    page = chrome_driver(url)
    diary_html = BeautifulSoup(page, "html.parser")

    embed = Embed(title="일정", description=f"구단 : {category}", color=0xFFE400)

    diary_title = diary_html.select("table.tb_type > tbody > tr")

    for a in diary_title:
        if choice != 5 and choice != 6:
            score = a.select("em.txt_score")[0].text
        else:
            score = a.select("em.team_score")[0].text

        if score == "VS":
            date = a.select("td.date")[0].text
            lft = a.select("em.team_lft")[0]
            rgt = a.select("em.team_rgt")[0]

            if lft.span:
                lft.span.decompose()
            if rgt.span:
                rgt.span.decompose()

            lft = lft.text
            rgt = rgt.text

            if choice != 1 and choice != 2:
                if choice == 4:
                    time = a.select("td.time")[0].text
                else:
                    time = a.select("td.time_v2")[0].text

                embed_name = f"{date} {time}"
                embed_value = f"{lft} {score} {rgt}"

            else:
                embed_name = f"{date}"
                embed_value = f"{lft} {score} {rgt}"

            embed.add_field(name=embed_name, value=embed_value, inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"{bot.user.name}이 작동되었습니다.")

bot.run(token)  # 토큰
