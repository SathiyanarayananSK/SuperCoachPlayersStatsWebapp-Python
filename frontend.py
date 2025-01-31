# Import necessary libraries and files
import streamlit as st
import pandas as pd
import backend


# Display the title of the app
st.title("Super Coach Players Stats")

# Get user inputs for year and round
st.header("Select Year and Round")
year = st.number_input("Enter Year", min_value=2024, max_value=2030, value=2024, step=1)
round_number = st.number_input("Enter Round", min_value=0, max_value=30, value=0, step=1)

# Try fetching data and handle potential exceptions
try:
    # Get players data from the API for the input year and round
    players_summary, players_stats, players_position = backend.get_players_data(year=year, rnd=round_number)

    # make data flat
    players_summary_flat = backend.make_data_flat(players_summary)
    players_stats_flat = backend.make_data_flat(players_stats)
    players_position_flat = backend.make_data_flat(players_position)

    # Create Dataframes
    players_summary_df = pd.DataFrame(players_summary_flat)
    players_stats_df = pd.DataFrame(players_stats_flat)
    players_position_df = pd.DataFrame(players_position_flat)

except Exception as e:
    st.write("No data found!")
    players_summary_df = pd.DataFrame()
    players_stats_df = pd.DataFrame()
    players_position_df = pd.DataFrame()

# Display the structured dataframe
st.header(f"Player Details for Year: {year}, Round:{round_number}")
st.dataframe(players_summary_df, use_container_width=True)

# Create two columns for the Stats and Position buttons
col1, col2 = st.columns([0.5, 2.5])

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
        st.dataframe(players_stats_df, use_container_width=True)
    except Exception as e:
        st.write("No Data found!")
        st.dataframe(players_stats_df, use_container_width=True)

if position_clicked:
    st.header("Players Position")
    try:
        st.dataframe(players_position_df, use_container_width=True)
    except Exception as e:
        st.write("No data found!")
        st.dataframe(players_position_df, use_container_width=True)