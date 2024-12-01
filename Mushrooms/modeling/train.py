import typer, pickle, sys, graphviz
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from loguru import logger

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
):
    """
    Entraîne un modèle de machine learning à partir des données fournies.
    """
    logger.info("Chargement des données...")
    # Charger les données
    features = pd.read_csv(features_path)
    labels = pd.read_csv(labels_path)

    # Combiner les caractéristiques et les labels
    champignons = pd.concat([features, labels], axis=1)

    # Séparation des données
    X = champignons.drop('TYPE', axis=1)
    y = champignons['TYPE']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    logger.info("Taille de l'ensemble d'entraînement : {}", len(X_train))
    logger.info("Taille de l'ensemble de test : {}", len(X_test))

    # Entraînement du modèle SVC (avec et sans mise à l'échelle)
    logger.info("Entraînement du modèle SVC...")

    # Sans mise à l'échelle
    model = SVC(random_state=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.success(f"Score de précision (SVC sans échelle) : {accuracy}")

    # Standardisation des données via StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Avec mise à l'échelle
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logger.success(f"Score de précision (SVC avec échelle) : {accuracy}")

    # Entraînement de l'arbre de décision
    logger.info("Entraînement de l'arbre de décision...")
    tree_model = DecisionTreeClassifier(max_depth=3, random_state=1)
    tree_model.fit(X_train, y_train)
    y_pred_tree = tree_model.predict(X_test)
    accuracy_tree = accuracy_score(y_test, y_pred_tree)
    logger.success(f"Score précision (Arbre de décision) : {accuracy_tree}")

    # Visualisation de l'arbre
    logger.info("Génération de la visualisation de l'arbre de décision...")
    feature_names = champignons.columns.drop('TYPE')
    export_graphviz(
        tree_model,
        out_file=str(PROCESSED_DATA_DIR / "arbre_decision.dot"),
        feature_names=feature_names,
        filled=True,
    )
    with open(PROCESSED_DATA_DIR / "arbre_decision.dot") as f:
        dot_graph = f.read()
    graphviz.Source(dot_graph).view()

    with open(MODELS_DIR / model_path, "wb") as file:
        pickle.dump(model, file)
    logger.success("Modèle SVC enregistré avec pickle.")

    logger.success("Entraînement terminé et modèles sauvegardés.")


if __name__ == "__main__":
    app()