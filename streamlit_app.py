# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Titre de l'application
st.set_page_config(
    page_title="Mon Application Streamlit",  
    page_icon="📊",  
    layout="wide" 
)

st.title("Exploration Interactive des Données avec Streamlit")

# Étape 1 : Charger une base de données
st.header("1. Charger votre Base de Données")

# Widget pour charger un fichier
uploaded_file = st.file_uploader("Chargez votre fichier CSV ici :", type=["csv"])

if uploaded_file is not None:
    # Lire le fichier CSV dans un DataFrame
    df = pd.read_csv(uploaded_file)
    
    st.write("Aperçu des 5 premières lignes :")
    st.write(df.head())
    
    # Étape 2 : Afficher des informations sur la base de données
    st.header("2. Informations sur les Données")

    # Dimensions et statistiques descriptives
    st.subheader("Dimensions et statistiques descriptives")
    st.write(f"Nombre de lignes et colonnes : {df.shape}")
    st.write(df.describe())

    # Afficher les colonnes disponibles
    st.write("Colonnes disponibles :")
    st.write(df.columns.tolist())
    
    # Filtrage interactif (si la base a des colonnes pertinentes)
    if st.checkbox("Filtrer les données"):
        column = st.selectbox("Choisissez une colonne pour le filtrage :", df.columns)
        unique_values = df[column].unique()
        filter_value = st.selectbox(f"Choisissez une valeur dans {column} :", unique_values)
        filtered_data = df[df[column] == filter_value]
        st.write(filtered_data)

    # Étape 3 : Graphiques
    st.header("3. Visualisations Graphiques")

    # Graphique Pairplot (si la base de données contient au moins deux colonnes numériques)
    if st.checkbox("Afficher un Pairplot des colonnes numériques"):
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) > 1:
            sns.pairplot(df, diag_kind="kde", corner=True)
            st.pyplot()
        else:
            st.write("La base de données ne contient pas assez de colonnes numériques pour un Pairplot.")

    # Histogramme d'une caractéristique
    st.subheader("Distribution d'une caractéristique")
    column = st.selectbox("Choisissez une colonne numérique :", df.select_dtypes(include=['float64', 'int64']).columns)
    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, bins=20, ax=ax)
    ax.set_title(f"Distribution de {column}")
    st.pyplot(fig)

    # Graphique scatter interactif
    st.subheader("Relation entre deux caractéristiques")
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) >= 2:
        x_axis = st.selectbox("Choisissez l'axe X :", numeric_columns)
        y_axis = st.selectbox("Choisissez l'axe Y :", numeric_columns)

        fig, ax = plt.subplots()
        sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        ax.set_title(f"{x_axis} vs {y_axis}")
        st.pyplot(fig)
    else:
        st.write("Pas assez de colonnes numériques pour afficher un graphique scatter.")
else:
    st.write("Veuillez charger un fichier CSV pour continuer.")
