"""
@file: random_tables.py
@author

Holds the rolling logic of non-functional roll tables in BREAK!!,
such as rolling a random character, an encounter site, or GMCs.
"""
import json
import numpy as np

from utils import get_tier


class RandomTables:
    def __init__(self, table_name):
        super().__init__()

        # Path of table names
        table_paths = {
            "pc": ("character_creation.json", self.player_character),
            "gmc": ("gmc_tables.json", self.game_master_character),
            "bg_indiv": ("gmc_tables.json", self.background_character_individual),
            "bg_bulk": ("gmc_tables.json", self.background_character_bulk)
        }

        # Load in the JSON of the given table
        self.table = json.load(open(table_paths[table_name][0], 'r'))

        # Set the function to roll on
        self.function = table_paths[table_name][1]

    def roll_on_table(self):
        """ Simple rerouting function that returns the result of the chosen table function """
        return self.function()

    def player_character(self):
        """
        Generates a formatted output of a randomly rolled BREAK!! character,
        based on the random tables presented in the rule book
        :return: formatted string
        """
        # Roll calling and species
        calling = get_tier(np.random.randint(1, 21), self.table['calling'])
        species = get_tier(np.random.randint(1, 21), self.table['species'])

        # Get the homeland and language
        homeland_roll = 21 if species == "Human, Dimensional Stray" else np.random.randint(1, 21)
        homeland = get_tier(homeland_roll, self.table['homeland'])
        homeland_name = homeland['name']
        language = np.random.choice(homeland['languages'])

        # Roll a history
        history = get_tier(np.random.randint(1, 21), self.table['histories'][homeland_name])

        # Roll traits, 2 positive and one negative
        pos_trait_one = get_tier(np.random.randint(1, 21), self.table['traits'])
        pos_trait_two = get_tier(np.random.randint(1, 21), self.table['traits'])
        neg_trait = get_tier(np.random.randint(1, 21), self.table['traits'])

        # Each species group has different tables and probabilities to roll on it for quirks
        if species in ["Gruun", "Chib", "Human, Native", "Human, Dimensional Stray", "Promethean", "Rai-Neko",
                       "Tenebrate"]:
            table = get_tier(np.random.randint(1, 21), table={
                "1-7": "spirit",
                "8-14": "physiology",
                "15-20": "fate"
            })
        elif species in ["Dwarf", "Elf", "Goblin"]:
            table = get_tier(np.random.randint(1, 21), table={
                "1-7": "spirit",
                "8-14": "physiology",
                "15-20": "eldritch"
            })
        else:
            table = get_tier(np.random.randint(1, 21), table={
                "1-10": "spirit",
                "11-20": "robotic"
            })

        # Roll the quirk
        quirk = get_tier(np.random.randint(1, 21), self.table['quirks'][table])

        # Build the return string
        return_string = f"Here's your Player Character!" \
                        f"```ansi\n" \
                        f"[1;2mCalling[0m[1;2m[0m: {calling}\n" \
                        f"[1;2mSpecies[0m[1;2m[0m: {species}\n" \
                        f"[1;2mHomeland[0m[1;2m[0m: {homeland_name}\n" \
                        f"[1;2mLanguages[0m[1;2m[0m: Low Tongue, {language}\n" \
                        f"[1;2mHistory[0m[1;2m[0m: {history}\n" \
                        f"[1;2mQuirk[0m[1;2m[0m: {quirk}\n" \
                        f"\n" \
                        f"[1;2mTraits[0m[1;2m[0m:\n" \
                        f"\t+1 {pos_trait_one}\n" \
                        f"\t+1 {pos_trait_two}\n" \
                        f"\t-1 {neg_trait}\n" \
                        f"```"
        return return_string

    def game_master_character(self):
        """
        Builds the output of a random Game Master Character (GMC) based on the source book's random tables
        :return: formatted string
        """
        # Build out the return string start
        return_string = "```\n"

        # Always give back a villain motivation
        motivation = get_tier(np.random.randint(1, 21), self.table['villain_motivation'])
        return_string += f"{'Villain Motivation:':25}{motivation}\n"

        # Roll for minor quirk
        quirk = self.table['quirk'][str(np.random.randint(1, 21))]
        return_string += f"{'Minor Quirk:':25}{quirk}\n"

        # Roll for profession
        profession = get_tier(np.random.randint(1, 21), self.table['profession'])
        profession_adj = get_tier(np.random.randint(1, 21), self.table['profession_adj'])
        return_string += f"{'Profession:':25}{profession_adj} {profession}\n"

        # Roll for Clothing Color
        clothing_color = get_tier(np.random.randint(1, 21), self.table['clothing_color'])
        return_string += f"{'Clothing Color:':25}{clothing_color}\n"

        # Roll for Prominent Accessory
        accessory = get_tier(np.random.randint(1, 21), self.table['prominent_accessory'])
        return_string += f"{'Prominent Accessory:':25}{accessory}\n"

        # Return formatted message
        return_string += "```"
        return return_string

    def background_character_individual(self):
        """
        Function that generates a string block of individual background characters' traits,
        given the BG table in the source book
        :return: formatted string
        """
        # Build return string and roll for the number of characters
        return_string = "```\n"
        num_characters = np.random.randint(2, 6)

        # For each character, roll it and add to the return string
        for i in range(num_characters):
            bg_adjective = get_tier(np.random.randint(1, 21), self.table['background_character'])[0]
            bg_appearance = get_tier(np.random.randint(1, 21), self.table['background_character'])[1]
            return_string += f"Character #{i:02d}: {bg_adjective:>15} & {bg_appearance:>15}\n"

        # Build and return it
        return_string += "```"
        return return_string

    def background_character_bulk(self):
        """
        Function that generates a single trait block for a group of background characters,
        given the random table in the source book
        :return: formatted string
        """
        # Build return string and roll for the number of characters
        return_string = "```\n"
        num_characters = np.random.randint(2, 6)

        # Roll for the characters and return the string
        bg_adjective = get_tier(np.random.randint(1, 21), self.table['background_character'])[0]
        bg_appearance = get_tier(np.random.randint(1, 21), self.table['background_character'])[1]
        return_string += f"There is a group of {num_characters} people that are {bg_adjective} and {bg_appearance}\n```"
        return return_string

