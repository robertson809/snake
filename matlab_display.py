import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from numpy.random import random

fig = plt.figure()
matrix = random((50,50))
im = plt.imshow(matrix, interpolation='nearest', cmap=cm.Spectral)

def update(data):
    im.set_array(data)

def data_gen():
    while True: 
        yield random((50,50))

ani = animation.FuncAnimation(fig, update, data_gen, interval=1000)

plt.show()