import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import datetime
import game
import asyncio
import random
from time import time as currtime
import urllib.request
import urllib.parse
from PIL import Image
import io
from settings import *
import os


intents = discord.Intents.default()
intents.members = True


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

pg = game.ProblemGenerator()
bot = commands.Bot(command_prefix='?', intents = intents)
bot_channel = None #current bot vc
start_time = 0
user_time = None
timer_on = False
rns_started = False

#create a list of the queued timers?

@bot.command()
async def ping(ctx):
  await ctx.send(bot.latency)
  #use of embed
  _embed = discord.Embed(name="Embed", description="Description of Embed")
  _embed.add_field(name=f"When the", value=house_of_rising_sun)
  await ctx.send(embed=_embed)

@bot.command()
async def rojo(ctx, num: int):
    global bot_channel

    if ctx.message.author.voice.channel is not None:
        channel = ctx.message.author.voice.channel
        await ctx.send(f'User {ctx.message.author.mention} is in channel: ' + channel.name)
        bot_channel = await channel.connect()
        print(bot_channel)
        await bot_channel.play(discord.FFmpegPCMAudio(ROJO_MUSIC[num-2]))
        await bot_channel.disconnect()

    else:
        await ctx.send(':x: User is not in a channel.')


@bot.command()
async def test(ctx,*args): #bot returns user message as test function
    if len(args) == 0:
        await ctx.send('bruh')
    else:
        await ctx.send(" ".join(args))

@bot.command()
async def quit_rns(ctx):
    global rns_started
    if rns_started:
        rns_started = False

@bot.command()
async def start_rns(ctx, type = None):
    global rns_started
    rns_started = True
    while rns_started:
        start = currtime()
        if type == None:
            random_method = random.choice(PG_METHODS)
            question = random_method(pg)
            _embed = discord.Embed(name="Prompt", description=f"Type: {random_method.__name__}")
            _embed.add_field(name=f"{question.prompt} = ", value="Answer in the next message.")
            await ctx.send(embed=_embed)
            # await ctx.send(f"Type: {random_method.__name__}\n{question.prompt}=")
        else:
            pg_methods_string = '\n-'.join(list(func.__name__.strip('pg.') for func in PG_METHODS))
            try:
                question = getattr(pg, type)()
                await ctx.send(f"{question.prompt}=")
            except:
                await ctx.send(f":x: Problem type not recognized. Available problem types: \n-{pg_methods_string}")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        elapsed_time = round(currtime() - start, 3)
        await ctx.send(f"It only took you {elapsed_time} seconds brickhead!")
        try:
            temp = int(msg.content.lower())
            if msg.content.lower() == f"{question.solution}":
                await ctx.send("when u get it right :100:")
            else:
                await ctx.send(
                    f"Wrong! Fucking dumbass ragamuffin! Bitch go die in a hole! Answer is {question.solution}")
        except:
            await ctx.send(f"Enter a number you idiot! :100:")

@bot.command()
async def rns(ctx, type=None):
    if not rns_started:
        start = currtime()
        if type == None:
            random_method = random.choice(PG_METHODS)
            question = random_method(pg)
            _embed = discord.Embed(name="Prompt", description=f"Type: {random_method.__name__}")
            _embed.add_field(name=f"{question.prompt} = ", value="Answer in the next message.")
            await ctx.send(embed=_embed)
            # await ctx.send(f"Type: {random_method.__name__}\n{question.prompt}=")
        else:
            pg_methods_string = '\n-'.join(list(func.__name__.strip('pg.') for func in PG_METHODS))
            try:
                question = getattr(pg,type)()
                await ctx.send(f"{question.prompt}=")
            except: await ctx.send(f":x: Problem type not recognized. Available problem types: \n-{pg_methods_string}")

        # This will make sure that the response will only be registered if the following
        # conditions are met:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await bot.wait_for("message", check=check)
        elapsed_time = round(currtime() - start,3)
        await ctx.send(f"It only took you {elapsed_time} seconds brickhead!")
        try:
            temp = int(msg.content.lower())
            if msg.content.lower() == f"{question.solution}":
                await ctx.send("when u get it right :100:")
            else:
                await ctx.send(f"Wrong! Fucking dumbass ragamuffin! Bitch go die in a hole! Answer is {question.solution}")
        except:
            await ctx.send(f"Enter a number you idiot! :100:")
    else:
        await ctx.send(f":x: start_rns already running!")

@bot.command()
async def timer(ctx, time : int = 30, type='s'): #timer with bot alarm
    global bot_channel,start_time, user_time, timer_on
    if not timer_on:
        timer_on = True
        try:
            await ctx.send(f'Timer started for {time} {type}')
            if type == 'm':
                time = time * 60
            elif type == 'h':
                time = time * 3600
            start_time = currtime()
            user_time = time

            while user_time - (currtime()-start_time) > 0:
                await asyncio.sleep(0.001)
                # print(user_time - (currtime()-start_time))
                if not timer_on:
                    await ctx.send("Timer stopped.")
                    return

            timer_on = False
            await ctx.send(f"Timer done.")

            try:
                channel = ctx.message.author.voice.channel
                await ctx.send('User is in channel: ' + channel.name)
                if channel is not None:
                    bot_channel = await channel.connect()

                    print(bot_channel,user_time)
                    await bot_channel.play(discord.FFmpegPCMAudio(os.path.join('sounds',"alarm.mp3")))

                else:
                    await ctx.send(':x: User is not in a channel.')
            except:
                pass

        except: await ctx.send(f':x: Wrong syntax\n?start_timer [time: integer] [type: s, m, h]')
    else:
        await ctx.send(f':x: Timer already running.')

@bot.command()
async def stop(ctx): #force bot to leave user's vc
    global bot_channel, timer_on
    if timer_on:
        timer_on = False
    if bot_channel is not None:
        await bot_channel.disconnect()
        bot_channel = None


@bot.command()
async def elapsed(ctx): #force bot to leave user's vc
    global start_time,user_time, timer_on
    if timer_on:
        formatted_time_left=round(int((user_time))-(currtime()-start_time),1)
        if formatted_time_left > 60 and formatted_time_left < 3600:
            unit = 'minutes'
            formatted_time_left = round(formatted_time_left / 60, 1)
        elif formatted_time_left > 3600:
            unit = 'hours'
            formatted_time_left = round(formatted_time_left / 3600,1)
        elif formatted_time_left < 60:
            unit = 'seconds'
        await ctx.send(f'{formatted_time_left} {unit} left.')
    else: await ctx.send(f':x: No timer running.')



@bot.command()
async def nnn(ctx):
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    members = '\n - '.join([member.name for member in guild.members])
    await ctx.send(f'{members}')
    # for guild in bot.guilds:
    #     for member in guild.members:
    #         await ctx.send(member)


@commands.has_permissions(administrator=True)
@bot.command()
async def clear(ctx,amount = 1):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ['y','n']
    if amount > 1000:
        await ctx.send(f'Are you sure you want to clear {amount} messages? [y/n]')
        msg = await bot.wait_for("message",check = check)
        if msg.content.lower() == 'y':
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send('Clear command canceled.')
    else:
        await ctx.channel.purge(limit = amount)


@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

### DEBUGGING ###
# @bot.command()
# async def join(ctx): #force bot to join user's vc
#     global bot_channel
#     channel = ctx.message.author.voice.channel
#     if bot_channel is None:
#         bot_channel = await channel.connect()
#     else:
#         await ctx.send(':x: Already connected to a voice channel.')
#
@bot.command()
async def leave(ctx): #force bot to leave user's vc
    global bot_channel, timer_on
    if bot_channel is not None:
        await bot_channel.disconnect()
        bot_channel = None
    else:
        await ctx.send(':x: Bot is not in a voice channel.')

###LATEX FORMATTING
async def generate_file(dpi, tex):
    MARGIN = 20
    URL = 'https://latex.codecogs.com/gif.latex?{}'
    TEMPLATE = '\\dpi{{{}}} \\bg_white {}'
    filename = '{}.png'.format(random.randint(1, 1000))
    query = TEMPLATE.format(dpi, tex)
    print(query)
    url = URL.format(urllib.parse.quote(query))
    bytes = urllib.request.urlopen(url).read()
    img = Image.open(io.BytesIO(bytes))
    old_size = img.size
    new_size = (old_size[0] + MARGIN, old_size[1] + MARGIN)
    new_img = Image.new("RGB", new_size, (255, 255, 255))
    new_img.paste(img, (int(MARGIN / 2), int(MARGIN / 2)))
    img_bytes = io.BytesIO()
    new_img.save(img_bytes, 'PNG')
    img_bytes.seek(0)
    return img_bytes

@bot.command()
async def latex(ctx, message):
    await ctx.trigger_typing()

    dpi = 200
    tex = ''
    print('{}: dpi={} tex={}'.format(ctx.author, dpi, tex))
    bytes = await generate_file(dpi, message)
    filename = '{}.png'.format(random.randint(1, 1000))
    await ctx.send(file=bytes)


bot.run(TOKEN)