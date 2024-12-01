import pickle
import typer
import sys
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from loguru import logger

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

@app.command()
def predict(
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",      # Le fichier des features d'entraînement
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",          # Le fichier des labels d'entraînement
    model_path: Path = MODELS_DIR / "model.pkl",                    # Le modèle pré-entraîné
    predictions_path: Path = PROCESSED_DATA_DIR / "predictions.csv",# Où enregistrer les prédictions
):
    """
    Effectuer des prédictions sur le jeu de test en recréant le même split que dans train.py.
    """
    logger.info("Chargement des données d'entraînement...")
    # Charger les données d'entraînement
    features = pd.read_csv(features_path)
    labels = pd.read_csv(labels_path)
    champignons = pd.concat([features, labels], axis=1)

    # Préparer les données
    X = champignons.drop('TYPE', axis=1)
    y = champignons['TYPE']

    # Recréer le même split que dans train.py
    logger.info("Recréation du jeu de test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=1
    )

    # Standardisation des données via StandardScaler
    logger.info("Mise à l'échelle des données...")
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Charger le modèle pré-entraîné
    logger.info("Chargement du modèle pré-entraîné...")
    with open(model_path, "rb") as file:
        model = pickle.load(file)

    # Vérifier que le nombre de features correspond
    if X_test_scaled.shape[1] != model.n_features_in_:
        logger.error(
            f"Le nombre de features dans les données de test ({X_test_scaled.shape[1]}) "
            f"ne correspond pas au nombre attendu ({model.n_features_in_})."
        )
        sys.exit(1)

    # Appliquer le modèle pour faire des prédictions
    logger.info("Prédictions en cours...")
    predictions = model.predict(X_test_scaled)

    # Sauvegarder les prédictions dans un fichier CSV
    logger.info(f"Enregistrement des prédictions dans {predictions_path}...")
    predictions_df = pd.DataFrame({
        "Prediction": predictions,
        "Actual": y_test.reset_index(drop=True)
    })
    predictions_df.to_csv(predictions_path, index=False)

    logger.success(f"Prédictions sauvegardées dans {predictions_path}")

if __name__ == "__main__":
    app()
