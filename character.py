#!/usr/local/bin/python3
"""
Character.py - Class definition for RPG Characters

Written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

# import required Python modules
import time
import random

######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character: #This is the character class, it dictates your stats
  """ Defines the attributes and methods of the base Character class """
  
  def __init__(self, char_name, app): #
    """ Parent constructor - called before child constructors """
    self. _mod = 1.0
    self.defense_mod = 1.0
    self.name = char_name
    self.shield = 0
    self.max_shield = 50
    self.app = app

  def __str__(self): #"You are John the Human"
    """ string representation of character """
    return str("You are " + self.name + " the " + self.__class__.__name__)

  def move(self, player):
    """
    Defines any actions that will be attempted before individual
    character AI kicks in - applies to all children
    """
    move_complete = False
    if self.health < 50 and self.potions > 0:
      self.set_stance('d')
      self.use_potion()
      move_complete = True
    return move_complete

  def set_stance(self, stance_choice):
    """ sets the fighting stance based on given parameter """
    
    if stance_choice == "a":
      self.attack_mod = 1.3
      self.defense_mod = 0.6
      self.app.write(self.name + " chose aggressive stance.")

    elif stance_choice == "d":
      self.attack_mod = 0.6
      self.defense_mod = 1.3
      self.app.write(self.name + " chose defensive stance.")

    else:
      self.attack_mod = 1.0
      self.defense_mod = 1.0
      self.app.write(self.name + " chose balanced stance.")
    self.app.write("")

  def attack_enemy(self, target):
    ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
    to be targeted). Returns True if target killed, False if still alive.'''

    roll = random.randint(0,10)
    hit = int(roll * self.attack_mod * self.attack)
    self.app.write(self.name + " attacks " + target.name + ".")
    time.sleep(1)

    crit_roll = random.randint(1, 10)
    if crit_roll == 10:
      hit = hit*2
      self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
      time.sleep(1)

    kill = target.defend_attack(hit)
    time.sleep(1)

    if kill:
      self.app.write(self.name + " has killed " + target.name + ".")
      self.app.write("")
      time.sleep(1)
      return True      
    else:
      return False

  def defend_attack(self, att_damage):
    ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
    a parameter. Returns True is character dies, False if still alive.'''
    
    roll = random.randint(1, 20)
    block = int(roll * self.defense_mod * self.defense)
        
    block_roll = random.randint(1, 10)
    if block_roll == 10:
      self.app.write(self.name + " successfully blocks the attack!")
      block = att_damage
      time.sleep(1)

    damage = att_damage - block
    if damage < 0:
      damage = 0

    if self.shield > 0:
      if damage <= self.shield:
        self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        self.shield = self.shield - damage
        damage = 0
      elif damage != 0:
        self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
        time.sleep(1)
        damage = damage - self.shield
        self.shield = 0
      
    self.app.write(self.name + " suffers " + str(damage) + " damage!")
    self.health = self.health - damage
    time.sleep(1)
      
    if self.health <= 0:
      self.health = 0
      self.app.write(self.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True
    else:
      self.app.write(self.name + " has " + str(self.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

  def valid_spell(self, choice):
    ''' Checks to see if the spell being cast is a valid spell i.e. can be cast by
    that race and the character has enough mana '''

    valid = False

    race = self.__class__.__name__
    
    if choice == 1:
      if race == "Wizard" and self.mana >= 10:
        valid = True
    elif choice == 2 and self.mana >= 20:
      valid = True
    elif choice == 3:
      if race == "Wizard":
        valid = True
    elif choice == 4:
      if race == "Dunedain":
        valid = True
    else:
        raise ValueError
        
    return valid

  def cast_spell(self, choice, target=False):
    ''' Casts the spell chosen by the character. Requires 2 parameters - the spell
    being cast and the target of the spell. '''

    kill = False

    race = self.__class__.__name__

    if choice == 1:
      if race == "Wizard":
        kill = self.cast_fireball(target)
    elif choice == 2:
      self.cast_shield()
    elif choice == 3:
      self.cast_mana_drain(target)
    elif choice == 4:
      if race == "Dunedain":
        self.cast_heal()
    elif choice == 5:
      if race == "Dragon":
        kill = self.cast_dragonfire(target)
    elif choice == 6:
      if race == "Nazgul":
        kill = self.cast_soul_steal(target)
    else:
      self.app.write("Invalid spell choice. Spell failed!")
      self.app.write("")

    return kill

  def cast_fireball(self, target):
    self.mana -= 10
    self.app.write(self.name + " casts Fireball on " + target.name + "!")
    time.sleep(1)
      
    roll = random.randint(1, 10)
    defense_roll = random.randint(1, 10)
    damage = int(roll * self.magic) - int(defense_roll * target.resistance)
    if damage < 0:
      damage = 0
      
    if target.shield > 0:
      if damage <= target.shield:
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        target.shield = target.shield - damage
        damage = 0
      elif damage != 0:
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(1)
        damage = damage - target.shield
        target.shield = 0
                        
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    target.health = target.health - damage
      
    if target.health <= 0:
      target.health = 0
      self.app.write(target.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True

    else:
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

  def cast_dragonfire(self, target):
    self.mana -= 20
    self.app.write(self.name + " breathes fire at " + target.name + "!")
    time.sleep(1)

    roll = random.randint(10, 15)
    defense_roll = random.randint(1, 5)
    damage = int(roll * self.magic) - int(defense_roll * target.resistance)
    if damage < 0:
      damage = 0

    if target.shield > 0:
      if damage <= target.shield:
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        target.shield = target.shield - damage
        if target.shield == 0:
          self.app.write(self.name + "'s dragon fire has destroyed " + target.name + "'s shield!")
        damage = 0
      elif damage != 0:
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(1)
        damage = damage - target.shield
        target.shield = 0

    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    target.health = target.health - damage

    if target.health <= 0:
      target.health = 0
      self.app.write(target.name + " was burnt to a crisp!")
      self.app.write("")
      time.sleep(1)
      return True

    else:
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

  def cast_shield(self):
    self.mana -= 20
    self.app.write(self.name + " casts Shield!")
    time.sleep(1)
    if self.shield <= self.max_shield:
      self.shield = self.max_shield
    self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
    self.app.write("")
    time.sleep(1)

  def cast_mana_drain(self, target):
    self.app.write(self.name + " casts Mana Drain on " + target.name + "!")
    time.sleep(1)

    if target.mana >= 20:
      drain = 20
    else:
      drain = target.mana
    self.app.write(self.name + " drains " + str(drain) + " mana from "+ target.name + ".")
    time.sleep(1)
      
    target.mana -= drain
    self.mana += drain
    if target.mana <= 0:
      target.mana = 0
      self.app.write(target.name + "'s mana has been exhausted!")
    else:
      self.app.write(target.name + " has " + str(target.mana) + " mana left")
    self.app.write("")

  def cast_soul_steal(self, target):
    self.app.write(self.name + " casts Soul Steal on " + target.name + "!")
    time.sleep(1)

    if target.health >= 20:
      drain = 20
    else:
      drain = target.health
    self.app.write(self.name + " steals " + str(drain) + " health from " + target.name + ".")
    time.sleep(1)

    target.health -= drain
    self.health += drain
    if target.health <= 0:
      target.health = 0
      self.app.write(target.name + "'s soul has been torn from their body!")
      return True
    else:
      self.app.write(target.name + " has " + str(target.health) + " health left")
      return False
    self.app.write("")

  def cast_heal(self):
    self.mana -= 20
    self.app.write(self.name + " heals their wounds.")
    time.sleep(1)
    if self.health <= self.max_health:
      self.health = self.max_health
    self.app.write(self.name + " has " + str(self.health) + " hit points.")
    self.app.write("")
    time.sleep(1)

  def valid_potion(self, choice):
    ''' Checks to see if the potion being used is a valid potion i.e. can be used by
    that race and the character has enough potions '''

    valid = False

    race = self.__class__.__name__

    if choice == 1 and self.potions >= 1:
      valid = True
    elif choice == 2 and self.potions >= 1:
      valid = True
    else:
      raise ValueError

    return valid

  def use_potion(self):
    self.app.wait_variable(self.app.inputVariable)
    potion_choice = self.app.inputVariable.get()
    has_attacked = False

    race = self.__class__.__name__

    if self.potions >= 1:
      if potion_choice == "1":
        if race == "Dunedain":
          has_attacked = self.use_manapotion()
      elif potion_choice == "2":
        has_attacked = self.use_healthpotion()
      else:
        self.app.write("Invalid potion choice. Please select a valid potion.")
        self.app.write("")

    return has_attacked

  def use_healthpotion(self):
    """
    Uses a health potion if the player has one. Returns True if has potion,
    false if hasn't
    """
    has_attacked = False
    if self.potions >= 1:
      self.potions -= 1
      self.health += 250
      if self.health > self.max_health:
        self.health = self.max_health
      self.app.write(self.name + " uses a potion!")
      time.sleep(1)
      self.app.write(self.name + " has " + str(self.health) + " hit points.")
      self.app.write("")
      time.sleep(1)
      has_attacked = True
      return has_attacked
    else:
      self.app.write("You have no potions left!")
      self.app.write("")
      return has_attacked

  def use_manapotion(self):
    """
    Uses a mana potion if the player has one. Returns True if has potion,
    false if hasn't
    """
    has_attacked = False
    if self.potions >= 1:
      self.potions -= 1
      self.mana += self.max_mana-self.mana
      if self.mana > self.max_mana:
        self.mana = self.max_mana
      self.app.write(self.name + " uses a potion!")
      time.sleep(1)
      self.app.write(self.name + " has " + str(self.mana) + " mana.")
      self.app.write("")
      time.sleep(1)
      has_attacked = True
      return has_attacked
    else:
      self.app.write("You have no potions left!")
      self.app.write("")
      return has_attacked

  def reset(self):
    ''' Resets the character to its initial state '''
    
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;
    self.shield = 0
    
  def print_status(self):
    ''' Prints the current status of the character '''
    self.app.write(self.name + "'s Status:")
    time.sleep(0.5)
    
    health_bar = "Health: "
    health_bar += "|"
    i = 0
    while i <= self.max_health:
      if i <= self.health:
        health_bar += "#"
      else:
        health_bar += " "
      i += 25
    health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
    self.app.write(health_bar)
    time.sleep(0.5)
        
    if self.max_mana > 0:
      mana_bar = "Mana: "
      mana_bar += "|"
      i = 0
      while i <= self.max_mana:
        if i <= self.mana:
          mana_bar += "*"
        else:
          mana_bar += " "
        i += 10
      mana_bar += "| " + str(self.mana) + " mp (" + str(int(self.mana*100/self.max_mana)) +"%)"
      self.app.write(mana_bar)
      time.sleep(0.5)
   
    if self.shield > 0:
      shield_bar = "Shield: "
      shield_bar += "|"
      i = 0
      while i <= 100:
        if i <= self.shield:
          shield_bar += "o"
        else:
          shield_bar += " "
        i += 10
      shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
      self.app.write(shield_bar)
      time.sleep(0.5)   

    self.app.write("Potions remaining: " + str(self.potions))
    self.app.write("")
    time.sleep(0.5)

######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Dwarf(Character):
  '''Defines the attributes of a Dwarf in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 300;
    self.max_mana = 30;
    self.starting_potions = 1;
    self.attack = 9;
    self.defense = 6;
    self.magic = 4;
    self.resistance = 5;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Dwarf class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False
    
class Elf(Character):
  '''Defines the attributes of an Elf in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 300;
    self.max_mana = 60;
    self.starting_potions = 1;
    self.attack = 6;
    self.defense = 8;
    self.magic = 8;
    self.resistance = 8;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Elf class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Goblin(Character):
  '''Defines the attributes of a Goblin in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 100;
    self.max_mana = 0;
    self.starting_potions = 0;
    self.attack = 3;
    self.defense = 3;
    self.magic = 0;
    self.resistance = 0;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Goblin class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      return self.attack_enemy(player)
    return False

class Hobbit(Character):
  '''Defines the attributes of a Hobbit in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_potions = 2;
    self.attack = 3;
    self.defense = 9;
    self.magic = 6;
    self.resistance = 10;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Hobbit class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Human(Character):
  '''Defines the attributes of a Human in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250;
    self.max_mana = 40;
    self.starting_potions = 1;
    self.attack = 7;
    self.defense = 8;
    self.magic = 5;
    self.resistance = 4;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Human class """
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health*100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health*100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Orc(Character):
  '''Defines the attributes of an Orc in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250;
    self.max_mana = 0;
    self.starting_potions = 0;
    self.attack = 7;
    self.defense = 5;
    self.magic = 2;
    self.resistance = 4;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Orc class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('b')
      return self.attack_enemy(player)
    return False

class Uruk(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''
  
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 400;
    self.max_mana = 20;
    self.starting_potions = 1;
    self.attack = 9;
    self.defense = 7;
    self.magic = 4;
    self.resistance = 6;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Uruk class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False

class Wizard(Character):
  '''Defines the attributes of a Wizard in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 150;
    self.max_mana = 100;
    self.starting_potions = 2;
    self.attack = 5;
    self.defense = 6;
    self.magic = 10;
    self.resistance = 10;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Wizard class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.mana < 10 and player.mana > 0:
        self.cast_spell(3, player)
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      elif self.mana >= 10:
        return self.cast_spell(1, player)
      else:
        return self.attack_enemy(player)
    return False


class Dunedain(Character):
  '''Defines the attributes of a Dunedain in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 225;
    self.max_mana = 60;
    self.starting_potions = 2;
    self.attack = 8;
    self.defense = 7;
    self.magic = 6;
    self.resistance = 7;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Dunedain class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.mana >= 20:
        self.cast_spell(4)
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False


class Haradrim(Character):
  '''Defines the attributes of a Haradrim in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 200;
    self.max_mana = 20;
    self.starting_potions = 2;
    self.attack = 9;
    self.defense = 5;
    self.magic = 3;
    self.resistance = 7;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Haradrim class """
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health * 100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health * 100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Dragon(Character):
  '''Defines the attributes of a Dragon in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 2000;
    self.max_mana = 200;
    self.starting_potions = 0;
    self.attack = 32;
    self.defense = 10;
    self.magic = 20;
    self.resistance = 9;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Dragon class """
    if self.mana >= 20:
      roll = random.randint(0, 1)
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health * 100 / self.max_health > 50 or roll == 0:
        self.set_stance('a')
      else:
        self.set_stance('b')
      if self.health * 100 / self.max_health > 50 and self.mana >= 20 or roll == 1:
        return self.cast_spell(5, player)
      return self.attack_enemy(player)

    return False

class Nazgul(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 750;
    self.max_mana = 750;
    self.starting_potions = 3;
    self.attack = 10;
    self.defense = 8;
    self.magic = 20;
    self.resistance = 10;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Wizard class """
    if self.mana >= 50:
      roll = random.randint(0, 1)
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.mana < 10 and player.mana > 0:
        self.cast_spell(3, player)
      elif self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      elif self.mana >= 10 or roll == 0:
        return self.cast_spell(1, player)
      elif self.mana >= 50 or roll == 1:
        return self.cast_spell(6, player)
      else:
        return self.attack_enemy(player)
    return False

class Spider(Character):
  '''Defines the attributes of a Spider  in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 1000;
    self.max_mana = 200;
    self.starting_potions = 1;
    self.attack = 12;
    self.defense = 6;
    self.magic = 10;
    self.resistance = 5;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Spider class """
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health * 100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health * 100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.mana >= 20:
        self.cast_spell(2)
      else:
        return self.attack_enemy(player)
    return False

class Skinchanger(Character):
  '''Defines the attributes of an Uruk in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 900;
    self.max_mana = 20;
    self.starting_potions = 0;
    self.attack = 25;
    self.defense = 9;
    self.magic = 4;
    self.resistance = 10;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Uruk class """
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health * 100 / self.max_health > 75:
        self.set_stance('a')
      else:
        self.set_stance('d')
      return self.attack_enemy(player)
    return False


class Crusader(Character):
  '''Defines the attributes of a Crusader in the game. Inherits the constructor and methods
  of the Character class '''

  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 1500;
    self.max_mana = 200;
    self.starting_potions = 5;
    self.attack = 35;
    self.defense = 20;
    self.magic = 7;
    self.resistance = 15;
    self.health = self.max_health;
    self.mana = self.max_mana;
    self.potions = self.starting_potions;

  def move(self, player):
    """ Defines the AI for the Crusader class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False