import numpy as np #arrays
import pandas as pd #dataframes
import PIL #image analysis
from PIL import Image
import glob #for getting list of files in a directory
import os #for file paths


#converts arrays into image compatible form then exports it as image with a specified file name
def export(array, string):
        img = PIL.Image.fromarray(array.astype(np.uint8))
        img.save(string)


# stacks the a list of images into a single array and then divides them by the number of images to average them.
def stack(list):
     return (np.add.reduce(np.array(list).astype(np.uint16))/len(list))


def materialList(search):
     materials = []
     addresses = glob.glob(search)
     for address in addresses:
          materials.append(address)
     return materials
     

base = input("Enter the path to the Sand Images Folder:")
materials = []
item = input("Enter a material to be composited, if no more to add enter 'None':")
while item != "None":
    materials.append(item)
    item = input("Enter a material to be composited:")
    

materialPaths = []
for material in materials:
    searchPath = os.path.join(base, '*' + material + '*')
    materialPaths.extend(materialList(searchPath))

for material in materialPaths:
    combName = os.path.basename(material)
    composite = os.path.join(base, 'Composites', combName)
    if os.path.exists(composite) == False:
        os.mkdir(composite)

    # Loop that finds the directoy of all the image folders inside the category folder
    for wavelength in next(os.walk(material))[1]:
        wave_dir = os.path.join(base, combName, wavelength)

        # Setting up the file pathing to for result files, Wet Sand(dirname)/Composites/MaterialType-Condition(basename)/wavelength
        pre_path = os.path.join(composite, wavelength)
        
        # Prepares a list for the pictures to be stored in and then unloads all the pictures in an image folder into it
        pictures = []
        pictures.clear()
        for picture in glob.glob(os.path.join(wave_dir, '*')):
            pictures.append(np.array(PIL.Image.open(picture)).astype(np.uint16))

        # finds all images in the folder, then stacks and averages files w/ type conversion to prevent overflows
        imageArrays = [picture for picture in pictures if (picture.sum()/picture.size) > 10]
        imageStack = stack(imageArrays)

        # stacks and averages all static images, and if static images were present, it subtracts the static average from theimage average
        # tags the filename if subtraction occured.
        staticArrays = [picture for picture in pictures if (picture.sum()/picture.size) < 10]
        if len(staticArrays) > 0:
            staticStack = stack(staticArrays)
            resultStack = imageStack - staticStack
            fileName = pre_path + '-.tiff' 
            export(resultStack, fileName)
        else:
            fileName = pre_path + '.tiff'
            export(imageStack, fileName)

        print(fileName)