#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game
Written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

import time
import gui  # Brings the GUI into the main code
import character  # "                         "
import battle  # "                            "
import random

app = gui.simpleapp_tk(None)
app.title('RPG Battle')  # Title at the head of the window

app.write('''
 _    _      _                             _         
| |  | |    | |                           | |        
| |  | | ___| | ___  ___  _ __ ___   ___  | |_  ___  
| |/\| |/ _ \ |/ __|/ _ \| '_ ` _ \ / _ \ | __|/ _ \ 
\  /\  /  __/ | (__| (_) | | | | | |  __/ | |_| (_) |
 \/  \/ \___|_|\___|\___/|_| |_| |_|\___|  \__|\___/
____________ _____  ______       _   _   _      _ 
| ___ \ ___ \  __ \ | ___ \     | | | | | |    | |
| |_/ / |_/ / |  \/ | |_/ / __ _| |_| |_| | ___| |
|    /|  __/| | __  | ___ \/ _` | __| __| |/ _ \ |
| |\ \| |   | |_\ \ | |_/ / (_| | |_| |_| |  __/_|
\_| \_\_|    \____/ \____/ \__,_|\__|\__|_|\___(_)
''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")  # The "logo" on the starting screen


def set_mode():
    """ Select the game mode """
    # This is an error checking version of reading user input
    # This uses exception handling as discussed in topic 3
    # Understanding try/except cases is important for
    # verifying user input
    try:
        app.write("Please select a side:")  # Determines the races you can select and what enemies you will face.
        app.write("1. Good")
        app.write("2. Evil")
        app.write("")
        app.wait_variable(app.inputVariable)
        mode = app.inputVariable.get()

        if mode == 'quit':
            app.quit()

        mode = int(mode)
        if mode not in range(1, 3):
            raise ValueError

    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        mode = set_mode()

    return mode


def set_race(mode):
    """ Set the player's race """
    if mode == 2:
        app.write("Playing as the Forces of Sauron.")
        app.write("")

        try:
            app.write("Please select your race:")
            app.write("1. Goblin")
            app.write("2. Orc")
            app.write("3. Uruk")
            app.write("4. Wizard")
            app.write("5. Haradrim")
            app.write("")
            app.wait_variable(app.inputVariable)
            race = app.inputVariable.get()

            if race == 'quit':
                app.quit()

            race = int(race)
            if race not in range(1, 7):
                raise ValueError

        except ValueError:
            app.write("You must enter a valid choice")
            app.write("")
            race = set_race(mode)

    else:
        app.write("Playing as the Free Peoples of Middle Earth.")
        app.write("")

        try:
            app.write("Please select your race:")
            app.write("1. Elf")
            app.write("2. Dwarf")
            app.write("3. Human")
            app.write("4. Hobbit")
            app.write("5. Wizard")
            app.write("6. Dunedain")
            app.write("")
            app.wait_variable(app.inputVariable)
            race = app.inputVariable.get()

            if race == 'quit':
                app.quit()
            race = int(race)

            if race not in range(1, 8):
                raise ValueError

        except ValueError:
            app.write("You must enter a valid choice")  # Race entered was not valid, will let you try again
            app.write("")
            race = set_race(mode)

    return race


def set_name():  # Player's name for the rest of the game
    """ Set the player's name """
    try:
        app.write("Please enter your Character Name:")
        app.write("")
        app.wait_variable(app.inputVariable)
        char_name = app.inputVariable.get()

        if char_name == 'quit':
            app.quit()

        if char_name == '':
            raise ValueError

    except ValueError:  # Character name not valid, will let you try again
        app.write("")
        app.write("Your name cannot be blank")
        char_name = set_name()

    return char_name


def create_player(mode, race, char_name):
    """ Create the player's character """
    if mode == 2:
        if race == 1:
            player = character.Goblin(char_name, app)
        elif race == 2:
            player = character.Orc(char_name, app)
        elif race == 3:
            player = character.Uruk(char_name, app)
        elif race == 4:
            player = character.Wizard(char_name, app)
        else:
            player = character.Haradrim(char_name, app)
    else:
        if race == 1:
            player = character.Elf(char_name, app)
        elif race == 2:
            player = character.Dwarf(char_name, app)
        elif race == 3:
            player = character.Human(char_name, app)
        elif race == 4:
            player = character.Hobbit(char_name, app)
        elif race == 5:
            player = character.Wizard(char_name, app)
        elif race == 6:
            player = character.Dunedain(char_name, app)
        elif race == 7:
            player = character.Crusader(char_name, app)
    return player  # Tells you your name & race e.g. "Gimli the Dwarf"


def set_difficulty():  # Will Determine what enemies you will face, how much damage they will do and the AI's intelligence
    """ Set the difficulty of the game """
    try:
        app.write("Please select a difficulty level:")
        app.write("b - beginner")
        app.write("e - Easy")
        app.write("m - Medium")
        app.write("h - Hard")
        app.write("l - Legendary")
        app.write("un - Ultra Nightmare - Boss Mode")  # In honour of DOOM
        app.write("")
        app.wait_variable(app.inputVariable)
        difficulty = app.inputVariable.get()

        if difficulty == 'quit':
            app.quit()

        if difficulty not in ['b', 'e', 'm', 'h', 'l', 'un'] or difficulty == '':
            raise ValueError

    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        difficulty = set_difficulty()

    return difficulty


def create_enemies(mode, difficulty):
    """ Create the enemies """
    roll = random.randint(0, 2)
    if mode == 2:
        if difficulty == 'm':
            enemies = [character.Hobbit("Peregrin", app), character.Hobbit("Meriadoc", app),
                       character.Human("Eowyn", app)]
        elif difficulty == 'h':
            enemies = [character.Dwarf("Gimli", app), character.Elf("Legolas", app), character.Human("Boromir", app)]
        elif difficulty == 'l':
            enemies = [character.Human("Faramir", app), character.Human("Aragorn", app),
                       character.Wizard("Gandalf", app)]
        elif difficulty == 'un':
            enemies = [character.Elf("Galadriel", app), character.Human("Treebeard", app), character.Uruk("Beorn", app)]
        elif difficulty == 'b':
            enemies = [character.Hobbit("Bilbo", app)]
        else:
            enemies = [character.Hobbit("Frodo", app), character.Hobbit("Sam", app)]

    else:
        if difficulty == 'm':
            enemies = [character.Goblin("Azog", app), character.Goblin("Gorkil", app), character.Orc("Sharku", app)]
        elif difficulty == 'h':
            enemies = [character.Orc("Shagrat", app), character.Orc("Gorbag", app), character.Uruk("Lurtz", app)]
        elif difficulty == 'l':
            enemies = [character.Orc("Grishnakh", app), character.Uruk("Lurtz", app), character.Wizard("Saruman", app)]
        elif difficulty == 'un':
            if roll == 0:
                enemies = [character.Nazgul("Witch-king of Angmar", app)]
            elif roll == 1:
                enemies = [character.Dragon("Smaug", app)]
            elif roll == 2:
                enemies = [character.Spider("Shelob", app)]
        elif difficulty == 'b':
            enemies = [character.Human("Grima", app)]
        else:
            enemies = [character.Goblin("Azog", app), character.Goblin("Gorkil", app)]

    return enemies


def quit_game():  # Determines whether or not the game will end or you will play again, against another set of enemies
    """ Quits the game """
    try:
        app.write("Play Again? (y/n)")
        app.write("")
        app.wait_variable(app.inputVariable)
        quit_choice = app.inputVariable.get()

        if quit_choice == 'quit':
            app.quit()

        if quit_choice not in 'yn' or quit_choice == '':  # if the player enters anything other than y, n or blank, it raises a value error and will prompt the player againb
            raise ValueError

    except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
        quit_choice = quit_game()

    return quit_choice


def print_results():
    app.write("Game Over!")
    app.write("No. Battles: {0}".format(str(battles)))
    app.write("No. Wins: {0}".format(wins))
    app.write("No. Kills: {0}".format(kills))
    app.write("Success Rate (%): {0:.2f}%".format(float(wins * 100 / battles)))
    app.write("Avg. kills per battle: {0:.2f}".format(float(kills) / battles))
    app.write("")


def Mapper():
    name = char_name[0][0]
    table = []
    app.wait_variable(app.inputVariable)
    size = int(app.inputVariable.get())
    for i in range(size):
        row = ["|", "|"]
        for j in range(size):
            row.insert(1, ".")
        table.append(row)

    x = 1
    y = 0
    table[y][x] = name
    rollx = random.randint(1, size-2)
    rolly = random.randint(1, size-2)
    xb = rollx
    yb = rolly
    table[yb][xb] = 'e'
    rollrockx = random.randint(2, size-2)
    rollrocky = random.randint(1, size-2)
    xr = rollrockx
    yr = rollrocky
    xrr = rollrockx - 1
    xrrr = rollrockx + 1
    table[yr][xr] = '/^\\'  # Mountain object
    table[yr][xrr] = ''  # This makes it so that there are no extra dots in this line
    table[yr][xrrr] = ''  # "                 "
    rolllakex = random.randint(2, size-1)
    rolllakey = random.randint(1, size-1)
    xl = rolllakex
    yl = rolllakey
    xll = rolllakex - 1
    xlll = rolllakex + 1
    xllll = rolllakex - 2
    table[yl][xl] = '~~~~'  # lake object
    table[yl][xll] = ''  # This makes it so that there are no extra dots in this line
    table[yl][xlll] = ''  # "                 "
    table[yl][xllll] = ''  # "                 "
    xs = xl + 1
    ys = yl - 1
    xsl = xs - 21
    table[ys][xs] = '~~'  # lake object
    table[ys][xsl] = ''  # This makes it so that there are no extra dots in this line
    if xr in range(xl-1, xl+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    if yr in range(yl-1, yl+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    if xb in range(xr-1, xr+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    if yb in range(yr-1, yr+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    if xs in range(xr-1, xr+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    if ys in range(yr-1, yr+1):
      app.write("The map ran into an error, please try again.")
      mapping = Mapper()
    app.write("Please Input Directions")
    app.write("W: Up")
    app.write("A: Left")
    app.write("S: Down")
    app.write("D: Right")
    app.write("")
    app.write("_" * size + "__")
    for row in table:
        app.write(''.join(row))
    app.write("=" * size + "==")
    app.wait_variable(app.inputVariable)
    line = app.inputVariable.get()
    while line:
        table[y][x] = '.'
        if line.strip() == 'd' or line.strip() == 'D':
            x += 1
        elif line.strip() == 'a' or line.strip() == 'A':
            x -= 1
        elif line.strip() == 'w' or line.strip() == 'W':
            y -= 1
        elif line.strip() == 's' or line.strip() == 'S':
            y += 1
        elif line.strip() == 'quit':
            app.quit()
        else:
            app.write('Please input a valid direction')
            app.wait_variable(app.inputVariable)
            line = app.inputVariable.get()
        table[y][x] = name
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")
        app.write("")  # This just makes it so that the screen isn't cluttered
        app.write("")
        app.write("Please Input Directions:")
        app.write("W: Up")
        app.write("A: Left")
        app.write("S: Down")
        app.write("D: Right")
        app.write("_" * size + "__")
        for row in table:
            app.write(''.join(row))
        app.write("=" * size + "==")
        app.wait_variable(app.inputVariable)
        line = app.inputVariable.get()
        if x == xb and y == yb:
            mapper = battle.Battle(player, enemies, app)
            return mapper


battles = 0
wins = 0
kills = 0

mode = set_mode()
race = set_race(mode)
char_name = set_name()
player = create_player(mode, race, char_name)
app.write(player)
app.write("")
difficulty = set_difficulty()
enemies = create_enemies(mode, difficulty)
mapping = Mapper()

while True:

    encounter = battle.Battle(player, enemies, app)
    battle_wins, battle_kills = encounter.play()

    battles += 1
    wins += battle_wins
    kills += battle_kills

    print_results()

    quit = quit_game()

    if quit == "n":
        app.write("Thank you for playing RPG Battle.")
        time.sleep(2)
        app.quit()

    else:  # This resets the player's health, mana, spells, potions, etc. It also resets all enemies, it will keep the kills, etc until the player stops playing
        # Playing again - reset all enemies and players
        player.reset()
        for enemy in enemies:
            enemy.reset()