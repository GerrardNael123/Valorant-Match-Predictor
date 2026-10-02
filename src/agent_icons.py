import requests
import streamlit as st

@st.cache_data(ttl=86400)
def get_agent_icons():
    """Ambil mapping nama agent -> URL ikon dari valorant-api.com"""
    url = "https://valorant-api.com/v1/agents"
    params = {"language": "en-US", "isPlayableCharacter": "true"}
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    return {agent["displayName"]: agent["displayIcon"] for agent in data}


@st.cache_data(ttl=86400)
def get_map_icons():
    """Ambil mapping nama map -> URL ikon dari valorant-api.com"""
    url = "https://valorant-api.com/v1/maps"
    params = {"language": "en-US"}
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    return {m["displayName"]: m["listViewIcon"] for m in data if m["listViewIcon"]}


@st.cache_data(ttl=86400)
def get_map_splash():
    """Ambil mapping nama map -> URL gambar splash (wide) dari valorant-api.com"""
    url = "https://valorant-api.com/v1/maps"
    params = {"language": "en-US"}
    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()["data"]
    return {m["displayName"]: m["splash"] for m in data if m.get("splash")}