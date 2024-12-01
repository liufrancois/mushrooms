import requests, csv, warnings
from bs4 import BeautifulSoup
import pandas as pd
warnings.filterwarnings("ignore")

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

def extract_mushroom_links(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    mushroom_links = []
    for a in soup.find_all('a', href=True):
        if 'https://ultimate-mushroom.com/' in a['href']:
            mushroom_links.append(a['href'])
    return mushroom_links

def write_mushrooms_to_csv(links, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])  # En-tête du CSV
        for link in links:
            writer.writerow([link])

def ajout_indicateur_colonne(df, nom_colonne):
    valeur_unique = pd.unique(df[nom_colonne].str.split("-").explode().dropna())
    
    for value in valeur_unique:
        df[f"{nom_colonne}_{value}"] = df[nom_colonne].str.contains(value, na=False).astype(int)

    


    #print(champignons.head())

def transformation_dataset(chemin_fichier_csv):
    champignons = pd.read_csv(chemin_fichier_csv)
    #print(champignons.head())

    #print(champignons["TYPE"].value_counts(dropna=False))

    champignons["TYPE"] = champignons["TYPE"].replace({"E": 0, "I": 1, "P": 2})
    champignons["TYPE"] = champignons["TYPE"].fillna(-1)

    #print(champignons.head())
    #print(champignons["TYPE"].value_counts(dropna=False))

    # Liste des couleurs individuelles présente dans le jeu de données 

    couleurs_individuelles = pd.unique(champignons["COLOR"].str.split("-").explode().dropna())

    print(couleurs_individuelles)

    print(f"Nombre total de couleurs uniques : {len(couleurs_individuelles)}")


    # Création d'un dataframe de toutes les couleurs individuelles

    colors_list = [
        {"Color": "Pale", "R": 240, "G": 221, "B": 215},
        {"Color": "White", "R": 255, "G": 255, "B": 255},
        {"Color": "Yellow", "R": 255, "G": 255, "B": 0},
        {"Color": "Brown", "R": 165, "G": 42, "B": 42},
        {"Color": "Pink", "R": 255, "G": 192, "B": 203},
        {"Color": "Purple", "R": 128, "G": 0, "B": 128},
        {"Color": "Tan", "R": 210, "G": 180, "B": 140},
        {"Color": "Orange", "R": 255, "G": 165, "B": 0},
        {"Color": "Gray", "R": 128, "G": 128, "B": 128},
        {"Color": "Red", "R": 255, "G": 0, "B": 0},
        {"Color": "Black", "R": 0, "G": 0, "B": 0}, #Dark
        {"Color": "Green", "R": 0, "G": 128, "B": 0},
        {"Color": "Blue", "R": 0, "G": 0, "B": 255},
        {"Color": "Violet", "R": 238, "G": 130, "B": 238},
        {"Color": "Lilac", "R": 200, "G": 162, "B": 200}
    ]

    colors_df = pd.DataFrame(colors_list)

    #print(colors_df)

    # Création d'un dataframe de toutes les couleurs conbinées ( ex red + green )

    couleurs_combinees = champignons[champignons['COLOR'].str.count('-') > 0]
    combinaisons_uniques = couleurs_combinees['COLOR'].unique()
    colors = pd.DataFrame({'Combined_Color': combinaisons_uniques})

    #print(colors)

    ajout_indicateur_colonne(champignons, "SHAPE")
    ajout_indicateur_colonne(champignons, "SURFACE")

    champignons = champignons.drop(['SHAPE', 'SURFACE'], axis=1)

    # Jointure de couleurs unique pour afficher les différentes couleurs conbinée

    colors['Color1'] = colors['Combined_Color'].str.split('-').str.get(0)
    colors['Color2'] = colors['Combined_Color'].str.split('-').str.get(1)

    merge_1 = colors.merge(colors_df, left_on='Color1', right_on='Color', suffixes=('', '_1'))
    merge_2 = merge_1.merge(colors_df, left_on='Color2', right_on='Color', suffixes=('', '_2'))

    merge_2['R_mean'] = merge_2[['R', 'R_2']].mean(axis=1)
    merge_2['G_mean'] = merge_2[['G', 'G_2']].mean(axis=1)
    merge_2['B_mean'] = merge_2[['B', 'B_2']].mean(axis=1)

    colors = merge_2[['Combined_Color', 'R_mean', 'G_mean', 'B_mean']]

    #print(colors)

    # Suppression de la collone COLOR maintenant devenu inutile
    champignons = champignons.merge(colors[['Combined_Color', 'R_mean', 'G_mean', 'B_mean']], how='left', left_on='COLOR', right_on='Combined_Color')
    champignons.rename(columns={'R_mean': 'R', 'G_mean': 'G', 'B_mean': 'B'}, inplace=True)
    champignons.drop(columns=['COLOR', 'Combined_Color'], inplace=True)
    champignons[['R', 'G', 'B']] = champignons[['R', 'G', 'B']].fillna(-255)

    return champignons
    