'''
Created on 11 oct. 2016

@author: jogr0001
'''
import wikipedia
from unidecode import unidecode

def has_wikipedia_page(NE):
    list_wiki = (wikipedia.search(NE, 10))
    if NE in list_wiki:
        print(list_wiki)
        return True
    return False


if __name__ == '__main__':
    print(has_wikipedia_page('Fig'))