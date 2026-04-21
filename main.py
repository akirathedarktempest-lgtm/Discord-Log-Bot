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

@bot.event
async def on_guild_role_create(role:discord.Role):
    embed=discord.Embed(description=f"Role ID: {role.id}\nName: {role.name}\nPosition: {role.position}\nPermissions: {role.permissions}\nColor: {role.color}\nTime when Created: {role.created_at} UTC")
    channel=role.guild.get_channel()#INSERT LOG CHANNEL ID IN ()
    await channel.send(embed=embed)

#So basically, this will run when the user who has role manage permission creates a role, although this is not necessary because when a role is created, it will be "new role" only and nothing special it will do actually

@bot.event
async def on_guild_role_delete(role:discord.Role):
    embed=discord.Embed(description=f"Role ID: {role.id}\nName: {role.name}\nPosition: {role.position}\nPermissions: {role.permissions}\nColor: {role.color}\nTime when Created: {role.created_at} UTC")
    channel=role.guild.get_channel()#INSERT LOG CHANNEL ID IN ()
    await channel.send("The Role is removed",embed=embed)

#this will run when a role is deleted

@bot.event
async def on_guild_role_update(before:discord.Role,after:discord.Role): 
    if before.name!=after.name: #we are using conditional statements because if one role gets updated, all the roles will be affected on their own and all the roles will appear, and can also break rate limits, so because of that, we only want this on specific updates and changes
        pass
    elif before.permissions!=after.permissions:
        pass
    elif before.color!=after.color:
        pass #now why not position of the role isn't here? Because, for example, if you create a new role, by default the position will be 0 or 1 (last or below) and like, there are 20 roles and you take it to position 20, others will also be affected, because the earlier 20 will update to 19,19 will update to 18, and so on and all will be affected and the bot will send of each...a humanity student teaching math, haha
    else:
        return  
    embed=discord.Embed()
    embed.add_field(name="Before",value=f"Role ID: {before.id}\nName: {before.name}\nPosition: {before.position}\nPermissions: {before.permissions}\nColor: {before.color}\nTime when Created: {before.created_at} UTC")
    embed.add_field(name="After",value=f"Role ID: {after.id}\nName: {after.name}\nPosition: {after.position}\nPermissions: {after.permissions}\nColor: {after.color}\nTime when Created: {after.created_at} UTC")
    channel=before.guild.get_channel()#INSERT LOG CHANNEL ID IN ()
    await channel.send(embed=embed)
#THIS WILL RUN WHEN a role is updated, like when a new role is created, role creation will run, and if updated, this happen, important
"""THIS IS NOW ROLE LOG, LOG CREATION, DELETE, UPDATE, ALTHOUGH THAT'S NOT SO MUCH NECESSARY...and that, role.permissions, that will give in number...there's a permission calculator at Discord Developer Portal, use that, I am not going to make the calculator bro, check by the calculator"""
#refrences are from Event Refrence, discord.py docs, https://discordpy.readthedocs.io/en/latest/api.html#event-reference check it out and I will cover more by that only
bot.run("TOKEN")
