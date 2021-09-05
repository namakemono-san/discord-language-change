import json
import discord
from discord.ext import commands

with open("config.json","r") as r:
    config = json.load(r)

bot = commands.Bot(command_prefix="L!")

def lang(ctx, value: str): # ここでサーバーごとに言語ファイルを読み込む
    with open("server-data.json", "r") as sd:
        server_data = json.load(sd)
    try:
        with open(f'langs/{server_data[str(ctx.guild.id)]["langs"]}.json', 'r', encoding='utf-8') as f:
            return json.load(f)[str(value)]
    except:
        with open(f'langs/{server_data[str(ctx.guild.id)]["langs"]}.json', 'r', encoding='utf-8-sig') as f:
            return json.load(f)[str(value)]

@bot.event
async def on_ready():
    print("bot is Ready")

@bot.event
async def on_guild_join(guild):
    with open('server-data.json', 'r')as f:
        server_data = json.load(f)
    
    server_data[str(guild.id)] = {"langs": "en"} # {"langs": "en"}を{"langs": "ja"}に変更したら初期言語を日本語に変更できる

    with open('server-data.json', 'w')as f:
        json.dump(server_data, f, indent=4)
    f.close()# 保存するために一回閉じる

@bot.event
async def on_guild_remove(guild):
    with open('server-data.json', 'r')as f:
        server_data = json.load(f)
    
    try:
        server_data.pop(str(guild.id))# ボットがサーバーから消されたときにデータを消すための処理
    except KeyError:
        pass

    with open('server-data.json', 'w')as f:
        json.dump(server_data, f, indent=4)
    f.close()

@bot.command()
async def set_lang(ctx, lang): # 言語を変更するコマンド
    if lang == "ja": # もし'lang'が'ja'なら
        with open('server-data.json','r') as f:
            langs = json.load(f)

        langs[str(ctx.guild.id)]['langs'] = "ja" #データを'ja'に変更する

        with open('server-data.json', 'w') as f:
            json.dump(langs, f, indent=4)

        em=discord.Embed(title="Language selection",description="ボットの言語を'ja'に変更",color=0x028760)
        await ctx.send(embed=em)

    elif lang == "en":
        with open('server-data.json','r') as f:
            langs = json.load(f)

        langs[str(ctx.guild.id)]['langs'] = "en"

        with open('server-data.json', 'w') as f:
            json.dump(langs, f, indent=4)

        em=discord.Embed(title="Language selection",description="ボットの言語を'en'に変更",color=0x028760)
        await ctx.send(embed=em)

    else:
        await ctx.send("存在しない言語です、以下の中から選んでください。\n`ja`,`en`")
        
@bot.command()
async def hello(ctx):
    await ctx.send(lang(ctx, "hello"))

bot.run(config["token"])