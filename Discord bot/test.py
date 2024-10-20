# -------------------- LIBRERIAS -------------------- #

import discord
import asyncio
import discord.ui
from discord.ui import Button, View
from discord.ext import commands
import json  # Importar el módulo json

# -------------------- CARGA DE CONFIGURACIÓN -------------------- #

def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

# -------------------- INICIO -------------------- #

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True

# Prefijo
bot = commands.Bot(command_prefix='test/', intents=intents)

# Evento: cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord')
    print('Discord Version: ', discord.__version__)

@bot.command(name='main')
async def main(ctx):
    await ctx.send("Comando de prueba funcionando")

# Cargar el token del bot desde el archivo JSON
config = load_config()
bot.run(config['TOKEN'])  # Usar el token cargado

# -------------------- FIN -------------------- #
