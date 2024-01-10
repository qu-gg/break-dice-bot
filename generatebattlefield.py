"""
@file generatebattlefield.py
@author Ferretsroq
"""
import io
import discord
import asyncio
import numpy as np

from perlin_noise import PerlinNoise
from PIL import Image, ImageDraw, ImageFont

# Define RGB codes for the different area types
biomes = {
    'CRAMPED': (102, 161, 255),
    'HARMFUL': (255, 0, 0),
    'ISOLATED': (255, 181, 138),
    'OBSCURED': (229, 230, 207),
    'PRECARIOUS': (136, 207, 112),
    'SHELTERED': (221, 224, 162),
    'SUFFOCATING': (54, 196, 6),
    'NEUTRAL': (187, 187, 187)
}

defaultConditions = {
    'Cramped': True,
    'Harmful': True,
    'Isolated': True,
    'Obscured': True,
    'Precarious': True,
    'Sheltered': True,
    'Suffocating': True,
    'Neutral': True
}


# Transform noise values to actual pixel values
def GetPixelValue(danger, elevation, space, conditions):
    if(danger < 0.5):
        if(not conditions['Neutral']):
            danger = 0.5
        else:
            return 'NEUTRAL'
    if(elevation > 0.9):
        if(not conditions['Isolated']):
            elevation = 0.9
        else:
            return 'ISOLATED'
    else:
        if(conditions['Cramped']):
            if(space < 0.1):
                return 'CRAMPED'
        else:
            space = 0.1
        if(conditions['Sheltered']):
            if(space < 0.4):
                return 'SHELTERED'
        else:
            space = 0.4
        if(conditions['Obscured']):
            if(danger < 0.6):
                return 'OBSCURED'
        if(conditions['Precarious']):
            if(danger < 0.7):
                return 'PRECARIOUS'
        if(conditions['Suffocating']):
            if(danger < 0.8):
                return 'SUFFOCATING'
        if(conditions['Harmful']):
            if(danger > 0.8):
                return 'HARMFUL'
    return 'NEUTRAL'


def GenerateBattlefield(dimension=250, complexity=1, conditions=defaultConditions):
    """ Generate noise maps and combine them into RGB pixel map """
    # Generate noise maps
    # Octaves increase complexity/granularity, i.e. higher octaves make busier maps with more areas
    dangerNoise = PerlinNoise(octaves=complexity)
    elevationNoise = PerlinNoise(octaves=complexity)
    spaceNoise = PerlinNoise(octaves=complexity)

    # Convert generators to arrays
    dangerMap = np.array([np.array([dangerNoise([i/dimension, j/dimension])+0.5 for j in range(dimension)]) for i in range(dimension)])
    elevationMap = np.array([np.array([elevationNoise([i/dimension, j/dimension])+0.5 for j in range(dimension)]) for i in range(dimension)])
    spaceMap = np.array([np.array([spaceNoise([i/dimension, j/dimension])+0.5 for j in range(dimension)]) for i in range(dimension)])

    # Convert arrays of noise to array of pixel values in RGB space
    myMap = np.array([np.array([biomes[GetPixelValue(dangerMap[i][j], elevationMap[i][j], spaceMap[i][j], conditions)] for j in range(dimension)]) for i in range(dimension)])
    return myMap


def GenerateImage(dimension=250, complexity=1, conditions=defaultConditions):
    """ Generate an RGB pixel map and convert to an IO stream for Discord """
    # Generate map
    battlefieldMap = GenerateBattlefield(dimension, complexity, conditions)

    # Convert map to Image object
    # NOTE: .astype('uint8') is required or else the pixels get all garbled
    mapIm = Image.fromarray(battlefieldMap.astype('uint8'), mode="RGB")

    # Initialize final image with Discord dark mode background because I'm the only one who uses light mode
    im = Image.new(mode='RGB', size=(dimension, dimension + 130), color=(64, 68, 75))

    # Place area map onto the new image
    im.paste(mapIm, (0, 0, dimension, dimension))

    # Initialize editing
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 10)

    # Put a legend with colors and labels of what each area is
    for biome in range(len(biomes)):
        draw.rectangle((((biome%2)*100), dimension+((biome//2)*30), 25+((biome%2)*100), (dimension+25)+((biome//2)*30)), fill=biomes[list(biomes.keys())[biome]])
        draw.text((((biome%2)*100)+30, dimension+((biome//2)*30)), list(biomes.keys())[biome].title(), fill="white", font=font)
    
    # Initialize IO stream
    data_stream = io.BytesIO()

    # Write to IO stream
    im.save(data_stream, format="JPEG")

    # NOTE: MUST SEEK BACK TO 0!
    data_stream.seek(0)
    return data_stream


class GenerateBattlefieldButtons(discord.ui.View):
    def __init__(self, dimension, complexity, *, timeout=360):
        super().__init__(timeout=timeout)
        self.conditions = {
            'Cramped': False,
            'Harmful': False,
            'Isolated': False,
            'Obscured': False,
            'Precarious': False,
            'Sheltered': False,
            'Suffocating': False,
            'Neutral': True
        }

        self.dimension = dimension
        self.complexity = complexity

    def reset_button_style(self):
        # Set all button colors
        for child in self.children:
            if child.custom_id in self.conditions:
                if self.conditions[child.custom_id]:
                    child.style = discord.ButtonStyle.green
                else:
                    child.style = discord.ButtonStyle.gray

    @discord.ui.button(label="Neutral".title(), style=discord.ButtonStyle.green, custom_id='Neutral', row=1)
    async def neutral(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Neutral'] = not self.conditions['Neutral']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="sheltered".title(), style=discord.ButtonStyle.gray, emoji="🏡", custom_id='Sheltered', row=1)
    async def sheltered(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Sheltered'] = not self.conditions['Sheltered']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="suffocating".title(), style=discord.ButtonStyle.gray, emoji="💦", custom_id='Suffocating', row=1)
    async def suffocating(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Suffocating'] = not self.conditions['Suffocating']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="precarious".title(), style=discord.ButtonStyle.gray, emoji="⚠", custom_id='Precarious', row=1)
    async def precarious(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Precarious'] = not self.conditions['Precarious']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Obscured".title(), style=discord.ButtonStyle.gray, emoji="🦮", custom_id='Obscured', row=2)
    async def obscured(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Obscured'] = not self.conditions['Obscured']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Isolated".title(), style=discord.ButtonStyle.gray, emoji="🪔", custom_id='Isolated', row=2)
    async def isolated(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Isolated'] = not self.conditions['Isolated']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Harmful".title(), style=discord.ButtonStyle.gray, emoji="🩹", custom_id='Harmful', row=2)
    async def harmful(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Harmful'] = not self.conditions['Harmful']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Cramped".title(), style=discord.ButtonStyle.gray, emoji="🦀", custom_id='Cramped', row=2)
    async def cramped(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Cramped'] = not self.conditions['Cramped']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Generate", style=discord.ButtonStyle.red, row=3)
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Edit original message for successful interaction
        self.reset_button_style()

        # Do a deferred interaction during image generation to prevent timeout
        await interaction.response.defer()
        image = GenerateImage(self.dimension, self.complexity, self.conditions)
        asyncio.sleep(self.dimension // 100)

        # Edit the message with the new battlefield
        await interaction.followup.edit_message(message_id=interaction.message.id, attachments=[discord.File(image, 'battlefield.jpg')], view=self)