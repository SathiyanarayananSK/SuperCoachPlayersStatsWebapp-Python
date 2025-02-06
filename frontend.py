# Import necessary libraries and files
import streamlit as st
import pandas as pd
import backend


def fetch_data(entered_year, entered_round):
    st.header(f"Players Details for Year: {entered_year} and Round: {entered_round}")
    # Get players data from the API for the input year and round
    summary, stats, position = backend.get_players_data(year=entered_year, rnd=entered_round)

    return summary, stats, position

def display_summary(summary_json):
    if len(summary_json) == 0:
        st.write("No Data Found! Try different values.")
        st.dataframe(pd.DataFrame(), use_container_width=True)
    else:
        # Make data flat, create a df using it and display it in the app
        players_summary_flat = backend.make_data_flat(summary_json)
        players_summary_df = pd.DataFrame(players_summary_flat)
        st.dataframe(players_summary_df, use_container_width=True)

def display_stats(stats_json):
    if len(stats_json) == 0:
        st.write("No Data Found! Try different values.")
        st.dataframe(pd.DataFrame(), use_container_width=True)
    else:
        # Make data flat, create a df using it and display it in the app
        players_stats_flat = backend.make_data_flat(stats_json)
        players_stats_df = pd.DataFrame(players_stats_flat)
        st.dataframe(players_stats_df, use_container_width=True)

def display_position(position_json):
    if len(position_json) == 0:
        st.write("No Data Found! Try different values.")
        st.dataframe(pd.DataFrame(), use_container_width=True)
    else:
        # Make data flat, create a df using it and display it in the app
        players_position_flat = backend.make_data_flat(position_json)
        players_position_df = pd.DataFrame(players_position_flat)
        st.dataframe(players_position_df, use_container_width=True)


if __name__ == "__main__":
    # Set config values
    st.set_page_config(layout="wide", page_title="SuperCoach NRL Stats")

    # Display the title of the app
    st.title("Super Coach Players Stats")

    # Get user inputs for year and round
    st.sidebar.title("Select Year and Round")
    year = st.sidebar.number_input("Enter Year", min_value=1950, max_value=2030, value=2024, step=1)
    round_number = st.sidebar.number_input("Enter Round", min_value=0, max_value=27, value=0, step=1)

    # Fetch data for the entered year and round number
    players_summary, players_stats, players_position = fetch_data(year, round_number)

    # Display Players Summary
    display_summary(players_summary)

    # Create Players Stats and Position buttons in sidebar
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

    if "search_id" not in st.session_state:
        st.session_state.search_id = None

    # Display data based on button clicks
    if stats_clicked:
        st.header(f"Players Stats for Year: {year} and Round:{round_number}")
        display_stats(players_stats)
        st.sidebar.write("Search Player Stats")
        search_id = st.sidebar.number_input("By Id", min_value=1, value=st.session_state.search_id, key="search_id")
        search_name = st.sidebar.text_input("By Name")
        filtered_stats = backend.filter_json_by_id(search_id, players_stats)
        display_stats(filtered_stats)

    if position_clicked:
        st.header(f"Players Position for Year: {year} and Round:{round_number}")
        display_position(players_position)

    # if stats_clicked or position_clicked:
    #     st.sidebar.write("Search Player Stats and Position")
    #     search_id = st.sidebar.number_input("By Id", min_value=1)
    #     search_name = st.sidebar.text_input("By Name")
    #     filtered_stats = backend.filter_json_by_id(search_id, players_stats)
    #     filtered_positions = backend.filter_json_by_id(search_id, players_position)
    #     #filtered_position = backend.filter_json_by_name()
