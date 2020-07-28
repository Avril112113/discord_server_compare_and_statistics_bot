from typing import List

import discord
import shlex
import traceback
import datetime


with open("bot_token.txt") as f:
	bot_token = f.read()


client = discord.Client()
prefix = "stat_bot"


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.Message):
	# make sure it's not our own message
	if message.author == client.user:
		return

	# Check if it's a command for this bot
	if message.content[:len(prefix)] == prefix:
		# Split up the args
		args = shlex.split(message.content[len(prefix) + 1:])
		if len(args) < 1:
			await message.channel.send("Command Error: no command supplied")
			return
		# take the first arg as the command
		cmd = args.pop(0)
		try:
			return await handle_command(cmd, args, message)
		except:
			await message.channel.send("Bot had an error :(")
			traceback.print_exc()


async def handle_command(cmd: str, args: List[str], message: discord.Message):
	if cmd == "ping":
		await message.channel.send("Playing Ping Pong?")
	elif cmd == "compare_server":
		if len(args) < 1:
			await message.channel.send("Command Error: other server id was not supplied")
			return
		guild_id = int(args[0])

		guild_a_tmp = [guild for guild in client.guilds if guild.id == guild_id]
		if len(guild_a_tmp) <= 0:
			await message.channel.send("Command Error: This command requires the bot to be in the other server")
			return
		guild_a: discord.Guild = guild_a_tmp[0]
		if len(args) >= 2:
			guild_b_tmp = [guild for guild in client.guilds if guild.id == guild_id]
			if len(guild_b_tmp) <= 0:
				await message.channel.send("Command Error: This command requires the bot to be in both servers")
				return
			guild_b = guild_b_tmp[0]
		elif message.channel.guild is not None:
			guild_b: discord.Guild = message.channel.guild
		else:
			await message.channel.send("Command Error: This command requires 2 server ids to be provided (for DM command)")
			return

		if len(guild_a.members) < len(guild_b.members):
			tmp = guild_a
			guild_a = guild_b
			guild_b = tmp

		guild_a_members = guild_a.members
		guild_b_members = guild_b.members

		# get the amount of users that are in both guilds
		members_in_both = sum([1 for user in guild_a_members if user in guild_b_members])
		members_more = len(guild_a_members) - len(guild_b_members)
		stats = [
			f"{guild_a} has {len(guild_a_members)} members and {guild_b} has {len(guild_b_members)} members",
			f"{guild_a} has {members_more} ({members_more / len(guild_a_members) * 100}%) more members than {guild_b}",
			f"Members in both servers: {members_in_both} ({members_in_both / len(guild_a_members) * 100}%)",
		]
		await message.channel.send("\n".join(stats))
	else:
		await message.channel.send("Command Error: invalid command")


client.run(bot_token)
