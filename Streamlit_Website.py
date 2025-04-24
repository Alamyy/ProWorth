import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Set the page title and layout

# Load data
new_predictions = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/predicted_market_values_2026.csv")
players = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/merged_df_2026.csv")
more_info = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/players.csv")
logo_clubs = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/logo_clubs.csv")

# Merge datasets
df = pd.merge(new_predictions, players, on='player_id', how='left')
df = df.merge(more_info[['player_id', 'image_url','current_club_name']], on='player_id', how='left')

# Config
st.set_page_config(page_title="Football Data Analysis", layout="centered")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Home", "Player Analyzer", "Club Market Value Analysis", "Top Market Values 2026"])

import streamlit as st

# Set the video URL (raw link from GitHub)
video_url = "https://github.com/Alamyy/ProWorth/raw/refs/heads/main/Football%20in%20slow%20motion%20-%20social%20media%20video%20ad%20-%20stock%20video.mp4"

# Set the video as background using HTML and CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        position: relative;
        overflow: hidden;
        height: 100vh;
    }}
    .video-background {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1;
    }}
    .content {{
        position: relative;
        z-index: 1;
        color: white;  /* White text color */
        text-align: center;
        padding-top: 50px;
    }}
    </style>
    <video class="video-background" autoplay muted loop>
        <source src="{video_url}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# Home page content
if page == "Home":
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #D35400;'>Welcome to the Football Data Analysis </h1>", unsafe_allow_html=True)
    st.markdown("<h3>Explore Football Data in Detail</h3>", unsafe_allow_html=True)
    st.markdown("<p>This application allows you to analyze football data with various tools. Choose one of the options in the navigation bar to get started:</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------- Club Market Value Analysis Page ----------------------
if page == "Club Market Value Analysis":
    st.markdown("<h1 style='text-align: center; color: #D35400;'>Market Value Analysis by Club</h1>", unsafe_allow_html=True)

    # Select club
    clubs = df['current_club_name'].dropna().unique()
    club_selected = st.selectbox("Select a Club", ["-- Select a Club --"] + sorted(clubs))

    if club_selected != "-- Select a Club --":
        # Merge with logo_clubs DataFrame to get the club logo
        club_logo = logo_clubs[logo_clubs['current_club_name'] == club_selected]['logo_url'].values
        if club_logo.size > 0:
            club_logo_url = club_logo[0]
        else:
            club_logo_url = None

        # Filter players from the selected club
        club_players = df[df['current_club_name'] == club_selected]

        # Create columns layout
        col1, col2 = st.columns([1, 3])

        with col1:
            # Display club logo if available
            if club_logo_url:
                st.image(club_logo_url, width=100)  # Display the club logo
            else:
                st.warning("Logo not found for the selected club.")

        with col2:
            # Select sub_position (optional filter)
            sub_positions = club_players['sub_position'].dropna().unique()
            sub_position_selected = st.selectbox("Select a Position", ["-- Select a Position --"] + sorted(sub_positions))

            # Select market value trend filter (increase or decrease)
            market_trend_filter = st.selectbox("Select Market Value Trend", ["-- Select Trend --", "Increase", "Decrease"])

        # Filter by sub_position if selected
        if sub_position_selected != "-- Select a Position --":
            club_players = club_players[club_players['sub_position'] == sub_position_selected]

        # Filter by market value trend (Increase/Decrease) if selected
        if market_trend_filter != "-- Select Trend --":
            if market_trend_filter == "Increase":
                club_players = club_players[club_players['predicted_value_2026'] > club_players['value_2024']]
            elif market_trend_filter == "Decrease":
                club_players = club_players[club_players['predicted_value_2026'] < club_players['value_2024']]

        # Display Players and Market Value Changes
        st.subheader(f"Players from {club_selected}")
        club_players_display = club_players[['name_x', 'sub_position', 'value_2024', 'predicted_value_2026']].rename(columns={
            'name_x': 'Player',
            'sub_position': 'Position',
            'value_2024': 'Current Value (€)',
            'predicted_value_2026': 'Predicted Value (€)'
        })

        # Format the values in millions
        club_players_display['Current Value (€)'] = club_players_display['Current Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")
        club_players_display['Predicted Value (€)'] = club_players_display['Predicted Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")

        # Display table
        st.dataframe(club_players_display)

        # Determine players with increased or decreased predicted value
        club_players['Market Value Change'] = club_players['predicted_value_2026'] - club_players['value_2024']
        club_players['Market Value Trend'] = club_players['Market Value Change'].apply(lambda x: 'Increase' if x > 0 else ('Decrease' if x < 0 else 'No Change'))

        # Count number of players going up or down
        increase_count = club_players[club_players['Market Value Trend'] == 'Increase'].shape[0]
        decrease_count = club_players[club_players['Market Value Trend'] == 'Decrease'].shape[0]
        no_change_count = club_players[club_players['Market Value Trend'] == 'No Change'].shape[0]

        # Display counts of increases, decreases, and no changes
        st.markdown(f"### Market Value Change Trend")
        st.markdown(f"- **Players with Increased Value**: {increase_count}")
        st.markdown(f"- **Players with Decreased Value**: {decrease_count}")
        st.markdown(f"- **Players with No Change in Value**: {no_change_count}")

    else:
        st.info("👈 Please select a club to get started.")


# ---------------------- Player Analyzer Page ----------------------
if page == "Player Analyzer":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'> Football Player Market Value Analyzer</h1>", unsafe_allow_html=True)

    player_names = df['name_x'].dropna().unique()
    player_name_input = st.selectbox("🔍 Search for a Player", ["-- Select a Player --"] + sorted(player_names))

    if player_name_input != "-- Select a Player --":
        player_data = df[df['name_x'] == player_name_input]
        if not player_data.empty:
            player_data = player_data.iloc[0]
            player_name = player_data['name_x']
            years = [2019, 2020, 2021, 2022, 2023, 2024, 2026]
            values = [
                player_data['value_2019'],
                player_data['value_2020'],
                player_data['value_2021'],
                player_data['value_2022'],
                player_data['value_2023'],
                player_data['value_2024'],
                player_data['predicted_value_2026']
            ]

            plt.style.use("ggplot")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(years[:-1], values[:-1], marker='o', color='dodgerblue', label="Actual", linewidth=3)
            ax.plot(years[-2:], values[-2:], linestyle='--', color='orange', label="Prediction", linewidth=3)
            ax.scatter(years[-1], values[-1], color='orange', s=150, marker='*', edgecolor='black')
            for x, y in zip(years, values):
                ax.text(x, y + 0.03 * max(values), f"€{y/1e6:.1f}M", ha='center')
            ax.set_title(f" Market Value Over Time – {player_name}")
            ax.set_xlabel("Year"); ax.set_ylabel("Market Value (€)")
            ax.set_xticks(years)
            ax.set_yticklabels([f"€{x/1e6:.1f}M" for x in ax.get_yticks()])
            ax.legend(); ax.grid(True)
            st.pyplot(fig)

            player_info = more_info[more_info['name'] == player_name].iloc[0]
            st.markdown("---")
            st.subheader(f"🧾 Detailed Profile: {player_name}")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(player_info['image_url'], width=180)
                st.markdown(f"**🌍 Country:** {player_info['country_of_citizenship']}")
                st.markdown(f"**🏙️ Birthplace:** {player_info['city_of_birth']}, {player_info['country_of_birth']}")
                st.markdown(f"**🎂 Date of Birth:** {player_info['date_of_birth']}")
                st.markdown(f"**📏 Height:** {player_info['height_in_cm']} cm")
                st.markdown(f"**🦶 Preferred Foot:** {player_info['foot']}")
            with col2:
                st.markdown(f"**📌 Current Club:** {player_info['current_club_name']}")
                st.markdown(f"**🧩 Position:** {player_info['position']} / {player_info['sub_position']}")
                st.markdown(f"**📄 Contract Expires:** {player_info['contract_expiration_date']}")
                st.markdown(f"**🤝 Agent:** {player_info['agent_name'] if pd.notnull(player_info['agent_name']) else 'N/A'}")
            st.markdown("### 💶 Market Value Insights")
            st.markdown(f"- **Current Market Value (2024):** €{player_data['value_2024'] / 1e6:.2f}M")
            st.markdown(f"- **Highest Market Value:** €{player_info['highest_market_value_in_eur'] / 1e6:.2f}M")
        else:
            st.error("❌ Player not found.")

    else:
        st.info("👈 Please select a player to get started.")

# ---------------------- Top Market Values Page ----------------------
elif page == "Top Market Values 2026":
    st.markdown("<h1 style='text-align: center; color: #D35400;'>Top Players by Predicted Market Value (2026)</h1>", unsafe_allow_html=True)
    
    # Slider to choose number of players to show
    num_players = st.slider("Select Number of Players to Display", min_value=1, max_value=100, value=20, step=1)

    # Sort and display top players
    top_players = df.sort_values(by="predicted_value_2026", ascending=False).dropna(subset=["name_x"]).head(num_players)
    
    # Create the table and make player names clickable
    top_players_display = top_players[['name_x', 'current_club_name', 'sub_position', 'value_2024', 'predicted_value_2026']].rename(columns={
        'name_x': 'Player',
        'current_club_name': 'Club',
        'sub_position': 'Position',
        'value_2024': 'Current Value (€)',
        'predicted_value_2026': 'Predicted Value (€)'
    })
    
    # Format the Current Value and Predicted Value in millions
    top_players_display['Current Value (€)'] = top_players_display['Current Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")
    top_players_display['Predicted Value (€)'] = top_players_display['Predicted Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")
    
    # Reorder columns to place Current Value before Predicted Value
    top_players_display = top_players_display[['Player', 'Club', 'Position', 'Current Value (€)', 'Predicted Value (€)']]
    
    # Reset the index and start from 1
    top_players_display = top_players_display.reset_index(drop=True)
    top_players_display.index = top_players_display.index + 1  # Start the index from 1
    
    # Display the table
    st.markdown(top_players_display.to_html(escape=False), unsafe_allow_html=True)
