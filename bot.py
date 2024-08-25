# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import asyncio
import random
import re
import argparse


parser = argparse.ArgumentParser(description="Iniciar o RPeuG Bot")
parser.add_argument("--token", type=str, required=True, help="O token do bot do Discord")
args = parser.parse_args()

intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content
intents.guilds = True  # Ensure the bot can access guild information
intents.members = True  # Ensure the bot can access member information

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot está pronto. Logado como {bot.user}')

@bot.command()
async def nc(ctx, *messages: str):
    # Check if the user has the "GM" role
    if any(role.name == "GM" for role in ctx.author.roles):
        # Capture the command message to delete it later
        command_message = ctx.message

        if len(messages) == 0:
            await ctx.send("Formato inválido. Use algo como !nc \"Primeira conquista: 10xp\" \"Segunda conquista:20xp\" \"Terceira conquista:230xp\"")
            return

        # Create a view to hold the buttons
        view = discord.ui.View()

        # Create buttons with sequential labels
        for index, message in enumerate(messages):
            button = discord.ui.Button(label=f"Conquista {index + 1}", style=discord.ButtonStyle.green)
            
            # Define the callback function for the button
            async def button_callback(interaction: discord.Interaction, msg=message):
                if any(role.name == "GM" for role in interaction.user.roles):
                    await interaction.response.send_message(msg, ephemeral=False)
                else:
                    await interaction.response.send_message("Tire suas mãos daí, mortal!", ephemeral=True, delete_after=5)

            # Attach the callback function to the button
            button.callback = button_callback
            view.add_item(button)

        # Send the message with the buttons to the channel
        await ctx.send(f"Existem {len(messages)} possíveis conquistas:", view=view)

        # Format the messages and send them to the user as a DM
        formatted_messages = "\n".join(f"Conquista {i + 1}: {msg}" for i, msg in enumerate(messages))
        await ctx.author.send(f"Aqui está a lista das conquistas:\n{formatted_messages}")

        # Delete the command message containing the !nc command
        await command_message.delete()
    else:
        await ctx.send("Esqueça, só os deuses fazem isso.", delete_after=5)  # Delete after 5 seconds

@bot.command()
async def roll(ctx, roll="", action=""):
    # Parse the roll parameter using regex
    match = re.match(r'(\d+)d(\d+)([+-]\d+)?', roll)
    if not match:
        await ctx.send("Formato inválido. Use algo como !roll 3d6+3 \"Atacar um goblin com minha espada\"")
        return

    num_dice = int(match.group(1))
    die_size = int(match.group(2))
    bonus = match.group(3)
    
    # Roll the dice
    rolls = [random.randint(1, die_size) for _ in range(num_dice)]
    total = sum(rolls)
    
    # Apply bonus if present
    if bonus:
        total += int(bonus)
    
    # Create an embed for the result
    embed = discord.Embed(title="Resultado da Rolagem", color=discord.Color.blue())
    
    if (action):
        embed.add_field(name="Ação", value=action, inline=False)
    
    embed.add_field(name="Dados Rolados", value=f'`{"`, `".join(map(str, rolls))}`', inline=False)
    
    if bonus:
        embed.add_field(name="Bônus", value=f'`{bonus}`', inline=False)

    embed.add_field(name="Total", value=f'`{total}`', inline=False)
    
    # Send the embed
    await ctx.send(embed=embed)
    
# Run the bot
bot.run(args.token)