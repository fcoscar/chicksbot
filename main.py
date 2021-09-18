import discord
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from discord.ext import commands
from settings import *


creds = service_account.Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPE)

service = build('sheets','v4', credentials = creds)
sheet = service.spreadsheets()

bot = commands.Bot(command_prefix="!")

def write_spreadsheet(time, username, status):
    val = [[str(time),str(username),status]]
    request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Bot!A1', valueInputOption="USER_ENTERED",insertDataOption='INSERT_ROWS',body= {"values":val}).execute()


bot = commands.Bot(command_prefix="!")

@bot.command(name='on')
@commands.has_role('Employee')
async def on_function(ctx):
    write_spreadsheet(datetime.now(), ctx.author, "START")
    await ctx.send(":white_check_mark:")

@bot.command(name='off')
@commands.has_role('Employee')
async def off_function(ctx):
    write_spreadsheet(datetime.now(), ctx.author, "FINISH")
    await ctx.send(":white_check_mark:")

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandError):
        await ctx.send(":negative_squared_cross_mark:")

@bot.event
async def on_ready():
    print(f"{bot.user} Connected")

bot.run(BOT_TOKEN)