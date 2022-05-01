import datetime
from sys import prefix

from discord.ext.commands import has_permissions, MissingPermissions
import discord
import asyncio
from discord.ext import commands, tasks
from discord_buttons_plugin import *
import os
import json
from itertools import cycle

def get_prefix(bot, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=(get_prefix), help_command=None)
buttons = ButtonsClient(bot)
status = cycle(['Ticket', 'Default prefix ^'])

		
@bot.event
async def on_guild_join(guild):
	
	

	with open ('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	
	prefixes[str(guild.id)] = "^"

	with open ('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)



@bot.event
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	
	prefixes.pop(str(guild.id))

	with open ('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

@bot.command()
async def changeprefix(ctx, prefix):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
	
	prefixes[str(ctx.guild.id)] = prefix
	

	with open ('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Changing prefix to `{prefix}`. By {ctx.author.name}", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")

	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)

	await ctx.send(f"Prefix changed to {prefix}")

@bot.command
async def createchannels(ctx):
	await ctx.create_text_channel("Tickets")
	await ctx.create_text_channel("log")

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")
	change_status.start()
	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Update of 5/1/2022!", color=0xe74c3c)
	log_embed.add_field(name="Thanks for adding me", value="Default prefix is ^. Channels will been created. Please don't delete them! or rename them!")
	log_embed.add_field(name="Log system!", value=f"On `5/1/2022` I added `Log system`! On guild join this channel will be created.")
	log_embed.add_field(name="Fun Commands!", value=f"Also Fun commands are on its way. **It will be a another BOT!**")
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="Tickets")

	#channel = bot.get_channel(966799146877079593)
	#await channel.send(embed = log_embed)

@tasks.loop(seconds=5)
async def change_status():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(status))))
#Whois
@bot.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):



    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.magenta(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))


    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def addcha(ctx, channel_name):
    await ctx.guild.create_text_channel(channel_name)
    await ctx.send(f"A new channel called {channel_name} was made")

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def addrole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f'I have successfully added {role.mention} to {user.mention}')

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def removerole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f'I have successfully removed {role.mention} from {user.mention}')

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def help(ctx):
	embed = discord.Embed(title="Help", description="This is all the commands!",color=0xe74c3c)
	embed.add_field(name="archive", value="The Archive command is a command that moves the channel, this is more for organisation. How to use? `^archive`")
	embed.add_field(name="Redo", value="The Redo command is for removing the ticket from Archive to ticket. How to use? `^redo`")
	embed.add_field(name="Clear", value="The Clear command is a command for purge of the channel, Deletes all the message. Must before 2 weeks. How to use? `^clear`")
	embed.add_field(name="Close", value="The Close command is for closing a ticket. How to use? `^close`")
	embed.add_field(name="Fclose", value="The Fclose command is for force closing a ticket. This command goes before the other. How to use? `^fclose` or `^forceclose`")
	embed.add_field(name="Playeradd", value="The Playeradd command is for adding a discord member to a ticket. How to use? `^playeradd`")
	embed.add_field(name="Playerremove", value="The Playerremove command is for removing a discord member from a ticket. How to use? `^playerremove`")
	embed.add_field(name="Ticket", value="The Ticket command is for sending a Embed for the basic ticket. How to use? `^ticket`")
	embed.timestamp = datetime.datetime.utcnow()
	embed.set_footer(text="AvenueMC")

	await ctx.send(embed=embed)


@buttons.click
async def Supportbutton(ctx):
	guild = ctx.message.guild
	name = 'Tickets'
	category = discord.utils.get(ctx.guild.categories, name=name) 

	ticket_report_embed = discord.Embed(title="❓ Support ticket", description=f"""Hello {ctx.member.name}!'\n\n Thanks for opening a ticket. \n**Please explain what for support you wil need!** \nA Staff Member will be right with you!  """, color=0xe91e63 )
	ticket_report_embed.timestamp = datetime.datetime.utcnow()
	ticket_report_embed.set_footer(text="AvenueMC")


	overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.member: discord.PermissionOverwrite(view_channel=True),
            
        }

	ticket = await guild.create_text_channel(f"Support-{ctx.member.name}", category=category, overwrites=overwrites )
	

    
	await ticket.send(
       embed=ticket_report_embed  
    )
	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Opening a ticket for {ctx.member.name}.\n The ticket type is `Support`", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")

	#Verander dit naar de ID van je channel
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)

@buttons.click
async def paymentbutton(ctx):
	guild = ctx.message.guild
	name = 'Tickets'
	category = discord.utils.get(ctx.guild.categories, name=name) 

	ticket_payment_embed = discord.Embed(title="🛒 Payment ticket", description=f"""Hello {ctx.member.name}!'\n\n Thanks for opening a ticket. \n**This is a Payment Ticket, please explain what you want to buy!** \nA Staff Member will be right with you! """, color=0xe91e63)


	overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.member: discord.PermissionOverwrite(view_channel=True),
            
        }


	ticket = await guild.create_text_channel(f"Payment-{ctx.member.name}", category=category, overwrites=overwrites )
	


    
	await ticket.send(
       embed=ticket_payment_embed  
    )

	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Opening a ticket for {ctx.member.name}.\n The ticket type is `Payment`", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	
	#Verander dit naar de ID van je channel
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)
@buttons.click
async def bugbutton(ctx):
	


	guild = ctx.message.guild
	name = 'Tickets'
	category = discord.utils.get(ctx.guild.categories, name=name) 


	ticket_bug_embed = discord.Embed(title="🐛 Bug ticket", description=f"""Hello {ctx.member.name}!'\n\n Thanks for opening a ticket. \n**This is a Bug Ticket, please explain what bug you find!** \nA Staff Member will be right with you!  """, color=0xe91e63)
	
	overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.member: discord.PermissionOverwrite(view_channel=True),
            
        }	

	ticket = await guild.create_text_channel(f"Bug-{ctx.member.name}", category=category, overwrites=overwrites )
	


	await ticket.send(
       embed=ticket_bug_embed  
    )

	overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.member: discord.PermissionOverwrite(view_channel=True),
            
        }

	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Opening a ticket for {ctx.member.name}.\n The ticket type is `Bug`", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	
	#Verander dit naar de ID van je channel
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)

@bot.command()
async def ticket(ctx):
	embed = discord.Embed( title="Support Tickets | AvenueMC", description="Do you need support? Feel free to open a ticket and a Staff member of our team will be with you in no time!\n\n Please ensure you choose the correct issue type, so that your ticket as quickly as possible. ", footer = "test", color=0xe74c3c)

	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Sending Embed ticket!", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	
	#Verander dit naar de ID van je channel
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)
	
	await buttons.send(
		

		
		content= None,
		embed=embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(

					style = ButtonType().Secondary,
					label = "❓ Support",
					custom_id = "Supportbutton",

				),

				Button(
					style = ButtonType().Secondary,
					label = "🛒 Payment",
					custom_id = "paymentbutton"

				),
				Button(
					style = ButtonType().Secondary,
					label = "🐛 Bug",
					custom_id = "bugbutton",
				),

			])
		]
	)

@bot.command(pass_context=True)
@has_permissions(manage_roles=True, ban_members=True, reason=None)
async def close(ctx):


			if int(ctx.channel.name[-1:]) > 0:
				log_embed = discord.Embed(title="AvenueMC Log System", description=f"Ticket has been closed\n\n ", color=0xe74c3c)
				log_embed.timestamp = datetime.datetime.utcnow()
				log_embed.set_footer(text="AvenueMC")

				await ctx.channel.send(f"{ctx.author.mention}. This ticket will be closing soon!")
				await asyncio.sleep(10)
				await ctx.channel.delete()
				#Verander dit naar de ID van je channel
				channel = bot.get_channel(966799146877079593)
				await channel.send(embed = log_embed)


	
@bot.command(aliases=["forceclose"], pass_context=True)
@has_permissions(manage_roles=True, ban_members=True)
async def fclose(ctx):

			if int(ctx.channel.name[-1:]) > 0:
				log_embed = discord.Embed(title="AvenueMC Log System", description=f"Force closing ticket. By {ctx.author.name} ", color=0xe74c3c)
				log_embed.timestamp = datetime.datetime.utcnow()
				log_embed.set_footer(text="AvenueMC")

				await ctx.channel.send(f"{ctx.author.mention}. This ticket will be closing soon!")

				await ctx.channel.delete()
				#Verander dit naar de ID van je channel
				channel = bot.get_channel(966799146877079593)
				await channel.send(embed = log_embed)

@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def playeradd(ctx, member: discord.Member):
	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Force closing ticket. By {ctx.author.name} ", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	#Verander dit naar de ID van je channel
	channel = bot.get_channel(966799146877079593)
	


	await ctx.send(f"{member} has beem added to the channel!")
	

	await ctx.channel.edit(overwrites=overwrites)
	await channel.send(embed = log_embed)
	overwrites = {
            ctx.author: discord.PermissionOverwrite(view_channel=True)}




@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def archive(ctx):
	B = discord.utils.get(ctx.guild.channels, name="Archive")  
	
	log_embed = discord.Embed(title="AvenueMC Log System", description=f"archiving ticket. By {ctx.author.name} ", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)


	await ctx.send(f"{ctx.author.mention} this channel will be archived")
	await asyncio.sleep(5)
	await ctx.channel.edit(category=B)
	await ctx.channel.edit(name=f"Support-{ctx.author.name}-Archive")	


@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def redo(ctx):

	B = discord.utils.get(ctx.guild.channels, name="Tickets")  

	log_embed = discord.Embed(title="AvenueMC Log System", description=f"Force closing ticket. By {ctx.author.name} ", color=0xe74c3c)
	log_embed.timestamp = datetime.datetime.utcnow()
	log_embed.set_footer(text="AvenueMC")
	channel = bot.get_channel(966799146877079593)
	await channel.send(embed = log_embed)

	await ctx.send(f"{ctx.author.mention} this channel will be redo")
	await asyncio.sleep(5)
	await ctx.channel.edit(category=B)
	await ctx.channel.edit(name=f"Support-{ctx.author.name}")


@bot.command()
@has_permissions(manage_roles=True, ban_members=True)
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


#errors
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to delete messages.", color=discord.Color.red)
		await ctx.send(embed=embed)

@help.error
async def help_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the help command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@redo.error
async def redo_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the redo command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@ticket.error
async def ticket_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the ticket command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@playeradd.error
async def playeradd_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the playeradd command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@archive.error
async def archive_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the archive command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@fclose.error
async def fclose_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the fclose command.", color=0xe74c3c)
		await ctx.send(embed=embed)

@close.error
async def close_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		embed = discord.Embed(title="Missing Permission", description="You dont have the permission to the close command.", color=0xe74c3c)
		await ctx.send(embed=embed)		

#Your token
bot.run()
