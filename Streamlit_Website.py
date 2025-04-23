import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import requests

# Load data
new_predictions = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/predicted_market_values_2026.csv")
players = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/merged_df.csv")
more_info = pd.read_csv("https://raw.githubusercontent.com/Alamyy/ProWorth/refs/heads/main/players.csv")

# Merge datasets
df = pd.merge(new_predictions, players, on='player_id', how='left')
df = df.merge(more_info[['player_id', 'image_url']], on='player_id', how='left')

# Page config
st.set_page_config(page_title="Player Market Value", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>⚽ Football Player Market Value Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Track player value evolution & future predictions 💸</p>", unsafe_allow_html=True)

# Input
player_names = df['name_x'].dropna().unique()
player_name_input = st.selectbox("🔍 Search for a Player", ["-- Select a Player --"] + sorted(player_names))

# Body
if player_name_input != "-- Select a Player --":
    player_data = df[df['name_x'] == player_name_input]

    if player_data.empty:
        st.error("❌ Player not found. Please try another name.")
    else:
        player_data = player_data.iloc[0]
        player_name = player_data['name_x']

        # Market Value Data
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

        # Plot
        plt.style.use("ggplot")  # Use a matplotlib style, e.g., 'ggplot'
        fig, ax = plt.subplots(figsize=(12, 6))

        # Actual values
        ax.plot(years[:-1], values[:-1], marker='o', linestyle='-', color='#1f77b4', linewidth=3, markersize=8, label="Actual")

        # Prediction
        ax.plot(years[-2:], values[-2:], linestyle='--', color='#FF7F0E', linewidth=3, label="Prediction")
        ax.scatter(years[-1], values[-1], color='#FF7F0E', s=120, marker='*', edgecolor='black', zorder=5)

        # Value labels
        for x, y in zip(years, values):
            label = f"€{y/1e6:.1f}M"
            ax.text(x, y + 0.02 * max(values), label, fontsize=11, ha='center', fontweight='bold', color='black')

        ax.set_title(f"Market Value Over Time – {player_name}", fontsize=18, fontweight='bold')
        ax.set_xlabel("Year", fontsize=14)
        ax.set_ylabel("Market Value (€)", fontsize=14)
        ax.set_xticks(years)
        ax.set_yticklabels([f"€{x/1e6:.1f}M" for x in ax.get_yticks()])
        ax.tick_params(axis='both', labelsize=12)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend()

        # Show plot
        st.pyplot(fig)

        # Info Card
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
    st.info("👈 Please select a player to get started.")
