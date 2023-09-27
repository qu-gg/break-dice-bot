"""
@file conditions.py

This file contains the ButtonHandler for the /conditions command in the discord bot.
Loads the file in once at bot launch and handles manipulating the message with new
BREAK!! conditions after a button interaction.
"""
import json
import discord


class Buttons(discord.ui.View):
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

    @discord.ui.button(label="Ballooned", style=discord.ButtonStyle.gray, emoji="🎈")
    async def ballooned(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'ballooned'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Blinded", style=discord.ButtonStyle.gray, emoji="🕶")
    async def blinded(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'blinded'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Chibbed", style=discord.ButtonStyle.gray, emoji="🐤")
    async def chibbed(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'chibbed'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Deafened", style=discord.ButtonStyle.gray, emoji="🎧")
    async def deafened(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'deafened'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Disoriented", style=discord.ButtonStyle.gray, emoji="💫")
    async def disoriented(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'disoriented'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Dispirited", style=discord.ButtonStyle.gray, emoji="😭")
    async def dispirited(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'dispirited'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Fatigued", style=discord.ButtonStyle.gray, emoji="🛌")
    async def fatigued(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'fatigued'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Jellyfied", style=discord.ButtonStyle.gray, emoji="🍮")
    async def jellyfied(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'jellyfied'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Overburdened", style=discord.ButtonStyle.gray, emoji="🎒")
    async def overburdened(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'overburdened'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Petrified", style=discord.ButtonStyle.gray, emoji="🗿")
    async def petrified_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'petrified'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Putrefied", style=discord.ButtonStyle.gray, emoji="☢")
    async def putrefied_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'putrefied'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Restrained", style=discord.ButtonStyle.gray, emoji="❌")
    async def restrained_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'restrained'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Starved", style=discord.ButtonStyle.gray, emoji="🍴")
    async def starved(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'starved'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Suffocated", style=discord.ButtonStyle.gray, emoji="💧")
    async def suffocated(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'suffocated'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Terrified", style=discord.ButtonStyle.gray, emoji="👻")
    async def terrified(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'terrified'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)

    @discord.ui.button(label="Toppled", style=discord.ButtonStyle.gray, emoji="🍂")
    async def toppled(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Get embedding
        condition_name = 'toppled'
        embed = self.get_condition_embed(condition_name)

        # Edit original message for successful interaction
        self.reset_button_style(button)
        await interaction.response.edit_message(content=f"Showing {condition_name.title()}:", embed=embed, view=self)
