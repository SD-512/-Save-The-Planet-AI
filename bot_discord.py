import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!", intents=commands.Intents.all())

puntajes = {}

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


@bot.command()
async def start(ctx):
    mensaje = (
        "🌎 **¡Bienvenido a Save The Planet AI!** 🌱\n\n"
        "Soy un bot educativo sobre el cuidado del medio ambiente.\n\n"
        "**📋 Comandos disponibles:**\n\n"
        "💧 `!agua` - Consejos para ahorrar agua.\n"
        "♻️ `!reciclaje` - Aprende a reciclar.\n"
        "⚡ `!energia` - Ahorra energía.\n"
        "🌳 `!arboles` - Beneficios de los árboles.\n"
        "🌎 `!clima` - Información sobre el cambio climático.\n"
        "🚲 `!transporte` - Transporte sostenible.\n"
        "🦊 `!animales` - Protege la fauna.\n"
        "🍃 `!eco` - Consejo ecológico aleatorio.\n"
        "❓ `!quiz` - Responde una pregunta.\n"
        "🏆 `!puntaje` - Consulta tu puntaje.\n"
        "ℹ️ `!helpme` - Muestra esta ayuda nuevamente.\n\n"
        "¡Gracias por ayudar al planeta! 💚"
    )

    await ctx.send(mensaje)


@bot.command()
async def helpme(ctx):
    await start(ctx)


@bot.command()
async def agua(ctx):
    await ctx.send("💧 Cierra la canilla mientras te cepillas los dientes. Ahorrarás muchos litros de agua.")


@bot.command()
async def reciclaje(ctx):
    await ctx.send("♻️ Separa papel, cartón, plástico, vidrio y metal para facilitar el reciclaje.")


@bot.command()
async def energia(ctx):
    await ctx.send("⚡ Apaga las luces cuando salgas de una habitación y desconecta los cargadores que no estés usando.")


@bot.command()
async def arboles(ctx):
    await ctx.send("🌳 Los árboles producen oxígeno, capturan CO₂ y ayudan a mantener un clima saludable.")


@bot.command()
async def clima(ctx):
    await ctx.send("🌎 El cambio climático provoca fenómenos extremos como sequías, inundaciones y olas de calor.")


@bot.command()
async def transporte(ctx):
    await ctx.send("🚲 Siempre que puedas, camina, usa bicicleta o transporte público para reducir la contaminación.")


@bot.command()
async def animales(ctx):
    await ctx.send("🦊 Proteger los hábitats naturales ayuda a conservar miles de especies de animales.")


@bot.command()
async def eco(ctx):
    consejos = [
        "🌱 Lleva una botella reutilizable.",
        "💡 Usa lámparas LED.",
        "🚿 Reduce el tiempo de tus duchas.",
        "🛍️ Usa bolsas reutilizables.",
        "🌳 Planta un árbol.",
        "♻️ Recicla correctamente tus residuos.",
        "🚴 Usa bicicleta para trayectos cortos."
    ]

    await ctx.send(random.choice(consejos))


pregunta = {
    "pregunta": "❓ ¿Cuál de estos residuos tarda más tiempo en degradarse?\n\nA) Papel\nB) Vidrio\nC) Cáscara de banana\n\nResponde con: A, B o C",
    "respuesta": "B"
}


@bot.command()
async def quiz(ctx):
    await ctx.send(pregunta["pregunta"])


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    respuesta = message.content.upper()

    if respuesta in ["A", "B", "C"]:

        if respuesta == pregunta["respuesta"]:

            usuario = str(message.author)

            puntajes[usuario] = puntajes.get(usuario, 0) + 1

            await message.channel.send("✅ ¡Correcto! Ganaste 1 punto.")

        else:

            await message.channel.send("❌ Incorrecto. La respuesta correcta era **B) Vidrio**.")

    await bot.process_commands(message)


@bot.command()
async def puntaje(ctx):
    usuario = str(ctx.author)
    puntos = puntajes.get(usuario, 0)
    await ctx.send(f"🏆 {ctx.author.mention}, tienes **{puntos}** punto(s).")

bot.run(TOKEN)