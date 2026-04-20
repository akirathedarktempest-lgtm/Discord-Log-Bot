import discord
from discord.ext import commands
from discord import app_commands
import asyncio

intents=discord.Intents.all()
bot=commands.Bot("!",intents=intents)

@bot.event
async def on_ready():
    print("The bot is loading...")
    await bot.tree.sync()
    print("The bot is ready...")

#FIRST IS PURGE COMMAND, you may ask why am I using this...but just for fun, actually, i think, there should be only one bot managing everything

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx:commands.Context,number):
    try:
        number=int(number)
        if ctx.author.guild_permissions.manage_messages is False:
            msg=await ctx.send("You don't have permissions!")
            await asyncio.sleep(5)
            await msg.delete()
        else:
            await ctx.channel.purge(limit=number+1)
            await asyncio.sleep(1)
            msg=await ctx.send(f"{number} messages are deleted by {ctx.author.mention}!")
            await asyncio.sleep(5)
            await msg.delete()
    except Exception as e:
        #await ctx.channel.purge(limit=1)#and this is to avoid the purge, if in case someone uses !purge hello and deletes it, then the log will also ignore that, so even before the message could be sent, it will be deleted immediately so that users can't trick our dear mods
        print(e)#i am removing this because i noticed it can be slow to delete itself, so await is not needed actually

#NOW, THIS IS THE REAL LOG OF MESSAGES, this will give you a message which is deleted in the server

@bot.event
async def on_message_delete(message:discord.Message):
    if message.author.bot: #this is because, if you want to clear the log, you deleted the bot message of log one by one, it will keep on posting that, so if the message is by bot, it will return nothing
        return
    #if message.content.startswith("!purge "):#this I used because purge command was deleting perfectly, just the command you said, !purge (like 3), it was deleting and the three messages were not coming on delete log, but the purge command was showing up so I just used it to avoid that
        #return#i am also removing this because it will just show one message, not so much necessary
    channel=message.guild.get_channel()#INSERT LOG CHANNEL ID IN ()
    embed=discord.Embed(title="Deleted Message",description=message.content)
    embed.set_footer(text=message.author,icon_url=message.author.display_avatar.url)
    await channel.send(embed=embed)

#THIS IS OF Message edited by a user

@bot.event
async def on_message_edit(before:discord.Message,after:discord.Message):
    if before.author.bot or after.author.bot:#...well, don't ask why this is...but the bot actually started a loop without this, it started saying message edited of itself, infinite loop so to avoid that we will just return
        return
    embed=discord.Embed()
    embed.set_author(name=before.author,icon_url=before.author.display_avatar.url)
    embed.add_field(name="*Original message*",value=before.content)
    embed.add_field(name="*Edited message*",value=after.content)
    embed.set_footer(text=after.author,icon_url=after.author.display_avatar.url)
    channel=before.guild.get_channel()#INSERT LOG CHANNEL ID IN ()
    await channel.send(embed=embed)
  """THIS IS THE LOG OF MESSAGES, I WILL EXPAND IT AND COVER OTHERS AS WELL"""



bot.run("TOKEN")
