import logging
from requests import Session as s
import telebot
from threading import Event
import time
import json
import random
import string
from jio import check 

# Telegram bot token
TOKEN = "7542551291:AAERpO130moNGztUh6MrXBAfs7WLHdqEfj4"
admins = [6304864760,6490103645,6656608288,7394590844,7379318591,2121771823,6843778127,5311223486,6329875412]  # Admins Telegram ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)


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
        text = f"""<b><i>CC » <code>{cc}</code>
RESPONSE » {res}
BIN » </i></b><code>{response["bin"]}</code><b><i> - {response["type"]} - {response["level"]}
COUNTRY » {response["country_name"]} {response["country_flag"]}
BANK » {response["bank"]} {response["country_flag"]}
TIME TAKEN » {time} Seconds
BY » @WerewolfDemon</i></b>"""
        return text
    except Exception as e:
        return e

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return
    bot.send_message(message.chat.id, "👋 welcome! use /register to register and get 10 credits. use the /chk command followed by card details in the format `cc|mm|yyyy|cvv`, or send a txt file with card details. use /stop to stop the card check process.")

# /cmds command handler
@bot.message_handler(commands=["cmds","cmd"])
def send_cmds(message):
    cmds_message = (
        "📋 available commands:\n"
        "/start - welcome message\n"
        "/cmds - list all commands\n"
        "/register - register and get 10 credits\n"
        "/info - get your information\n"
        "/add - authorize a group or user\n"
        "/remove - unauthorize a group or user\n"
        "/chk - check card details\n"
        "/stop - stop the card check process\n"
        "/buy - view credit packages and pricing\n"
        "/block - block a user\n"
        "/unblock - unblock a user\n"
        "/get_credit <number> - generate credit code\n"
        "/redeem <code> - redeem a credit code\n"
        "/use <code> - redeem a credit code\n"
        "/users - get user statistics (owner only)\n"
        "/br <message> - broadcast a message to all users (owner only)\n"
    )
    bot.reply_to(message, cmds_message)

# /register command handler
@bot.message_handler(commands=['register'])
def register_user(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return
    user_id = message.from_user.id
    if user_id in user_credits:
        bot.reply_to(message, "✅ you are already registered.")
        return
    
    user_credits[user_id] = 10
    save_user_credits()

    username = message.from_user.username or "n/a"
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    user_info = f"ℹ️ new user registration:\n👤 username: @{username}\n🆔 user id: {user_id}\n📛 full name: {full_name}\n💰 credits: 10\n"
    for admin in admins:
        bot.send_message(admin, user_info)
    bot.reply_to(message, f"🎉 you have been registered and received 10 credits.\n\n{user_info}")

# /info command handler
@bot.message_handler(commands=['info'])
def user_info(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return
    user_id = message.from_user.id
    if user_id not in user_credits and user_id not in admins:
        bot.reply_to(message, "❌ you are not registered. use /register to register.")
        return

    credits = "unlimited" if user_id in admins else user_credits.get(user_id, 0)
    rank = "admin" if user_id in admins else "premium" if credits > 10 else "free"
    username = message.from_user.username or "n/a"
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    
    info_message = (
        f"ℹ️ user information:\n"
        f"👤 username: @{username}\n"
        f"🆔 user id: {user_id}\n"
        f"📛 full name: {full_name}\n"
        f"💰 credits: {credits}\n"
        f"🔰 rank: {rank}\n"
    )
    bot.reply_to(message, info_message)

# /add command handler to authorize a group or user
@bot.message_handler(commands=['add'])
def add_authorization(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
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
            bot.reply_to(message, f"✅ group {group_id} has been authorized for cc checks.")
        else:
            bot.reply_to(message, f"ℹ️ group {group_id} is already authorized.")

    else:
        if len(args) != 3:
            bot.reply_to(message, "ℹ️ usage: /add <user_id> <credits>")
            return
        user_id = int(args[1])
        credits = int(args[2])
        user_credits[user_id] = user_credits.get(user_id, 0) + credits
        save_user_credits()
        bot.reply_to(message, f"✅ user {user_id} has been authorized with {credits} credits.")
        
        username = message.from_user.username or "n/a"
        full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
        owner_info = f"ℹ️ credits added:\n👤 username: @{username}\n🆔 user id: {user_id}\n📛 full name: {full_name}\n💰 credits added: {credits}\n"

        bot.send_message(OWNER_ID, owner_info)

# /remove command handler to unauthorize a group or user
@bot.message_handler(commands=['remove'])
def remove_authorization(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "ℹ️ usage: /remove group <group_id> or /remove userid <user_id> <credits>")
        return

    if args[1] == 'group':
        group_id = int(args[2])
        if group_id in authorized_groups:
            authorized_groups.remove(group_id)
            save_authorized_groups()
            bot.reply_to(message, f"✅ group {group_id} has been unauthorized.")
        else:
            bot.reply_to(message, f"ℹ️ group {group_id} is not authorized.")

    elif args[1] == 'userid':
        user_id = int(args[2])
        credits = int(args[3])
        if user_id in user_credits:
            user_credits[user_id] = max(0, user_credits[user_id] - credits)
            save_user_credits()
            bot.reply_to(message, f"✅ user {user_id} has been deducted {credits} credits.")
        else:
            bot.reply_to(message, f"ℹ️ user {user_id} is not authorized.")

    else:
        bot.reply_to(message, "❌ invalid type. use 'group' or 'userid'.")

# /chk command handler
@bot.message_handler(commands=["chk","cc"])
def check_card(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return
    user_id = message.from_user.id
    if user_id not in admins and user_id not in user_credits and message.chat.id not in authorized_groups:
        bot.reply_to(message, "❌ you are not registered. use /register to register.")
        return

    if user_id not in admins and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "❌ you don't have enough credits to use this command.")
        return

    card_details = message.text.split()[1:]
    if not card_details:
        bot.reply_to(message, "ℹ️ please provide card details in the format `cc|mm|yyyy|cvv`.")
        return

    stop_event.clear()

    for card in card_details:
        if stop_event.is_set():
            bot.reply_to(message, "🛑 card check process stopped.")
            break

        if user_id not in admins:
            user_credits[user_id] -= 1
            save_user_credits()

        start_time = time.time()
        ko = (bot.reply_to(message, "Checking Your Card...⌛").message_id)
        try:
            response = check(card)
            bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=bin_lookup(card,response,f"{(time.time() - start_time):.2f}"),parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, f"❌ error: {e}")
            continue
        
        time.sleep(1)

# document handler
@bot.message_handler(content_types=['document'])
def handle_file(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return
    user_id = message.from_user.id
    if user_id not in user_credits and user_id not in admins:
        bot.reply_to(message, "❌ you are not registered. use /register to register.")
        return

    if user_id not in admins and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "❌ you don't have enough credits to use this command.")
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
                bot.reply_to(message, "🛑 card check process stopped.")
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
                    bot.reply_to(message, f"❌ error: {e}")
                    continue
 
                time.sleep(10)

# /stop command handler
@bot.message_handler(commands=['stop'])
def stop_process(message):
    if message.from_user.id in admins:
        stop_event.set()
        bot.reply_to(message, "🛑 card check process has been stopped.")
    else:
        bot.reply_to(message, "❌ you are not authorized to use this command.")

# /buy command handler
@bot.message_handler(commands=['buy'])
def buy_credits(message):
    buy_message = (
        "💳 credit packages:\n"
        "100 credits - $2\n"
        "500 credits - $4\n"
        "1000 credits - $8\n"
        "contact @WerewolfDemon to purchase."
    )
    bot.reply_to(message, buy_message)

# /block command handler
@bot.message_handler(commands=['block'])
def block_user(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ usage: /block <user_id>")
        return

    user_id = int(args[1])
    if user_id not in blocked_users:
        blocked_users.append(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ user {user_id} has been blocked.")
    else:
        bot.reply_to(message, f"ℹ️ user {user_id} is already blocked.")

# /unblock command handler
@bot.message_handler(commands=['unblock'])
def unblock_user(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ usage: /unblock <user_id>")
        return

    user_id = int(args[1])
    if user_id in blocked_users:
        blocked_users.remove(user_id)
        save_blocked_users()
        bot.reply_to(message, f"✅ user {user_id} has been unblocked.")
    else:
        bot.reply_to(message, f"ℹ️ user {user_id} is not blocked.")

# /get_credit command handler
@bot.message_handler(commands=['get_credit'])
def get_credit_code(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ usage: /get_credit <number_of_credits>")
        return

    credits = int(args[1])
    code = generate_random_code()
    credit_codes[code] = credits
    save_credit_codes()
    bot.reply_to(message, f"✅ credit code generated: <code>{code}</code> for {credits} credits.",parse_mode="HTML")

# /redeem and /use command handler
@bot.message_handler(commands=['redeem', 'use'])
def redeem_code(message):
    if message.from_user.id in blocked_users:
        bot.reply_to(message, "❌ you are blocked from using this bot.")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ usage: /redeem <code> or /use <code>")
        return

    code = args[1]
    if code in credit_codes:
        credits = credit_codes.pop(code)
        save_credit_codes()
        user_id = message.from_user.id
        user_credits[user_id] = user_credits.get(user_id, 0) + credits
        save_user_credits()
        bot.reply_to(message, f"🎉 you have redeemed {credits} credits.")
    else:
        bot.reply_to(message, "❌ invalid code.")

# /users command handler (owner only)
@bot.message_handler(commands=['users'])
def users_stats(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    total_users = len(user_credits)
    free_users = sum(1 for credits in user_credits.values() if credits <= 10)
    premium_users = total_users - free_users
    total_groups = len(authorized_groups)

    stats_message = (
        f"📊 user statistics:\n"
        f"👥 total users: {total_users}\n"
        f"🆓 free users: {free_users}\n"
        f"💎 premium users: {premium_users}\n"
        f"👥 total groups: {total_groups}\n"
    )
    bot.reply_to(message, stats_message)

# /br command handler (owner only)
@bot.message_handler(commands=['br'])
def broadcast_message(message):
    if message.from_user.id not in admins:
        bot.reply_to(message, "❌ you are not authorized to use this command.")
        return

    args = message.text.split(' ', 1)
    if len(args) != 2:
        bot.reply_to(message, "ℹ️ usage: /br <message>")
        return

    broadcast_msg = args[1]
    for user_id in user_credits.keys():
        try:
            bot.send_message(user_id, f"📢 broadcast message:\n\n{broadcast_msg}")
        except Exception as e:
            logging.error(f"error sending message to {user_id}: {e}")

    bot.reply_to(message, "✅ broadcast message sent to all users.")

if __name__ == "__main__":
    print("Bot Is Running Now 🎉")
    logging.basicConfig(level=logging.INFO)
    bot.infinity_polling()
    
                    
