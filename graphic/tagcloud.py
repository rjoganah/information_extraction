'''
Created on 26 sept. 2016

@author: jogr0001
'''
#!/usr/bin/env python
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS
import matplotlib.image as mpimg

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(80, 100)

def create_tag_cloud(text,filename):
    d = path.dirname(__file__)
    # Generate a word cloud image)
    wc = WordCloud(background_color='white',max_words=20, margin=2, max_font_size=20).generate(text)
    # store default colored image
    default_colors = wc.to_array()
    plt.title("Custom colors")
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
    wc.to_file(filename + ".png")
    plt.close()
    #===========================================================================
    # plt.axis("off")
    # plt.figure()
    # plt.title("Default colors")
    # plt.imshow(default_colors)
    # plt.axis("off")
    # plt.show()
    #===========================================================================


