import json
import scraper
# import steam_sale
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from config import invocation
import pandas
from datetime import datetime
import asyncio
bot = commands.Bot(command_prefix=invocation)

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")


# async def update_sales(ctx):
#     message_text = ""
#     ctx.channel = bot.get_channel(729799766153887744)
#     async for message in ctx.channel.history(limit=200):
#         if not message.pinned:
#             await message.delete()
#         elif message.id == 729809509979127818:
#             sales_board_message = message
#     async with ctx.channel.typing():
#         # await ctx.send("[Steam Sales Go Here]")
#         await sales_board_message.edit(content="Fetching data...one moment")
#         sale_data = await steam_sale.fetch_sale_data()
#         i = 1
#         for key in sale_data.keys():
#             if i < 16:
#                 message_text = f'{message_text}{key} >> \
# {sale_data[key]["Price"]}\
# ({sale_data[key]["Discount"]} off): \
# {sale_data[key]["Steam URL"]}\n\n'
#             else:
#                 break
#             i += 1
#         message_text = f"{message_text}:star:Last Updated: *{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Central*:star:"
#         await sales_board_message.edit(content=message_text)


async def update_leaderboard(ctx):
    url_list = []
    ctx.channel = bot.get_channel(729482860292997180)
    message_text = ""
    async for message in ctx.channel.history(limit=200):
        url_list.append(message.clean_content)
    ctx.channel = bot.get_channel(729094984069939250)
    async for message in ctx.channel.history(limit=200):
        if not message.pinned:
            await message.delete()
        elif message.id == 729527525696471130:
            leaderboard_message = message
    async with ctx.channel.typing():
        await leaderboard_message.edit(content="Fetching data...one moment.")
        leaderboard_json = scraper.fetch_leaderboard(url_list)
        leaderboard_dict = json.loads(leaderboard_json)
        message_text = f"{message_text}\nLast Updated: *{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Central*"
        for key in leaderboard_dict.keys():
            message_text = f'{message_text}\n**{leaderboard_dict[key]["Player Name"]}**: {key}'
        await leaderboard_message.edit(content=message_text)


async def fetch_context_from_channel_with_pin(channel_id):
    channel = bot.get_channel(channel_id)
    async for message in channel.history(limit=200):
        if message.pinned:
            ctx = await bot.get_context(message)
            return ctx


async def hourly_update():
    await bot.wait_until_ready()
    while True:
        ctx = await fetch_context_from_channel_with_pin(729094984069939250)
        await update_leaderboard(ctx)
        # ctx = await fetch_context_from_channel_with_pin(729799766153887744)
        # await update_sales(ctx)
        await asyncio.sleep(3600)


@bot.event
async def on_ready():
    print("Connecting to Guilds...")
    guildsDisplay = {
        "Guild Name": [],
        "Total Memebers": [],
        "Members Online": [],
    }

    for guild in bot.guilds:
        membersOnline = 0
        guildsDisplay["Guild Name"].append(guild.name)
        guildsDisplay["Total Memebers"].append(len(guild.members))
        for member in guild.members:
            if member.status.name == "online":
                membersOnline += 1
        guildsDisplay["Members Online"].append(membersOnline)

    df = pandas.DataFrame(guildsDisplay)

    print(df.to_string(index=False))


@bot.command(help="Use this command in #score-saber-leaderboard to refresh the leaderboard.", brief="Refreshes the leaderboard")
async def leaderboard(ctx):
    await update_leaderboard(ctx)


# @bot.command(help="Use this command in #steam-vr-sales to refresh the salesboard.", brief="Refreshes the salesboard")
# async def sales(ctx):
#     await update_sales(ctx)

# 729799766153887744

bot.loop.create_task(hourly_update())
bot.run(discord_token)
