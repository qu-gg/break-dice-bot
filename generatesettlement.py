import discord
import random
import json
import os
import io
import requests

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

attributions = {'SpectacularSettlements': 'Powered by [Spectacular Settlements](https://nordgamesllc.com/product/spectacular-settlements-pdf/) copyright © Nord Games LLC'}

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
    
    def toJSON(self):
        return json.dumps(self.__dict__, cls=SettlementJSONEncoder)

class ViewSettlementButton(discord.ui.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.view.ViewSettlement()
        await interaction.response.edit_message(view=self.view, embeds=[self.view.settlement.overview.overview])

class DownloadSettlementButton(discord.ui.Button):
    def __init__(self, settlement, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settlement = settlement
    async def callback(self, interaction: discord.Interaction):
        stream = io.BytesIO()
        jsonString = self.settlement.toJSON().encode()
        stream.write(jsonString)
        stream.seek(0)
        await interaction.channel.send(file=discord.File(stream, 'settlement.json'))

class Settlement:
    def __init__(self, size=0):
        self.size = size
        if(self.size < 1):
            self.size = random.randint(1,5)
        if(self.size > 5):
            self.size = 5
        self.settlementType = self.RollSettlementType()
        self.grid = [[Cell.NewCell(row, column, self.settlementType) for column in range(self.size)] for row in range(self.size)]
        self.overview = SettlementOverview(self.settlementType)
    def toJSON(self):
        return json.dumps(self.__dict__, cls=SettlementJSONEncoder, indent=2)
    def RollSettlementType(self):
        if(self.size <= 2):
            return random.choice(['Trading Post', 'Village'])
        elif(self.size <= 3):
            return random.choice(['Trading Post', 'Town'])
        elif(self.size <= 5):
            return random.choice(['Town', 'City'])
        return 'Town'
        #return random.choice(['Trading Post', 'Village', 'Town', 'City'])
    
class SettlementOverview:
    def __init__(self, settlementType):
        self.settlementType = settlementType
        if(self.settlementType == 'Trading Post'):
            self.initializeTradingPost()
        elif(self.settlementType == 'Village'):
            self.initializeVillage()
        elif(self.settlementType == 'Town'):
            self.initializeTown()
        elif(self.settlementType == 'City'):
            self.initializeCity()
    def initializeTradingPost(self):
        self.condition = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Condition')
        self.visitorTraffic = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Visitor Traffic')
        self.residentPopulation = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Resident Population')
        self.residentDisposition = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Disposition')
        self.lawEnforcement = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Law Enforcement')
        self.leadership = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Leadership')
        self.events = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Events')
        self.opportunities = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Opportunities')
        self.overview = self.GenerateOverviewTradingPost()
    def GenerateOverviewTradingPost(self):
        embed = discord.Embed(title='Trading Post', description=f'**Condition:** {self.condition}')
        embed.add_field(name='**Traffic**', value=self.visitorTraffic)
        embed.add_field(name='**Residents**', value=f'Population: {self.residentPopulation}\nDisposition: {self.residentDisposition}')
        embed.add_field(name='**Leadership**', value=f'Style: {self.leadership}\nLaw Enforcement: {self.lawEnforcement}')
        embed.add_field(name='**Hooks**', value=f'{self.events}\n{self.opportunities}')
        return embed
    def initializeVillage(self):
        self.numHardships = int(RollOnServer('Spectacular_Settlements/Oracles/Village/Hardship Likelihood'))
        self.hardships = []
        for hardship in range(self.numHardships):
            self.hardships.append(RollOnServer('Spectacular_Settlements/Oracles/Village/Hardship Type'))
        self.condition = RollOnServer('Spectacular_Settlements/Oracles/Village/Condition')
        self.resource = RollOnServer('Spectacular_Settlements/Oracles/Village/Resource')
        self.recentHistory = RollOnServer('Spectacular_Settlements/Oracles/Village/Recent History')
        self.residentPopulation = RollOnServer('Spectacular_Settlements/Oracles/Village/Population Density')
        self.disposition = RollOnServer('Spectacular_Settlements/Oracles/Village/Disposition')
        self.overview = self.GenerateOverviewVillage()
    def GenerateOverviewVillage(self):
        embed = discord.Embed(title='Village', description=f'**Condition:** {self.condition}')
        embed.add_field(name='**Resource**', value=self.resource)
        embed.add_field(name='**Recent History**', value=self.recentHistory)
        embed.add_field(name='**Hardships**', value='\n'.join(self.hardships))
        embed.add_field(name='**Residents**', value=f'Population: {self.residentPopulation}\nDisposition: {self.disposition}')
        return embed
    def initializeTown(self):
        self.priority = RollOnServer('Spectacular_Settlements/Oracles/Town/Priority')
        self.specialty = RollOnServer('Spectacular_Settlements/Oracles/Town/Specialty')
        self.condition = RollOnServer('Spectacular_Settlements/Oracles/Town/Condition')
        self.prosperity = RollOnServer('Spectacular_Settlements/Oracles/Town/Prosperity')
        self.residentPopulation = RollOnServer('Spectacular_Settlements/Oracles/Town/Population Density')
        self.disposition = RollOnServer('Spectacular_Settlements/Oracles/Town/Disposition')
        self.leadership = RollOnServer('Spectacular_Settlements/Oracles/Town/Leadership')
        self.lawEnforcement = RollOnServer('Spectacular_Settlements/Oracles/Town/Law Enforcement')
        self.overview = self.GenerateOverviewTown()
    def GenerateOverviewTown(self):
        embed = discord.Embed(title='Town', description=f'**Specialty:** {self.specialty}\n**Priority:** {self.priority}')
        embed.add_field(name='**Condition**', value=self.condition)
        embed.add_field(name='**Prosperity**', value=self.prosperity)
        embed.add_field(name='**Residents**', value=f'Population: {self.residentPopulation}\nDisposition: {self.disposition}')
        embed.add_field(name='**Leadership**', value=f'Style: {self.leadership}\nLaw Enforcement: {self.lawEnforcement}')
        return embed
    def initializeCity(self):
        self.priority = RollOnServer('Spectacular_Settlements/Oracles/City/Priority')
        self.stewardship = RollOnServer('Spectacular_Settlements/Oracles/City/Stewardship')
        self.condition = RollOnServer('Spectacular_Settlements/Oracles/City/General Condition')
        self.residentPopulation = RollOnServer('Spectacular_Settlements/Oracles/City/Population Density')
        self.disposition = RollOnServer('Spectacular_Settlements/Oracles/City/Disposition')
        self.leadership = RollOnServer('Spectacular_Settlements/Oracles/City/Leadership')
        self.lawEnforcement = RollOnServer('Spectacular_Settlements/Oracles/City/Law Enforcement')
        self.overview = self.GenerateOverviewCity()
    def GenerateOverviewCity(self):
        embed = discord.Embed(title='City', description=f'**Priority:** {self.priority}\n**Stewardship:** {self.stewardship}')
        embed.add_field(name='**Condition**', value=self.condition)
        embed.add_field(name='**Residents**', value=f'Population: {self.residentPopulation}\nDisposition: {self.disposition}')
        embed.add_field(name='**Leadership**', value=f'Style: {self.leadership}\nLaw Enforcement: {self.lawEnforcement}')
        return embed
    def toJSON(self):
        return {}

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

    def NewCell(row, col, settlementType):
        cell = Cell()
        if(settlementType == 'Trading Post'):
            districtPurpose = RollOnServer('Spectacular_Settlements/Oracles/Trading Post/Specialty')
            cell.name = districtPurpose
            cell.color = int(hex(random.randrange(0, 2**24)), 16)
            for poi in range(3):
                commercialType = random.choice(['Shop', 'Service'])
                commercialSpecific = RollOnServer(f'Spectacular_Settlements/Oracles/Trading Post/{commercialType}s')
                cell.contents.append(CellContent(commercialSpecific, 'Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                for content in range(len(cell.contents[poi].contents)):
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
        elif(settlementType == 'Village'):
            districtPurpose = RollOnServer('Spectacular_Settlements/Oracles/Village/Specialty')
            cell.name = districtPurpose
            cell.color = int(hex(random.randrange(0, 2**24)), 16)
            for poi in range(3):
                locationType = random.choices(['Place of Worship', 'Place of Gathering', 'Other Locations'], [0.1, 0.4, 0.5])[0]
                if(locationType == 'Place of Worship'):
                    size = RollOnServer(f'Spectacular_Settlements/Oracles/Village/Place of Worship Size')
                    location = f'Place of Worship ({size})'
                else:
                    location = RollOnServer(f'Spectacular_Settlements/Oracles/Village/{locationType}')
                cell.contents.append(CellContent(location, 'Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                for content in range(len(cell.contents[poi].contents)):
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
        elif(settlementType == 'Town'):
            districtPurpose = random.choices(['Non-Commercial', 'Commercial'], [0.75, 0.25])[0]
            
            cell.color = int(hex(random.randrange(0, 2**24)), 16)
            if(districtPurpose == 'Non-Commercial'):
                for poi in range(3):
                    category = RollOnServer('Spectacular_Settlements/Oracles/Town/Non-Commercial Location Type')
                    cell.name = category.split()[-1]
                    location = RollOnServer(f'Spectacular_Settlements/Oracles/Town/{category}')
                    cell.contents.append(CellContent(location, 'Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    for content in range(len(cell.contents[poi].contents)):
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
            elif(districtPurpose == 'Commercial'):
                for poi in range(3):
                    category = RollOnServer('Spectacular_Settlements/Oracles/Town/Shop or Service')
                    cell.name = category
                    location = RollOnServer(f'Spectacular_Settlements/Oracles/Town/{category}s')
                    cell.contents.append(CellContent(location, 'Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                    for content in range(len(cell.contents[poi].contents)):
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                        cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
        elif(settlementType == 'City'):
            districtPurpose = RollOnServer('Spectacular_Settlements/Oracles/City/District Type')
            cell.name = districtPurpose
            cell.color = int(hex(random.randrange(0, 2**24)), 16)
            for poi in range(3):
                location = RollOnServer(f'Spectacular_Settlements/Oracles/City/{districtPurpose} District Additional Locations')
                cell.contents.append(CellContent(location, 'Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                cell.contents[poi].AddContent(random.choice(names), 'NPC Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
                for content in range(len(cell.contents[poi].contents)):
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
                    cell.contents[poi].contents[content].AddContent(random.choice(names), 'NPC Hooks/Detail/Relationship', int(hex(random.randrange(0, 2**24)), 16), '')
        #districtPurpose = RollOnServer('Starforged/Oracles/Settlements/Projects')
        #cell.name = districtPurpose
        #cell.color = int(hex(random.randrange(0, 2**24)), 16)
        #category = RollOnServer('Spectacular_Settlements/Oracles/Town/Non-Commercial Location Type')
        #actualContent = RollOnServer(f'Spectacular_Settlements/Oracles/Town/{category}')
        #cell.contents.append(CellContent(actualContent, 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
        #category = RollOnServer('Spectacular_Settlements/Oracles/Town/Non-Commercial Location Type')
        #actualContent = RollOnServer(f'Spectacular_Settlements/Oracles/Town/{category}')
        #cell.contents.append(CellContent(actualContent, 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))
        #category = RollOnServer('Spectacular_Settlements/Oracles/Town/Non-Commercial Location Type')
        #actualContent = RollOnServer(f'Spectacular_Settlements/Oracles/Town/{category}')
        #cell.contents.append(CellContent(actualContent, 'District Content Placeholder', int(hex(random.randrange(0, 2**24)), 16), attributions['SpectacularSettlements']))

        #cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        #cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        #cell.contents[0].AddContent(random.choice(names), 'Detail Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        #cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        #cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        #cell.contents[0].contents[0].AddContent(random.choice(names), 'Nested Placeholder', int(hex(random.randrange(0, 2**24)), 16), '')
        cell.rowcol = f'{row},{col}'
        cell.button = DistrictButton(label=cell.name, custom_id=cell.rowcol, embeds = cell.toEmbed(), content=cell.toString(), row=row)
        return cell
    
    def toJSON(self):
        jsonDict = {'name': self.name, 'contents': self.contents, 'rowcol': self.rowcol, 'color': self.color}
        return jsonDict
    
class CellContent:
    def __init__(self, name, description, color, attribution):
        self.name = name
        self.description = description
        self.color = color
        self.attribution = attribution
        self.contents = []
        self.button = ContentButton(label=self.name, embeds=self.toEmbed(True))
    def toEmbed(self, recursive=True):
        embed = discord.Embed(title=self.name, color=self.color, description=f'{self.description}\n\n{self.attribution}')
        if(recursive):
            embeds = [embed]
            for content in self.contents:
                embeds.append(content.toEmbed(recursive=False))
            return embeds
        return embed
    def AddContent(self, name, description, color, attribution):
        newContent = CellContent(name, description, color, attribution)
        self.contents.append(newContent)
        self.button = ContentButton(label=self.name, embeds=self.toEmbed(True), contents=self.contents)
    
    def toJSON(self):
        jsonDict = {'name': self.name, 'description': self.description, 'color': self.color, 'attribution': self.attribution, 'contents': self.contents}
        return jsonDict

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
        print(depthString)
        print(parentOracle)
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

class SettlementJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)
        
def RollOnServer(id):
    url = 'http://18.220.137.34:8080/table'
    payloadobj = {'id': id}
    response = requests.post(url=url, data=payloadobj)
    return response.text.strip('"')
        
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
    history = RollOnOracle(GetOracle(data, 'Worlds_Without_Number/Oracles/History/Why_fail'))
    print(history)
    pass
    #nonComm = OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))
    #print(nonComm)
    #nonCommDetail = RollOnOracle(GetOracle(data, OracleFromOracle(GetOracle(data, 'Spectacular_Settlements/Oracles/Points_of_Interest/Non-Commercial_Location_Type/Non-Commercial Location Type'))))
    #print(nonCommDetail)



