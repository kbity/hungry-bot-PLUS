import discord
bot = discord.Client(intents=discord.Intents(message_content=True, messages=True, guilds=True))
with open("nouns.txt", 'r') as file:
    words = {line.strip() for line in file}
file_path = "channels.txt"
with open(file_path, 'r') as file:
    channels = [i.strip() for i in file]
noun_memory = {}

def refrshchannels():
    with open(file_path, 'r') as file:
        channels = [i.strip() for i in file]
    return channels

def savefile(lines):
    with open(file_path, "w") as file:
        file.writelines(lines)

def openfile():
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

@bot.event
async def on_message(message):
    global channels
    channelide = str(message.channel.id)
    noun_memory.setdefault(channelide, [])
    if message.author.bot:
        return

    if message.content == "hb+add":
        if not message.channel.permissions_for(message.author).manage_channels and not message.guild is None:
            await message.reply(f"yeah ok liberal")
            return
        channelse = openfile()
        channelse.append(f"{channelide}\n")
        await message.reply(f"channel added to hungry bot+")
        savefile(channelse)
        channels = refrshchannels()
        return

    if message.content == "hb+rem":
        if not message.channel.permissions_for(message.author).manage_channels and not message.guild is None:
            await message.reply(f"yeah ok liberal")
            return
        channelse = openfile()
        channelse = [line.replace(f"{channelide}\n", "") for line in channelse]
        await message.reply(f"channel removed from hungry bot+")
        savefile(channelse)
        channels = refrshchannels()
        return

    nouns_found = []
    if not channelide in channels:
        return
    for word in message.content.lower().replace("\n", " ").split(" "):
        if word in words:
            nouns_found.append(word)
    for noun in nouns_found:
        use_times = 0
        for things in noun_memory[channelide]:
            if noun in things:
                use_times += 1
        if use_times > 2:
            await message.channel.send(f"eats the {noun}")
            noun_memory[channelide] = []
            return
    noun_memory[channelide].append(nouns_found)
    noun_memory[channelide] = noun_memory[channelide][-10:]
bot.run("put token here")
