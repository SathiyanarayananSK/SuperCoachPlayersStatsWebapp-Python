# Import necessary libraries and files
import streamlit as st
import pandas as pd
import backend

st.set_page_config(layout="wide", page_title="SuperCoach NRL Stats")

# Display the title of the app
st.title("Super Coach Players Stats")

# Get user inputs for year and round
st.sidebar.title("Select Year and Round")
year = st.sidebar.number_input("Enter Year", min_value=2024, max_value=2030, value=2024, step=1)
round_number = st.sidebar.number_input("Enter Round", min_value=0, max_value=27, value=0, step=1)

players_summary, players_stats, players_position = ([],[],[])

# Try fetching data and handle potential exceptions
try:
    # Get players data from the API for the input year and round
    players_summary, players_stats, players_position = backend.get_players_data(year=year, rnd=round_number)

    # make data flat
    players_summary_flat = backend.make_data_flat(players_summary)

    # Create Dataframe
    players_summary_df = pd.DataFrame(players_summary_flat)

except Exception as e:
    st.write("No data found!")
    players_summary_df = pd.DataFrame()



# Display the structured dataframe
st.header(f"Player Details for Year: {year} and Round:{round_number}")
st.dataframe(players_summary_df, use_container_width=True)

st.sidebar.title("Players Stats and Positions")

with st.sidebar:
    # Create two columns for the Stats and Position buttons
    col1, col2 = st.columns([1, 1])

    # Track which button was clicked
    stats_clicked = False
    position_clicked = False

    with col1:
        if st.button('Players stats'):
            stats_clicked = True

    with col2:
        if st.button('Players position'):
            position_clicked = True

# Display data based on button clicks
if stats_clicked:
    st.header("Players Stats")
    try:
        players_stats_flat = backend.make_data_flat(players_stats)
        players_stats_df = pd.DataFrame(players_stats_flat)
        st.dataframe(players_stats_df, use_container_width=True)
    except Exception as e:
        st.write("No Data found!")
        players_stats_df = pd.DataFrame()
        st.dataframe(players_stats_df, use_container_width=True)

if position_clicked:
    st.header("Players Position")
    try:
        players_position_flat = backend.make_data_flat(players_position)
        players_position_df = pd.DataFrame(players_position_flat)
        st.dataframe(players_position_df, use_container_width=True)
    except Exception as e:
        st.write("No data found!")
        players_position_df = pd.DataFrame()
        st.dataframe(players_position_df, use_container_width=True)