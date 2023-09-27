"""
@file battleifled.py

This file contains the ButtonHandler for the /battlefield command in the discord bot.
Loads the file in once at bot launch and handles manipulating the message with new
BREAK!! battlefield conditions after a button interaction.
"""
import json
import discord


class BattlefieldButtons(discord.ui.View):
    def __init__(self, conditions, *, timeout=360):
        super().__init__(timeout=timeout)
        self.conditions = conditions

    def get_condition_embed(self, condition_name):
        # Get condition values
        condition_dict = self.conditions[condition_name]
        condition_url = condition_dict['image_url']
        condition_desc = condition_dict['description']
        condition_effects = condition_dict['effects']

        # Build embed to return
        embed = (discord.Embed(title=f"{condition_name.title()}", color=0x15dbc7))
        embed.set_thumbnail(url=condition_url)
        embed.add_field(name="Description", value=condition_desc, inline=False)
        embed.add_field(name="Effects", value=condition_effects, inline=False)
        return embed

    def reset_button_style(self, button):
        # Set all buttons to gray
        for child in self.children:
            child.style = discord.ButtonStyle.gray

        # Set the active button to green
        button.style = discord.ButtonStyle.green

    @discord.ui.button(label="Cramped", style=discord.ButtonStyle.gray, emoji="🦀")
    async def cramped(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'cramped'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Harmful", style=discord.ButtonStyle.gray, emoji="🩹")
    async def harmful(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'harmful'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="isolated".title(), style=discord.ButtonStyle.gray, emoji="🪔")
    async def isolated(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'isolated'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="obscured".title(), style=discord.ButtonStyle.gray, emoji="🦮")
    async def obscured(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'obscured'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="precarious".title(), style=discord.ButtonStyle.gray, emoji="⚠")
    async def precarious(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'precarious'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="sheltered".title(), style=discord.ButtonStyle.gray, emoji="🏡")
    async def sheltered(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'sheltered'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="suffocating".title(), style=discord.ButtonStyle.gray, emoji="💦")
    async def suffocating(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'suffocating'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)
