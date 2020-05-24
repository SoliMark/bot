import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
import json
import os

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.loads(jfile.read())

bot = commands.Bot(command_prefix='[')

@bot.event
async def on_ready():
    member="育盟大肥肥"
    channel = bot.get_channel(int(jdata['大廳']))
    message = "{} join!".format(member)
    await channel.send(message)
    print(">> Bot online <<")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['大廳']))
    message = "{} join!".format(member)
    await channel.send(message)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata['大廳']))
    message = "{} leave!".format(member)
    await channel.send(message)

@bot.command()
async def ping(ctx):
    message = "{} ms".format(bot.latency*1000)
    await ctx.send(message)

@bot.command()
async def picture(ctx,i):
   path = 'D:\\bot\\pic\\{}.jpg'.format(i)
   pic = discord.File(path) 
   await ctx.send(file=pic)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.guild
    voice_client = ctx.guild.voice_client
    await voice_client.disconnect()

async def joinMusicChannel(ctx):
    try:
        channel = ctx.author.voice.channel
    except:
        await ctx.send(ctx.author.mention + " Please join the music voice channel.")
        return False

    vc = ctx.voice_client
    if vc == None:
        await channel.connect()
    return True

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def endSong(guild, path):
    os.remove(path)


@bot.command()
async def play(ctx, url):
    data = await joinMusicChannel(ctx)
    if data == True:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
        guild = ctx.message.guild
        voice_client = guild.voice_client
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
bot.run(jdata['TOKEN'])




