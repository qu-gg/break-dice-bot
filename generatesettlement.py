import discord
import random
import json
import os

#ironswornFile = open('./data/ironsworn_oracles.json', 'r', encoding='utf8')
#ironswornData = json.load(ironswornFile)
#ironswornFile.close()
#starforgedFile = open('./data/starforged_oracles.json', 'r', encoding='utf8')
#starforgedData = json.load(starforgedFile)
#starforgedFile.close()
data = []
for file in os.listdir('./data'):
    if file.endswith('.json'):
        fileObj = open(f'./data/{file}', 'r', encoding='utf8')
        fileData = json.load(fileObj)
        fileObj.close()
        data = data + fileData


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
        super().__init__(timeout=None)
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
        if len(contents) > 0:
            for content in contents:
                self.add_item(content.button)
        self.add_item(ViewSettlementButton(label='View Settlement'))
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
        districtPurpose = RollOnOracle(GetOracle(data, 'Starforged/Oracles/Settlements/Projects'))
        #nonComm = OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))
        #nonCommDetail = RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))))
        cell.name = districtPurpose
        cell.color = int(hex(random.randrange(0, 2**24)), 16)
        cell.contents.append(CellContent(RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type')))), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))
        cell.contents.append(CellContent(RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type')))), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))
        cell.contents.append(CellContent(RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type')))), 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16)))

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

def GetOracle(data, id):
    splitID = id.split('/')
    parentOracle = list(filter(lambda oracle: oracle['$id'].startswith(f'{splitID[0]}/{splitID[1]}/{splitID[2]}'), data))[0]
    depth = 3
    for oracle in parentOracle['Oracles']:
        if oracle['$id'] == id:
            return oracle['Table']
    while 'Oracles' in parentOracle.keys():
        depth += 1
        depthString = ''
        for split in range(depth):
            depthString += f'{splitID[split]}/'
        depthString = depthString.strip('/')
        parentOracle = list(filter(lambda oracle: oracle['$id'].startswith(depthString), parentOracle['Oracles']))[0]
        for oracle in parentOracle['Oracles']:
            if oracle['$id'] == id:
                return oracle['Table']
    
    
    #if 'Oracles' in parentOracle['Oracles']:
    #    for oracle in parentOracle['Oracles']['Oracles']:
    #        if oracle['$id'] == id:
    #            return oracle['Table']
    return {}
        
def RollOnOracle(oracle):
    result = '⏵'
    while('⏵' in result):
        roll = random.randrange(1, oracle[-1]['Ceiling'])
        for entry in oracle:
            if roll >= entry['Floor'] and roll <= entry['Ceiling']:
                result = entry['Result']
            
    return result

def OracleFromOracle(oracle):
    roll = random.randrange(1, oracle[-1]['Ceiling'])
    for entry in oracle:
        if roll >= entry['Floor'] and roll <= entry['Ceiling']:
            return entry['Oracle rolls'][0]
    return ''

if __name__ == '__main__':
    #nameType = OracleFromOracle(GetOracle(ironswornData, 'Ironsworn/Oracles/Settlement/Name'))
    #while nameType.endswith('Something_Else'):
    #    nameType = OracleFromOracle(GetOracle(ironswornData, 'Ironsworn/Oracles/Settlement/Name'))

    #name = RollOnOracle(GetOracle(ironswornData, nameType))
    #quickNamePrefix = RollOnOracle(GetOracle(ironswornData, 'Ironsworn/Oracles/Settlement/Quick_Name/Prefix'))
    #quickNameSuffix = RollOnOracle(GetOracle(ironswornData, 'Ironsworn/Oracles/Settlement/Quick_Name/Suffix'))
    #trouble = RollOnOracle(GetOracle(ironswornData, 'Ironsworn/Oracles/Settlement/Trouble'))

    #for i in range(10000):
    #    project = RollOnOracle(GetOracle(data, 'Starforged/Oracles/Settlements/Projects'))
    #print(nameType)
    #print(name)
    #print(quickNamePrefix)
    #print(quickNameSuffix)
    #print(trouble)
    #    print(project)
    pass
    #nonComm = OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))
    #print(nonComm)
    nonCommDetail = RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))))
    print(nonCommDetail)



