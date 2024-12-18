import logging
from requests import Session as s
import telebot
from telebot import types
from threading import Event
import time
import json
import random
import string
from Demon import check 

# Telegram bot token
TOKEN = "7328966851:AAGOTLBDdrxfkPs7ktCZg0Kx3lCm9Af6otQ"
admins = [6656608288,6843778127,6304864760,6490103645,7394590844]  # Admins Telegram ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

my = types.InlineKeyboardButton(text="Owner",url="t.me/WereWolf_Demon")
gr = types.InlineKeyboardButton(text="𝗖𝗛𝗔𝗡𝗡𝗘𝗟",url="https://t.me/kaalCarder")
xx = types.InlineKeyboardMarkup()
xx.add(my,gr)

# Event to control the stopping of the card check process
stop_event = Event()

# Lists to store authorized group IDs, user IDs with credits, blocked users, and credit codes
authorized_groups = []
user_credits = {}
blocked_users = []
credit_codes = {}

# Load authorized groups, user credits, blocked users, and credit codes from file (if exists)
try:
    with open('authorized_groups.json', 'r') as file:
        authorized_groups = json.load(file)
except FileNotFoundError:
    authorized_groups = []

try:
    with open('user_credits.json', 'r') as file:
        user_credits = json.load(file)
except FileNotFoundError:
    user_credits = {}

try:
    with open('blocked_users.json', 'r') as file:
        blocked_users = json.load(file)
except FileNotFoundError:
    blocked_users = []

try:
    with open('credit_codes.json', 'r') as file:
        credit_codes = json.load(file)
except FileNotFoundError:
    credit_codes = {}

def save_authorized_groups():
    with open('authorized_groups.json', 'w') as file:
        json.dump(authorized_groups, file,indent=2)

def save_user_credits():
    with open('user_credits.json', 'w') as file:
        json.dump(user_credits, file,indent=2)

def save_blocked_users():
    with open('blocked_users.json', 'w') as file:
        json.dump(blocked_users, file,indent=2)

def save_credit_codes():
    with open('credit_codes.json', 'w') as file:
        json.dump(credit_codes, file,indent=2)

def generate_random_code(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
def bin_lookup(cc,res,time):
    api = f"https://bins.antipublic.cc/bins/{cc[:6]}"
    response = s().get(api).json()
    try:
        text = f"""<b><i>
𝗖𝗔𝗥𝗗 💳 » <code>{cc}</code>

𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 🧠 » {res}

𝗕𝗜𝗡 🖤 » </i></b><code>{response["bin"]}</code><b><i> - {response["type"]} - {response["level"]}

𝗚𝗔𝗧𝗘𝗪𝗔𝗬 🎫 » 𝗦𝗧𝗥𝗜𝗣𝗘 𝗖𝗛𝗔𝗥𝗚𝗘𝗗 $𝟰

𝗖𝗢𝗨𝗡𝗧𝗥𝗬 🗺️ » {response["country_name"]} {response["country_flag"]}

𝗕𝗔𝗡𝗞 🎭 » {response["bank"]} {response["country_flag"]}

𝗧𝗜𝗠𝗘 𝗧𝗔𝗞𝗘𝗡 🧠 » {time} Seconds

𝗕𝗬 🖤🫀 » @WerewolfDemonInfo</i></b>"""
        return text
    except Exception as e:
        return e

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🖕🤣")
        return
    bot.send_message(message.chat.id, "👋 𝘄𝗲𝗹𝗰𝗼𝗺𝗲! 𝘂𝘀𝗲 /register 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗮𝗻𝗱 𝗴𝗲𝘁 𝟭𝟬 𝗰𝗿𝗲𝗱𝗶𝘁𝘀. 𝘂𝘀𝗲 𝘁𝗵𝗲 /chk 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗳𝗼𝗹𝗹𝗼𝘄𝗲𝗱 𝗯𝘆 𝗰𝗮𝗿𝗱 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗳𝗼𝗿𝗺𝗮𝘁 𝗰𝗰|𝗺𝗺|𝘆𝘆𝘆𝘆|𝗰𝘃𝘃, 𝗼𝗿 𝘀𝗲𝗻𝗱 𝗮 𝘁𝘅𝘁 𝗳𝗶𝗹𝗲 𝘄𝗶𝘁𝗵 𝗰𝗮𝗿𝗱 𝗱𝗲𝘁𝗮𝗶𝗹𝘀. 𝘂𝘀𝗲 /stop 𝘁𝗼 𝘀𝘁𝗼𝗽 𝘁𝗵𝗲 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸 𝗽𝗿𝗼𝗰𝗲𝘀𝘀. /help 𝗔𝗹𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝘀𝘂𝗽𝗽𝗼𝗿𝘁.🧠 𝗮𝗻𝘆 𝗽𝗿𝗼𝗯𝗹𝗲𝗺 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗜𝗗 = @Werewolf_Demon👹🧠",reply_markup=xx)

# /cmds command handler
@bot.message_handler(commands=["cmds","cmd","Help","help"])
def send_cmds(message):
    cmds_message = (
        "📋 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
        "/start - 𝘄𝗲𝗹𝗰𝗼𝗺𝗲 𝗺𝗲𝘀𝘀𝗮𝗴𝗲\n"
        "/cmds - 𝗹𝗶𝘀𝘁 𝗮𝗹𝗹 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀\n"
        "/register - 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿 𝗮𝗻𝗱 𝗴𝗲𝘁 𝟭𝟬 𝗰𝗿𝗲𝗱𝗶𝘁𝘀\n"
        "/info - 𝗴𝗲𝘁 𝘆𝗼𝘂𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻\n"
        "/add - 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲 𝗮 𝗴𝗿𝗼𝘂𝗽 𝗼𝗿 𝘂𝘀𝗲𝗿\n"
        "/remove - 𝘂𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲 𝗮 𝗴𝗿𝗼𝘂𝗽 𝗼𝗿 𝘂𝘀𝗲𝗿\n"
        "/chk - 𝗰𝗵𝗲𝗰𝗸 𝗰𝗮𝗿𝗱 𝗱𝗲𝘁𝗮𝗶𝗹𝘀\n"
        "/stop - 𝘀𝘁𝗼𝗽 𝘁𝗵𝗲 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸 𝗽𝗿𝗼𝗰𝗲𝘀𝘀\n"
        "/buy - 𝘃𝗶𝗲𝘄 𝗰𝗿𝗲𝗱𝗶𝘁 𝗽𝗮𝗰𝗸𝗮𝗴𝗲𝘀 𝗮𝗻𝗱 𝗽𝗿𝗶𝗰𝗶𝗻𝗴\n"
        "/block  - 𝗯𝗹𝗼𝗰𝗸 𝗮 𝘂𝘀𝗲𝗿\n"
        "/unblock - 𝘂𝗻𝗯𝗹𝗼𝗰𝗸 𝗮 𝘂𝘀𝗲𝗿\n"
        "/get_credit <number> - 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗰𝗿𝗲𝗱𝗶𝘁 𝗰𝗼𝗱𝗲\n"
        "/redeem <code> - 𝗿𝗲𝗱𝗲𝗲𝗺 𝗮 𝗰𝗿𝗲𝗱𝗶𝘁 𝗰𝗼𝗱𝗲\n"
        "/use <code> - 𝗿𝗲𝗱𝗲𝗲𝗺 𝗮 𝗰𝗿𝗲𝗱𝗶𝘁 𝗰𝗼𝗱𝗲\n"
        "/users - 𝗴𝗲𝘁 𝘂𝘀𝗲𝗿 𝘀𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀 (𝗼𝘄𝗻𝗲𝗿 𝗼𝗻𝗹𝘆)\n"
        "/br <message> - 𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗮 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀 (𝗼𝘄𝗻𝗲𝗿 𝗼𝗻𝗹𝘆)\n"
    )
    bot.reply_to(message, cmds_message,reply_markup=xx)

# /register command handler
@bot.message_handler(commands=['register'])
def register_user(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🖕😁")
        return
    user_id = message.from_user.id
    if user_id in user_credits:
        bot.reply_to(message, "✅ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱.💞")
        return
    
    user_credits[user_id] = 10
    save_user_credits()

    username = message.from_user.username or "n/a"
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    user_info = f"ℹ️ new user registration:\n👤 username: @{username}\n🆔 user id: {user_id}\n📛 full name: {full_name}\n💰 credits: 10\n"
    for admin in admins:
        bot.send_message(admin, user_info)
    bot.reply_to(message, f"🎉 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝗮𝗻𝗱 𝗿𝗲𝗰𝗲𝗶𝘃𝗲𝗱 𝟭𝟬 🧠credits.\n\n{user_info}")

# /info command handler
@bot.message_handler(commands=['info'])
def user_info(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🖕")
        return
    user_id = message.from_user.id
    if user_id not in user_credits and user_id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱. 𝘂𝘀𝗲 /register 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿.")
        return

    credits = "unlimited" if user_id in admins else user_credits.get(user_id, 0)
    rank = "admin" if user_id in admins else "premium" if credits > 10 else "free"
    username = message.from_user.username or "n/a"
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    
    info_message = (
        f"ℹ️ 𝘂𝘀𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻:\n"
        f"👤 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{username}\n"
        f"🆔 𝘂𝘀𝗲𝗿 𝗶𝗱: {user_id}\n"
        f"📛 𝘂𝘀𝗲𝗿 𝗶𝗱: {full_name}\n"
        f"💰 𝗰𝗿𝗲𝗱𝗶𝘁𝘀: {credits}\n"
        f"🔰 𝗿𝗮𝗻𝗸: {rank}\n"
    )
    bot.reply_to(message, info_message)

# /add command handler to authorize a group or user
@bot.message_handler(commands=['add'])
def add_authorization(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.💞")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "ℹ️ usage: /add group <group_id> or /add <user_id> <credits>")
        return

    if args[1] == 'group':
        group_id = int(args[2])
        if group_id not in authorized_groups:
            authorized_groups.append(group_id)
            save_authorized_groups()
            bot.reply_to(message, f"✅ 𝗴𝗿𝗼𝘂𝗽 {group_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗳𝗼𝗿 𝗰𝗰 𝗰𝗵𝗲𝗰𝗸𝘀.💞🧠")
        else:
            bot.reply_to(message, f"ℹ️ 𝗴𝗿𝗼𝘂𝗽 {group_id} 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱.🧠🫀")

    else:
        if len(args) != 3:
            bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /add <user_id> <credits>")
            return
        user_id = int(args[1])
        credits = int(args[2])
        user_credits[user_id] = user_credits.get(user_id, 0) + credits
        save_user_credits()
        bot.reply_to(message, f"✅ 𝘂𝘀𝗲𝗿 {user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘄𝗶𝘁𝗵😜 {credits} 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.💞")
        
        username = message.from_user.username or "n/a"
        full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        owner_info = f"𝗶 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗱𝗱𝗲𝗱:\n👤 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{username}\n🆔 𝘂𝘀𝗲𝗿 𝗶𝗱: {user_id}\n📛 𝗳𝘂𝗹𝗹 𝗻𝗮𝗺𝗲: {full_name}\n💰 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝗮𝗱𝗱𝗲𝗱: {credits}\n"

        bot.send_message(OWNER_ID, owner_info)

# /remove command handler to unauthorize a group or user
@bot.message_handler(commands=['remove'])
def remove_authorization(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /remove group <group_id> or /remove userid <user_id> <credits>")
        return

    if args[1] == 'group':
        group_id = int(args[2])
        if group_id in authorized_groups:
            authorized_groups.remove(group_id)
            save_authorized_groups()
            bot.reply_to(message, f"✅ 𝗴𝗿𝗼𝘂𝗽 {group_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘂𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱.")
        else:
            bot.reply_to(message, f"𝗶 𝗴𝗿𝗼𝘂𝗽 {group_id} 𝗶𝘀 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱.")

    elif args[1] == 'userid':
        user_id = int(args[2])
        credits = int(args[3])
        if user_id in user_credits:
            user_credits[user_id] = max(0, user_credits[user_id] - credits)
            save_user_credits()
            bot.reply_to(message, f"✅ 𝘂𝘀𝗲𝗿 {user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗱𝗲𝗱𝘂𝗰𝘁𝗲𝗱🧠 {credits} 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.🧠")
        else:
            bot.reply_to(message, f"𝗶 𝘂𝘀𝗲𝗿 {user_id} 𝗶𝘀 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱.🧠🎭")

    else:
        bot.reply_to(message, "❌ 𝗶𝗻𝘃𝗮𝗹𝗶𝗱 𝘁𝘆𝗽𝗲. 𝘂𝘀𝗲🧠 'group' 𝗼𝗿 'userid'.")

# /chk command handler
@bot.message_handler(commands=["chk","cc"])
def check_card(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🖕😆")
        return
    user_id = message.from_user.id
    if user_id not in admins and user_id not in user_credits and message.chat.id not in authorized_groups:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱. 𝘂𝘀𝗲 💞 /register 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿.💞🖤")
        return

    if user_id not in admins and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝗲𝗻𝗼𝘂𝗴𝗵 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠🫀")
        return

    card_details = message.text.split()[1:]
    if not card_details:
        bot.reply_to(message, "𝗶 𝗽𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗰𝗮𝗿𝗱 𝗱𝗲𝘁𝗮𝗶𝗹𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗳𝗼𝗿𝗺𝗮𝘁🧠 `cc|mm|yyyy|cvv`.")
        return

    stop_event.clear()

    for card in card_details:
        if stop_event.is_set():
            bot.reply_to(message, "🛑 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘀𝘁𝗼𝗽𝗽𝗲𝗱.🧠😁")
            break

        if user_id not in admins:
            user_credits[user_id] -= 1
            save_user_credits()

        start_time = time.time()
        ko = (bot.reply_to(message, "𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗬𝗼𝘂𝗿 𝗖𝗮𝗿𝗱...🧠⌛").message_id)
        try:
            response = check(card)
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=bin_lookup(card,response,f"{(time.time() - start_time):.2f}"),parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, f"❌ 𝗲𝗿𝗿𝗼𝗿: {e}")
            continue
        
        time.sleep(1)

# document handler
@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🧠")
        return
    user_id = message.from_user.id
    if user_id not in user_credits and user_id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱. 𝘂𝘀𝗲 /register 𝘁𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿.🫀🧠")
        return

    if user_id not in admins and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝗲𝗻𝗼𝘂𝗴𝗵 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.💞🧠")
        return

    if message.document.mime_type == 'text/plain':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open('lista.txt', 'wb') as f:
            f.write(downloaded_file)
        
        with open('lista.txt', 'r') as f:
            lista_values = f.readlines()
        
        stop_event.clear()

        for lista in lista_values:
            if stop_event.is_set():
                bot.reply_to(message, "🛑 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘀𝘁𝗼𝗽𝗽𝗲𝗱.🫀🧠")
                break

            if user_id not in admins:
                user_credits[user_id] -= 1
                save_user_credits()

            start_time = time.time()
            lista = lista.strip()
            if lista:
                try:
                    response = check(lista)
                    bot.reply_to(message,bin_lookup(lista,response,f"{(time.time() - start_time):.2f}"),parse_mode="HTML")
                except Exception as e:
                    bot.reply_to(message, f"❌ 𝗲𝗿𝗿𝗼𝗿: {e}")
                    continue
 
                time.sleep(10)

# /stop command handler
@bot.message_handler(commands=['stop'])
def stop_process(message):
    if message.from_user.id in admins:
        stop_event.set()
        bot.reply_to(message, "🛑 𝗰𝗮𝗿𝗱 𝗰𝗵𝗲𝗰𝗸 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝘁𝗼𝗽𝗽𝗲𝗱.🫀🧠")
    else:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🫀💞")

# /buy command handler
@bot.message_handler(commands=['buy'])
def buy_credits(message):
    buy_message = (
        "💳 𝗰𝗿𝗲𝗱𝗶𝘁 𝗽𝗮𝗰𝗸𝗮𝗴𝗲𝘀:\n"
        "𝟭𝟬𝟬 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - $𝟮 💸\n"
        "𝟱𝟬𝟬 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - $𝟰 💵\n"
        "𝟭𝟬𝟬𝟬 𝗰𝗿𝗲𝗱𝗶𝘁𝘀 - $𝟴 💰\n"
        "𝗰𝗼𝗻𝘁𝗮𝗰𝘁 @WerewolfDemon 𝘁𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲."
    )
    bot.reply_to(message, buy_message)

# /block command handler
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠🫀")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /block <user_id>")
        return

    user_id = int(args[1])
    if user_id not in blocked_users:
        blocked_users.append(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ 𝘂𝘀𝗲𝗿  {user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗯𝗹𝗼𝗰𝗸𝗲𝗱.🧠")
    else:
        bot.reply_to(message, f"𝗶  𝘂𝘀𝗲𝗿 {user_id} 𝗶𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗯𝗹𝗼𝗰𝗸𝗲𝗱.")

# /unblock command handler
@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠🫀")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /unblock <user_id>")
        return

    user_id = int(args[1])
    if user_id in blocked_users:
        blocked_users.remove(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ 𝘂𝘀𝗲𝗿 {user_id} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗯𝗹𝗼𝗰𝗸𝗲𝗱.🧠")
    else:
        bot.reply_to(message, f"𝗶  𝘂𝘀𝗲𝗿 {user_id} 𝗶𝘀 𝗻𝗼𝘁 𝗯𝗹𝗼𝗰𝗸𝗲𝗱.🖤🧠")

# /get_credit command handler
@bot.message_handler(commands=['get_credit'])
def get_credit_code(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🫀🧠")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /get_credit <number_of_credits>")
        return

    credits = int(args[1])
    code = generate_random_code()
    credit_codes[code] = credits
    save_credit_codes()
    bot.reply_to(message, f"✅ 𝗰𝗿𝗲𝗱𝗶𝘁 𝗰𝗼𝗱𝗲 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱: <code>{code}</code> for {credits} 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.🫀",parse_mode="HTML")

# /redeem and /use command handler
@bot.message_handler(commands=['redeem', 'use'])
def redeem_code(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗯𝗹𝗼𝗰𝗸𝗲𝗱 𝗳𝗿𝗼𝗺 𝘂𝘀𝗶𝗻𝗴 𝘁𝗵𝗶𝘀 𝗯𝗼𝘁.🖤🧠")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /redeem <code> or /use <code>")
        return

    code = args[1]
    if code in credit_codes:
        credits = credit_codes.pop(code)
        save_credit_codes()
        user_id = message.from_user.id
        user_credits[user_id] = user_credits.get(user_id, 0) + credits
        save_user_credits()
        bot.reply_to(message, f"🎉 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗿𝗲𝗱𝗲𝗲𝗺𝗲𝗱 {credits} 𝗰𝗿𝗲𝗱𝗶𝘁𝘀.🧠🫀")
    else:
        bot.reply_to(message, "❌ 𝗶𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗼𝗱𝗲.🖕")

# /users command handler (owner only)
@bot.message_handler(commands=['users'])
def users_stats(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠🫀")
        return

    total_users = len(user_credits)
    free_users = sum(1 for credits in user_credits.values() if credits <= 10)
    premium_users = total_users - free_users
    total_groups = len(authorized_groups)

    stats_message = (
        f"📊 𝘂𝘀𝗲𝗿 𝘀𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗰𝘀:\n"
        f"👥 𝘁𝗼𝘁𝗮𝗹 𝘂𝘀𝗲𝗿𝘀: {total_users}\n"
        f"🆓 𝗳𝗿𝗲𝗲 𝘂𝘀𝗲𝗿𝘀:  {free_users}\n"
        f"💎 𝗽𝗿𝗲𝗺𝗶𝘂𝗺 𝘂𝘀𝗲𝗿𝘀: {premium_users}\n"
        f"👥 𝘁𝗼𝘁𝗮𝗹 𝗴𝗿𝗼𝘂𝗽𝘀: {total_groups}\n"
    )
    bot.reply_to(message, stats_message)

# /br command handler (owner only)
@bot.message_handler(commands=['br'])
def broadcast_message(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ 𝘆𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱.🧠💞")
        return

    args = message.text.split(' ', 1)
    if len(args) != 2:
        bot.reply_to(message, "𝗶  𝘂𝘀𝗮𝗴𝗲: /br <message>")
        return

    broadcast_msg = args[1]
    for user_id in user_credits.keys():
        try:
            bot.send_message(user_id, f"📢 𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲:💞🫀\n\n{broadcast_msg}")
        except Exception as e:
            logging.error(f"𝗲𝗿𝗿𝗼𝗿 𝘀𝗲𝗻𝗱𝗶𝗻𝗴 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼🧠🎭 {user_id}: {e}")

    bot.reply_to(message, "✅ 𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘀𝗲𝗻𝘁 𝘁𝗼 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀.💞🫀")

if __name__ == "__main__":
    print("𝗕𝗼𝘁 𝗜𝘀 𝗥𝘂𝗻𝗻𝗶𝗻𝗴 𝗡𝗼𝗪 🎉")
    logging.basicConfig(level=logging.INFO)
    bot.infinity_polling()
    
                    
