import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Load data
new_predictions = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/predicted_market_values_2026.csv")
players = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/merged_df_2026.csv")
more_info = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/players.csv")

# Merge datasets
df = pd.merge(new_predictions, players, on='player_id', how='left')
df = df.merge(more_info[['player_id', 'image_url','current_club_name']], on='player_id', how='left')

# Config
st.set_page_config(page_title="Football Market Value", layout="wide")
st.sidebar.title("⚽ Navigation")
page = st.sidebar.selectbox("Go to", ["Player Analyzer", "Top Market Values 2026"])

# ---------------------- Player Analyzer Page ----------------------
if page == "Player Analyzer":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>⚽ Football Player Market Value Analyzer</h1>", unsafe_allow_html=True)

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
            ax.set_title(f"📈 Market Value Over Time – {player_name}")
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
    st.markdown("<h1 style='text-align: center; color: #D35400;'>🔥 Top 20 Players by Predicted Market Value (2026)</h1>", unsafe_allow_html=True)
    
    top_players = df.sort_values(by="predicted_value_2026", ascending=False).dropna(subset=["name_x"]).head(20)
    
    # Create the table and make player names clickable
    top_players_display = top_players[['name_x', 'current_club_name', 'sub_position', 'predicted_value_2026']].rename(columns={
        'name_x': 'Player',
        'current_club_name': 'Club',
        'sub_position': 'Position',
        'predicted_value_2026': 'Predicted Value (€)'
    })
    
    # Format the Predicted Value in millions
    top_players_display['Predicted Value (€)'] = top_players_display['Predicted Value (€)'].apply(lambda x: f"€{x/1e6:.1f}M")
    
    # Create clickable links for player names
    
    st.markdown(top_players_display.to_html(escape=False), unsafe_allow_html=True)
