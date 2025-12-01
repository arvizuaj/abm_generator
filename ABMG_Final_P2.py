import pandas as pd
import streamlit as st

base_url = "https://image.tmdb.org/t/p/w500"

#For local execution:
#lbox_all = pd.read_csv("C:\\Users\\andre\\OneDrive\\Documents\\Py\\Answering Unimportant Qs With Data\\Andrew's Biased Movie Generator (ABMG)\\Outputs\\ABMG_Cleaned_Data.csv")

#For production:
lbox_all = pd.read_csv("data/ABMG_Cleaned_Data.csv")

genres = ["","Comedy", "Drama", "Action", "Adventure", "Science Fiction", "Crime", "Fantasy", "Family", "Romance", "Thriller",
         "History", "Animation", "Horror", "Music", "War", "Mystery","Documentary"]
decade = ["<1980", "1980 - 1989", "1990 - 1999", "2000 - 2009", "2010 - 2019", "2020+"]


st.title("Andrew's Biased Movie Generator :popcorn: :movie_camera:")
#st.image
st.markdown("Make selections below to generate a random movie from Andrew's watched films")

st.image("https://townsquare.media/site/442/files/2025/10/attachment-struzan-posters-1.jpeg?w=780&q=75",use_container_width=True)


#USER MAKES A SELECTION FOR A GENRE
st.subheader("Genre")
selected_genre = st.selectbox("Select a genre of interest",genres)

#USER MAKES A SELECTION FOR A MAX RUNTIME
st.subheader("Runtime")
input_runtime = st.slider("Select a runtime range (in minutes) of interest", min_value=0,max_value=300,value=(0,150),step=10)
min_runtime, max_runtime = input_runtime

#USER MAKES A SELECTION FOR A TIME FRAME
st.subheader("Years")
selected_time = st.multiselect("Select decade(s) of interest ",decade)

#USER MAKES A SELECTION FOR Rating
st.subheader("Rating")
input_rating = st.slider("Select a rating range of interest", min_value=0,max_value=10,value=(0,10),step=1)
min_rating, max_rating = input_rating

st.markdown("---")

final_df = lbox_all[lbox_all["genres"].str.contains(selected_genre, case=False, na=False)]
final_df = final_df[(final_df["runtime"] >= min_runtime) & (final_df["runtime"] <= max_runtime)]
final_df = final_df[final_df["decade"].isin(selected_time)]
final_df = final_df[(final_df["Rating_Integer"] >= min_rating) & (final_df["Rating_Integer"] <= max_rating)]

final_df = final_df[["Name","lbox_year","Letterboxd URI", "lbox_rating", "poster_path","overview","tagline"]]


if selected_time and len(final_df) > 2:

    final_sp = final_df.sample(n=3)

    for Name, Year, Rating, Poster, Description in zip(final_sp["Name"],final_sp["lbox_year"],final_sp["lbox_rating"],final_sp["poster_path"],final_sp["overview"]):
    
        col1, col2 = st.columns([1,2])

        with col1:
            st.image(f"{base_url}{Poster}",width=100)

        with col2:
            if (Rating == '9/10' or Rating == '10/10'):
                st.subheader(f":dvd: {Name}")
            else:
                st.subheader(Name)
            st.write(f":calendar: **Release Year:** {Year}")
            st.write(f":star: **Andrew's Rating:** {Rating}")
            if Description:
                st.write(f":writing_hand: **Description:** {Description}")
    
        st.markdown("---")

elif selected_time and len(final_df) > 0:

    final_sp = final_df

    for Name, Year, Rating, Poster, Description in zip(final_sp["Name"],final_sp["lbox_year"],final_sp["lbox_rating"],final_sp["poster_path"],final_sp["overview"]):
    
        col1, col2 = st.columns([1,2])

        with col1:
            st.image(f"{base_url}{Poster}",width=100)

        with col2:
            if (Rating == '9/10' or Rating == '10/10'):
                st.subheader(f":dvd: {Name}")
            else:
                st.subheader(Name)
            st.write(f":calendar: **Release Year:** {Year}")
            st.write(f":star: **Andrew's Rating:** {Rating}")
            if Description:
                st.write(f":writing_hand: **Description:** {Description}")

        st.markdown("---")


elif selected_time and len(final_df) == 0:
    st.subheader("Andrew is uncultured and hasn't seen any movies that match your search!")

if selected_time:
    st.button(label=":boom: Generate :boom:",key='random_widget',type="secondary",use_container_width=True)