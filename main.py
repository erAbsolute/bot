# bot.py
import asyncio
import discord
import os
from discord.ext import commands
from discord.ext import bridge
import datetime
import pytz
from secrets import token, path_main, path_python
from time import sleep

madrid = pytz.timezone("Europe/Madrid")
#As of PyCord beta 5 (which uses API v10), specifying the message content intent will be required for receiving message content.
#
#You will need to enable the intent on the developer portal, as well as in your code:
intents = discord.Intents.default()
intents.message_content = True

bot = bridge.Bot(command_prefix=';', description='Bot prueba v2', help_command=None, intents=intents)

#Funcion para mandar el embed
async def embed(ctx, des, color, name, delete=0):
    e = discord.Embed(description= des,
    timestamp=datetime.datetime.now(tz=madrid),
    color= color)
    e.set_footer(text="Solicitado por: {}".format(str(ctx.author)), icon_url=ctx.author.avatar)
    e.set_author(name= name)
   #  Sale la foto en grande en una esquina
   #  embed.set_thumbnail(url=ctx.author.avatar_url)
    if delete == 0:
     await ctx.send(embed=e)
    else:
     await ctx.send(embed=e, delete_after=delete)

@bot.bridge_command(name='ping',description='Muestra el ping que tiene el bot con los servidores de Discord')
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

@bot.bridge_command(name='ayuda',description='Muestra los comandos del bot')
async def help(ctx):
    des = """
    Comandos disponibles:\n
    > Prefijo:  `;`\n
    > ayuda: Muestra este panel de ayuda\n
    > ping: El bot te dice cuanto tarda en procesar el pong\n
    > reiniciar: Reinicia el bot, hace falta tener el rol <@&980096058820534273>\n
    > mostrarinfo: Muestra datos del usuario seleccionado\n
    Hecho en Python\n
    """
    name='Lista de comandos'
    color=discord.Color.blue()
    await embed(ctx, des, color, name)

@bot.bridge_command(name ='reiniciar', description='Reinicia el bot')
@commands.has_role('Bot Manager')
async def restart(ctx):
    des = "Reiniciando el bot."
    name = 'Reiniciando...'
    color=discord.Color.gold()
    await embed(ctx, des, color, name, delete=0.1)
    sleep(1)
    #des = f"{str(ctx.author)} me ha reiniciado."
    des = "He sido reiniciado."
    name = 'Bot reiniciado.'
    color=discord.Color.green()
    await embed(ctx, des, color, name)
    os.execv(path_python, ["python"] + [path_main])

@bot.bridge_command(name="mostrarinfo", description="Muestra la información del usuario")
async def info(ctx, user: discord.Member = None):
    user = user or ctx.author  # if no user is provided it'll use the the author of the message
    e = discord.Embed(timestamp=datetime.datetime.now(tz=madrid))
    e.set_author(name=str(user))
    e.set_thumbnail(url=user.avatar.url)
    e.add_field(name="ID", value=user.id, inline=False)  # user ID
    # When the user joined the server
    e.add_field(
        name="Se unió en:",
        value=discord.utils.format_dt(user.joined_at, "F"),
        inline=True,
    )
    e.add_field(
        name="Creado en:",
        value=discord.utils.format_dt(user.created_at, "F"),
        inline=True,
    )   # When the user's account was created
    e.set_footer(text="Solicitado por: {}".format(str(ctx.author)), icon_url=ctx.author.avatar)
    colour = user.colour
    if colour.value:  # if user has a role with a color
        e.colour = colour

    if isinstance(user, discord.User):  # checks if the user in the server
        e.set_footer(text="Este miembro no está en este servidor.")

    if user.nick is not None:
        e.set_author(name=str(user)+' AKA '+user.nick) 
    await ctx.respond(embed=e)  # sends the embed

@bot.bridge_command(name="limpiar", description="Limpia la cantidad de mensajes que le digas")
@commands.has_permissions()
async def clear(ctx, number):
    number = int(number) #Converting the amount of messages to delete to an integer
    counter = 0
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        if counter < number:
            await bot.delete_message(x)
            counter += 1
            await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even

#@restart.error
#async def restart_error(ctx, error):
#    if error == 'MissingRole':
#     des = "Necesitas el rol <@&735506792494399638> para reiniciar el bot"
#     color=discord.Color.red()
#     name='Fallo al reiniciar'
#     await embed(ctx, des, color, name)
#    else:
#     print(error) 

@bot.event
async def on_command(ctx):
    await ctx.message.delete()

#@bot.event
#async def on_application_command(ctx):
#    await ctx.message.delete()

@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.errors.MissingRole):
     des = "Necesitas el rol <@&980096058820534273> para reiniciar el bot"
     color=discord.Color.red()
     name='Fallo al reiniciar'
     await embed(ctx, des, color, name)
    else:
     des = f"Error: {error}"
     color=discord.Color.red()
     name=f'Fallo con el comando {ctx}'
     await embed(ctx, des, color, name)

@bot.event
async def on_application_command_error(ctx, error):
#    await ctx.message.delete()
    if isinstance(error, commands.errors.MissingRole):
     des = "Necesitas el rol <@&980096058820534273> para reiniciar el bot"
     color=discord.Color.red()
     name='Fallo al reiniciar'
     await embed(ctx, des, color, name)
    else:
     des = f"Error: {error}"
     color=discord.Color.red()
     name=f'Fallo con el comando {ctx}'
     await embed(ctx, des, color, name)

@bot.event
async def on_ready():
    print(f'Te has logeado como {bot.user}')
    # 'Watching' status
    name = "Bioshock: The Collection gratis en Epic Games"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=name),status='streaming')
bot.run(token)