import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Titre de l'application
st.title("Filtrage des films avec Nicolas Cage et Visualisations")

# Charger les données CSV
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Chemin vers ton fichier CSV
file_path = "data/imdb-movies-dataset 2.csv"

# Charger les données
df = load_data(file_path)

# Dictionnaire pour corriger les années
year_updates = {
    "Mandy": 2018,
    "The Unbearable Weight of Massive Talent": 2022,
    "The Retirement Plan": 2023,
    "Pig": 2021,
    "Leaving Las Vegas": 1995,
    "Wild at Heart": 1990,
    "Gone in Sixty Seconds": 2000,
    "Butcher's Crossing": 2023,
    "Color Out of Space": 2019,
    "National Treasure": 2004,
    "City of Angels": 1998,
    "The Croods": 2013,
    "The Sorcerer's Apprentice": 2010,
    "8MM": 1999,
    "The Family Man": 2000,
    "Running with the Devil": 2019,  # Corrigé
    "World Trade Center": 2006,      # Corrigé
    "Captain Corelli's Mandolin": 2001,  # Corrigé
    "Astro Boy": 2009,                # Corrigé
    "Red Rock West": 1992,             # Corrigé
    "Inconceivable": 2017,
    "Ghost Rider: Spirit of Vengeance": 2012,
    "Ghost Rider": 2007,
    "The Surfer": 2024,
    "Con Air": 1997,
    "Arcadian": 2024,
    "Longlegs": 2024,
    "The Old Way": 2023,
    "Knowing": 2009,
    "Trespass": 2011,
    "Moonstruck": 1987,
    "Lord of War": 2005,
    "Face/Off": 1997,
    "The Rock": 1996,
    "Valley Girl": 1983,
    "Renfield": 2023,
    "Birdy": 1984,
    "Adaptation.": 2002,
    "The Ant Bully": 2006,
    "Prisoners of the Ghostland": 2021,
    "Lords of War": 2005,
    "Stolen": 2012,
    "The Trust": 2016,
    "The Gunslingers": 2025,
    "Drive Angry": 2011,
    "National Treasure: Book of Secrets": 2007,
    "Kick-Ass": 2010,
    "The Bad Lieutenant: Port of Call - New Orleans": 2010,
    "Left Behind": 2014,
    "The Croods: A New Age": 2023,
    "Bringing Out the Dead": 1999,
    "The Weather Man": 2005,
    "Snake Eyes": 1998,
    "The Wicker Man": 2006,
    "Joe": 2013,
    "USS Indianapolis: Men of Courage": 2016,
    "It Could Happen to You": 1994,
    "Dream Scenario": 2023,
    "National Treasure": 2004,
    "Raising Arizona": 1987,
    "The Frozen Ground": 2013,
    "Season of the Witch": 2011,
    "Windtalkers": 2002,
    "Willy's Wonderland": 2021,
    "Vengeance: A Love Story": 2019,
    "Mom and Dad": 2017,
    "Army of One": 2016,
    "Matchstick Men": 2003,
    "Vampire's Kiss": 1988,
    "The Carpenter's Son": 2020,
    "Jiu Jitsu": 2020,
    "Next": 2007,
    "Wild at Heart": 1990,
    "Sympathy for the Devil": 2023,
    "Primal": 2019
}

# Mettre à jour les années dans le DataFrame
for title, new_year in year_updates.items():
    df.loc[df['Title'] == title, 'Year'] = new_year

# Filtrer les films avec Nicolas Cage dans le casting
filtered_df = df[df['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Remplacer les NaN par une valeur par défaut (ex : 0 ou une autre année)
filtered_df['Year'] = filtered_df['Year'].fillna(0).astype(int)

# Supprimer les lignes où 'Year' est NaN
filtered_df = filtered_df.dropna(subset=['Year'])

# Classer par ordre décroissant de l'année
filtered_df = filtered_df.sort_values(by='Year', ascending=False)

# Afficher les résultats
st.subheader("Films avec Nicolas Cage dans le casting :")

# Menu déroulant pour sélectionner un film
film_titles = filtered_df['Title'].tolist()
selected_film = st.selectbox("Sélectionnez un film :", film_titles)

# Afficher les détails du film sélectionné
selected_row = filtered_df[filtered_df['Title'] == selected_film].iloc[0]
st.write(f"**Titre :** {selected_row['Title']}  \n**Année :** {selected_row['Year']}  \n**Durée :** {selected_row['Duration (min)']} min  \n**Genre :** {selected_row['Genre']}  \n**Note :** {selected_row['Rating']}  \n**Réalisateur :** {selected_row['Director']}")
if 'Poster' in selected_row and pd.notna(selected_row['Poster']):
    st.image(selected_row['Poster'], width=150)
if 'Description' in selected_row and pd.notna(selected_row['Description']):
    st.write(f"**Description :** {selected_row['Description']}")  # Afficher la description

# Durée des films par année de sortie
st.subheader("Durée des films par année de sortie")
if 'Year' in filtered_df.columns and 'Duration (min)' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))  # Agrandir le graphique
    filtered_df.groupby('Year')['Duration (min)'].mean().plot(kind='bar', ax=ax)
    ax.set_ylabel("Durée moyenne des films (min)")
    ax.set_xlabel("Année de sortie")
    ax.set_title("Durée des films de Nicolas Cage par année de sortie")
    st.pyplot(fig)  # Afficher le graphique
else:
    st.write("Les colonnes 'Year' ou 'Duration (min)' ne sont pas présentes dans les données.")

# Distribution des genres
st.subheader("Distribution des genres des films")
if 'Genre' in filtered_df.columns:
    # Séparer les genres en utilisant ',' comme séparateur
    genres_split = filtered_df['Genre'].str.split(',').explode().str.strip()  # Str.strip pour enlever les espaces
    genre_counts = genres_split.value_counts().head(10)  # Compter les genres et garder les 10 premiers

    fig, ax = plt.subplots(figsize=(10, 6))  # Agrandir le graphique
    genre_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel("Nombre de films")
    ax.set_xlabel("Genre")
    ax.set_title("10 Genres les plus représentés des films de Nicolas Cage")
    st.pyplot(fig)  # Afficher le graphique
else:
    st.write("La colonne 'Genre' n'est pas présente dans les données.")

# Graphique des 10 films les mieux notés de Nicolas Cage
st.subheader("Les 10 films les mieux notés de Nicolas Cage")
if 'Rating' in filtered_df.columns and 'Title' in filtered_df.columns:
    # Sélectionner les 10 films avec la note la plus élevée
    top_rated_films = filtered_df[['Title', 'Rating']].sort_values(by='Rating', ascending=False).head(10)

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Rating', y='Title', data=top_rated_films, ax=ax, palette='viridis')

    # Ajouter une flèche pour indiquer la meilleure note
    max_rating = top_rated_films['Rating'].max()
    ax.annotate(
        'Meilleure note',
        xy=(max_rating, top_rated_films['Title'].iloc[0]), 
        xytext=(max_rating + 0.5, top_rated_films['Title'].iloc[0]),  # Position de la flèche
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        fontsize=10,
        color='black'
    )

    # Configurer les labels et le titre
    ax.set_xlabel("Note")
    ax.set_ylabel("Titre")
    ax.set_title("Les 10 films les mieux notés de Nicolas Cage")
    st.pyplot(fig)  # Afficher le graphique
else:
    st.write("Les colonnes 'Rating' ou 'Title' ne sont pas présentes dans les données.")

# Nuage de mots des acteurs présents dans le cast
st.subheader("Nuage de mots des acteurs présents dans le cast (hors Nicolas Cage)")
if 'Cast' in filtered_df.columns:
    # Concaténer tous les noms dans la colonne 'Cast'
    cast_text = ' '.join(filtered_df['Cast'].dropna())

    # Exclure "Nicolas Cage" des noms
    cast_text = cast_text.replace("Nicolas Cage", "")

    # Séparer les noms et créer une liste
    cast_names = cast_text.split(',')

    # Nettoyer les espaces et convertir en minuscules
    cast_names = [name.strip() for name in cast_names]

    # Compter la fréquence des noms
    name_counts = pd.Series(cast_names).value_counts()

    # Créer le nuage de mots avec les noms les plus fréquents
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(name_counts)

    # Afficher le nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Ne pas afficher les axes
    st.pyplot(plt)  # Afficher le nuage de mots
else:
    st.write("La colonne 'Cast' n'est pas présente dans les données.")

