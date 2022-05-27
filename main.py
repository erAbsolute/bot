# bot.py
import discord
import os
from discord.ext import commands
import datetime
import pytz
import secrets
from time import sleep


madrid = pytz.timezone("Europe/Madrid")

bot = commands.Bot(command_prefix=';', description='Bot prueba v2', help_command=None)

#Funcion para mandar el embed
async def embed(ctx, des, color, name, delete=0.0):
    embed = discord.Embed(description= des,
    timestamp=datetime.datetime.now(tz=madrid),
    color= color)
    embed.set_footer(text="Solicitado por: {}".format(ctx.author.name), icon_url=ctx.author.avatar_url)
    embed.set_author(name= name)
   #  Sale la foto en grande en una esquina
   #  embed.set_thumbnail(url=ctx.author.avatar_url)

    if delete == 0.0:
     await ctx.send(embed=embed)
    else:
     await ctx.send(embed=embed, delete_after=delete)

@bot.command(description='Muestra el ping que tiene el bot con los servidores de Discord')
async def ping(ctx):
    ping = round(bot.latency * 1000)
    name = 'Ping!'
    des = f'`Pong! en {ping}ms`'
    if ping <= 60:
     color = discord.Color.green()
    if ping >= 61 and ping <=120:
     color = discord.Color.gold()
    if ping > 120:
     color = discord.Color.red()    
    await embed(ctx, des, color, name)

@bot.command(description='Muestra los comandos del bot')
async def help(ctx):
    des = """
    Comandos disponibles:\n
    > Prefijo:  `;`\n
    > help: Muestra este panel de ayuda\n
    > ping: El bot te dice cuanto tarda en procesar el pong\n
    > restart: Reinicia el bot, hace falta tener el rol <@&735506792494399638>\n
    Hecho en Python\n
    """
    name='Lista de comandos'
    color=discord.Color.blue()
    await embed(ctx, des, color, name)

@bot.command(description='Reinicia el bot')
@commands.has_role(735506792494399638)
async def restart(ctx):
    des = "Reiniciando el bot."
    name = 'Reiniciando...'
    color=discord.Color.gold()
    await embed(ctx, des, color, name, delete=0.01)
    sleep(0.1)
    des = f"{ctx.message.author.mention} me ha reiniciado."
    name = 'Bot reiniciado.'
    color=discord.Color.green()
    await embed(ctx, des, color, name)
    os.execv(secrets.path_python, ["python"] + [secrets.path_main])

@restart.error
async def restart_error(ctx, error):
    des = "Necesitas el rol <@&735506792494399638> para reiniciar el bot"
    color=discord.Color.red()
    name='Fallo al reiniciar'
    await embed(ctx, des, color, name)

@bot.event
async def on_command(ctx):
    await ctx.message.delete()

@bot.event
async def on_application_command(ctx):
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'Te has logeado como {bot.user}')
    # 'Watching' status
    name = "Bioshock: The Collection gratis en Epic Games"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name))

bot.run(secrets.token)