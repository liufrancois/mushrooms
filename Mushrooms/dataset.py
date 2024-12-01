from pathlib import Path
import csv
import typer
from loguru import logger
from tqdm import tqdm

from scraper import comestible, color, shape, surface
from scraper import extract_mushroom_links, write_mushrooms_to_csv, transformation_dataset
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
import time
app = typer.Typer()

@app.command()
def main(
    mushroom_list_url: str = 'https://ultimate-mushroom.com/mushroom-alphabet.html',
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",  # Fichier CSV de sortie
):
    logger.info("Extracting mushroom links...")
    t = time.time()

    mushroom_links = extract_mushroom_links(mushroom_list_url)
    
    write_mushrooms_to_csv(mushroom_links, 'champignons.csv')

    logger.info("Processing dataset...")

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
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
                if (t > time.time() + 15):
                    break

                print(f"Champignon {count} traité.")
            except Exception as e:
                print(f"Erreur lors du traitement de l'URL {url}: {e}")

        print(f"Tous les champignons ont été traités. Nombre total : {count}")

    logger.success("Debut de la transformation du dataset.")
    champignons = transformation_dataset(output_path)
    champignons.to_csv(PROCESSED_DATA_DIR / 'dataset.csv', index=False)

    logger.success("Processing dataset complete.")

if __name__ == "__main__":
    app()
