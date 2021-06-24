import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import random
from discord.utils import get
import youtube_dl
import time

client = commands.Bot(command_prefix="=")

x = []
for i in range(1, 501):
  x.append(i)


@client.event
async def on_ready():
    print("Mr.Inspector at your server!")
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="=commandhelp"
    ))


@client.command()
async def join(ctx):
  channel = ctx.author.voice.channel
  await channel.connect()


@client.command()
async def yesno(ctx, *, message):
    await ctx.message.delete()
    embed = discord.Embed(
        title=message, url="https://youtu.be/wDgQdr8ZkTw", color=0xFF5733)
    embed.add_field(
        name="👍 Yes", value='.', inline=False)
    embed.add_field(
        name="👎 No", value='.', inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    channel = ctx.author.voice.channel
    await channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await ctx.send("> The song has been played!")


@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("No audio is playing right now.")


@client.command()
async def leave(ctx):
    if ctx.author.voice is None:
        await ctx.send("> Im not in a channel ")
        return
    await ctx.voice_client.disconnect()
    await ctx.send("> I am disconnected!")


@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def lootbox(ctx):
  output = random.choice(x)
  if output == 69:
    await ctx.send("> CONGRATS, YOU JUST GOT THE **Lucky_boi** ROLE! " + str(output))
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="Lucky_boi")
    await member.add_roles(role)

  elif output == 420:
    await ctx.send("> CONGRATS, YOU JUST GOT THE **Lucky_boi** ROLE! " + str(output))
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="Lucky_boi")
    await member.add_roles(role)

  else:
    await ctx.send(f"> {str(output)}  Sadly, you did not won the jackpot (69 and 420 are the winning number)")


@client.command()
async def commandhelp(ctx):
    embed = discord.Embed(title="Command List", url="https://youtu.be/oHg5SJYRHA0",
                          description="This is the list of command you can use. Prefix: = ", color=0xFF5733)
    embed.add_field(
        name="=addrole", value="This command required manage role permission. It can be use to give any role as long as the bot's role is higher than that role. =addrole {@target} {@role}", inline=False)
    embed.add_field(name="=removerole",
                    value="This command required manage role permission. It can be use to remove any role as long as the bot's role is higher than that role. =removerole {@target} {@role}", inline=False)
    embed.add_field(name="=lootbox", value="This command is a like a gacha machine. It will random a number between 1 to 500. If you got 69 or 420, you will get a special role!", inline=False)
    embed.add_field(
        name="=play", value='Play any music! Use: =play {url} The command has a slight delay of 10 second to 1 minute. Please be patient. In addition, there is a bug right now with this function, if the bot are in a voice chat before you use this command it will not work. This issue will be fix soon. Solution for right now is to use command =leave every time before playing a new song', inline=False)
    embed.add_field(
        name="=leave", value='Made the bot leave the voice chat', inline=False)
    embed.add_field(
        name="=rroll", value='I do not have much to say about it... JUST TRY IT OUT. VERY RECOMMENDED', inline=False)
    embed.add_field(
        name="=yesno", value='Ask any yes or no question. Use: =yesno {Question}', inline=False)
    embed.add_field(
        name="=vote", value='Let any memeber create a poll for anything. Any question or answer need to be put in a quotation mark. Use: =vote "{Question}" "{Answer1}" "{Answer2}"', inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"> hey {ctx.message.author.mention}, {member.name} has been given a role called: {role.name}")


@client.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"> hey {ctx.message.author.mention}, {member.name} has been removed from a role called: {role.name}")


@client.event
async def on_command_error(ctx, error):
  await ctx.send(f"> An error occured: {str(error)}")


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def ping(ctx):
    await ctx.send("> Pong!")


@client.command(pass_context=True)
async def rroll(ctx):
  if (ctx.author.voice):
    channel = ctx.author.voice.channel
    await channel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("rick.m4a"))
    await ctx.send(f"> AHA, you've been rick roll'd by {ctx.message.author.mention}")
  else:
    await ctx.send("> I cannot rick roll you because you are not in a voice channel!")

  time.sleep(19)
  await ctx.voice_client.disconnect()


@client.command()
async def vote(ctx, q, a1, a2):
  await ctx.message.delete()
  embed = discord.Embed(
      title=q, url="https://youtu.be/VBlFHuCzPgY", color=0x4FFAE1)
  embed.add_field(name=f"1️⃣ {a1}", value=".", inline=False)
  embed.add_field(name=f"2️⃣ {a2}", value=".", inline=False)
  msg = await ctx.send(embed=embed)
  await msg.add_reaction('1️⃣')
  await msg.add_reaction('2️⃣')


keep_alive()
client.run(os.getenv('TOKEN'))
