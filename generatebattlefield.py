from perlin_noise import PerlinNoise
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io


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

# Transform noise values to actual pixel values
def GetPixelValue(danger, elevation, space):
    if(danger < 0.5):
        return 'NEUTRAL'
    elif(elevation > 0.9):
        return 'ISOLATED'
    else:
        if(space < 0.1):
            return 'CRAMPED'
        elif(space < 0.4):
            return 'SHELTERED'
        else:
            if(danger < 0.6):
                return 'OBSCURED'
            elif(danger < 0.7):
                return 'PRECARIOUS'
            elif(danger < 0.8):
                return 'SUFFOCATING'
            else:
                return 'HARMFUL'
            
def GenerateBattlefield(dimension=250, complexity=1):
    '''Generate noise maps and combine them into RGB pixel map
    '''

    # Maybe make this configurable?
    # Sets size of image in pixels
    #dimension = 250
    
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
    myMap = np.array([np.array([biomes[GetPixelValue(dangerMap[i][j], elevationMap[i][j], spaceMap[i][j])] for j in range(dimension)]) for i in range(dimension)])

    return myMap


def GenerateImage(dimension=250, complexity=1):
    '''Generate an RGB pixel map and convert to an IO stream for Discord'''
    # Generate map
    battlefieldMap = GenerateBattlefield(dimension, complexity)
    # Convert map to Image object
    # NOTE: .astype('uint8') is required or else the pixels get all garbled
    mapIm = Image.fromarray(battlefieldMap.astype('uint8'), mode="RGB")
    # Initialize final image with Discord dark mode background because I'm the only one who uses light mode
    im = Image.new(mode='RGB', size=(dimension,370), color=(64, 68, 75))
    # Place area map onto the new image
    im.paste(mapIm, (0,0,dimension,dimension))
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

