# bot.py
from http import client
import discord
import os
from discord.ext import commands
import datetime
import pytz

madrid = pytz.timezone("Europe/Madrid")
TOKEN = os.getenv('token')

bot = commands.Bot(command_prefix=';', description='Bot prueba v2', help_command=None)

#Ver cuanto ping tiene el bot
@bot.command(
    help="Vemos el ping del bot",
    brief="Vemos el ping del bot"
)
async def ping(ctx):
    await ctx.send(f'Pong en {round(bot.latency * 1000)}ms')

@bot.command()
async  def  help(ctx):
  des = """
  Comandos disponibles:\n
  > Prefijo:  `;`\n
  > ping: El bot te dice cuanto tarda en procesar el pong\n
  Hecho con amor en Python\n
  """
  embed = discord.Embed(title="Bot en pruebas",url="https://cdn.discordapp.com/avatars/185405355117903873/2133ec67021514b0bb0de712d88f5950.webp?size=1024",description= des,
  timestamp=datetime.datetime.now(),
  color=discord.Color.blue())
  embed.set_footer(text="solicitado por: {}".format(ctx.author.name))
  embed.set_author(name="erAbsolute",
  icon_url="https://cdn.discordapp.com/avatars/185405355117903873/2133ec67021514b0bb0de712d88f5950.webp?size=1024")


  await ctx.send(embed=embed)



@bot.event
async def on_ready():
    print(f'Te has logeado como {bot.user}')
    # 'Watching' status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

bot.run(TOKEN)