import discord
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from discord.ext import commands
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_FILE = 'spreedshit-python-b5241b06efee.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPE)
SPREADSHEET_ID = "1Z5BjJ-Ec6idDmDdiOwwfnWgouOo79HrYpKeSKkNvpx0"


service = build('sheets','v4', credentials = creds)
sheet = service.spreadsheets()

client = discord.Client()
bot = commands.Bot(command_prefix="!")

def check_role(message):
    employee = False
    for i in range(len(message.author.roles)):
        if str(message.author.roles[i]) == "Employee":
            employee = True
    return employee

def write_spreadsheet(time, username, status):
    val = [[str(time),str(username),status]]
    request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Bot!A1', valueInputOption="USER_ENTERED",insertDataOption='INSERT_ROWS',body= {"values":val}).execute()


@client.event
async def on_ready():
    print(f"logg in {client.user}")

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content=="!on" and check_role(message):
        try:
            write_spreadsheet(datetime.now(), message.author, "START")
        except:
            await message.channel.send(":negative_squared_cross_mark:")
        else:
            await message.channel.send(":white_check_mark:")
    elif message.content=="!off" and check_role(message):
        try:
            write_spreadsheet(datetime.now(), message.author, "FINISH")
        except:
            await message.channel.send(":negative_squared_cross_mark:")
        else:
            await message.channel.send(":white_check_mark:")
    elif message.content.startswith("!"):
        await message.channel.send(":negative_squared_cross_mark:")

client.run("ODg4MTczMzEzMTQ5NTAxNDYw.YUO12w.atIQEp2R6jGg217N52LkTC8s-GU")