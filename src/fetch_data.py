import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.henrikdev.xyz/valorant"

try:
    API_KEY = st.secrets["HENRIK_API_KEY"]
except Exception:
    API_KEY = os.getenv("HENRIK_API_KEY")

HEADERS = {"Authorization": API_KEY}


def get_match_history(name: str, tag: str, region: str = "ap", size: int = 20):
    """Ambil riwayat match untuk satu akun Valorant."""
    url = f"{BASE_URL}/v3/matches/{region}/{name}/{tag}"
    params = {"size": size}
    response = requests.get(url, params=params, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return response.json()["data"]


def extract_match_rows(matches: list, target_puuid: str):
    """Ubah raw JSON match jadi baris-baris data yang siap dipakai model."""
    rows = []
    for match in matches:
        try:
            players = match["players"]["all_players"]
            player_data = next((p for p in players if p["puuid"] == target_puuid), None)
            if not player_data:
                continue

            team = player_data["team"]

            if team.lower() not in match["teams"]:
                continue

            team_data = match["teams"][team.lower()]
            team_won = team_data["has_won"]
            rounds_won = team_data.get("rounds_won", 0)
            rounds_lost = team_data.get("rounds_lost", 0)

            rows.append({
                "match_id": match["metadata"]["matchid"],
                "map": match["metadata"]["map"],
                "agent": player_data["character"],
                "kills": player_data["stats"]["kills"],
                "deaths": player_data["stats"]["deaths"],
                "assists": player_data["stats"]["assists"],
                "score": player_data["stats"]["score"],
                "headshots": player_data["stats"]["headshots"],
                "bodyshots": player_data["stats"]["bodyshots"],
                "legshots": player_data["stats"]["legshots"],
                "won": team_won,
                "rounds_won": rounds_won,
                "rounds_lost": rounds_lost,
            })
        except (KeyError, TypeError) as e:
            print(f"Skip match karena error: {e}")
            continue

    return rows


def extract_weapon_kills(matches: list, target_puuid: str):
    """Hitung jumlah kill per senjata dari semua match, khusus milik target_puuid."""
    weapon_counts = {}
    weapon_icons = {}

    for match in matches:
        kills = match.get("kills", [])
        for kill in kills:
            if kill.get("killer_puuid") != target_puuid:
                continue

            weapon_name = kill.get("damage_weapon_name")
            if not weapon_name:
                continue

            weapon_counts[weapon_name] = weapon_counts.get(weapon_name, 0) + 1

            icon = kill.get("damage_weapon_assets", {}).get("display_icon")
            if icon:
                weapon_icons[weapon_name] = icon

    return weapon_counts, weapon_icons


if __name__ == "__main__":
    NAME = "Yagami"
    TAG = "TST"

    account_url = f"{BASE_URL}/v1/account/{NAME}/{TAG}"
    account_resp = requests.get(account_url, headers=HEADERS).json()

    if "data" not in account_resp:
        print("Gagal ambil akun:", account_resp)
        exit()

    puuid = account_resp["data"]["puuid"]

    matches = get_match_history(NAME, TAG, size=50)
    rows = extract_match_rows(matches, puuid)

    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_csv("data/matches.csv", index=False)
    print(f"Saved {len(df)} matches to data/matches.csv")