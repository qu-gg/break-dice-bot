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
    'SUFFOCATING': (187, 187, 187),
    'NEUTRAL': (54, 196, 6)
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
    # Define default thresholds
    neutralThreshold = 0.5
    isolatedThreshold = 0.9
    crampedThreshold = 0.1
    shelteredThreshold = 0.4
    obscuredThreshold = 0.6
    precariousThreshold = 0.7
    suffocatingThreshold = 0.8
    harmfulThreshold = 0.8

    # Adjust based on conditions dict
    if(not conditions['Neutral']):
        neutralThreshold = 0
    if(not conditions['Isolated']):
        isolatedThreshold = 1.1
    if(not conditions['Cramped']):
        crampedThreshold = 0
    if(not conditions['Sheltered']):
        shelteredThreshold = 0
    if(not conditions['Obscured']):
        obscuredThreshold = 0
    if(not conditions['Precarious']):
        precariousThreshold = 0
    if(not conditions['Suffocating']):
        suffocatingThreshold = 0
    if(not conditions['Harmful']):
        harmfulThreshold = 1.1

    if(danger < neutralThreshold):
        return 'NEUTRAL'
    if(elevation > isolatedThreshold):
        return 'ISOLATED'
    else:
        if(space < crampedThreshold):
            return 'CRAMPED'
        elif(space < shelteredThreshold):
            return 'SHELTERED'
        if(danger < obscuredThreshold):
            return 'OBSCURED'
        elif(danger < precariousThreshold):
            return 'PRECARIOUS'
        elif(danger < suffocatingThreshold):
            return 'SUFFOCATING'
        elif(danger > harmfulThreshold):
            return 'HARMFUL'
    return 'NEUTRAL'


def GenerateBattlefield(dimension=250, complexity=1, conditions=defaultConditions, extraDanger=0):
    """ Generate noise maps and combine them into RGB pixel map """
    # Generate noise maps
    # Octaves increase complexity/granularity, i.e. higher octaves make busier maps with more areas
    dangerNoise = PerlinNoise(octaves=complexity)
    elevationNoise = PerlinNoise(octaves=complexity)
    spaceNoise = PerlinNoise(octaves=complexity)

    # Convert generators to arrays
    dangerMap = np.array([np.array([dangerNoise([i/dimension, j/dimension])+0.5+extraDanger for j in range(dimension)]) for i in range(dimension)])
    elevationMap = np.array([np.array([elevationNoise([i/dimension, j/dimension])+0.5 for j in range(dimension)]) for i in range(dimension)])
    spaceMap = np.array([np.array([spaceNoise([i/dimension, j/dimension])+0.5 for j in range(dimension)]) for i in range(dimension)])

    # Convert arrays of noise to array of pixel values in RGB space, including biome types
    pixelValues = []
    mapBiomes = []
    for i in range(dimension):
        mapBiomeRow = []
        for j in range(dimension):
            pixelValue = GetPixelValue(dangerMap[i][j], elevationMap[i][j], spaceMap[i][j], conditions)
            pixelValues.append(pixelValue)
            mapBiomeRow.append(biomes[pixelValue])

        mapBiomes.append(np.array(mapBiomeRow))

    # Condense pixel values to np array and get the set of biome types
    myMap = np.array(mapBiomes)
    biomesUsed = set(pixelValues)
    return myMap, biomesUsed


def GenerateImage(dimension=250, complexity=1, conditions=defaultConditions, extraDanger=0):
    """ Generate an RGB pixel map and convert to an IO stream for Discord """
    # Generate map
    battlefieldMap, battlefieldBiomes = GenerateBattlefield(dimension, complexity, conditions, extraDanger)

    # Convert map to Image object
    # NOTE: .astype('uint8') is required or else the pixels get all garbled
    mapIm = Image.fromarray(battlefieldMap.astype('uint8'), mode="RGB")

    # Initialize final image with Discord dark mode background because I'm the only one who uses light mode
    im = Image.new(mode='RGB', size=(dimension, dimension + (35 * int(np.ceil(len(battlefieldBiomes) / 2)))), color=(64, 68, 75))

    # Place area map onto the new image
    im.paste(mapIm, (0, 0, dimension, dimension))

    # Initialize editing
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("arial.ttf", 10)

    # Put a legend with colors and labels of what each area is
    for biome_idx, biome_name in enumerate(battlefieldBiomes):
        draw.rectangle((((biome_idx%2)*100), dimension+5+((biome_idx//2)*30), 25+((biome_idx%2)*100), (dimension+25)+5+((biome_idx//2)*30)), fill=biomes[biome_name])
        draw.text((((biome_idx%2)*100)+30, dimension+5+((biome_idx//2)*30)), biome_name.title(), fill="white", font=font)
    
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
        self.danger = 0

    def reset_button_style(self):
        # Set all button colors
        for child in self.children:
            if child.custom_id in self.conditions:
                if self.conditions[child.custom_id]:
                    child.style = discord.ButtonStyle.green
                else:
                    child.style = discord.ButtonStyle.gray

    def return_string(self):
        return f"Extra Danger Level: {int(self.danger * 100)}%"

    @discord.ui.button(label="Neutral".title(), style=discord.ButtonStyle.green, custom_id='Neutral', row=1)
    async def neutral(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Neutral'] = not self.conditions['Neutral']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="sheltered".title(), style=discord.ButtonStyle.gray, emoji="🏡", custom_id='Sheltered', row=1)
    async def sheltered(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Sheltered'] = not self.conditions['Sheltered']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="suffocating".title(), style=discord.ButtonStyle.gray, emoji="💦", custom_id='Suffocating', row=1)
    async def suffocating(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Suffocating'] = not self.conditions['Suffocating']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="precarious".title(), style=discord.ButtonStyle.gray, emoji="⚠", custom_id='Precarious', row=1)
    async def precarious(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Precarious'] = not self.conditions['Precarious']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Obscured".title(), style=discord.ButtonStyle.gray, emoji="🦮", custom_id='Obscured', row=2)
    async def obscured(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Obscured'] = not self.conditions['Obscured']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Isolated".title(), style=discord.ButtonStyle.gray, emoji="🪔", custom_id='Isolated', row=2)
    async def isolated(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Isolated'] = not self.conditions['Isolated']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Harmful".title(), style=discord.ButtonStyle.gray, emoji="🩹", custom_id='Harmful', row=2)
    async def harmful(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Harmful'] = not self.conditions['Harmful']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Cramped".title(), style=discord.ButtonStyle.gray, emoji="🦀", custom_id='Cramped', row=2)
    async def cramped(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.conditions['Cramped'] = not self.conditions['Cramped']
        # Edit original message for successful interaction
        self.reset_button_style()
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Increase Danger", style=discord.ButtonStyle.gray, row=3)
    async def increasedanger(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Increment danger for map
        self.danger += 0.1
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Decrease Danger", style=discord.ButtonStyle.gray, row=3)
    async def decreasedanger(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Decrement danger for map
        self.danger -= 0.1
        await interaction.response.edit_message(view=self, content=self.return_string())

    @discord.ui.button(label="Generate", style=discord.ButtonStyle.red, row=4)
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Edit original message for successful interaction
        self.reset_button_style()

        # Do a deferred interaction during image generation to prevent timeout
        await interaction.response.defer()
        image = GenerateImage(self.dimension, self.complexity, self.conditions, self.danger)
        asyncio.sleep(self.dimension // 100)

        # Edit the message with the new battlefield
        await interaction.followup.edit_message(message_id=interaction.message.id,
                                                attachments=[discord.File(image, 'battlefield.jpg')],
                                                view=self, content=self.return_string())
