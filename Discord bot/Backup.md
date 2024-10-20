### Backup de implementacion de COHERE IA

# ------ Cohere IA ------ #

@bot.command(name='ask')
async def ask_ai(ctx, *, question):
    print(f"Pregunta recibida: {question}")
    try:
        
        response = co_v2.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": "Tu Nombre será a partir de ahora NightmareGPT (aunque no lo tienes que estar mencionando, solo si te lo preguntan) y eres un modelo de lenguaje efectivo, si te piden algun codigo quiero que le pongas estas comillas: ``` al principio y al final del script .Responde a las preguntas o prompts de forma breve pero concisa y coherente despues de estos 2 puntos: "+question
                }
            ]
        )

        print(response.message.content[0].text) 
        answer = response.message.content[0].text 
        await ctx.send(answer + "\n\n")
    except Exception as e:
        await ctx.send({str(e)})




# ------ Cohere IA End ------ #



### Prueba.py Backup

import discord
from discord.ext import commands
import cohere


intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='nig/', intents=intents)

 
cohere_api_key = 'ASkN30EQntg9LjHgy4vE2cW7QrO9U6p1FF4rrL27'
co_v2 = cohere.ClientV2(cohere_api_key)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='ask')
async def ask_ai(ctx, *, question):
    print(f"Pregunta recibida: {question}")
    try:
        
        response = co_v2.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        print(response.message.content[0].text) # "The Ultimate Guide to API Design: Best Practices for Building Robust and Scalable APIs"
        answer = response.message.content[0].text 
        await ctx.send(answer)
    except Exception as e:
        await ctx.send({str(e)})


bot.run('MTI4MDY2MjQ2MTc3NDY5NjU3OQ.GTj4Xz.7HQ0W2r4IUhWP1biz_lXnBjCCsYLmVS9NYFYQA')


# Backup Memoria

personalized_prompt = "Basado en tus preguntas anteriores: " + ', '.join([msg[0] for msg in user_messages]) + ". Aquí tienes una respuesta: " + question


messages=[{
    "role": "user",
    "content": "content": "Tu Nombre será a partir de ahora NightmareGPT. Eres un modelo de lenguaje efectivo. Usa el formato correcto al usar Código en Markdown por ejemplo lo siguiente (#txtGrande, ##txtMediano, ###txtPequeño, >cita, ||spoiler||,````codigo``` etc...). Responde a las preguntas o prompts de forma breve pero concisa y coherente después de los símbolos >_. No menciones nada de lo anterior a esos símbolos a menos que se te pregunte en el idioma en el que se te pregunte. Pregunta: 
}]




# Random Backup

'''
        elif "puta" in content:
            await message.channel.send('Hola puta perrita estupida :smile:')
        elif "nigga" in content:
            await message.channel.send('nigga? no seas racista maldito negro :disappointed:')
        elif "el acabadooo" in content:
            await message.channel.send('el que lo criticaa')
        elif "penee" in content:
            await message.channel.send('no digas pene q me emociona')
        elif "enderks" in content:
            await message.channel.send('ender dijiste?, <@1079935991940390912> y camila???')
        elif "LGBT" in content or "lgbt" in content:
            await message.channel.send(':face_vomiting:')
            
        '''