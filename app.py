import streamlit as st
import requests
import pandas as pd
import random
import sys
sys.path.append("src")
from fetch_data import get_match_history, extract_match_rows, extract_weapon_kills, BASE_URL, HEADERS
from agent_icons import get_agent_icons, get_map_icons, get_map_splash

st.set_page_config(
    page_title="Valorant Match Predictor",
    page_icon="🎯",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* ---------- Background bergerak pelan ---------- */
    @keyframes bgShift {
        0%   { background-position: 0% 0%, 100% 100%, 0 0; }
        50%  { background-position: 35% 25%, 65% 75%, 0 0; }
        100% { background-position: 0% 0%, 100% 100%, 0 0; }
    }
    .stApp {
        font-family: 'Inter', sans-serif;
        background:
            radial-gradient(circle at 20% 20%, rgba(255,70,85,0.22), transparent 45%),
            radial-gradient(circle at 80% 80%, rgba(0,170,200,0.16), transparent 45%),
            repeating-linear-gradient(135deg, rgba(255,255,255,0.025) 0 2px, transparent 2px 24px),
            #0f1923;
        background-size: 200% 200%, 200% 200%, auto;
        animation: bgShift 25s ease-in-out infinite;
    }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f1923; }
    ::-webkit-scrollbar-thumb { background: #ff4655; border-radius: 4px; }

    /* ---------- Hero header ---------- */
    @keyframes slowZoom {
        0% { background-size: 110%; background-position: center 40%; }
        50% { background-size: 125%; background-position: center 55%; }
        100% { background-size: 110%; background-position: center 40%; }
    }
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 20px;
        min-height: 170px;
        background-repeat: no-repeat;
        animation: slowZoom 16s ease-in-out infinite;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(15,25,35,0.96) 30%, rgba(15,25,35,0.55) 100%);
        z-index: 1;
    }
    .hero::after {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 5px;
        background: #ff4655;
        z-index: 2;
    }
    .hero-content { position: relative; z-index: 2; padding: 26px 30px; }
    .hero-tag {
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 3px;
        font-size: 13px;
        font-weight: 700;
        color: #ff4655;
    }
    .hero-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 46px;
        font-weight: 700;
        line-height: 1.05;
        color: #ece8e1;
        margin: 4px 0;
    }
    .hero-title span { color: #ff4655; }
    .hero-sub { color: #b8b4ad; font-size: 14px; }
    @media (max-width: 600px) {
        .hero-title { font-size: 32px; }
        .hero-content { padding: 20px; }
    }

    /* ---------- Form, tombol, metric, tab ---------- */
    [data-testid="stForm"] {
        background: rgba(26,36,47,0.6);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
    }
    [data-testid="stFormSubmitButton"] button {
        background: #ff4655;
        color: #fff;
        border: none;
        border-radius: 4px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all .15s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: #ff6673;
        color: #fff;
        transform: translateY(-1px);
        box-shadow: 0 4px 18px rgba(255,70,85,0.35);
    }
    [data-testid="stMetric"] {
        background: rgba(26,36,47,0.75);
        border: 1px solid rgba(255,255,255,0.06);
        border-top: 3px solid #ff4655;
        border-radius: 8px;
        padding: 12px 16px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.04);
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .stTabs [aria-selected="true"] { background: rgba(255,70,85,0.15); }

    /* ---------- Cards ---------- */
    .glass-card {
        background: rgba(26,36,47,0.8);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        backdrop-filter: blur(6px);
    }
    .win-badge {
        background-color: #1f6e43;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
    }
    .loss-badge {
        background-color: #7a1f2b;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
    }
    .match-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(26,36,47,0.8);
        border: 1px solid rgba(255,255,255,0.06);
        border-left: 3px solid transparent;
        backdrop-filter: blur(6px);
        margin-bottom: 8px;
        transition: transform .15s ease, background-color .15s ease;
    }
    .match-card:hover {
        transform: translateX(4px);
        background-color: rgba(31,44,58,0.95);
    }
    .match-card.win { border-left-color: #4ade80; }
    .match-card.loss { border-left-color: #ff4655; }
    .match-card img {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #2a2c35;
    }
    .map-card {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 12px;
        min-height: 140px;
        background-repeat: no-repeat;
        animation: slowZoom 12s ease-in-out infinite;
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .map-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(to right, rgba(10,11,15,0.95) 30%, rgba(10,11,15,0.5));
        z-index: 1;
    }
    .map-card-content {
        position: relative;
        z-index: 2;
    }
    .footer-note {
        text-align: center;
        color: #6b7280;
        font-size: 12px;
        margin-top: 32px;
        padding-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# --- Foto map acak untuk hero (tetap sama selama satu sesi) ---
if "hero_bg" not in st.session_state:
    try:
        splash_urls = list(get_map_splash().values())
        st.session_state["hero_bg"] = random.choice(splash_urls) if splash_urls else ""
    except Exception:
        st.session_state["hero_bg"] = ""
hero_bg = st.session_state["hero_bg"]

st.markdown(f"""
<div class="hero" style="background-image: url('{hero_bg}');">
    <div class="hero-content">
        <div class="hero-tag">VALORANT · MATCH ANALYTICS</div>
        <div class="hero-title">MATCH <span>PREDICTOR</span></div>
        <div class="hero-sub">Cari Riot ID kamu untuk melihat statistik & performa match terakhir.</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.form("search_form"):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        name = st.text_input("Riot Name", placeholder="Yagami")
    with col2:
        tag = st.text_input("Tag", placeholder="1702")
    with col3:
        region = st.selectbox("Region", ["ap", "na", "eu", "kr", "latam", "br"])
    submitted = st.form_submit_button("🔍 Cari", use_container_width=True)

if submitted and name and tag:
    with st.spinner("Mengambil data match..."):
        try:
            agent_icons = get_agent_icons()
            map_icons = get_map_icons()
            map_splash = get_map_splash()

            account_resp = requests.get(
                f"{BASE_URL}/v1/account/{name}/{tag}", headers=HEADERS
            ).json()

            if "data" not in account_resp:
                st.error(f"Akun tidak ditemukan: {account_resp}")
            else:
                puuid = account_resp["data"]["puuid"]
                matches = get_match_history(name, tag, region=region, size=20)
                rows = extract_match_rows(matches, puuid)
                weapon_counts, weapon_icons = extract_weapon_kills(matches, puuid)
                df = pd.DataFrame(rows)

                if df.empty:
                    st.warning("Tidak ada data match tim yang ditemukan (mungkin semua Deathmatch).")
                else:
                    df["kd_ratio"] = (df["kills"] / df["deaths"].replace(0, 1)).round(2)
                    win_rate = df["won"].mean() * 100
                    avg_kd = df["kd_ratio"].mean()
                    total_matches = len(df)

                    st.subheader(f"Statistik untuk {name}#{tag}")

                    m1, m2, m3 = st.columns(3)
                    m1.metric("Win Rate", f"{win_rate:.1f}%")
                    m2.metric("Rata-rata K/D", f"{avg_kd:.2f}")
                    m3.metric("Total Match", total_matches)

                    st.divider()

                    tab1, tab2, tab3, tab4 = st.tabs([" Match Terakhir", " Agent Stats", " Map Stats", " Weapon Stats"])

                    # ============ TAB 1: MATCH TERAKHIR ============
                    with tab1:
                        for _, row in df.iterrows():
                            icon_url = agent_icons.get(row["agent"], "")
                            result_class = "win" if row["won"] else "loss"
                            badge_class = "win-badge" if row["won"] else "loss-badge"
                            badge_text = "MENANG" if row["won"] else "KALAH"
                            score_text = f"{row['rounds_won']}-{row['rounds_lost']}"

                            st.markdown(f"""
                            <div class="match-card {result_class}">
                                <img src="{icon_url}" alt="{row['agent']}">
                                <div style="flex: 1;">
                                    <strong>{row['agent']}</strong> — {row['map']}<br>
                                    <span style="font-size: 13px; color: #999;">
                                        {row['kills']}/{row['deaths']}/{row['assists']} · K/D {row['kd_ratio']}
                                    </span>
                                </div>
                                <div style="text-align: right;">
                                    <span class="{badge_class}">{badge_text}</span><br>
                                    <span style="font-size: 13px; color: #ccc; margin-top: 2px; display: inline-block;">{score_text}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()
                        st.subheader("Tren K/D Ratio")
                        chart_df = df[["kd_ratio"]].reset_index()
                        chart_df.columns = ["Match ke-", "K/D Ratio"]
                        st.line_chart(chart_df.set_index("Match ke-"), color="#ff4655")

                    # ============ TAB 2: AGENT STATS ============
                    with tab2:
                        st.subheader("Win Rate per Agent")
                        agent_stats = df.groupby("agent")["won"].mean().sort_values(ascending=False) * 100
                        st.bar_chart(agent_stats, color="#ff4655")

                        st.divider()
                        st.subheader("Detail Statistik per Agent")

                        agent_detail = df.groupby("agent").agg(
                            matches=("agent", "count"),
                            wins=("won", "sum"),
                            kills=("kills", "sum"),
                            deaths=("deaths", "sum"),
                            assists=("assists", "sum"),
                            avg_score=("score", "mean"),
                            headshots=("headshots", "sum"),
                            bodyshots=("bodyshots", "sum"),
                            legshots=("legshots", "sum"),
                        ).reset_index()

                        agent_detail["win_pct"] = (agent_detail["wins"] / agent_detail["matches"] * 100).round(1)
                        agent_detail["kd_ratio"] = (agent_detail["kills"] / agent_detail["deaths"].replace(0, 1)).round(2)
                        total_shots = agent_detail["headshots"] + agent_detail["bodyshots"] + agent_detail["legshots"]
                        agent_detail["hs_pct"] = (agent_detail["headshots"] / total_shots.replace(0, 1) * 100).round(1)
                        agent_detail["avg_kills"] = (agent_detail["kills"] / agent_detail["matches"]).round(1)
                        agent_detail["avg_deaths"] = (agent_detail["deaths"] / agent_detail["matches"]).round(1)
                        agent_detail["avg_assists"] = (agent_detail["assists"] / agent_detail["matches"]).round(1)

                        agent_detail = agent_detail.sort_values("matches", ascending=False)

                        header_cols = st.columns([2.5, 1, 1, 1, 1.2, 1, 1])
                        headers = ["Agent", "Matches", "Win %", "K/D", "Avg Score", "HS%", "K/D/A"]
                        for col, h in zip(header_cols, headers):
                            col.markdown(f"<span style='color:#999; font-size:12px; font-weight:600;'>{h}</span>", unsafe_allow_html=True)

                        st.markdown("<hr style='margin: 4px 0; border-color: #333;'>", unsafe_allow_html=True)

                        for _, row in agent_detail.iterrows():
                            icon_url = agent_icons.get(row["agent"], "")
                            row_cols = st.columns([2.5, 1, 1, 1, 1.2, 1, 1])

                            with row_cols[0]:
                                st.markdown(f"""
                                <div style="display:flex; align-items:center; gap:8px;">
                                    <img src="{icon_url}" style="width:28px; height:28px; border-radius:50%; background:#2a2c35;">
                                    <span style="font-weight:600;">{row['agent']}</span>
                                </div>
                                """, unsafe_allow_html=True)

                            row_cols[1].markdown(f"{int(row['matches'])}")

                            win_color = "#4ade80" if row['win_pct'] >= 50 else "#f87171"
                            row_cols[2].markdown(f"<span style='color:{win_color}; font-weight:600;'>{row['win_pct']:.1f}%</span>", unsafe_allow_html=True)

                            kd_color = "#facc15" if row['kd_ratio'] >= 1.0 else "#ddd"
                            row_cols[3].markdown(f"<span style='color:{kd_color};'>{row['kd_ratio']:.2f}</span>", unsafe_allow_html=True)

                            row_cols[4].markdown(f"{row['avg_score']:.0f}")
                            row_cols[5].markdown(f"{row['hs_pct']:.1f}%")
                            row_cols[6].markdown(f"{row['avg_kills']:.1f}/{row['avg_deaths']:.1f}/{row['avg_assists']:.1f}")

                            st.markdown("<hr style='margin: 4px 0; border-color: #262830;'>", unsafe_allow_html=True)

                    # ============ TAB 3: MAP STATS ============
                    with tab3:
                        map_groups = df.groupby("map")
                        map_order = map_groups.size().sort_values(ascending=False).index

                        for map_name in map_order:
                            map_df = map_groups.get_group(map_name)

                            matches_played = len(map_df)
                            win_rate_map = map_df["won"].mean() * 100
                            avg_kd_map = (map_df["kills"] / map_df["deaths"].replace(0, 1)).mean()
                            favorite_agent = map_df["agent"].mode()[0]
                            map_icon_url = map_icons.get(map_name, "")
                            splash_url = map_splash.get(map_name, "")

                            wins = int(map_df["won"].sum())
                            losses = matches_played - wins

                            st.markdown(f"""
                            <div class="map-card" style="background-image: url('{splash_url}');">
                                <div class="map-card-content">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <img src="{map_icon_url}" alt="{map_name}" style="width: 32px; height: 32px; border-radius: 6px; object-fit: cover;">
                                            <strong style="font-size: 18px; color: white;">{map_name}</strong>
                                        </div>
                                        <span style="font-size: 13px; color: #ccc;">{matches_played} match dimainkan</span>
                                    </div>
                                    <div style="background-color: rgba(42,44,53,0.8); border-radius: 6px; height: 8px; margin: 10px 0;">
                                        <div style="background-color: #1f6e43; width: {win_rate_map}%; height: 8px; border-radius: 6px;"></div>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; font-size: 13px; color: #eee;">
                                        <span>🟢 {wins}W · 🔴 {losses}L ({win_rate_map:.0f}% win rate)</span>
                                        <span>Agent favorit: {favorite_agent} · K/D {avg_kd_map:.2f}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    # ============ TAB 4: WEAPON STATS ============
                    with tab4:
                        st.subheader("Distribusi Tembakan")

                        total_hs = int(df["headshots"].sum())
                        total_bs = int(df["bodyshots"].sum())
                        total_ls = int(df["legshots"].sum())
                        total_hits = total_hs + total_bs + total_ls

                        if total_hits == 0:
                            st.info("Data tembakan tidak tersedia.")
                        else:
                            head_pct = total_hs / total_hits * 100
                            body_pct = total_bs / total_hits * 100
                            leg_pct = total_ls / total_hits * 100

                            head_color = "#ff4655"
                            body_color = "#ece8e1"
                            leg_color = "#6b7280"

                            st.markdown(f"""
                            <div class="glass-card" style="display:flex; align-items:center; justify-content:center; gap:28px; padding:16px; margin-bottom:16px;">
                                <svg width="80" height="150" viewBox="0 0 60 120" xmlns="http://www.w3.org/2000/svg">
                                    <circle cx="30" cy="13" r="10" fill="{head_color}"/>
                                    <rect x="16" y="26" width="28" height="46" rx="9" fill="{body_color}"/>
                                    <rect x="6" y="28" width="9" height="40" rx="4.5" fill="{body_color}"/>
                                    <rect x="45" y="28" width="9" height="40" rx="4.5" fill="{body_color}"/>
                                    <rect x="17" y="74" width="12" height="42" rx="5" fill="{leg_color}"/>
                                    <rect x="31" y="74" width="12" height="42" rx="5" fill="{leg_color}"/>
                                </svg>
                                <div style="display:flex; flex-direction:column; gap:10px;">
                                    <div>
                                        <span style="font-size:26px; font-weight:700; color:{head_color};">{head_pct:.0f}%</span>
                                        <span style="font-size:12px; color:#999; margin-left:6px;">Head · {total_hs} hits</span>
                                    </div>
                                    <div>
                                        <span style="font-size:26px; font-weight:700; color:{body_color};">{body_pct:.0f}%</span>
                                        <span style="font-size:12px; color:#999; margin-left:6px;">Body · {total_bs} hits</span>
                                    </div>
                                    <div>
                                        <span style="font-size:26px; font-weight:700; color:{leg_color};">{leg_pct:.0f}%</span>
                                        <span style="font-size:12px; color:#999; margin-left:6px;">Legs · {total_ls} hits</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            st.caption("Gabungan semua senjata dari match yang dimuat. Breakdown per senjata tidak tersedia dari API.")

                        st.divider()

                        st.subheader("Senjata Paling Sering Digunakan")

                        if not weapon_counts:
                            st.info("Tidak ada data kill senjata yang ditemukan.")
                        else:
                            sorted_weapons = sorted(weapon_counts.items(), key=lambda x: x[1], reverse=True)
                            total_kills_weapon = sum(weapon_counts.values())

                            for weapon_name, count in sorted_weapons:
                                icon_url = weapon_icons.get(weapon_name, "")
                                pct = (count / total_kills_weapon) * 100

                                st.markdown(f"""
                                <div class="glass-card" style="display:flex; align-items:center; gap:12px; padding:8px; margin-bottom:6px;">
                                    <img src="{icon_url}" style="width:60px; height:32px; object-fit:contain;">
                                    <div style="flex:1;">
                                        <div style="display:flex; justify-content:space-between;">
                                            <strong>{weapon_name}</strong>
                                            <span style="color:#999; font-size:13px;">{count} kills ({pct:.1f}%)</span>
                                        </div>
                                        <div style="background:#2a2c35; border-radius:6px; height:6px; margin-top:4px;">
                                            <div style="background:#ff4655; width:{pct}%; height:6px; border-radius:6px;"></div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Gagal ambil data: {e}")
else:
    st.info("Masukkan Riot Name dan Tag, lalu klik Cari untuk melihat statistik.")

st.markdown(
    "<div class='footer-note'>Bukan produk resmi Riot Games · Data via HenrikDev API & valorant-api.com</div>",
    unsafe_allow_html=True,
)