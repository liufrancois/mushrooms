import requests
from bs4 import BeautifulSoup
import csv

#ex1
def comestible(url):
    contenu = requests.get(url)
    contenu.raise_for_status()

    soup = BeautifulSoup(contenu.content, 'html.parser')
    
    a_elements = soup.find_all('a', href=True)
    for a in a_elements:
        i_element = a.find('i')
        if i_element:
            if "poisonous" in i_element.get('class', []):
                return "P"
            elif "edible" in i_element.get('class', []):
                return "E"
            elif "inedible" in i_element.get('class', []):
                return "I"

    return ""

#ex2
def color(url):
    contenu = requests.get(url)
    contenu.raise_for_status()

    soup = BeautifulSoup(contenu.content, 'html.parser')
    
    color_paragraphs = soup.find_all('p')
    for paragraph in color_paragraphs:
        if 'Color:' in paragraph.text:
            a_elements = paragraph.find_all('a')
            colors = [a.text for a in a_elements if a.text.strip()]
            return '-'.join(colors)
    return ''

#ex3
def shape(url):
    contenu = requests.get(url)
    contenu.raise_for_status()

    soup = BeautifulSoup(contenu.content, 'html.parser')

    strong_elements = soup.find_all('p')
    for strong in strong_elements:
        if 'Shape:' in strong.text:
            next_a = strong.find_next('a')
            if next_a:
                shape_text = next_a.text.replace(" ", "").replace("-", "")
                return shape_text
    return ''

def surface(url):
    contenu = requests.get(url)
    contenu.raise_for_status()

    soup = BeautifulSoup(contenu.content, 'html.parser')

    p_elements = soup.find_all('p')
    for p in p_elements:
        if 'Surface:' in p.text:
            next_a = p.find_next('a')
            if next_a:
                surface_text = next_a.text.replace(" ", "").replace("-", "")
                return surface_text
    return ''

#ex4
def csv_champignon(url):
    type_champignon = comestible(url)
    color_champignon = color(url)
    shape_champignon = shape(url)
    surface_champignon = surface(url)

    return f"{type_champignon},{color_champignon},{shape_champignon},{surface_champignon}"
   