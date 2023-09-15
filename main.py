"""
@file @main.py
@author
"""
import discord
import numpy as np

from bot_token import TOKEN, GUILD_ID
from discord import app_commands


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="check", description="Command to roll a regular BREAK!! check, rolling under a given stat.", guild=discord.Object(id=GUILD_ID))
async def check(interaction, stat: int=10, edge: bool=False, bonus: int=0):
    # If no edge is given, then roll once and send
    if edge is False:
        # Roll the dice
        roll_one = np.random.randint(1, 20)
        roll_two = ""

        # Check against stat
        result_string = f"[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
        if roll_one - bonus <= stat:
            result_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

        if roll_one == stat:
            result_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

        # Scenario when there's no edge or bonus
        if roll_two == "" and bonus == 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll: {roll_one}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

        # Scenario with no edge but a bonus
        elif roll_two == "" and bonus != 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll: {roll_one}\n" \
                            f"Bonus: {bonus}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

    # With the edge, roll twice - pick best result
    else:
        # Roll the dice
        roll_one = np.random.randint(1, 20)
        roll_two = np.random.randint(1, 20)

        # Set highest and lowest
        if roll_one < roll_two:
            lower_roll = roll_one
            higher_roll = roll_two
        elif roll_two < roll_one:
            lower_roll = roll_two
            higher_roll = roll_one
        else:
            lower_roll = roll_one
            higher_roll = roll_two

        # Check against stat
        result_string = f"[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
        if lower_roll - bonus <= stat:
            result_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

        if lower_roll == stat:
            result_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

        # Scenario when there's no edge or bonus
        if bonus == 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll (w/ Edge): {lower_roll} ({higher_roll})\n" \
                            f"Result: {result_string}\n" \
                            f"```"

        # Scenario with no edge but a bonus
        elif bonus != 0:
            return_string = f"```ansi\n" \
                            f"Stat: {stat}\n" \
                            f"Roll (w/ Edge): {lower_roll} ({higher_roll})\n" \
                            f"Bonus: {bonus}\n" \
                            f"Result: {result_string}\n" \
                            f"```"

    await interaction.response.send_message(return_string)


@tree.command(name="contest", description="Contest command for BREAK!!, in which two opponents try to roll under each other.", guild=discord.Object(id=GUILD_ID))
async def contest(interaction, player_stat: int=10, opponent_stat: int=10,
                  player_edge: bool=False, opponent_edge: bool=False, player_bonus: int=0, opponent_bonus: int=0):
    """
    Contest check function, which handles rolling and checking between two opponent rolls in every situation (e.g.
    both succeed, one succeeds, both fail, etc.)
    :param interaction:
    :param player_stat:
    :param opponent_stat:
    :param player_edge:
    :param opponent_edge:
    :param player_bonus:
    :param opponent_bonus:
    :return:
    """

    """ Player Rolls """
    player_roll_one = np.random.randint(1, 20)
    player_roll_two = np.random.randint(1, 20)

    # General catch for equal or lower first roll
    player_roll = player_roll_one
    player_roll = 10

    # If an edge given, check if roll 2 was lower
    if player_edge is True:
        if player_roll_two < player_roll_one:
            player_roll = player_roll_two

    # Check for player success
    player_success = False
    player_success_string = "[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
    if player_roll - player_bonus <= player_stat:
        player_success = True
        player_success_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

    # Check for player critical success
    player_special_success = False
    if player_roll == player_stat:
        player_success = True
        player_special_success = True
        player_success_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

    # Get string for player bonus
    player_bonus_string = ""
    if player_bonus != 0:
        player_bonus_string = f"- {player_bonus} = {player_roll - player_bonus}"

    """ Opponent Rolls """
    opponent_roll_one = np.random.randint(1, 20)
    opponent_roll_two = np.random.randint(1, 20)

    # General catch for equal or lower first roll
    opponent_roll = opponent_roll_one
    opponent_roll = 5

    # If an edge given, check if roll 2 was lower
    if opponent_edge is True:
        if opponent_roll_two < opponent_roll_one:
            opponent_roll = opponent_roll_two

    # Check for opponent success
    opponent_success = False
    opponent_success_string = "[2;34m[2;34m[2;31mFailure![0m[2;34m[0m[2;34m[0m"
    if opponent_roll - opponent_bonus <= opponent_stat:
        opponent_success = True
        opponent_success_string = f"[2;34m[2;34mSuccess![0m[2;34m[0m"

    # Check for opponent critical success
    opponent_special_success = False
    if opponent_roll == opponent_stat:
        opponent_success = True
        opponent_special_success = True
        opponent_success_string = f"[2;34m[2;34m[2;31m[1;31m[1;35mCritical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m"

    # Get string for opponent bonus
    opponent_bonus_string = ""
    if opponent_bonus != 0:
        opponent_bonus_string = f"- {opponent_bonus} = {opponent_roll - opponent_bonus}"

    """ Win Condition Checks """
    return_string = f"```ansi\n" \
                    f"Player Stat: {player_stat}\n" \
                    f"Player Edge: {player_edge}\n" \
                    f"Player Roll: {player_roll} {player_bonus_string}\n" \
                    f"Player Result: {player_success_string}\n" \
                    f"\n" \
                    f"Opponent Stat: {opponent_stat}\n" \
                    f"Opponent Edge: {opponent_edge}\n" \
                    f"Opponent Roll: {opponent_roll} {opponent_bonus_string}\n" \
                    f"Opponent Result: {opponent_success_string}\n" \
                    f"\n" \

    # Player succeeds, Opponent Fails
    if player_success is True and opponent_success is False:
        return_string += f"[2;34m[2;34mPlayer Success![0m[2;34m[0m\n```"

    # Player fails, Opponent Succeeds
    elif player_success is False and opponent_success is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed, player has a special success
    elif (player_success is True and opponent_success is True) and player_special_success is True and opponent_special_success is False:
        return_string += f"[2;34m[2;34m[2;31m[1;31m[1;35mPlayer Critical Success![1;35m[0m[1;35m[0m[1;31m[0m[2;31m[0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed, opponent has a special success
    elif (player_success is True and opponent_success is True) and player_special_success is False and opponent_special_success is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Special Success![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has an edge
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_edge is True and opponent_edge is False:
        return_string += f"[2;34m[2;34mPlayer Success by Edge![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has an edge
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_edge is False and opponent_edge is True:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Edge![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has larger bonus
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_bonus > opponent_bonus:
        return_string += f"[2;34m[2;34mPlayer Success by Larger Bonus![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has an edge
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and opponent_bonus > player_bonus:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Larger Bonus![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has less penalty
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_bonus >= 0 and opponent_bonus < 0:
        return_string += f"[2;34m[2;34mPlayer Success by Least Penalty![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has less penalty
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_bonus < 0 and opponent_bonus >= 0:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Least Penalty![0m[2;34m[0m[2;34m[0m\n```"

    # Both succeed/fail, player has the best natural roll
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and player_roll > opponent_roll:
        return_string += f"[2;34m[2;34mPlayer Success by Best Natural Roll![0m[2;34m[0m\n```"

    # Both succeed/fail, opponent has the best natural roll
    elif (player_success is True and opponent_success is True) or (player_success is False and opponent_success is False) and opponent_roll > player_roll:
        return_string += f"[2;34m[2;34m[2;31mOpponent Success by Best Natural Roll![0m[2;34m[0m[2;34m[0m\n```"

    # Error or Stalemate
    else:
        return_string += f"[2;34m[2;34mEither this is an Error or a Stalemate![0m[2;34m[0m\n```"

    await interaction.response.send_message(return_string)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

client.run(TOKEN)
