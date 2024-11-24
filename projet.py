import requests
from bs4 import BeautifulSoup
import csv

def comestible(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    i_element = soup.find('i', class_=["poisonous", "eat", "inedible"])
    if i_element:
        if "poisonous" in i_element['class']:
            return "P"
        elif "eat" in i_element['class']:
            return "E"
        elif "inedible" in i_element['class']:
            return "I"

    return ""

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

def csv_champignon(url):
    type_champignon = comestible(url)
    color_champignon = color(url)
    shape_champignon = shape(url)
    surface_champignon = surface(url)

    return f"{type_champignon},{color_champignon},{shape_champignon},{surface_champignon}"

def extract_mushroom_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    mushroom_links = []
    for a in soup.find_all('a', href=True):
        if 'https://ultimate-mushroom.com/' in a['href']:
            mushroom_links.append(a['href'])
    return mushroom_links

def write_mushrooms_to_csv(mushroom_links, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['TYPE', 'COLOR', 'SHAPE', 'SURFACE'])
        
        for count, url in enumerate(mushroom_links, 1):
            try:
                print(f"Traitement de l'URL : {url}")
                
                champignon_type = comestible(url)
                champignon_color = color(url)
                champignon_shape = shape(url)
                champignon_surface = surface(url)
                
                print(f"Caractéristiques extraites : TYPE={champignon_type}, COLOR={champignon_color}, SHAPE={champignon_shape}, SURFACE={champignon_surface}")
                
                writer.writerow([champignon_type, champignon_color, champignon_shape, champignon_surface])
                file.flush()

                print(f"Champignon {count} traité.")
            except Exception as e:
                print(f"Erreur lors du traitement de l'URL {url}: {e}")

        print(f"Tous les champignons ont été traités. Nombre total : {count}")

mushroom_list_url = 'https://ultimate-mushroom.com/mushroom-alphabet.html'
mushroom_links = extract_mushroom_links(mushroom_list_url)
write_mushrooms_to_csv(mushroom_links, 'champignons.csv')
   
