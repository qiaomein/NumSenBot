import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import datetime
import game
import asyncio
import random


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

pg = game.ProblemGenerator()
bot = commands.Bot(command_prefix='?')
bot_channel = None #current bot vc
timer_on = False

@bot.command()
async def ping(ctx):
  await ctx.send(bot.latency)
  #use of embed
  _embed = discord.Embed(name="Embed", description="Description of Embed")
  _embed.add_field(name="Hi", value="Bye")
  await ctx.send(embed=_embed)

@bot.command()
async def test(ctx,*args): #bot returns user message as test function
    if len(args) == 0:
        await ctx.send("bruh")
    else:
        await ctx.send(" ".join(args))

@bot.command()
async def random_problem(ctx):
    question = random.choice([pg.square5,pg.random2x2,pg.random3x3])()
    await ctx.send(f"{question.prompt}=")

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == f"{question.solution}":
        await ctx.send("i guess u got it right")
    else:
        await ctx.send(f"Wrong! Fucking dumbass ragamuffin! Bitch go die in a hole! Answer is {question.solution}")

@bot.command()
async def start_timer(ctx, time='30', type='s'): #timer with bot alarm
    global bot_channel,timer_on
    await ctx.send(f'Timer started for {time} {type}')
    if type == 'm':
        time = int(time) * 60
    elif type == 'h':
        time = int(time) * 3600

    timer_on = True

    if timer_on:
        await asyncio.sleep(int(time))
        await ctx.send(f"Timer done.")

        channel = ctx.message.author.voice.channel
        await ctx.send('User is in channel: ' + channel.name)
        # only play music if user is in a voice channel
        try:
            if channel is not None:
                bot_channel = await channel.connect()

                print(bot_channel)
                await bot_channel.play(discord.FFmpegPCMAudio("alarm.mp3"))

            else:
                await ctx.send(':x: User is not in a channel.')
        except:
            pass
        timer_on = False

@bot.command()
async def stop_timer(ctx): #force bot to leave user's vc
    global bot_channel, timer_on
    if bot_channel is not None:
        await bot_channel.disconnect()
        bot_channel = None
    timer_on = False

@bot.command()
async def join(ctx): #force bot to join user's vc
    global bot_channel
    channel = ctx.message.author.voice.channel
    if bot_channel is None:
        bot_channel = await channel.connect()
    else:
        await ctx.send(':x: Already connected to a voice channel.')

# @bot.command()
# async def stop_alarm(ctx):

@bot.command()
async def nnn(ctx):
    # guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    # members = '\n - '.join([member.name for member in guild.members])
    # await ctx.send(f'{members}')
    for guild in bot.guilds:
        for member in guild.members:
            await ctx.send(member)

@bot.command()
async def leave(ctx): #force bot to leave user's vc
    global bot_channel
    if bot_channel is not None:
        await bot_channel.disconnect()
        bot_channel = None
    else:
        await ctx.send(':x: Bot is not in a voice channel.')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


bot.run(TOKEN)