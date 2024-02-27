import os

import pandas as pd

import cv2
import image_slicer


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure -- the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()


images = os.listdir("images")
images = [os.path.join("images",i) for i in images]

threshold = 300

df = pd.DataFrame()
tile_df = pd.DataFrame()

for image_path in images:

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)

    if fm < threshold:
        text = "Blurry"
    else:
        text = "Not Blurry"


    print('-----------------------------------------------------')
    print(image_path)
    print('focus measure', fm)     
    print('result', text)
    print("\n")
    
    data = pd.DataFrame({"image": image_path, "lapVar": fm, "result": text},index=[0])
    df = pd.concat([df, data])

    # check individual tiles if not blurry
    if text == "Not Blurry":
        
        print("checking image tiles")
        
        tiles = image_slicer.slice(image_path, 4, save=False)
        image_slicer.save_tiles(tiles, directory='tiles',\
                            prefix='slice', format='png')

        tiles = os.listdir("tiles")
        tile_paths = [os.path.join("tiles",i) for i in tiles]

        for tp in tile_paths:

            image_tile = cv2.imread(tp)
            gray = cv2.cvtColor(image_tile, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)

            if "1_" in tp:
                tile_row = "upper"
            else:
                tile_row = "lower"
            if "_01." in tp:
                tile_col = "left"
            else:
                tile_col = "right"
            
            if fm < threshold:
                result = "blurry"
            else:
                result = "not blurry"
            text = tile_row + ' ' + tile_col + ' ' + "tile is" + ' ' + result
            
            tile = tile_row + ' ' + tile_col 
            tile_data = pd.DataFrame({"image": image_path, "tile": tile, "lapVar": fm, "result": result},index=[0])
            tile_df = pd.concat([tile_df, tile_data])

            print('--- --- --- --- --- --- --- --- ---')
            print(tp)
            print('focus measure', fm)     
            print(text)
            print("\n")

        # delete tiles
        for filename in os.listdir('tiles'):
            file_path = os.path.join('tiles', filename)
            os.unlink(file_path)

full_df = df.merge(tile_df, left_on = 'image', right_on = 'image', how="left")
full_df.sort_values(["image","tile"])