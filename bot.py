import discord
import youtube_dl
from discord.ext import commands
import json

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
    
@bot.command(pass_context=True)
async def play(ctx,url):
    voice = ctx.message.author.voice
    voice_client = ctx.guild.voice_client
    player = await voice_client.create_ytdl_player(url)
    players[guild.id] = player
    player.start()
    
bot.run(jdata['TOKEN'])




