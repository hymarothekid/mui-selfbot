import discord
import requests
import datetime

client = discord.Client()

allowed_user_id = SEU ID

boost_emojis = {
    "guild_booster_lvl1": "<:boost1month:1079151643336136199>",
    "guild_booster_lvl2": "<:boost2month:1079151645054734478>",
    "guild_booster_lvl3": "<:boost3month:1079151643724601859>",
    "guild_booster_lvl4": "<:boost4month:1079151644231870464>",
    "guild_booster_lvl5": "<:boost5month:1079151643110574594>",
    "guild_booster_lvl6": "<:boost6month:1079151643699321859>",
    "guild_booster_lvl7": "<:boost7month:1079151644469242884>",
    "guild_booster_lvl8": "<:boost8month:1079151644103471610>",
    "guild_booster_lvl9": "<:boost9month:1079151641575589889>",
}

boost_names = [
    "Nível 1",
    "Nível 2",
    "Nível 3",
    "Nível 4",
    "Nível 5",
    "Nível 6",
    "Nível 7",
    "Nível 8",
    "Nível 9"
]

bot_replied = False

def get_next_boost_info(user_id):
    url = f'https://betterapi.hostza.me/user/{user_id}'
    response = requests.get(url)
    response.raise_for_status()
    user_data = response.json()
    
    next_boost_info = user_data.get('next_boost', None)
    if next_boost_info:
        next_boost_level = next_boost_info.get('level', None)
        next_boost_date = next_boost_info.get('date', None)
        
        if next_boost_level and next_boost_date:
            next_boost_date_formatted = datetime.datetime.fromisoformat(next_boost_date[:-1]).strftime('%d-%m-%Y %H:%M:%S')
            next_boost_timestamp = int(datetime.datetime.fromisoformat(next_boost_date[:-1]).timestamp())
            return next_boost_level, next_boost_timestamp
    
    return None, None

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}#{client.user.discriminator}')

@client.event
async def on_message(message):
    global bot_replied
    if message.author == client.user:
        bot_replied = False
    if message.content.startswith('mui') and not bot_replied and message.author.id == allowed_user_id:
        next_boost_level, next_boost_timestamp = get_next_boost_info(message.author.id)
        if next_boost_level:
            boost_emoji = boost_emojis.get(next_boost_level, '')
            boost_name = boost_names[int(next_boost_level[-1]) - 1]
            next_boost_date = datetime.datetime.fromisoformat(next_boost_timestamp[:-1]).strftime('%d-%m-%Y %H:%M:%S')
            response = f'{boost_emoji} | **Seu próximo nível de boost é {boost_name} em:** {next_boost_date}'
        else:
            response = 'Você não possui um próximo nível de boost.'
        await message.channel.send(response)
        bot_replied = True

client.run('your token', bot=False)
