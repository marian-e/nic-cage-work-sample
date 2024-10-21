import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# App title
st.title("Nicolas Cage: The Summary of a Legend")

# CSV download
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Path through CSV
file_path = "data/imdb-movies-dataset 2.csv"

# Download data
df = load_data(file_path)

# Correction of the CSV
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
    "Running with the Devil": 2019,  # Corrected
    "World Trade Center": 2006,      # Corrected
    "Captain Corelli's Mandolin": 2001,  # Corrected
    "Astro Boy": 2009,                # Corrected
    "Red Rock West": 1992,             # Corrected
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

# Data updates
for title, new_year in year_updates.items():
    df.loc[df['Title'] == title, 'Year'] = new_year

# Filter films with Nicolas Cage
filtered_df = df[df['Cast'].str.contains("Nicolas Cage", case=False, na=False)]

# Replace NaN with "unknown" for Duration and "unknown" for Rating
filtered_df['Duration (min)'] = filtered_df['Duration (min)'].fillna("unknown")
filtered_df['Rating'] = filtered_df['Rating'].fillna("unknown")  # Replace NaN with "unknown"

# Replace NaN for Year with 0 and convert to int
filtered_df['Year'] = filtered_df['Year'].fillna(0).astype(int)

# NaN suppression
filtered_df = filtered_df.dropna(subset=['Year'])

# Ranking
filtered_df = filtered_df.sort_values(by='Year', ascending=False)

# Display results
st.subheader("Films Featuring Nicolas Cage:")

# Menu
film_titles = filtered_df['Title'].tolist()
selected_film = st.selectbox("Select a film:", film_titles)

# Details
selected_row = filtered_df[filtered_df['Title'] == selected_film].iloc[0]
st.write(f"**Title:** {selected_row['Title']}  \n**Year:** {selected_row['Year']}  \n**Duration:** {selected_row['Duration (min)']} min  \n**Genre:** {selected_row['Genre']}  \n**Rating:** {selected_row['Rating']}  \n**Director:** {selected_row['Director']}")
if 'Poster' in selected_row and pd.notna(selected_row['Poster']):
    st.image(selected_row['Poster'], width=150)
if 'Description' in selected_row and pd.notna(selected_row['Description']):
    st.write(f"**Description:** {selected_row['Description']}")  

# Duration of the films
st.subheader("Duration of Films by Year of Release")
if 'Year' in filtered_df.columns and 'Duration (min)' in filtered_df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))  
    # Check if 'unknown' values need to be handled for duration
    filtered_df['Duration (min)'] = pd.to_numeric(filtered_df['Duration (min)'], errors='coerce')
    filtered_df.groupby('Year')['Duration (min)'].mean().plot(kind='bar', ax=ax)
    ax.set_ylabel("Average Duration of Films (min)")
    ax.set_xlabel("Year of Release")
    ax.set_title("Duration of Nicolas Cage Films by Year of Release")
    st.pyplot(fig)  
else:
    st.write("The columns 'Year' or 'Duration (min)' are not present in the data.")

# Distribution of genres
st.subheader("Distribution of Film Genres")
if 'Genre' in filtered_df.columns:
    genres_split = filtered_df['Genre'].str.split(',').explode().str.strip()  
    genre_counts = genres_split.value_counts().head(10)  

    fig, ax = plt.subplots(figsize=(10, 6))  
    genre_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel("Number of Films")
    ax.set_xlabel("Genre")
    ax.set_title("Top 10 Most Represented Genres in Nicolas Cage Films")
    st.pyplot(fig)  
else:
    st.write("The column 'Genre' is not present in the data.")

# Top 10 ranked movies
st.subheader("The 10 Highest Rated Movies of Nicolas Cage")
if 'Rating' in filtered_df.columns and 'Title' in filtered_df.columns:
    # Convert Rating to numeric, handling 'unknown' as NaN
    filtered_df['Rating'] = pd.to_numeric(filtered_df['Rating'].replace("unknown", pd.NA), errors='coerce')
    top_rated_films = filtered_df[['Title', 'Rating']].sort_values(by='Rating', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Rating', y='Title', data=top_rated_films, ax=ax, palette='viridis')

    if not top_rated_films.empty:
        max_rating = top_rated_films['Rating'].max()
        ax.annotate(
            'Highest Rating',
            xy=(max_rating, top_rated_films['Title'].iloc[0]), 
            xytext=(max_rating + 0.5, top_rated_films['Title'].iloc[0]),  # Arrow position
            arrowprops=dict(facecolor='black', arrowstyle='->'),
            fontsize=10,
            color='black'
        )

    ax.set_xlabel("Rating")
    ax.set_ylabel("Title")
    ax.set_title("The 10 Highest Rated Movies of Nicolas Cage")
    st.pyplot(fig)  
else:
    st.write("The columns 'Rating' or 'Title' are not present in the data.")

# Word cloud for cast excluding Nicolas Cage
st.subheader("Word Cloud of Cast Members (Excluding Nicolas Cage)")
if 'Cast' in filtered_df.columns:
    cast_series = filtered_df['Cast'].str.replace("Nicolas Cage", "").str.cat(sep=', ')
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cast_series)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)  
else:
    st.write("The column 'Cast' is not present in the data.")
