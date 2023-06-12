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
     

# Category folder to be searched through
path = input('Enter the category folder path (format is ...Sand Images/MaterialName-Condition):')

# Loop that finds the directoy of all the image forlders inside the category folder
for wavelength in next(os.walk(path))[1]:
    wave_dir = os.path.join(path, wavelength)

    # Setting up the file pathing to for result files, Wet Sand(dirname)/Composites/MaterialType-Condition(basename)/wavelength
    pre_path = os.path.join(os.path.dirname(path), 'Composites', os.path.basename(path), wavelength)
    
    # Prepares a list for the pictures to be stored in and then unloads all the pictures in an image folder into it
    pictures = []
    pictures.clear()
    for picture in glob.glob(wave_dir + '/*'):
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
        fileName = pre_path + '-.png' 
        export(resultStack, fileName)
    else:
         fileName = pre_path + '.png'
         export(imageStack, fileName)

    print(fileName)