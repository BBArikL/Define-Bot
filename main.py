import discord #Discord libraries
import os
import json #Support for json files
from keepalive import keep_alive # imports the web server that pings the bot continually
from discord.ext import commands

client = discord.Client() # Connects to the discord client
client = commands.Bot(command_prefix = '?')
#discord.ext.commands.Bot(command_prefix = get_prefix, case_insensitive = True)
client.remove_command("help") # Removes the default "help" function to replace it pby our own

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='?Define <Word>'))

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
  #Handles errors
  if isinstance(error, commands.CommandNotFound): # Command not found
    await ctx.send(f'Invalid command. Try {client.command_prefix}help to search for usable commands.')
  elif isinstance(error, commands.MissingRequiredArgument): # Manque d'arguments
    await ctx.send(f'A required argument is needed. Try {client.command_prefix}help to see required arguments.')
  elif isinstance(error, commands.MissingPermissions):
    await ctx.send('You do not have the permission to do that.')
  else: # Erreurs non supporté pour le moment
    await ctx.send('Word not  found....')

@client.group(invoke_without_command=True, case_insensitive = True)
async def help(ctx): # Custom Help command
  embed=discord.Embed(title="Define", description="?define <word>")
  embed.set_footer(text="Check the bot here: https://github.com/BBArikL/Define-Bot")
  await ctx.send(embed=embed)

async def send(ctx, defin, word):
  embed = discord.Embed(title = word)
  embed.add_field(name = 'Definition', value = defin)
  embed.set_footer(text ="Bot Git page: https://github.com/BBArikL/Define-Bot")
  await ctx.send(embed=embed)

@client.command()
async def Define(ctx, *, question=None): # Checks the documentation of a certain app/language
  # Lis le fichier json
  with open('dictionary.json', 'r') as f:
    doc = json.load(f)

  word = question.split(" ")[0].lower()

  try: # Now the on_command_error() function works too much better, then the Try/Except block doesnt nearly do anything
    definition = doc[word]

    await send(ctx,'Here is the definition: ' + definition, word)
  except ValueError:
    await ctx.send('Word not found...')

@client.command()
async def git(ctx): # Links back to the github page
  await ctx.send("Want to help the bot? Go here: https://github.com/BBArikL/Define-Bot")

keep_alive() # Keeps the bot alive

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token