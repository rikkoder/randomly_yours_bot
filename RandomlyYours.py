from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import re
import requests
    
TOKEN = "1865226416:AAGFgw2c6-cLULNxhi8IZRN-EOHjxfQJWFQ"
superHeroToken = "871978677050085"
kittyApi = "https://api.thecatapi.com/v1/images/search?limit=1"
sfwWaifuApi = "https://api.waifu.pics/sfw/waifu"
pokeApi = "https://pokeapi.co/api/v2/pokemon/"


def get_image(url):
    allowed_ext = ['jpg', 'jpeg', 'png']
    file_ext = re.search("([^.]*)$", url).group(1).lower()

    return True if file_ext in allowed_ext else False


def get_doggo_pic_url():
    contents = requests.get("https://random.dog/woof.json").json()
    img_url = contents['url']
    
    while not get_image(img_url):
        img_url = get_doggo_pic_url()

    return img_url


def get_kitty_pic_url():
    contents = requests.get(kittyApi).json()[0]
    img_url = contents['url']

    while not get_image(img_url):
        img_url = get_kitty_pic_url()

    return img_url


def get_sfw_waifu_url():
    contents = requests.get(sfwWaifuApi).json()
    img_url = contents['url']

    while not get_image(img_url):
        img_url = get_sfw_waifu_url()

    return img_url


def get_pokemon(name=None):
    data = {}
    stat = {}

    if name:
        result = requests.get(f"{pokeApi}{name}")
        if result:
            data = result.json()
        else:
            return False #when searched with name and not found, handled by super func

    else:
        id = random.randint(1, 898)
        data = requests.get(f"{pokeApi}{id}").json()
    

    if data:
        print('success')
        img_url = data['sprites']['other']['official-artwork']['front_default']
        name = data['name']
        stat = data['stats']
        print(img_url, name)
    else:
        print("error")
        error() #when other error occured
    
    return (img_url, name, stat)


def get_super(name=None):
    data = {}
    power_stat = {}

    if name:
        result = requests.get(f"https://superheroapi.com/api/{superHeroToken}/search/{name}").json()
        if result['response']=="success":
            matches = list(filter(lambda obj: obj['name'].lower()==name.lower(), result['results']))
            print(matches)
            data = random.choice(matches)
            data['response'] = "success"
        else:
            data['response'] = result['response']
            data['error'] = result['error']

    else:
        id = random.randint(1, 731)
        data = requests.get(f"https://superheroapi.com/api/{superHeroToken}/{id}").json()
    

    if data['response'] == "success":
        print('success')
        img_url = data['image']['url']
        name = data['name']
        power_stat = data['powerstats']
        print(img_url, name)
    else:
        print(data["error"])
        if name:
            return False #when searched with name and not found, handled by super func
        error() #when other error occured
    
    return (img_url, name, power_stat)


def help_start(update, context):
    update.message.reply_text("there's not much about this command to know, you can use it know whether i am alive or not :)")


def help_help(update, context):
    update.message.reply_text("Hmmm, i saw what you did there, really brilliant.")


def help_greet(update, context):
    update.message.reply_text("Just casual greeting, nothing that you can't understand (: asuming you are social enough :)")


def help_roll(update, context):
    update.message.reply_text("Have you never seen a die?\nA normal die has 6 faces with numbers on it (1, 2, 3, 4, 5, 6). Rolling it gives a random number which i , randomly_yours, give to you :)")


def help_toss(update, context):
    update.message.reply_text("Coins are like DC, both has two-face :D\ntoss command helps you simulate a coin toss and results in either Head or Tail")


def help_pick(update, context):
    update.message.reply_text("A deck of Playing Cards contains 52 cards, by this command i will randomly pick one for you :)")


def help_play(update, context):
    update.message.reply_text("A variation of famous rock paper scissors game.\nJust place one of the options (rock, paper, scissors, lizard, spock) after play command, e.g: /play rock\n\n(if you are unaware of rules, just type /play rules)")


def help_doggo(update, context):
    update.message.reply_text("Dogs are said to be humans loyal friend.. (is it humans or humen ? o_O) anyway they are cute lethal animals so why not look at some random pics of them, exactly what this command does.\nOn your command i provide you your doggo :)")


def help_kitty(update, context):
    update.message.reply_text("As once a woman said to a man `soft kitty, warm kitty little ball of fur, happy kitty sleepy kitty purr purr purrrr`\n\nIf you like cats (or don't) i will provide a random kitty pic if you command me to :)")


def help_waifu(update, context):
    update.message.reply_text("If you don't know what it means, then you probably shouldn't use it.\nThis command is basically for some special species like geek, weeb, reddit users, etc who need UwU kinda feeling, kinda sad tho.. isn't it ? Nah just kidding enjoi (PS: not a typo)")


def help_pokedex(update, context):
    update.message.reply_text("I am not personally a big fan of creatures living in small balls, but i can give you every pokemon out there :)\n\nBy default you get a random pokemon with some stats but if you want a specific pokemon type it's name after command, e.g. /pokedex pokemon\n\n(ya i can't remember any other name at moment, no wait there's one named raichu, i wonder why their names are similar, i really do)")


def help_super(update, context):
    update.message.reply_text("This command gives you a random super hero/villain (ya like you could've thought of better command name for this purpose :|)\n\nIf you want any specific character just type it's name after command, e.g. /super batman.\nIf character's name has more than one words then use ', e.g. /super 'Mr Incredible'\n\n(note: this command can provide you hundreds of characters with stat but not all, here's the list of [characters](https://superheroapi.com/ids.html) available)", parse_mode = 'Markdown')


def help_callme(update, context):
    update.message.reply_text("Using this command you can tell me what you like to be called, i will then greet you using that nick name then :)\n\nIf you want a nick name of more than one word then remember to use ', e.g. /callme 'nick name'")


def help_clearnick(update, context):
    update.message.reply_text("If you don't like your nick name and wanna remove it, you can simply run this command and then wooosh your nick name will be cleared :)")


def main():
    updater = Updater(TOKEN) #, use_context = True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("greet", greet))
    dispatcher.add_handler(CommandHandler("roll", roll))
    dispatcher.add_handler(CommandHandler("toss", toss))
    dispatcher.add_handler(CommandHandler("pick", pick))
    dispatcher.add_handler(CommandHandler("play", play))
    dispatcher.add_handler(CommandHandler("doggo", doggo))
    dispatcher.add_handler(CommandHandler("kitty", kitty))
    dispatcher.add_handler(CommandHandler("waifu", waifu))
    dispatcher.add_handler(CommandHandler("pokedex", pokedex))
    dispatcher.add_handler(CommandHandler("super", super))
    dispatcher.add_handler(CommandHandler("callme", callme))
    dispatcher.add_handler(CommandHandler("clearnick", clearnick))

    dispatcher.add_handler(MessageHandler(Filters.text, text))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text("starting... bhroom bhroom...")


def help(update, context):
    commands = ['start', 'help', 'greet', 'roll', 'toss', 'pick','play', 'doggo', 'kitty', 'waifu', 'pokedex', 'super', 'callme', 'clearnick']

    if len(context.args)>0 and context.args[0].lower() in commands:
        command = context.args[0].lower()
        if command == 'start':
            help_start(update, context)

        elif command == 'help':
            help_help(update, context)

        elif command == 'greet':
            help_greet(update, context)

        elif command == 'roll':
            help_roll(update, context)

        elif command == 'toss':
            help_toss(update, context)

        elif command == 'pick':
            help_pick(update, context)

        elif command == 'play':
            help_play(update, context)

        elif command == 'doggo':
            help_doggo(update, context)

        elif command == 'kitty':
            help_kitty(update, context)

        elif command == 'waifu':
            help_waifu(update, context)

        elif command == 'pokedex':
            help_pokedex(update, context)

        elif command == 'super':
            help_super(update, context)

        elif command == 'callme':
            help_callme(update, context)

        elif command == 'clearnick':
            help_clearnick(update, context)
            

    else:
        update.message.reply_text("no help for you :)")
        context.bot.send_message(chat_id = update.message.chat_id, text = "nah just kidding ;)\n\nI basically give random results, like result of coin toss. But i can do more, i can give you a cute dog's pic (: don't worry if you are a cat person i give those too, well not cats but pics of them :)\nYou can probably see a menu button or command button (if you have eye(s)) by clicking it(button, not your eye) you can see all the commands with descriptions.\n\nBut if you still face trouble with any command, just type /help <command> for more info on that command, e.g. /help play\n\n(: hope you enjoy chatting :)")


def greet(update, context):
    name = ''
    if 'nick_name' in context.user_data.keys():
        name = context.user_data['nick_name']
    else:
        name = update.message.from_user.first_name
        
    update.message.reply_text(f"Hello there {name}! How you doing ?")


def roll(update, context):
    update.message.reply_text(random.randint(1,6))


def toss(update, context):
    update.message.reply_text(["Head", "Tail"][1 if random.random()>0.5 else 0])


def pick(update, context):
    suits = ['heart', 'spades', 'diamond', 'club']
    ranks = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

    update.message.reply_text(f"{random.choice(ranks)} of {random.choice(suits)}")


def play(update, context):
    gestures = {'rock':{'scissors':'crushes', 'lizard':'crushes'},
            'paper':{'rock':'covers', 'spock':'disproves'},
            'scissors':{'paper':'cuts', 'lizard':'decapitates'},
            'lizard':{'paper':'eats', 'spock':'poisons'},
            'spock':{'rock':'vaporizes', 'scissors':'smashes'}}
    print('inside play')

    def rules():
        print('inside rules', gestures)
#         rule = ''
#         temp = {'rock':0, 'paper':0, 'scissors':0, 'lizard':0, 'spock': 0}
#         curr = 'rock'
#         while 0 in temp.values():
#             print('inside while')
#             print(gestures[curr][temp[curr]].keys()[0])
#             target = list(gestures[curr][temp[curr]].keys())[0]
#             action = gestures[curr][temp[curr]][target]
#             rule+=f"{curr} {action} {target}\n"
#             temp[curr]+=1
#             curr = target
#             print(curr, action, target)
        
        rule = "Scissors cuts Paper\nPaper covers Rock\nRock crushes Lizard\nLizard poisons Spock\nSpock smashes Scissors\nScissors decapitates Lizard\nLizard eats Paper\nPaper disproves Spock\nSpock vaporizes Rock\n(and as it always has) Rock crushes Scissors"

        update.message.reply_text(f"Rules: \n\n{rule}")
        context.bot.send_photo(chat_id = update.message.chat_id, photo = "https://en.wikipedia.org/wiki/File:Rock_paper_scissors_lizard_spock.png")#, caption = "(img_src: wikipedia)")
#         update.message.reply_photo(photo = "https://en.wikipedia.org/wiki/File:Rock_paper_scissors_lizard_spock.png")#, caption = "(img_src: wikipedia)")

    print('after rules')

    if len(context.args)>0 and context.args[0].lower()=='rules':
        rules()
        return None

    elif len(context.args)==0 or context.args[0].lower() not in gestures.keys():
        print('inside elif')
        help_play(update, context)
        return None
    
    else:
        players_gesture = context.args[0].lower()
        bots_gesture = random.choice(list(gestures.keys()))

        tie_chat = ["looks like we have a lot in common ;)", "would you just stop copying me :/", "you copy cat, no no you copy donkey :D", "o_O", "what are the odds ?\n\nno seriously calculate it", "awww, made for each other", "well that's a tie", "wanna do a tie breaker ?"]

        bot_win_chat = ["haha, i won", "(: you lost :)", "accept it, you can't beat me :D", "(: you truely are worthless :)", "thank you, thank you :)\nno more autographs please", "i've been winning befor your birth you little fella", "no hope for you"]

        bot_lose_chat = ["ya you won", "whatever", "that was just luck :|", "i challenge you for rematch ~_~", "you know i let you win , right?", "not again :')", "i am dissapointed in myself :')\ni mean, how can i lose to someone like you"]

        update.message.reply_text(bots_gesture)

        if players_gesture == bots_gesture:
            context.bot.send_message(chat_id = update.message.chat_id, text = random.choice(tie_chat))

        elif players_gesture in gestures[bots_gesture].keys():
            context.bot.send_message(chat_id = update.message.chat_id, text = random.choice(bot_win_chat))

        else:
            context.bot.send_message(chat_id = update.message.chat_id, text = random.choice(bot_lose_chat))


def doggo(update, context):
    pic_url = get_doggo_pic_url()
    print(pic_url)
#     context.bot.send_photo(chat_id = update.message.chat_id, photo = pic_url, caption = "your doggo")
    update.message.reply_photo(photo = pic_url, caption = "your doggo")


def kitty(update, context):
    print('inside kitty')
    pic_url = get_kitty_pic_url()
    print('got kitty', pic_url)
#     context.bot.send_photo(chat_id = update.message.chat_id, photo = pic_url, caption = "your kitty")
    update.message.reply_photo(photo = pic_url, caption = "your kitty")


def waifu(update, context):
    print(f"\n{update.message.from_user.first_name} requested waifu\n")
    pic_url = get_sfw_waifu_url()
#     context.bot.send_photo(chat_id = update.message.chat_id, photo = pic_url, caption = "your waifu")
    update.message.reply_photo(photo = pic_url, caption = "your waifu")


def pokedex(update, context):
    print('inside pokedex')
    found = ()
    name = ''

    if len(context.args)>0:
        name = context.args[0].lower()

    found = get_pokemon(name)

    if found:
        print('found')
        pic_url, name, stat = found
        stat_str = ''
#         print(stat)
        for s in stat:
            print(s)
            stat_str += f"{s['stat']['name']}: {s['base_stat']}\n"
        
        caption = name+'\n\n'+stat_str
        print(caption)
#         context.bot.send_photo(chat_id = update.message.chat_id, photo = pic_url, caption = caption)
        update.message.reply_photo(photo = pic_url, caption = caption)

    else:
        update.message.reply_text(f"): {name} not found :(")


def super(update, context):
    found = ()
    name = ''

    if len(context.args)==1:
        name = context.args[0]

    elif len(context.args)>1:
        text = " ".join(context.args).split("'")
        if len(text)>1:
            name = text[1]
        else:
            update.message.reply_text("use '")
            return None

    found = get_super(name)

    if found:
        pic_url, name, power_stat = found
        power_stat_str = ''
        for key in power_stat:
            power_stat_str += key+': '+power_stat[key]+'\n'
        
        caption = name+'\n\n'+power_stat_str
#         context.bot.send_photo(chat_id = update.message.chat_id, photo = pic_url, caption = caption)
        update.message.reply_photo(photo = pic_url, caption = caption)

    else:
        update.message.reply_text(f"): {name} not found :(")


def callme(update, context):
    if len(context.args)==0:
        update.message.reply_text("call you what?")

    elif len(context.args)==1:
        context.user_data['nick_name'] = context.args[0]
        update.message.reply_text("(: okie dokie :)")

    else:
        context.user_data['nick_name'] = " ".join(context.args).split("'")[1]
        update.message.reply_text("(: okie dokie :)")


def clearnick(update, context):
    if 'nick_name' in context.user_data.keys():
        del context.user_data['nick_name']
        update.message.reply_text("(: cleared :)")

    else:
        update.message.reply_text("(: already clear :)")


def text(update, context):
    text_recieved = update.message.text
    print(f"\n<<--- {text_recieved} --->> ~{update.message.from_user.first_name}\n")
    if(text_recieved[0]=='.' or text_recieved[0]=='/'):
        return None
#     update.message.reply_text(f"`{text_recieved}` to you too :)")


def error(update, context):
    update.message.reply_text("oops, error !!")



if __name__ == "__main__":
    print("starting bot...")
    main()
