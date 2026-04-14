

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from db_connection import get_connection

# ── PAGE CONFIG ────────
st.set_page_config(
    page_title="NEWS PULSE",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLOURS ───────────────────────────────────────────────────────────────────
BK = "#0a0a0a"
MR = "#6b0f1a"
RD = "#c0152a"
WH = "#f5f0eb"
DK = "#141414"
BR = "#1e0a0d"
TL = "#5a4a4d"


CSS = """

st.markdown(CSS, unsafe_allow_html=True)
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a !important;
    color: #f5f0eb !important;
    font-family: 'DM Sans', sans-serif !important;
}

h1, h2, h3, h4 {
    font-family: 'Libre Baskerville', Georgia, serif !important;
    color: #f5f0eb !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0e0608 !important;
    border-right: 1px solid #1e0a0d !important;
    min-width: 260px !important;
}

[data-testid="stSidebar"] * {
    color: #f5f0eb !important;
    font-family: 'DM Sans', sans-serif !important;
}


[data-testid="collapsedControl"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 32px !important;
    height: 32px !important;
    padding: 0 !important;
    color: transparent !important;  /* hides 'keyboard_do' */
    background-color: #1e0a0d !important;
    border-radius: 0 6px 6px 0 !important;
}


[data-testid="collapsedControl"] svg {
    width: 18px !important;
    height: 18px !important;
    fill: #f5f0eb !important;
}

/* OPTIONAL HOVER EFFECT */
[data-testid="collapsedControl"]:hover {
    background-color: #c0152a !important;
}

/* METRICS */
/* ===== APPLE / TRADING KPI DESIGN ===== */

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #050505, #0d0d0d) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    position: relative !important;
    overflow: hidden !important;
    backdrop-filter: blur(10px) !important;

    box-shadow: 
        0 6px 25px rgba(0,0,0,0.7),
        inset 0 0 0 1px rgba(255,255,255,0.04) !important;

    transition: all 0.3s ease !important;
}

/* top glow line */
div[data-testid="metric-container"]::before {
    content: "" !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 3px !important;
    background: linear-gradient(90deg, #ff2d55, #ff6b81) !important;
}

/* hover effect */
div[data-testid="metric-container"]:hover {
    transform: translateY(-6px) scale(1.02) !important;
    box-shadow: 
        0 15px 40px rgba(0,0,0,0.9),
        0 0 20px rgba(255,45,85,0.25) !important;
}

/* value */
div[data-testid="stMetricValue"] {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* label */
div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: rgba(255,255,255,0.6) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button:hover {
    background: #6b0f1a !important;
}

/* SELECT BOX */
div[data-baseweb="select"] > div {
    background-color: #141414 !important;
    border-color: #1e0a0d !important;
    border-radius: 4px !important;
    color: #f5f0eb !important;
}

/* GENERAL */
hr {
    border-color: #1e0a0d !important;
    margin: 18px 0 !important;
}

#MainMenu, footer { visibility: hidden; }

header {
    visibility: visible !important;
    background-color: #0a0a0a !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb {
    background: #6b0f1a;
    border-radius: 2px;
}
/* ===== FORCE KPI REDESIGN (WORKING FIX) ===== */

/* target the actual metric card wrapper */
div[data-testid="column"] div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #050505, #0d0d0d) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;

    box-shadow: 
        0 6px 25px rgba(0,0,0,0.8),
        inset 0 0 0 1px rgba(255,255,255,0.05) !important;

    position: relative !important;
    overflow: hidden !important;
}

/* glowing top bar */
div[data-testid="column"] div[data-testid="metric-container"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #ff2d55, #ff6b81);
}

/* hover animation */
div[data-testid="column"] div[data-testid="metric-container"]:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 
        0 15px 40px rgba(0,0,0,0.9),
        0 0 20px rgba(255,45,85,0.3);
}

/* BIG NUMBER */
div[data-testid="column"] div[data-testid="stMetricValue"] {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* LABEL */
div[data-testid="column"] div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: rgba(255,255,255,0.6) !important;
    letter-spacing: 2px !important;
}
</style>
"""



def styled(fig, h=260):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=TL, size=11),
        height=h,
        margin=dict(l=8, r=8, t=24, b=8),
        xaxis=dict(gridcolor=BR, linecolor=BR, zerolinecolor=BR),
        yaxis=dict(gridcolor=BR, linecolor=BR, zerolinecolor=BR),
    )
    return fig


# ── DB HELPERS 
@st.cache_data(ttl=300)
def get_articles(hours, country, category, topic):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    sql  = """
        SELECT a.title, a.description, a.source_name, a.country,
               a.category, a.url, a.published_at,
               s.sentiment, s.score, s.keywords, s.topic
        FROM articles a
        JOIN article_sentiment s ON a.id = s.article_id
        WHERE a.published_at >= NOW() - INTERVAL %s HOUR
    """
    p = [hours]
    if country  != "All": sql += " AND a.country = %s";  p.append(country)
    if category != "All": sql += " AND a.category = %s"; p.append(category)
    if topic    != "All": sql += " AND s.topic = %s";    p.append(topic)
    sql += " ORDER BY a.published_at DESC"
    cur.execute(sql, p)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return pd.DataFrame(rows)


@st.cache_data(ttl=300)
def get_trend(hours):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DATE(a.published_at)  AS d,
               HOUR(a.published_at)  AS h,
               AVG(s.score)          AS avg_s,
               COUNT(*)              AS cnt,
               SUM(s.sentiment = 'positive') AS pos,
               SUM(s.sentiment = 'negative') AS neg
        FROM articles a
        JOIN article_sentiment s ON a.id = s.article_id
        WHERE a.published_at >= NOW() - INTERVAL %s HOUR
        GROUP BY DATE(a.published_at), HOUR(a.published_at)
        ORDER BY d, h
    """, (hours,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    df = pd.DataFrame(rows)
    if not df.empty:
        df["slot"] = df.apply(
            lambda r: datetime(r["d"].year, r["d"].month, r["d"].day, int(r["h"])),
            axis=1
        )
    return df


@st.cache_data(ttl=300)
def get_topics(hours):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.topic, COUNT(*) AS cnt, AVG(s.score) AS avg_s
        FROM articles a
        JOIN article_sentiment s ON a.id = s.article_id
        WHERE a.published_at >= NOW() - INTERVAL %s HOUR
        GROUP BY s.topic ORDER BY cnt DESC
    """, (hours,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return pd.DataFrame(rows)


@st.cache_data(ttl=300)
def get_countries(hours):
    conn = get_connection()
    cur  = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.country, AVG(s.score) AS avg_s, COUNT(*) AS cnt
        FROM articles a
        JOIN article_sentiment s ON a.id = s.article_id
        WHERE a.published_at >= NOW() - INTERVAL %s HOUR
        GROUP BY a.country ORDER BY cnt DESC
    """, (hours,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    return pd.DataFrame(rows)


@st.cache_data(ttl=300)
def count_total():
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM articles")
    n = cur.fetchone()[0]
    cur.close(); conn.close()
    return n



with st.sidebar:
    st.markdown(
        "<div style='padding:24px 4px 20px 4px'>"
        "<div style='font-family:Libre Baskerville,serif;font-size:20px;"
        "font-weight:700;color:#f5f0eb;letter-spacing:0.1em;"
        "text-transform:uppercase'>NEWS PULSE</div>"
        "<div style='font-size:10px;color:#5a4a4d;letter-spacing:3px;"
        "text-transform:uppercase;margin-top:4px'>Global Sentiment</div>"
        "<div style='width:28px;height:2px;background:#c0152a;margin-top:8px'></div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("<div style='font-size:10px;color:#5a4a4d;letter-spacing:2px;"
                "text-transform:uppercase;margin-bottom:6px'>Time Window</div>",
                unsafe_allow_html=True)
    hours = st.slider("Hours", 1, 72, 72, label_visibility="collapsed")
    st.caption(f"Last **{hours} hours**")

    st.markdown("<div style='font-size:10px;color:#5a4a4d;letter-spacing:2px;"
                "text-transform:uppercase;margin:14px 0 6px'>Country</div>",
                unsafe_allow_html=True)
    country = st.selectbox("Country", ["All","us","in","gb","au","ca"],
                           label_visibility="collapsed")

    st.markdown("<div style='font-size:10px;color:#5a4a4d;letter-spacing:2px;"
                "text-transform:uppercase;margin:14px 0 6px'>Category</div>",
                unsafe_allow_html=True)
    category = st.selectbox("Category",
        ["All","business","technology","health","science",
         "sports","entertainment","general"],
        label_visibility="collapsed")

    st.markdown("<div style='font-size:10px;color:#5a4a4d;letter-spacing:2px;"
                "text-transform:uppercase;margin:14px 0 6px'>Topic</div>",
                unsafe_allow_html=True)
    topic = st.selectbox("Topic",
        ["All","Politics","Economy","Technology","Health",
         "Climate","Sports","Crime","General"],
        label_visibility="collapsed")

    st.divider()
    if st.button("REFRESH DATA"):
        st.cache_data.clear()
        st.rerun()
    st.markdown(
        "<div style='font-size:10px;color:#3a2225;margin-top:10px;letter-spacing:1px'>"
        "Updated " + datetime.now().strftime("%H:%M:%S") + "</div>",
        unsafe_allow_html=True
    )


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df     = get_articles(hours, country, category, topic)
df_tr  = get_trend(hours)
df_top = get_topics(hours)
df_ctr = get_countries(hours)
total  = count_total()


# ── MASTHEAD ──────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='border-bottom:2px solid #c0152a;padding-bottom:16px;margin-bottom:22px'>"
    "<div style='font-family:Libre Baskerville,Georgia,serif;"
    "font-size:clamp(2rem,4vw,3.6rem);font-weight:700;color:#f5f0eb;"
    "letter-spacing:0.08em;text-transform:uppercase;line-height:1.0'>"
    "GLOBAL NEWS PULSE</div>"
    "<div style='display:flex;align-items:center;gap:10px;margin-top:8px;"
    "font-family:DM Sans,sans-serif;font-size:11px;color:#5a4a4d;"
    "letter-spacing:2px;text-transform:uppercase'>"
    "<span style='display:inline-block;width:7px;height:7px;"
    "background:#c0152a;border-radius:50%'></span>"
    "LIVE &nbsp;&middot;&nbsp; " + str(hours) + "H WINDOW &nbsp;&middot;&nbsp; "
    + datetime.now().strftime('%A, %d %B %Y').upper() +
    "</div></div>",
    unsafe_allow_html=True
)


# ── KPI ROW ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.metric("ARTICLES", f"{len(df):,}")
with k2: st.metric("TOTAL STORED", f"{total:,}")
with k3:
    v = f"{round(len(df[df.sentiment=='positive'])/len(df)*100,1)}%" if not df.empty else "—"
    st.metric("POSITIVE", v)
with k4:
    v = f"{round(len(df[df.sentiment=='negative'])/len(df)*100,1)}%" if not df.empty else "—"
    st.metric("NEGATIVE", v)
with k5:
    v = f"{df.score.mean():+.3f}" if not df.empty else "—"
    st.metric("AVG SCORE", v)

st.divider()

if df.empty:
    st.warning("No articles found. Run `python scripts/ingest.py` first, then click REFRESH DATA.")
    st.stop()


# ── ROW 1 — Trend + Topics ──────────
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown(
        "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
        "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
        "letter-spacing:2px;margin-bottom:12px'>Sentiment Timeline</div>",
        unsafe_allow_html=True
    )
    if not df_tr.empty and "slot" in df_tr.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_tr["slot"], y=df_tr["pos"].astype(float),
            name="Positive", mode="lines", fill="tozeroy",
            line=dict(color=MR, width=1.5),
            fillcolor="rgba(107,15,26,0.15)",
        ))
        fig.add_trace(go.Scatter(
            x=df_tr["slot"], y=(-df_tr["neg"]).astype(float),
            name="Negative", mode="lines", fill="tozeroy",
            line=dict(color=RD, width=1.5),
            fillcolor="rgba(192,21,42,0.1)",
        ))
        fig.add_trace(go.Scatter(
            x=df_tr["slot"], y=df_tr["avg_s"].astype(float) * 30,
            name="Score x30", mode="lines+markers",
            line=dict(color=WH, width=1.5, dash="dot"),
            marker=dict(size=3, color=WH),
        ))
        fig.add_hline(y=0, line_color=BR)
        styled(fig, h=300)
        fig.update_layout(
            legend=dict(orientation="h", y=1.12, x=0,
                        font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data yet.")

with col2:
    st.markdown(
        "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
        "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
        "letter-spacing:2px;margin-bottom:12px'>Topics</div>",
        unsafe_allow_html=True
    )
    if not df_top.empty:
        df_top["avg_s"] = df_top["avg_s"].astype(float)
        bar_colors = [MR if v >= 0 else RD for v in df_top["avg_s"]]
        fig2 = go.Figure(go.Bar(
            x=df_top["cnt"], y=df_top["topic"], orientation="h",
            marker_color=bar_colors, marker_line_width=0,
            text=df_top["cnt"], textposition="outside",
            textfont=dict(size=10, color=TL),
        ))
        styled(fig2, h=300)
        fig2.update_layout(yaxis=dict(tickfont=dict(size=11, color=WH)))
        st.plotly_chart(fig2, use_container_width=True)

st.divider()


# ── ROW 2 — Country + Donut + Word Cloud ─────────────────────────────────────
col3, col4, col5 = st.columns([2, 2, 3], gap="large")

with col3:
    st.markdown(
        "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
        "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
        "letter-spacing:2px;margin-bottom:12px'>By Country</div>",
        unsafe_allow_html=True
    )
    if not df_ctr.empty:
        cmap_c = {"us":"USA","in":"India","gb":"UK","au":"AUS","ca":"Canada"}
        df_ctr["label"] = df_ctr["country"].map(cmap_c).fillna(
            df_ctr["country"].str.upper()
        )
        df_ctr["avg_s"] = df_ctr["avg_s"].astype(float)
        bar_c = [MR if v >= 0 else RD for v in df_ctr["avg_s"]]
        fig3 = go.Figure(go.Bar(
            x=df_ctr["label"], y=df_ctr["avg_s"],
            marker_color=bar_c, marker_line_width=0,
            text=df_ctr["cnt"], textposition="outside",
            textfont=dict(size=10, color=TL),
        ))
        fig3.add_hline(y=0, line_color=BR)
        styled(fig3, h=260)
        fig3.update_layout(xaxis=dict(tickfont=dict(size=11, color=WH)))
        st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown(
        "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
        "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
        "letter-spacing:2px;margin-bottom:12px'>Sentiment Mix</div>",
        unsafe_allow_html=True
    )
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    cmap2 = {"positive": MR, "negative": RD, "neutral": "#2a1215"}
    fig4 = px.pie(
        counts, values="count", names="sentiment",
        color="sentiment", color_discrete_map=cmap2, hole=0.62,
    )
    fig4.update_traces(
        textfont_size=11, textfont_color=WH,
        marker=dict(line=dict(color=BK, width=3)),
    )
    styled(fig4, h=260)
    fig4.update_layout(
        legend=dict(font=dict(size=11, color=WH),
                    bgcolor="rgba(0,0,0,0)",
                    orientation="h", y=-0.12),
        annotations=[dict(
            text="<b>" + str(len(df)) + "</b><br>articles",
            x=0.5, y=0.5, font_size=15,
            showarrow=False, font_color=WH,
        )],
    )
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.markdown(
        "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
        "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
        "letter-spacing:2px;margin-bottom:12px'>Keywords</div>",
        unsafe_allow_html=True
    )
    all_kw = " ".join(df["keywords"].dropna().tolist())
    if all_kw.strip():
        wc = WordCloud(
            width=900, height=260,
            background_color=DK,
            color_func=lambda *args, **kwargs: WH,
            max_words=80, collocations=False,
            prefer_horizontal=0.8,
        ).generate(all_kw)
        fig_wc, ax = plt.subplots(figsize=(9, 2.6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        fig_wc.patch.set_facecolor(DK)
        plt.tight_layout(pad=0)
        st.pyplot(fig_wc)
    else:
        st.info("No keywords yet.")

st.divider()


# ── LIVE FEED ──────
st.markdown(
    "<div style='font-family:Libre Baskerville,serif;font-size:13px;"
    "font-weight:700;color:#f5f0eb;text-transform:uppercase;"
    "letter-spacing:2px;margin-bottom:14px'>Live Feed</div>",
    unsafe_allow_html=True
)

fc1, fc2 = st.columns([2, 2])
with fc1:
    sort_by = st.selectbox("Sort",
        ["Most Recent", "Most Positive", "Most Negative"],
        label_visibility="collapsed")
with fc2:
    show_n = st.slider("Show", 5, 50, 15, label_visibility="collapsed")

if sort_by == "Most Recent":
    disp = df.sort_values("published_at", ascending=False).head(show_n)
elif sort_by == "Most Positive":
    disp = df.sort_values("score", ascending=False).head(show_n)
else:
    disp = df.sort_values("score", ascending=True).head(show_n)

for _, row in disp.iterrows():
    s     = row["sentiment"]
    score = float(row["score"])
    ts    = pd.to_datetime(row["published_at"]).strftime("%d %b · %H:%M")
    desc  = (row["description"] or "")[:150]

    if s == "positive":
        border_col = MR
        badge_bg   = "rgba(107,15,26,0.3)"
        badge_fg   = "#e8a0a8"
        label      = "POSITIVE"
    elif s == "negative":
        border_col = RD
        badge_bg   = "rgba(192,21,42,0.2)"
        badge_fg   = RD
        label      = "NEGATIVE"
    else:
        border_col = "#2a1215"
        badge_bg   = "rgba(42,18,21,0.4)"
        badge_fg   = TL
        label      = "NEUTRAL"

    score_str  = f"{score:+.3f}"
    country_up = row['country'].upper()
    topic_up   = row['topic'].upper()
    title_safe = row['title']
    url_safe   = row['url']
    source     = row['source_name']

    st.markdown(
        "<div style='background:" + DK + ";border:1px solid " + BR + ";"
        "border-left:3px solid " + border_col + ";border-radius:4px;"
        "padding:14px 18px;margin-bottom:8px'>"
        "<div style='margin-bottom:8px'>"
        "<span style='background:" + badge_bg + ";color:" + badge_fg + ";"
        "border-radius:3px;padding:2px 9px;font-size:9px;font-weight:700;"
        "letter-spacing:2px;margin-right:6px'>" + label + "</span>"
        "<span style='background:rgba(192,21,42,0.12);color:#c0152a;"
        "border-radius:3px;padding:2px 9px;font-size:9px;font-weight:700;"
        "letter-spacing:2px;margin-right:6px'>" + topic_up + "</span>"
        "<span style='color:#5a4a4d;font-size:9px;letter-spacing:1px'>"
        + score_str + "</span></div>"
        "<div style='font-family:Libre Baskerville,Georgia,serif;font-size:14px;"
        "font-weight:700;color:#f5f0eb;line-height:1.45;margin-bottom:5px'>"
        + title_safe + "</div>"
        "<div style='font-size:12px;color:#5a4a4d;line-height:1.6;margin-bottom:8px'>"
        + desc + "</div>"
        "<div style='font-size:10px;color:#3a2225;text-transform:uppercase;letter-spacing:1px'>"
        + source + " &middot; " + ts + " &middot; " + country_up +
        " &nbsp; <a href='" + url_safe + "' target='_blank' "
        "style='color:#c0152a;text-decoration:none;font-weight:600'>Read &rarr;</a>"
        "</div></div>",
        unsafe_allow_html=True
    )


# ── FOOTER ───────────
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:10px;color:#3a2225;"
    "letter-spacing:2px;text-transform:uppercase;padding:4px 0'>"
    "BUILT WITH PYTHON &middot; MYSQL &middot; STREAMLIT &middot; NEWSAPI"
    "</div>",
    unsafe_allow_html=True
)
