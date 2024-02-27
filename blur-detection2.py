#!/Users/peerchristensen/miniconda3/envs/blur_detection

from skimage.measure import blur_effect
import skimage as ski
import os

images = os.listdir("images")
images = [os.path.join("images",i) for i in images]
img = ski.io.imread(images[5])
blur_effect(img)
ski.io.imshow(img)

'''for i in images:
    img = ski.io.imread(i)
    blur_effect(img)'''

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.imshow(img)
plt.show()
