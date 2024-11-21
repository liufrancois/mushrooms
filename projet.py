import requests
from bs4 import BeautifulSoup

#ex1
def comestible(url):
    categorie = url.split("/")[-2]
    if "edible" in categorie:
        return "E"
    elif "inedible" in categorie:
        return "I"
    elif "poisonous" in categorie:
        return "P" 
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

url = "https://ultimate-mushroom.com/poisonous/1176-trogia-venenata.html"
couleur = color(url)
print("Couleur du champignon :", couleur)





