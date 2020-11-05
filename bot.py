import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import datetime
import game
import asyncio



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix='?')
bot_channel = None #current bot vc

@bot.command()
async def ping(ctx):
  await ctx.send(bot.latency)
  await ctx.send(bot.guilds)
  _embed = discord.Embed(name="Embed", description="Description of Embed")
  _embed.add_field(name="Hi", value="Bye")
  await ctx.send(embed=_embed)

@bot.command()
async def test(ctx,*args):
    if len(args) == 0:
        await ctx.send("bruh")
    else:
        await ctx.send(" ".join(args))

@bot.command()
async def random(ctx):
    problem = game.problem()
    await ctx.send(f"{problem[0]}=")

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == f"{problem[1]}":
        await ctx.send("i guess u got it right")
    else:
        await ctx.send("Wrong! Fucking dumbass ragamuffin! Bitch go die in a hole!")

@bot.command()
async def start_timer(ctx, time='30', type='s'):
    global bot_channel
    await ctx.send(f'Timer started for {time} {type}')
    if type == 'm':
        time = int(time) * 60
    elif type == 'h':
        time = int(time) * 3600
    await asyncio.sleep(int(time))
    await ctx.send(f"Timer done.")



    channel = ctx.message.author.voice.channel
    await ctx.send('User is in channel: ' + channel.name)


    # only play music if user is in a voice channel
    if channel is not None:

        bot_channel = await channel.connect()

        # grab user's voice channel


        # create StreamPlayer
        print(bot_channel)
        await bot_channel.play(discord.FFmpegPCMAudio("alarm.mp3"))

        # asyncio.sleep()
        # player = vc.create_ffmpeg_player('alarm.mp3', after=lambda: print('done'))
        # player.start()
        # while not player.is_done():
        #     await asyncio.sleep(1)
        # # disconnect after the player has finished
        # player.stop()
        # # await vc.disconnect()
    else:
        await ctx.send(':x: User is not in a channel.')

@bot.command()
async def join(ctx):
    global bot_channel
    channel = ctx.message.author.voice.channel
    if bot_channel is None:
        bot_channel = await channel.connect()
    else:
        await ctx.send(':x: Already connected to a voice channel.')

# @bot.command()
# async def stop_alarm(ctx):


@bot.command()
async def leave(ctx):
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