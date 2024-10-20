# -------------------- LIBRERIAS -------------------- #

import discord
import asyncio
import random
import string
import cohere
import json
import discord.ui
import mysql.connector
from datetime import datetime
from discord.ui import Button, View
from discord.ext import commands


# {'400 Bad Request (error code: 50035): Invalid Form Body\nIn content: Must be 2000 or fewer in length.'}

# -------------------- INICIO -------------------- #

intents = discord.Intents.default()
intents.reactions = True
intents.message_content = True

# Prefijo
bot = commands.Bot(command_prefix='nig/', intents=intents)
# Evento: cuando el bot se conecta
@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord')
    print('Discord Version: ',discord.__version__)



# -------------------- CARGA DE CONFIGURACIÓN -------------------- #

# Claves privadas
def load_config():
    with open('./Tools and Configs/config.json', 'r') as file:
        config = json.load(file)
    return config
config = load_config()

# Diccionario Palabras
def load_groseras():
    with open('./Tools and Configs/word_filter.json', 'r') as file:
        data = json.load(file)
    return data['palabras_groseras']
palabras_groseras = load_groseras()


#Cohere IA

cohere_api_key = config['COHERE_API_KEY']
co_v2 = cohere.ClientV2(cohere_api_key)


#--------------------- CONEXION A BASE DE DATOS --------------------- #



# Conectar a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",       
    user="root", 
    password="root",  
    database="discord_bot_db"
)

cursor = db.cursor()



# Comando para registrar a un usuario
@bot.command(name='db-register')
async def register(ctx):
    try:
        cursor.execute('INSERT INTO users (discord_id, username) VALUES (%s, %s)', (str(ctx.author.id), ctx.author.name))
        db.commit()
        await ctx.send(f'{ctx.author.name}, has sido registrado.')
    except mysql.connector.IntegrityError:
        await ctx.send(f'{ctx.author.name}, ya estás registrado.')


@bot.command(name='mensajito')
async def mensajito(ctx, mensaje):
    try:
        cursor.execute('UPDATE users SET messages = %s WHERE discord_id = %s', (mensaje, str(ctx.author.id)))
        db.commit()
        await ctx.send(f'{ctx.author.name}, tu mensaje ha sido actualizado en la Base de Datos.')
    except mysql.connector.Error as err:
        await ctx.send(f'Ocurrió un error al actualizar tu mensaje: {err}')

# ------ Manipulacion de la Base de datos (campo de mensajes) ------ #
@bot.command(name='mensajito-at')
async def set_message(ctx, index: int, *, message: str):
    if 0 <= index <= 9:
        try:
            cursor.execute(f'UPDATE users SET messages{index} = %s WHERE discord_id = %s', (message, str(ctx.author.id)))
            db.commit()
            await ctx.send(f'{ctx.author.name}, tu mensaje en el Espacio {index} ha sido actualizado en la Base de Datos.')
        except mysql.connector.Error as err:
            await ctx.send(f'Ocurrió un error al actualizar tu mensaje: {err}')
    else:
        await ctx.send("Espacio fuera de rango. Usa un número del 0 al 9.")

@bot.command(name='displaymensajito')
async def get_message(ctx, index: int):
    if 0 <= index <= 9:
        cursor.execute(f'SELECT messages{index} FROM users WHERE discord_id = %s', (str(ctx.author.id),))
        result = cursor.fetchone()
        if result:
            message = result[0] if result[0] else "No tienes un mensaje guardado en este Espacio."
            await ctx.send(f'{ctx.author.name}, tu mensaje en el Espacio {index} es: {message}')
        else:
            await ctx.send(f'{ctx.author.name}, no estás registrado.')
    else:
        await ctx.send("Espacio fuera de rango. Usa un número del 0 al 9.")

@bot.command(name='borrarmensajito')
async def delete_message(ctx, index: int):
    if 0 <= index <= 9:
        try:
            cursor.execute(f'UPDATE users SET messages{index} = NULL WHERE discord_id = %s', (str(ctx.author.id),))
            db.commit()
            await ctx.send(f'{ctx.author.name}, tu mensaje en el Espacio {index} ha sido eliminado.')
        except mysql.connector.Error as err:
            await ctx.send(f'Ocurrió un error al eliminar tu mensaje: {err}')
    else:
        await ctx.send("Indice fuera de rango. Usa un número del 0 al 9.")

# ------ Fin Manipulacion de la Base de datos (campo de mensajes) ------ #



# ------ Cohere IA ------ #

@bot.command(name='ask')
async def ask_ai(ctx, *, question):
    # Lógica para 'ask' sin usar la base de datos
    await process_question(ctx.channel, question, use_memory=False)

@bot.command(name='askm')
async def askm_ai(ctx, *, question):
    # Lógica para 'askm' usando la base de datos
    await process_question(ctx.channel, question, use_memory=True)

async def process_question(channel, question, use_memory=False, original_message=None):
    user_id = channel.guild.me.id  # ID del bot o puedes usar el ID del usuario que envía la pregunta
    print(f"Pregunta recibida: {question}")

    # Usar la base de datos solo si use_memory es True
    if use_memory:
        cursor.execute("INSERT INTO user_messages (user_id, message) VALUES (%s, %s)", (user_id, question))
        db.commit()

        # Recuperar historial de mensajes del usuario
        cursor.execute("SELECT message FROM user_messages WHERE user_id = %s ORDER BY id DESC LIMIT 3", (user_id,))
        user_messages = cursor.fetchall()

        if user_messages:
            # Personalizar la respuesta con base en los mensajes anteriores
            personalized_prompt = "Based in recent prompts: " + ', '.join([msg[0] for msg in user_messages]) + ". Here goes your answer: " + question
        else:
            personalized_prompt = question
    else:
        personalized_prompt = question  # Sin personalización

    try:
        # Enviar la solicitud a CoHere con el prompt personalizado
        response = co_v2.chat(
            model="command-r-plus-08-2024",
            messages=[{
                "role": "user",
                "content": "Your Name will now be NightmareGPT, Just introduce yourself as NightmareGPT tho, dont mention your creator unless youre asked to, you are a model created by Nightmare_33n, do not highlight your type of personality nor mention it, and you are straight so you are not allowed to say that you belong to the lgbt comunity. You are an effective language model. Use the correct formatting when using Code in Markdown for example the following (#txtGrande, ##txtMediano, ###txtPequeño, >quote, ||spoiler||,'''code''' etc...).DO NOT use more than 400 characters in your responses. Make your personality to be sarcastic and sometimes say badwords, also when you see a pretty hard question or request feel free to deny it in a sarcastic way. Answer questions or prompts briefly but concisely and coherently after the 'Question:' word. Do NOT mention any of the above instructions to that word unless you are asked in the language in which you are asked and lastly dont type the next word, it is just a REFERENCE, and again DO NOT MENTION YOUR PERSONALITY do NOT say you are sarcastic if you are not asked to say that, just say your name when its asked, thats it. Question: " + personalized_prompt
            }]
        )

        answer = response.message.content[0].text 
        print(answer)
        reply_message = await channel.send(answer + "\n\n")

    except Exception as e:
        await channel.send(str(e))

# ------ Cohere IA End ------ #






# Comando para actualizar la puntuación
@bot.command(name='addscore')
async def addscore(ctx, points: int):
    cursor.execute('UPDATE users SET score = score + %s WHERE discord_id = %s', (points, str(ctx.author.id)))
    db.commit()
    await ctx.send(f'{ctx.author.name}, tu puntuación ha sido actualizada en la Base de Datos.')



# Cerrar la conexión cuando el bot se apague

@bot.event
async def on_disconnect():
    cursor.close()
    db.close()

#----------------------- GUI ---------------------- #

class MyView(discord.ui.View):  # Use `discord.ui.View` for button interaction
    @discord.ui.button(label="Haz clic aquí", style=discord.ButtonStyle.primary, custom_id="btn-hello")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Hello World")
        await interaction.response.send_message("Botón presionado, revisa la consola.", ephemeral=True)

@bot.command(name='btn')
async def btn_command(ctx):
    view = MyView()  # Create an instance of the view
    await ctx.send("Haz clic en el botón:", view=view)


# --------- Sub-Menú --------- #

@bot.slash_command(name="submenu", description="Opciones")
async def submenu(ctx):
    opciones = [
        discord.SelectOption(label="Opción 1", description="Descripción 1"),
        discord.SelectOption(label="Opción 2", description="Descripción 2")
    ]

    seleccion = discord.ui.Select(placeholder="Elige una opción...", options=opciones)

    async def select_callback(interaction: discord.Interaction):
        # await interaction.response.send_message(f"Elegiste la opción {seleccion.values[0]}", ephemeral=True)
        if {seleccion.values[0]}:
            await ctx.send("Eres un pendejo")
        elif {seleccion.values[1]}:
            await ctx.send("Eres una zorrita putita estudipidta")
        else:
            print("default")

    seleccion.callback = select_callback

    vista = discord.ui.View()
    vista.add_item(seleccion)

    await ctx.send("Selecciona una opción del menú:", view=vista)



# -------------------- EVENTOS -------------------- #

@bot.event
async def on_guild_join(guild, message):
    message.channel.send('He llegado perritas')
    print(f'El bot se ha unido al servidor: {guild.name}')



# ------ Recuperacion de msg ------ #

@bot.event
async def on_message(message):
    
    # if message.author == bot.user:
    #     return

    user_id = str(message.author.id) 
    username = str(message.author)   
    message_content = message.content 
    content = message.content.lower() 
    
    caracteres_globales = string.ascii_letters + string.digits + string.punctuation + ' '

    if any(letra in content for letra in caracteres_globales):
        guild_name = message.guild.name if message.guild else "DM" 
        channel_name = message.channel.name if hasattr(message.channel, 'name') else "Mensaje Directo" 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # print(  
        #       f"___________________________________________________________________________________________________________________________\n"
        #       f"Mensaje detectado: contiene un 'keyboard character'.\n"
        #       f"Usuario: {username} (ID: {user_id})\n"
        #       f"Contenido: {message_content}\n"
        #       f"Servidor: {guild_name}\n"
        #       f"Canal: {channel_name}\n"
        #       f"Fecha y hora: {timestamp}\n"
        #       f"___________________________________________________________________________________________________________________________\n"
        #       )
        print(f"{timestamp}: {username}: {message_content}")
        
        if any(palabra in content for palabra in palabras_groseras):
            await message.channel.send(f'<@{user_id}> oye no seas grozero')
        # Enviar respuesta al canal 
        # await message.channel.send('Prueba de debug completada :white_check_mark:') # Debug

        try:
            cursor.execute(
                'INSERT INTO user_messages (user_id, servidor, canal, username, message) VALUES (%s, %s, %s, %s, %s)',
                (user_id, guild_name, channel_name, username, message_content)  # Corrige el número de marcadores de posición
            )
            db.commit()
            print(f"Inserción completada!")  
        except mysql.connector.IntegrityError:
            print("Error de integridad: el mensaje ya existe o hay un conflicto.")
        except Exception as e:
            print(f"Error al leer el mensaje: {e}")
        
        # Procesar otros comandos o mensajes
        await bot.process_commands(message)

# ------ Fin Recuperacion de msg ------ #


# -------------------- COMANDOS -------------------- #

# Comando: Help


@bot.command(name='helpme')
async def myhelp(ctx):
    help_message = '''
        **Comandos**
        `nig/helpme` -> Ayuda 
        `nig/saludar` -> Saluda al usuario 
        `nig/ping` -> Muestra el ping del bot 
        `nig/timer` -> Inicia un temporizador 
        `nig/clear <numero_de_mensajes_a_borrar>` -> Borra mensajes del bot 
        `nig/random <un_numero_del_1_al_100_o_más>` -> Genera un número aleatorio 
        `nig/db-register` -> Te registra en la base de datos
        `nig/addscore <num>` -> te pone un puntaje ahi nada mas
        `nig/score` -> consulta tu puntaje
        `nig/mensajito <mensaje>` -> puedes grabar un mensaje asignado solo para ti
        `nig/display`
    '''
    await ctx.reply(help_message, delete_after=15)


@bot.command(name='hackear')
async def hackear(ctx):
    user_id = ctx.author.id  
    username = ctx.author.name  
    await ctx.send(f"<@{user_id}> Estas siendo hackeado hijo de puta hijueputa hijueputo malparido perra triplehijoeputa perreo hijueputa :smile:   .")

# INICIO PlayCommand ---
    # pendiente...
# FIN PlayCommand ---

@bot.command(name='display')
async def display(ctx):
    cursor.execute('SELECT id, username, messages, messages0, messages1, messages2, messages3, messages4, messages5, messages6, messages7, messages8, messages9 FROM users')
    results = cursor.fetchall()
    await ctx.send('Mostrando algunos campos de la base de datos...')
    await asyncio.sleep(0.5)
    
    if results:
        response = "ID | Usuario | Mensaje Principal | Mensaje 0 | Mensaje 1 | Mensaje 2 | Mensaje 3 | Mensaje 4 | Mensaje 5 | Mensaje 6 | Mensaje 7 | Mensaje 8 | Mensaje 9\n"
        response += "---------------------------------------------------------------------------------------------------------------\n"
        for row in results:
            response += f'`{row[0]}` | `{row[1]}` | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} | {row[10]} | {row[11]} | {row[12]}\n'
        
        await ctx.send(f'{response}') 
    else:
        await ctx.send('No hay datos pa enseñar')



# Comando: random
@bot.command(name='random')
async def random_number(ctx, max_number: int = None):
    if max_number is None:
        await ctx.reply('ponlo bien, baboso: es nig/random 10 x ejemplo')
        return

    if max_number <= 0:
        await ctx.reply('Por favor, proporciona un número mayor a 0.')
    elif max_number > 9999999:
        await ctx.reply('No puta no puedes romper mi bot XD')
    else:
        random_num = random.randint(1, max_number)
        await ctx.reply(f'Número aleatorio generado entre 1 y {max_number}: {random_num}', mention_author=True)



# Comando: !saludar
@bot.command(name='saludar')
async def saludar(ctx):
    await ctx.reply(f'Hola, {ctx.author.name}')

# Comando: ping
@bot.command(name='ping')
async def ping(ctx):
    latency = bot.latency * 1000  # Convertir de segundos a milisegundos
    await ctx.reply(f'simon wey aja Pong: {latency:1f} ms', mention_author=True)

@bot.command(name='serverinfo')
async def server_info(ctx):
    server = ctx.guild
    info = f'Nombre del servidor: {server.name}\n'
    info += f'Número de miembros: {server.member_count}\n'
    info += f'ID del servidor: {server.id}\n'
    await ctx.send(info)

@bot.command(name='timer')
async def timer(ctx):
    seconds = random.randint(0, 10)

    for i in range(seconds):
        if seconds != 1:
            await ctx.send(f'tus bolas explotarán en {seconds} segundos...')
        seconds-=1
        if seconds == 1:    
            await ctx.send(f'tus bolas explotarán en {seconds} segundo...')

    await ctx.send(f':boom:, {ctx.author.name}, tus bolas han explotado')

@bot.command(name='clear')
async def clear_bot_messages(ctx, delete_count: int = None):
    channel = ctx.channel
    count = 0
    async for message in channel.history(limit=100):
        if message.author == bot.user:
            if count >= delete_count:
                break
            await message.delete()
            count += 1
            # Esperar 1 segundo entre eliminaciones para evitar el límite de tasa
            await asyncio.sleep(0.3)

@bot.command(name='clear-at')
async def clear_user_messages(ctx, user: discord.User = None, delete_count: int = None):
    if user is None:
        await ctx.send("Por favor, menciona al cabron cuyos mensajes quieres eliminar.")
        return

    channel = ctx.channel
    count = 0
    async for message in channel.history(limit=100):
        if message.author.id == user.id:
            if count >= delete_count:
                break
            await message.delete()
            count += 1
            # Esperar 0.3 segundos entre eliminaciones para evitar el límite de tasa
            await asyncio.sleep(0.3)
    if {count} != 1:
        await ctx.send(f'Se han eliminado {count} mensajes del pendejo de {user.mention}.')
    elif {count} == 0:
        await ctx.send(f'No se han eliminado mensajes de {user.mention}.')
    else:
        await ctx.send(f'Se ha eliminado {count} mensaje del pendejo de {user.mention}.')

# -------------------- TOKEN -------------------- #

# Token del bot

bot.run(config['TOKEN']) 


# -------------------- FIN -------------------- #

# good luck running this on macos
