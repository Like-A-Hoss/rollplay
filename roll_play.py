import discord
import random

class ik_dice():
    def __init__(self):
        self.boosted = False #Boosted roll.  A Roll can only ever be boosted once
        self.drop = False #Tells the dice if they need to drop the lowest
        self.add = False #Tells the dice to add an additional die
        self.less = False #Tells the dice to remove a die, to things like difficulty or a crippling injury
        self.number = 2 #base number of dice in a roll
        self.dmg = False
    def set_boosted(self):
        self.boosted = True
    def set_add(self):
        self.add = True
    def set_drop(self):
        self.drop = True
    def set_less(self):
        self.less = True
    def set_number(self):
        if self.add == True:
            self.number += 1
        if self.less ==True:
            self.number -= 1
        if self.boosted == True:
            self.number += 1
        if self.dmg == True:
            self.number += 1
    def set_dmg(self):
        self.dmg = True
        
    def roll_dice(self):
        results=[]
        dice = self.number
        for _ in range(dice):
            results.append(random.randint(1,6))
        if self.drop == True:
            results.sort()
            results.pop(0)
        return results

class dnddice():
    def __init__(self):
        """Base Variables needed to do this"""
        self.number = 1
        self.sides = 20
        self.advantage = False
        self.disadvantage = False
    def set_sides(self, number):
        """sets number of die sides"""
        self.sides = number
    def set_number(self, number):
        """sets number of dice to roll."""
        self.number = number
    def set_advantage(self):
        """sets Advantage flag to true"""
        self.advantage=True
    def set_disadvatage(self):
        """sets Disadvantage flag to true"""
        self.disadvantage = True
    def check_advantage(self):
        """Checks to make sure both advantage and disadvantage flags are both not set at same time."""
        if self.advantage == True and self.disadvantage==True:
            self.advantage = False
            self.disadvantage = False
    def roll_dice(self):
        """rolls dice"""
        results =[]
        dice = self.number
        sides = self.sides
        self.check_advantage()
        if self.advantage == True or self.disadvantage == True:
            dice += 1
        for _ in range(dice):
            results.append(random.randint(1,sides))
        if self.advantage == True:
            results.sort()
            results.pop(0)
            return results
        elif self.disadvantage == True:
            results.sort()
            results.pop()
            return results
        else:
            return results


class Chronicles_Of_Darkness():
    def __init__(self):
        self.number = 0
        self.rote = False
        self.again8 = False
        self.again9 = False
        self.again10 = True
    def set_dice(self, dice):
        self.number = dice
    def set_rote(self):
        self.rote = True
    def set_8again(self):
        self.again8 = True
    def set_9again(self):
        self.again9 = True
    def set_10again(self):
        self.again10 = False
    def roll_dice(self):
        num = self.number
        results = []
        x=0
        print(num)
        while x < num:
            die = random.randint(1,10)
            if self.again8 == True:
                if die >= 8:
                    num += 1
            elif self.again9 == True:
                print ("9's path")
                if die >= 9:
                    print("user rolled a 9+")
                    num += 1
            elif self.again10 == True:
                if die == 10:
                    num += 1
                    print("user rolled a 10")
                    print (num)
            else:
                print("nothing special")
            results.append(die)
            x += 1
        return results
    def count_successes(self, results):
        successes = 0
        for die in results:
            if die >= 8:
                successes +=1
        return successes
    def rote_roll(self, results):
        rerolls = 0
        new_results =[]
        for die in results:
            if die <= 8:
                rerolls += 1
        for _ in range(1, rerolls):
            x = random.randint(1,10)
            new_results.append(x)
            if self.again8 == True:
                if die >= 8:
                    rerolls += 1
            elif self.again9 == True:
                if die >= 9:
                    rerolls += 1
            elif self.again10 == True:
                if die == 10:
                    rerolls += 1
        return new_results
    def chance_die(self):
        x = random.randint(1,10)
        successes = 10
        dramatic_fail = 1
        if x == successes:
            return f"Sucess [{x}]"
        elif x == dramatic_fail:
            return f"Dramatic Failure [{x}]"
        else:
            return f"Fail [{x}]"



    

        
        


client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    user = message.author.name
    #Automating generation of a list of numbers as a string to input bonuses.
    def gen_bonus_words():
        numbers = []
        for num in range(0,20):
            numbers.append(str(num))
        return numbers
    def calc_bonus():
        """Calculates the bonus in a roll statement"""
        bonus_final =""
        bonus =0
        bonus_maker = []
        if any(word in msg for word in bonus_words):
            for word in msg:
                if word in bonus_words:
                    bonus_maker.append(word)
            for word in bonus_maker:
                bonus_final += word
        bonus = int(bonus_final)
        return bonus         
    
    #check to see if message was went by bot if so Ignore it
    if message.author == client.user:
        return
    msg = message.content
    #greeting system
    if msg.startswith('$hello'):
        #A freindly greeting for users, that goes over functions, and what the little cutie can do.
        await message.channel.send("hello!  I am Roll Play your friendly Rollplaying bot!  Currently I am configured for playing Iron Kingdoms Full Metal Fantasy.")
        await message.channel.send("Pretty soon I'll be able to do many things.  Like Roll Dice for other games, and even handle character sheets.")
        await message.channel.send("I hope to be able to play with you soon @{0.author.name}" .format(message))
    #Instructions for playing Iron Kingdoms
    if msg.startswith('$ik'):
        #Vairables needed for an Iron Kingdoms Full Metal Fantasy roll
        roller = ik_dice()
        
        boost_words = ["boost", "boosted"]
        bonus_words = gen_bonus_words()
        add_words =["additional", "add", "bonus", "extra", "+die"]
        drop_words = ["drop", "lowest", "cc"]
        less_words = ["crippled", "less", "-die"]
        dmg_words = ["damage", "dmg"]
        bonus = calc_bonus()
        location = 0
        #Instructions on how to read the message
        if any(word in msg for word in boost_words):
            roller.set_boosted()
        #detects if roll is boosted
        if any(word in msg for word in add_words):
            roller.set_add()
        #Detects if roll has an additional dice
        if any(word in msg for word in less_words):
            roller.set_less()        
        #Detects if roll should have 1 less die than normal
        if any(word in msg for word in drop_words):
            roller.set_drop()
        #Detects if Roll should drop lowest
        roller.set_number()
        if any(word in msg for word in dmg_words):
            roller.set_dmg()
        results = roller.roll_dice()
        final = 0
        for num in results:
            final += num
        final += bonus
        if roller.dmg==True:
            location = random.randint(1,6)
            await message.channel.send(f"{user} you rolled {final} to the {location}, with results of {results}.")
        else:
            await message.channel.send(f"{user} you rolled {final}, with a roll of {results}.")
    #help to teach users how to use the bot
    if msg.startswith('$help'):
        await message.channel.send(f"{user} thank you for asking.  To use Iron kingdoms dice just start with your message with $ik then you can put in any order the bonus and other keywords")
        await message.channel.send(f"for a boosted roll {boost_words}")
        await message.channel.send(f"for an additional dice {add_words}")
        await message.channel.send(f"if you need to drop the lowest {drop_words}")
        await message.channel.send(f"if you need to roll one less die than normal {less_words}")
    #instructions for rolling D&D dice
    if msg.startswith('$dnd'):
        roller = dnddice()
        advantage_words = ["advantage", "vantage", "ad","good"]
        disadvantage_words = ["disadvantage", "dis", "bad"]
        numbers = gen_bonus_words()
        #dnd_bonus_words= gen_math_adder()
        final =0
        if any(word in msg for word in advantage_words):
            #checks for advantage, and sets advantage flag
            roller.set_advantage()
        if any(word in msg for word in disadvantage_words):
            #checks for disadvantage, and sets disadvantage flag
            roller.set_disadvatage()
        # Check for common die notation, ie 1d20+10 which would be one 20 sided die with a bonus of 10
        if len(msg) > 4:
            if msg[5] in numbers:
                stop = False
                msg_length = len(msg)
                to_parse = []
                sides_parse =[]
                sides_word = ""
                dice_raw = []
                dice_word = ""
                #dice_counter = 0
                bonus_raw = []
                bonus_string = ""
                for numb in range(5,msg_length):
                    to_parse.append(msg[numb])
                #find number of dice, and set die roller for it
                while stop == False:
                    word = to_parse.pop(0)
                    if word == "d":
                        stop = True
                    else:
                        dice_raw.append(word)
                for word in dice_raw:
                    dice_word += word
                dice = int(dice_word)
                print(f"This many dice: {dice}")
                roller.set_number(dice)
                #dice_counter +=1
                #find number of sides
                stop = False
                while stop == False:
                    x = to_parse.pop(0)
                    if x in numbers:
                        sides_parse.append(x)
                        #dice_counter += 1
                    else:
                        stop = True
                for word in sides_parse:
                    sides_word += word
                sides = int(sides_word)
                roller.set_sides(sides)
                print(f"with this many sides: {sides}")
                results = roller.roll_dice()
                print(f"expected rolls: {results}")
                print(f"check for bonus: {to_parse[0]}")
                print(f"what is length of to_parse? {len(to_parse)}")
                if len(to_parse) > 0:
                    print(f"starting bonus parse")
                    if to_parse[0] in numbers:
                        stop2 = False
                        while stop2 == False:
                            if len(to_parse)>0:
                                y= to_parse.pop(0)
                                if y in numbers:
                                    bonus_raw.append(y)
                                else:
                                    stop2 = True
                                print("Stoping bonus parse")
                            else:
                                stop2 = True
                    for word in bonus_raw:
                        bonus_string += word
                #        print(word)
                #    print(bonus_string)
                    bonus = int(bonus_string)
                    print(f"we are on bonus path: Bonus is {bonus}")
                #    bonus = find_math_bonus(msg, dnd_bonus_words)
                #    bonus = 1
                    print("ending bonus path")
                else:
                    bonus = 0
                print("Starting wrap up")
                for num in results:
                    final += num
                    print(final)
                final += bonus
                print(final)
                await message.channel.send(f"{user} rolled a {final} with {results} on the dice (with {sides} sides) and a +{bonus}.")
            else:
                final = roller.roll_dice()
                await message.channel.send(f"{user} rolled a {final} on a {roller.sides} die")
        #just a basic d20 roll
        else:
            if any(word in msg for word in advantage_words):
                roller.set_advantage()
            if any(word in msg for word in disadvantage_words):
                roller.set_disadvatage()
            final = roller.roll_dice()
            await message.channel.send(f"{user} rolled a {final} on a {roller.sides} die")

    if msg.startswith('$cod'):
        roller = Chronicles_Of_Darkness()
        again8_words = ["8again", "8s", "8's"]
        again9_words = ["9again", "9s", "9's"]
        to_parse = []
        parse_dice = []
        dice_word =""
        dice = 0
        no_10s = ["no", "10off", "no_again"]
        rote_words = ["rote", "no_fail"]
        chance_words = ["chance", "don't tell me the odds", "this will suck", "do you take bribes"]
        numbers = ["0","1","2","3","4","5","6","7","8","9"]
        # Checking for dice tricks
        if any(word in msg for word in again8_words):
            roller.set_8again()
        if any(word in msg for word in again9_words):
            roller.set_9again()
        if any(word in msg for word in rote_words):
            roller.set_rote()
        if any(word in msg for word in no_10s):
            roller.set_10again()
        
        if msg[5] in numbers:
            stop = False
            to_parse =[]
            num = 5
            while stop == False:
                    if msg[num] in numbers:
                        y = msg[num]
                        parse_dice.append(y)
                        num += 1
                    else:
                        stop = True
            for num in parse_dice:
                dice_word += num
            dice = int(dice_word)
            roller.set_dice(dice)
            results = roller.roll_dice()
            successes = roller.count_successes(results)
            if any(word in msg for word in rote_words):
                rerolls = roller.rote_roll(results)
                successes += roller.count_successes(rerolls)
                await message.channel.send(f"{user} has {successes} on rolls of {results} with the rerolls being {rerolls}.")
            else:
                await message.channel.send(f"{user} has {successes} on rolls of {results}.")
        elif any(word in msg for word in chance_words):
            hope = roller.chance_die()
            await message.channel.send(f"I can't look!  {user} got a {hope} on a chance die.")
        else:
            await message.channel.send("I didn't quite catch that?  Please try again")







            
                


                




            
            

        

client.run('OTEyODc3ODM0MTk0ODA4ODYy.YZ2VvA.k6F2xpNqCmYbgwOwTC1d36soBLA')


