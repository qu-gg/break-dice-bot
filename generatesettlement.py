import discord
import random

names = ['Lorem',
        'ipsum',
        'dolor',
        'sit',
        'amet', 
        'consectetur', 
        'adipiscing', 
        'elit',
        'Nulla', 
        'consectetur', 
        'in', 
        'ipsum', 
        'in', 
        'semper', 
        'Etiam', 
        'lobortis',
        'venenatis', 
        'tellus', 
        'nec', 
        'luctus', 
        'purus', 
        'Phasellus', 
        'iaculis', 
        'in', 
        'turpis', 
        'a', 
        'blandit', 
        'Cras', 
        'pharetra', 
        'eros', 
        'vel', 
        'leo', 
        'dapibus', 
        'non', 
        'condimentum',
        'nisl', 
        'accumsan', 
        'Proin', 
        'congue', 
        'accumsan', 
        'dui', 
        'id', 
        'efficitur', 
        'neque', 
        'dapibus', 
        'at', 
        'Morbi', 
        'rhoncus', 
        'tristique', 
        'mollis']

class GenerateSettlementButtons(discord.ui.View):
    def __init__(self, size):
        super().__init__()
        self.settlement = Settlement(size)
        self.ViewSettlement()

    def ViewSettlement(self):
        self.clear_items()
        for row in range(self.settlement.size):
            for column in range(self.settlement.size):
                self.add_item(self.settlement.grid[row][column].button)
    
    async def ViewDistrict(self, interaction):
        self = self.clear_items()
        rowcol = interaction.data['custom_id'].split(',')
        districtCell = self.settlement.grid[int(rowcol[0])][int(rowcol[1])]
        for content in districtCell.contents:
            self.add_item(content.button)
        self.add_item(ViewSettlementButton(label='View Settlement'))
        await interaction.response.edit_message(embeds=districtCell.toEmbed(), view=self)
    
    async def ViewContent(self, interaction, embeds, contents):
        self.clear_items()
        self.add_item(ViewSettlementButton(label='View Settlement'))
        if len(contents) > 0:
            for content in contents:
                self.add_item(content.button)
        await interaction.response.edit_message(embeds=embeds, view=self)

class DistrictButton(discord.ui.Button):
    def __init__(self, custom_id, content, embeds, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_id = custom_id
        self.content = content
        self.embeds = embeds

    async def callback(self, interaction: discord.Interaction):
        await self.view.ViewDistrict(interaction)

class ContentButton(discord.ui.Button):
    def __init__(self, contents=[], embeds=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contents = contents
        self.embeds = embeds
    
    async def callback(self, interaction: discord.Interaction):
        await self.view.ViewContent(interaction, self.embeds, self.contents)

class ViewSettlementButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.view.ViewSettlement()
        await interaction.response.edit_message(view=self.view, embeds=[])

class Settlement:
    def __init__(self, size=0):
        self.size = size
        if(self.size == 0):
            self.size = random.randint(1,5)
        self.grid = [[Cell.NewCell(row, column) for column in range(self.size)] for row in range(self.size)]

class Cell:
    def __init__(self):
        self.name = ''
        self.contents = []
        self.rowcol = '0,0'
        self.button = None
        self.color = 0

    def toString(self):
        #returnString = f'**{self.name}**'
        returnString = ''
        for content in self.contents:
            returnString += f'\n{content.name}'
        return returnString

    def toEmbed(self):
        embeds = []
        embeds.append(discord.Embed(title=f'{self.name} District', color=self.color, description=self.toString()))
        for content in self.contents:
            embeds.append(content.toEmbed(False))
        return embeds

    def NewCell(row, col):
        cell = Cell()
        cell.name = random.choice(names)
        cell.color = int(hex(random.randrange(0, 2**24)), 16)
        cell.contents.append(CellContent(random.choice(names), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))
        cell.contents.append(CellContent(random.choice(names), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))
        cell.contents.append(CellContent(random.choice(names), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))

        cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16))
        cell.rowcol = f'{row},{col}'
        cell.button = DistrictButton(label=cell.name, custom_id=cell.rowcol, embeds = cell.toEmbed(), content=cell.toString(), row=row)
        return cell
    
class CellContent:
    def __init__(self, name, description, color):
        self.name = name
        self.description = description
        self.color = color
        self.contents = []
        self.button = ContentButton(label=self.name, embeds=self.toEmbed(True))
    def toEmbed(self, recursive=True):
        embed = discord.Embed(title=self.name, color=self.color, description=self.description)
        if(recursive):
            embeds = [embed]
            for content in self.contents:
                embeds.append(content.toEmbed(recursive=False))
            return embeds
        return embed
    def AddContent(self, name, description, color):
        newContent = CellContent(name, description, color)
        self.contents.append(newContent)
        self.button = ContentButton(label=self.name, embeds=self.toEmbed(True), contents=self.contents)