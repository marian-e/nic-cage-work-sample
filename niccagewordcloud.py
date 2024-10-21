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

# Filtrer les films avec Nicolas Cage dans le casting
filtered_df = df[df['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Afficher les résultats
st.subheader("Films avec Nicolas Cage dans le casting :")
st.write(filtered_df)

# Durée des films par année de sortie
st.subheader("Durée des films par année de sortie")
if 'Year' in filtered_df.columns and 'Duration (min)' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))  # Agrandir le graphique
    filtered_df.groupby('Year')['Duration (min)'].mean().plot(kind='bar', ax=ax)
    ax.set_ylabel("Durée moyenne des films (min)")
    ax.set_xlabel("Année de sortie")
    ax.set_title("Durée des films de Nicolas Cage par année de sortie")
    st.pyplot(fig)
else:
    st.write("Les colonnes 'Year' ou 'Duration (min)' ne sont pas présentes dans les données.")

# Distribution des genres
st.subheader("Distribution des genres des films")
if 'Genre' in filtered_df.columns:
    genre_counts = filtered_df['Genre'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))  # Agrandir le graphique
    genre_counts.plot(kind='bar', ax=ax)
    ax.set_ylabel("Nombre de films")
    ax.set_xlabel("Genre")
    ax.set_title("Distribution des genres des films de Nicolas Cage")
    st.pyplot(fig)
else:
    st.write("La colonne 'Genre' n'est pas présente dans les données.")

# Scatter plot des notes par réalisateur
st.subheader("Notes des films par réalisateur")
if 'Director' in filtered_df.columns and 'Rating' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))  # Agrandir le graphique
    sns.scatterplot(x='Rating', y='Director', data=filtered_df, ax=ax)
    ax.set_xlabel("Note")
    ax.set_ylabel("Réalisateur")
    ax.set_title("Notes des films de Nicolas Cage par réalisateur")
    st.pyplot(fig)
else:
    st.write("Les colonnes 'Rating' ou 'Director' ne sont pas présentes dans les données.")

# Matrice de corrélation pour les acteurs qui ont le plus souvent joué avec Nicolas Cage
st.subheader("Matrice de corrélation des acteurs ayant joué avec Nicolas Cage")
if 'Cast' in df.columns:
    # Extraire tous les acteurs des films de Nicolas Cage
    cast_list = filtered_df['Cast'].str.split(',').apply(lambda x: [actor.strip() for actor in x] if isinstance(x, list) else [])
    
    # Vérifier le contenu de cast_list
    st.write("Vérification de la liste des acteurs :")
    st.write(cast_list.head())  # Affiche les premières lignes de cast_list pour vérifier
    
    cast_explode = pd.DataFrame(cast_list.explode())
    
    # Vérifier que la colonne '0' existe après l'explosion des acteurs
    st.write("Vérification de la structure après explosion des acteurs :")
    st.write(cast_explode.head())  # Affiche les premières lignes pour voir la structure
    
    if 0 in cast_explode.columns:
        # Compter le nombre d'apparitions pour chaque acteur
        cast_counts = cast_explode[0].value_counts()

        # Garder les acteurs ayant joué avec Nicolas Cage plus d'une fois
        top_actors = cast_counts[cast_counts > 1].index

        # Filtrer uniquement les films avec ces acteurs et créer une matrice de co-occurrence
        cooccurrence_matrix = pd.DataFrame(0, index=top_actors, columns=top_actors)
        for cast in cast_list:
            present_actors = [actor for actor in cast if actor in top_actors]
            for i, actor1 in enumerate(present_actors):
                for actor2 in present_actors[i+1:]:
                    cooccurrence_matrix.at[actor1, actor2] += 1
                    cooccurrence_matrix.at[actor2, actor1] += 1

        # Tracer la matrice de corrélation
        fig, ax = plt.subplots(figsize=(12, 10))  # Agrandir la matrice
        sns.heatmap(cooccurrence_matrix, ax=ax, cmap="coolwarm", annot=True, fmt="d")
        ax.set_title("Matrice de corrélation des acteurs ayant joué avec Nicolas Cage")
        st.pyplot(fig)
    else:
        st.write("La colonne '0' n'existe pas dans le DataFrame après explosion.")
else:
    st.write("La colonne 'Cast' n'est pas présente dans les données.")

# Nuage de mots à partir des reviews
st.subheader("Nuage de mots des reviews")
if 'Review' in filtered_df.columns:
    # Concaténer toutes les reviews
    reviews_text = ' '.join(filtered_df['Review'].dropna())
    
    # Liste des mots à exclure
    stopwords = set(["the", "a", "Nicolas Cage", "he", "be", "have", "that","for","but","I","an","his","their","if","you","and","it","in","is","to","are","even","was","with","this","on","at","there","into", "or","of","not","just","all","by","not","as","film","movie","so","one","out","from","what","like","about","as","they","has","much","when","then","any","Cage","can","who","see"])
    
    # Créer le nuage de mots
    wordcloud = WordCloud(stopwords=stopwords, background_color='white', width=800, height=400).generate(reviews_text)
    
    # Afficher le nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Ne pas afficher les axes
    st.pyplot(plt)
else:
    st.write("La colonne 'Review' n'est pas présente dans les données.")
