import json

def GenerateBaseByInput():
    supplement = input('Supplement: ')
    category = input('Category: ')
    initialID = f'{supplement}/Oracles/{category}'
    jsonDict = {"$id": initialID, "Oracles": []}
    return jsonDict

def GenerateParentOracleByInput(baseOracle):
    category = input('Child category: ')
    inputValue = ''
    oracleRolls = []
    while inputValue != 'stop':
        floor = int(input('Floor: '))
        ceiling = int(input('Ceiling: '))
        result = input('Result: ')
        oracleRolls.append({'Floor': floor, 'Ceiling': ceiling, 'Result': f'{baseOracle['$id']}/{category}/{result}'})
        inputValue = input('ENTER to continue, \'stop\' to stop ')
    baseOracle['Oracles'].append({'$id': f'{baseOracle['$id']}/{category}', 'Oracle rolls': oracleRolls})

def GenerateChildOracleByInput(baseOracle):
    category = input('Child category: ')
    inputValue = ''
    table = []
    while inputValue != 'stop':
        floor = int(input('Floor: '))
        ceiling = int(input('Ceiling: '))
        result = input('Result: ')
        table.append({'Floor': floor, 'Ceiling': ceiling, 'Result': result})
        inputValue = input('ENTER to continue, \'stop\' to stop ')
    baseOracle['Oracles'].append({'$id': f'{baseOracle['$id']}/{category}', 'Table': table})

def OracleByString(inputString):
    table = []
    for line in inputString.splitlines()[1:]:
        rollRange = line.split()[0]
        if('–' in rollRange):
            floor = int(rollRange.split('–')[0])
            ceiling = int(rollRange.split('–')[1])
        else:
            floor = ceiling = int(rollRange)
        if(ceiling == 0):
            ceiling = 100
        if(floor == 0):
            floor = 100
        text = ' '.join(line.split()[1:])
        print(floor)
        print(ceiling)
        print(text)
        table.append({'Floor': floor, 'Ceiling': ceiling, 'Result': text})
    oracle = {'$id': f'{inputString.splitlines()[0]}', 'Table': table}
    return oracle



if __name__ == '__main__':
    
    parentID = 'Worlds_Without_Number/Oracles/History'
    oracles = []
    oracleInput = ''
    while oracleInput != 'stop':
        childID = input('childID: ')
        contents = [f'{parentID}/{childID}']
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == 'stop':
                break
            contents.append(line)
        inputString = '\n'.join(contents)
        oracle = OracleByString(inputString)
        oracles.append(oracle)
        oracleInput = input('ENTER to continue, \'stop\' to stop ')
    parentOracle = {'$id': parentID, 'Oracles': oracles}
    myFile = open(f'{'.'.join(parentID.split('/'))}.json', 'w', encoding='utf8')
    json.dump([parentOracle], myFile, indent=2)
    myFile.close()
