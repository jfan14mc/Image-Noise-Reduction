import numpy as np #
import pandas as pd #dataframes
import PIL #image analysis
from PIL import Image
import glob #for getting list of files in a directory
import os #for file paths

# /Users/fanjx1/Documents/Sand Images/Anthracite-Dry
# Category folder to be searched through
path = input('Enter the category folder path (format is ...Sand Images/MaterialName-Liquid):')

# Loop that finds the directoy of all the image forlders inside the category folder
for wavelength in next(os.walk(path))[1]:
    wave_dir = os.path.join(path, wavelength)
    
    # Prepares a list for the pictures to be stored in and then unloads all the pictures in an image folder into it
    pictures = []
    pictures.clear()
    for picture in glob.glob(wave_dir + '/*'):
        pictures.append(np.array(PIL.Image.open(picture)).astype(np.uint16))

    
    imageArrays = [picture for picture in pictures if (picture.sum()/picture.size) > 10]
    count = len(imageArrays)
    print((np.add.reduce(np.array(imageArrays))/count).astype(np.uint8))
    print(wave_dir, 'images')

    # # Stacking and counting the pictures. Pictures are filtered by their higher average brightness than static images
    # for image in pictures:   
    #     if image.sum()/size > 10: 
    #         interest += image
    #         interestCount += 1
            
    # # Static image array preparation. 
    # statics = np.zeros(pictures[0].shape) 
    # staticCount = 0 
    
    # # Stacking and counting static images.
    # for static in pictures:
    #     if static.sum()/size < 10: 
    #         statics += static
    #         staticCount += 1
    
    # # Setting up the file pathing to for result files
    # sand_images = os.path.dirname(path) 
    # category = os.path.basename(path)
    # pre_path = os.path.join(sand_images, 'Composites', category, wavelength)

    # # if/else averages images, also checks to see if there are static images that can be subtracted from the main images and operates accordingly
    # # Image file names are marked with a '-' if were subtracted from
    # if staticCount < 1:
    #     result = (interest/interestCount).astype(np.uint8)
    #     img = PIL.Image.fromarray(result)
    #     fileName = pre_path + '.png'
    #     img.save(fileName)
    #     print(fileName + 'processed')

    # else:
    #     result = (interest/interestCount).astype(np.uint8) - (statics/staticCount).astype(np.uint8)
    #     img = PIL.Image.fromarray(result)
    #     fileName = pre_path + '-.png'
    #     img.save(fileName)
    #     print(fileName, 'processed')

