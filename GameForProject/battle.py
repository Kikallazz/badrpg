#!/usr/local/bin/python3
"""
Battle.py - The battle class manages the events of the battle

Written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

import sys
import time

class Battle: #The battle engine

  def __init__(self, player, enemies, app):
    """
    Instantiates a battle object between the players and
    specified,
    sending output to the given gui instance
    """
    self.player = player
    self.enemies = enemies
    self.app = app
    self.turn = 1
    self.wins = 0
    self.kills = 0
    self.player_won = False
    self.player_lost = False
  
  def play(self):#Controls the turn-based aspect of the game and tracks kills and wins
    """
    Begins and controls the battle
    returns tuple of (win [1 or 0], no. kills)
    """

    while not self.player_won and not self.player_lost:

      self.app.write("Turn "+str(self.turn))
      self.app.write("")
      time.sleep(1)

      #The bulk of the action occurs here
      self.do_player_actions()
      self.do_enemy_actions()

      self.turn += 1

    return (self.wins, self.kills)

  def get_action(self):#At the start of the turn, the player chooses their actions e.g. Aggressive, attack, (enemy 1)
    """ Gets the player's chosen action for their turn """
    try:
      self.app.write(self.player.name + "'s Turn:")
      self.app.write("1. Attack Enemies")
      self.app.write("2. Cast Magic")
      self.app.write("3. Use Potion")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      player_action = self.app.inputVariable.get()

      if player_action == 'quit':
        self.app.quit()

      player_action = int(player_action)
      if player_action not in range(1,4):
        raise ValueError

    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      player_action = self.get_action()

    return player_action

  def select_spell(self):#If player selects spells, it displays the available spells and then shows their resource cost and damage, etc.
    """ Selects the spell the player would like to cast """
    player_race = self.player.__class__.__name__

    try:
      self.app.write("Select your spell:")
      if player_race == "Dunedain":
          self.app.write("4. Heal wounds (20 mp)")
      if player_race == "Wizard" and self.player.mana >= 10:
        self.app.write("1. Fireball (10 mp)")
      if self.player.mana >= 20:
        self.app.write("2. Shield (20 mp)")
      if player_race == "Wizard":
        self.app.write("3. Mana Drain (no mp cost)")
      self.app.write("0. Cancel Spell")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      spell_choice = self.app.inputVariable.get()

      if spell_choice == 'quit':
        self.app.quit()
      spell_choice = int(spell_choice)
      if spell_choice == 0:
        return False
      valid_spell = self.player.valid_spell(spell_choice)
      if not valid_spell:
        raise ValueError
    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      spell_choice = self.select_spell()

    return spell_choice #Tells the player which spell they picked

  def choose_target(self):#Asks for input for target, e.g. 0. Azog, 1. Lurtz, 2. Saruman
    """ Selects the target of the player's action """
    try:
      self.app.write("Choose your target:")
      j = 0
      while j < len(self.enemies):
        if self.enemies[j].health > 0:
          self.app.write(str(j) + ". " + self.enemies[j].name)
        j += 1
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      target = self.app.inputVariable.get()

      if target == 'quit':
        self.app.quit()

      target = int(target)
      if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
        raise ValueError
    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      target = self.choose_target()

    return target #"You attacked Azog, damage, health remaining, etc.

  def choose_stance(self): #Determines your choices for attacking and defending, as well as taken dealt and taken
    try:
      self.app.write("Choose your stance:")
      self.app.write("a - Aggressive")
      self.app.write("d - Defensive")
      self.app.write("b - Balanced")
      self.app.write("")
      self.app.write("f - Flee From Battle")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      stance_choice = self.app.inputVariable.get()

      if stance_choice == 'quit':
        self.app.quit()

      if stance_choice not in ['a','d','b','f'] or stance_choice == '':
        raise ValueError

      elif stance_choice == 'f':
        self.app.quit()

      elif stance_choice == 'a':
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("      /| _________________")
          self.app.write("O|===|* >________________/")
          self.app.write("      \|")
          self.app.write("")

      elif stance_choice == 'd':
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("")
          self.app.write("  |`-._/\_.-`|")
          self.app.write("  |    ||    |")
          self.app.write("  |___o()o___|")
          self.app.write("  |__((<>))__|")
          self.app.write("  \   o\/o   /")
          self.app.write("   \   ||   /")
          self.app.write("    \  ||  /")
          self.app.write("     '.||.'")
          self.app.write("       ``")
          self.app.write("")



    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      stance_choice = self.choose_stance()

    return stance_choice

  def select_potions(self):
    has_attacked = False
    player_race = self.player.__class__.__name__
    try:
      self.app.write("Select your potion:")
      if self.player.potions >= 1:
          self.app.write("2. Health Potion")
      if player_race == "Dunedain" and self.player.potions >= 1:
        self.app.write("1. Mana Potion")
      self.app.write("")
      self.app.wait_variable(self.app.inputVariable)
      potion_choice = self.app.inputVariable.get()

      if potion_choice == 'quit':
        self.app.quit()
      potion_choice = int(potion_choice)
      if potion_choice == 0:
        return False
    except ValueError:
      self.app.write("You must enter a valid choice")
      self.app.write("")
      potion_choice = self.select_potions()
    if potion_choice == "2":
      has_attacked = self.player.use_healthpotion()
    elif potion_choice == "1":
      has_attacked = self.player.use_manapotion()
    return int(potion_choice)

  def do_player_actions(self):#Tells player whether their attack hit the target and its damage, whether the they blocked, etc.
    """ Performs the player's actions """
  
    turn_over = False
  
    while not self.player_won and not turn_over:

      self.player.print_status()
      stance_choice = self.choose_stance()
      self.player.set_stance(stance_choice)

      player_action = self.get_action()

      has_attacked = False

      if player_action == 3:
        potion_choice = self.select_potions()
        if potion_choice == 2:
          has_attacked = self.player.use_potion(potion_choice)
        elif potion_choice == 1:
          has_attacked = self.player.use_potion(potion_choice)

      elif player_action == 2:
        spell_choice = self.select_spell()

        if spell_choice != 0:
          has_attacked = True
          if spell_choice == 1 or spell_choice == 3:
            target = self.choose_target()
            if self.player.cast_spell(spell_choice, self.enemies[target]):
              self.kills += 1
          else:
            self.player.cast_spell(spell_choice)

      else:
        target = self.choose_target()
        has_attacked = True

        if self.player.attack_enemy(self.enemies[target]):
          self.kills += 1

      turn_over = True
      if not has_attacked:
        turn_over = False
      else:
        self.player_won = True
        for enemy in self.enemies:
          if enemy.health > 0:
            self.player_won = False
            break

        if self.player_won == True:
          self.app.write("Your enemies have been vanquished!!")
          self.app.write("")
          time.sleep(1)
          self.wins += 1

  def do_enemy_actions(self):#Determines whether or not the AI's attack hit you, whether they blocked your attack or if they healed using a potion, etc.
    """ Performs the enemies' actions """

    turn_over = False

    if not self.player_won:
      self.app.write("Enemies' Turn:")
      self.app.write("")
      time.sleep(1)

      for enemy in self.enemies:
        if enemy.health > 0 and not self.player_lost:

          if not self.player_lost:
            self.player_lost = enemy.move(self.player)

      if self.player_lost == True:
        self.app.write("You have been killed by your enemies.")
        self.app.write("")
        time.sleep(1)