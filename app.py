"""
NETFLIX CONTENT ANALYTICS — PREMIUM CINEMATIC DASHBOARD
Exploring Movies and TV Shows Around the World
Version 2.0 — Premium Redesign

Ujian Tengah Semester (UTS) Mata Kuliah Visualisasi Data
Mahasiswa: Ayu Maesaroh | NIM: 241041010
Prodi: Manajemen Informatika
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from analysis.data_analysis import (
    load_and_clean_data,
    get_exploded_countries,
    get_exploded_genres,
    generate_analytical_insights
)

# =============================================================================
# 1. PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Netflix Content Analytics | UTS Visualisasi Data",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. CSS INJECTION
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Color palette constants ---
RED        = "#E50914"
RED_DARK   = "#B81D24"
WHITE      = "#FFFFFF"
GRAY       = "#A1A1AA"
DARK_GRAY  = "#242424"
CARD_BG    = "#141414"
BG         = "#080808"

# =============================================================================
# 3. PLOTLY UNIFIED THEME
# =============================================================================
def style_fig(fig, title: str = "", height: int = 420, transparent: bool = False):
    bg = "rgba(0,0,0,0)" if transparent else CARD_BG
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        height=height,
        font=dict(family="Inter, -apple-system, sans-serif", color=WHITE, size=12),
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(color=WHITE, size=14),
            x=0.01, y=0.97
        ),
        margin=dict(l=30, r=24, t=52 if title else 20, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right",  x=1,
            font=dict(color=GRAY, size=11),
            bgcolor="rgba(0,0,0,0)"
        ),
        xaxis=dict(
            gridcolor="#1e1e1e",
            zerolinecolor="#1e1e1e",
            tickfont=dict(color=GRAY, size=11),
            title=dict(font=dict(color=GRAY, size=12))
        ),
        yaxis=dict(
            gridcolor="#1e1e1e",
            zerolinecolor="#1e1e1e",
            tickfont=dict(color=GRAY, size=11),
            title=dict(font=dict(color=GRAY, size=12))
        ),
        hoverlabel=dict(
            bgcolor="#0d0d0d",
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor=RED
        )
    )
    return fig

# =============================================================================
# 4. DATA — LOAD & CACHE
# =============================================================================
@st.cache_data(show_spinner=False)
def get_data():
    raw     = os.path.join(BASE_DIR, "data", "netflix_titles.csv")
    cleaned = os.path.join(BASE_DIR, "data", "netflix_cleaned.csv")
    if os.path.exists(cleaned):
        df = pd.read_csv(cleaned)
    else:
        df = load_and_clean_data(raw, cleaned)
    df['date_added_clean'] = pd.to_datetime(df['date_added_clean'], errors='coerce')
    df_c = get_exploded_countries(df)
    df_g = get_exploded_genres(df)
    ins   = generate_analytical_insights(df)
    return df, df_c, df_g, ins

df, df_countries, df_genres, insights_data = get_data()

# Pre-compute common stats
_valid_c   = df_countries[~df_countries['country'].isin(['Unknown Country', ''])]
TOTAL_CNT  = len(df)
TOTAL_MOV  = int((df['type'] == 'Movie').sum())
TOTAL_TV   = int((df['type'] == 'TV Show').sum())
TOTAL_CTR  = int(_valid_c['country'].nunique())
TOTAL_GEN  = int(df_genres['genre'].nunique())
MOV_PCT    = TOTAL_MOV / TOTAL_CNT * 100
TV_PCT     = TOTAL_TV  / TOTAL_CNT * 100

# =============================================================================
# 5. SIDEBAR — PREMIUM DASHBOARD SHELL
# =============================================================================
with st.sidebar:

    # ── A. LOGO + BRANDING ──────────────────────────────────────────────────
    st.markdown(
        """
        <div class="sb-logo-wrap">
            <div class="sb-logo-n">N</div>
            <div class="sb-brand-title">NETFLIX</div>
            <div class="sb-brand-sub">Content Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── B. STUDENT IDENTITY CARD (top of sidebar) ───────────────────────────
    st.markdown(
        f"""
        <div class="sb-identity-card">
            <div class="sb-id-header">
                <div class="sb-id-avatar">👩‍🎓</div>
                <div class="sb-id-name-block">
                    <div class="sb-id-label">Mahasiswa UTS</div>
                    <div class="sb-id-name">Ayu Maesaroh</div>
                    <div class="sb-id-nim-badge">NIM · 241041010</div>
                </div>
            </div>
            <div class="sb-id-divider"></div>
            <div class="sb-id-row">
                <div class="sb-id-field">
                    <div class="sb-id-field-label">Mata Kuliah</div>
                    <div class="sb-id-field-value">Visualisasi Data</div>
                </div>
                <div class="sb-id-field">
                    <div class="sb-id-field-label">Dosen Pengampu</div>
                    <div class="sb-id-field-value">Muryan Awaludin, S.Kom, M.Kom</div>
                </div>
                <div class="sb-id-field">
                    <div class="sb-id-field-label">Program Studi</div>
                    <div class="sb-id-field-value">Manajemen Informatika</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── C. NAV SECTION LABEL ────────────────────────────────────────────────
    st.markdown(
        '<div class="sb-nav-header">Navigation</div>',
        unsafe_allow_html=True
    )

    # ── D. MENU NAVIGATION ──────────────────────────────────────────────────
    menu = st.radio(
        label="nav",
        options=[
            "📊  Executive Summary",
            "🎬  Content Analysis",
            "🏷️  Genre Analysis",
            "🌍  Country Analysis",
            "🎯  Rating Analysis",
            "🔍  Data Explorer",
        ],
        index=0,
        label_visibility="collapsed"
    )

    # ── E. SIDEBAR FOOTER (dataset status) ──────────────────────────────────
    st.markdown(
        f"""
        <div class="sb-footer">
            <div class="sb-footer-dataset">
                <div class="sb-footer-dot"></div>
                <div>
                    <div class="sb-footer-dataset-name">Netflix Movies &amp; TV Shows</div>
                    <div class="sb-footer-ready">● Dataset Ready</div>
                </div>
            </div>
            <div class="sb-footer-records">{TOTAL_CNT:,} records · Kaggle Official</div>
            <div class="sb-footer-uts">UTS Visualisasi Data · 2026</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# 6. KPI CARD RENDERER
# =============================================================================
def kpi_card(icon, label, value, caption, bar_pct=None):
    bar_html = ""
    if bar_pct is not None:
        bar_html = f"""
        <div class="kpi-bar">
            <div class="kpi-bar-fill" style="width:{min(bar_pct,100):.1f}%"></div>
        </div>"""
    return f"""
    <div class="kpi-card">
        <div class="kpi-card-glow"></div>
        <div class="kpi-icon-wrap">
            <div class="kpi-icon-box">{icon}</div>
        </div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-caption">{caption}</div>
        {bar_html}
    </div>"""

def render_kpi_row(total, movies, tvshows, countries):
    mov_p = movies / total * 100 if total else 0
    tv_p  = tvshows / total * 100 if total else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("📺", "TOTAL KONTEN", f"{total:,}", "Seluruh katalog global Netflix"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("🎬", "TOTAL MOVIES", f"{movies:,}", f"{mov_p:.1f}% dari keseluruhan katalog", mov_p), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("🍿", "TOTAL TV SHOWS", f"{tvshows:,}", f"{tv_p:.1f}% dari keseluruhan katalog", tv_p), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("🌍", "TOTAL NEGARA", f"{countries:,}", "Negara produsen di seluruh dunia"), unsafe_allow_html=True)

# =============================================================================
# 7. PAGE ROUTING
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — EXECUTIVE SUMMARY (OVERVIEW)
# ─────────────────────────────────────────────────────────────────────────────
if "Executive Summary" in menu:

    # ── HERO ────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-bg"></div>
            <div class="hero-accent-line"></div>
            <div class="hero-content">
                <div class="hero-eyebrow">
                    <div class="hero-eyebrow-dot"></div>
                    <span class="hero-eyebrow-text">Netflix Content Intelligence</span>
                </div>
                <h1 class="hero-title">NETFLIX CONTENT <span class="accent">ANALYTICS</span></h1>
                <p class="hero-subtitle">Global Streaming Content Insights &amp; Data Intelligence Platform<br>
                Eksplorasi mendalam katalog film dan serial TV Netflix secara global berbasis data aktual.</p>
                <div class="hero-stats">
                    <div class="hero-stat">
                        <div class="hero-stat-value">{TOTAL_CNT:,}</div>
                        <div class="hero-stat-label">Titles Analyzed</div>
                    </div>
                    <div class="hero-stat-sep"></div>
                    <div class="hero-stat">
                        <div class="hero-stat-value">{TOTAL_CTR}</div>
                        <div class="hero-stat-label">Countries</div>
                    </div>
                    <div class="hero-stat-sep"></div>
                    <div class="hero-stat">
                        <div class="hero-stat-value">{TOTAL_GEN}</div>
                        <div class="hero-stat-label">Genres</div>
                    </div>
                    <div class="hero-stat-sep"></div>
                    <div class="hero-stat">
                        <div class="hero-stat-value">{df['release_year'].min()}–{df['release_year'].max()}</div>
                        <div class="hero-stat-label">Release Range</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── KPI CARDS ───────────────────────────────────────────────────────────
    render_kpi_row(TOTAL_CNT, TOTAL_MOV, TOTAL_TV, TOTAL_CTR)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 1: Donut + Line ──────────────────────────────────────────────────
    col_a, col_b = st.columns([1, 1.4])

    with col_a:
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']
        fig_donut = go.Figure(data=[go.Pie(
            labels=type_counts['type'],
            values=type_counts['count'],
            hole=0.65,
            marker=dict(colors=[RED, "#D1D5DB"], line=dict(color=CARD_BG, width=3)),
            textinfo='label+percent',
            textfont=dict(color=WHITE, size=12),
            hovertemplate="<b>%{label}</b><br>%{value:,} judul<br>%{percent}<extra></extra>"
        )])
        fig_donut.add_annotation(
            text=f"<b>{TOTAL_CNT:,}</b><br><span style='font-size:10px'>Total</span>",
            x=0.5, y=0.5, font_size=17, font_color=WHITE, showarrow=False
        )
        style_fig(fig_donut, "Movie vs TV Show")
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_b:
        rel = df.groupby(['release_year', 'type']).size().reset_index(name='count')
        rel = rel[rel['release_year'] >= 1980]
        fig_line = px.line(rel, x='release_year', y='count', color='type',
                           color_discrete_map={'Movie': RED, 'TV Show': '#D1D5DB'},
                           markers=True)
        fig_line.update_traces(line=dict(width=2.5), marker=dict(size=5))
        style_fig(fig_line, "Tren Konten Berdasarkan Tahun Rilis (1980–2021)")
        fig_line.update_xaxes(title_text="Tahun Rilis")
        fig_line.update_yaxes(title_text="Jumlah Judul")
        st.plotly_chart(fig_line, use_container_width=True)

    # ── ROW 2: Top Countries + Top Genres ────────────────────────────────────
    col_c, col_d = st.columns(2)

    with col_c:
        tc = (_valid_c['country'].value_counts().head(10)
              .reset_index().rename(columns={'country':'country','count':'count'}))
        tc.columns = ['country', 'count']
        tc = tc.sort_values('count', ascending=True)
        fig_tc = px.bar(tc, x='count', y='country', orientation='h', text='count',
                        color='count', color_continuous_scale=['#3f0608','#8b0000', RED])
        fig_tc.update_traces(textposition='outside', textfont=dict(color=WHITE, size=11),
                             hovertemplate="<b>%{y}</b><br>%{x:,} judul<extra></extra>")
        fig_tc.update_coloraxes(showscale=False)
        style_fig(fig_tc, "Top 10 Negara Produsen Konten Terbanyak")
        fig_tc.update_xaxes(title_text="Jumlah Konten")
        fig_tc.update_yaxes(title_text="")
        st.plotly_chart(fig_tc, use_container_width=True)

    with col_d:
        tg = df_genres['genre'].value_counts().head(10).reset_index()
        tg.columns = ['genre', 'count']
        tg = tg.sort_values('count', ascending=True)
        fig_tg = px.bar(tg, x='count', y='genre', orientation='h', text='count',
                        color='count', color_continuous_scale=['#2a2a2a','#5a5a5a', WHITE])
        fig_tg.update_traces(textposition='outside', textfont=dict(color=WHITE, size=11),
                             hovertemplate="<b>%{y}</b><br>%{x:,} kemunculan<extra></extra>")
        fig_tg.update_coloraxes(showscale=False)
        style_fig(fig_tg, "Top 10 Genre Paling Populer di Netflix")
        fig_tg.update_xaxes(title_text="Frekuensi Judul")
        fig_tg.update_yaxes(title_text="")
        st.plotly_chart(fig_tg, use_container_width=True)

    # ── KEY INSIGHTS ─────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div>
                <div style="font-size:1.1rem;font-weight:800;color:{WHITE};">💡 Key Analytical Insights</div>
                <div style="font-size:0.78rem;color:{GRAY};margin-top:3px;">Temuan fakta utama berdasarkan pemrosesan data aktual Netflix</div>
            </div>
            <div style="background:rgba(229,9,20,0.15);color:{RED};border:1px solid rgba(229,9,20,0.35);
                        padding:4px 12px;border-radius:20px;font-size:0.65rem;font-weight:700;letter-spacing:0.8px;">
                VERIFIED BY DATA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    ins_items = list(insights_data.values())
    for row_start in range(0, len(ins_items[:6]), 3):
        cols = st.columns(3)
        for i, item in enumerate(ins_items[row_start:row_start+3]):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="insight-box">
                        <div class="insight-tag">INSIGHT #{row_start+i+1}</div>
                        <div class="insight-title">{item['title']}</div>
                        <div class="insight-metric-pill">{item['stat']}</div>
                        <p class="insight-desc">{item['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — CONTENT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif "Content Analysis" in menu:

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Format &amp; Temporal Growth Analysis</span>
            <h1 class="hero-title">CONTENT <span>ANALYSIS</span></h1>
            <p class="hero-subtitle">Eksplorasi Komparasi Format Film vs Serial TV, Tren Rilis, &amp; Karakteristik Durasi</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Quick stat row
    movie_count = (df['type'] == 'Movie').sum()
    tv_count    = (df['type'] == 'TV Show').sum()
    peak_yr     = df['release_year'].value_counts().idxmax()
    peak_cnt    = df['release_year'].value_counts().max()
    peak_add    = df['year_added'].value_counts().idxmax()
    peak_add_c  = df['year_added'].value_counts().max()

    s1, s2, s3, s4 = st.columns(4)
    for col, lbl, val, sub in [
        (s1, "Total Movies",       f"{movie_count:,}",  f"{movie_count/len(df)*100:.1f}%"),
        (s2, "Total TV Shows",     f"{tv_count:,}",     f"{tv_count/len(df)*100:.1f}%"),
        (s3, "Puncak Tahun Rilis", str(peak_yr),        f"{peak_cnt:,} Judul"),
        (s4, "Puncak Ditambahkan", str(peak_add),       f"{peak_add_c:,} Judul Baru"),
    ]:
        col.metric(lbl, val, sub)

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Distribusi Konten per Tahun
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">📅</div>
            <div><div class="section-title">1. Distribusi Konten Berdasarkan Tahun Rilis</div>
            <div class="section-subtitle">Volume produksi film vs serial TV per tahun (slider interaktif)</div></div>
        </div>""", unsafe_allow_html=True
    )

    yr_range = st.slider("Rentang Tahun:", min_value=1960, max_value=int(df['release_year'].max()), value=(1995, 2021))
    ydf = df[(df['release_year'] >= yr_range[0]) & (df['release_year'] <= yr_range[1])]
    yt  = ydf.groupby(['release_year', 'type']).size().reset_index(name='count')
    fig_yr = px.bar(yt, x='release_year', y='count', color='type', barmode='stack',
                    color_discrete_map={'Movie': RED, 'TV Show': '#D1D5DB'})
    style_fig(fig_yr, f"Distribusi Konten Rilis ({yr_range[0]}–{yr_range[1]})")
    fig_yr.update_xaxes(title_text="Tahun Rilis")
    fig_yr.update_yaxes(title_text="Jumlah Judul")
    st.plotly_chart(fig_yr, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Area Chart Date Added
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">📈</div>
            <div><div class="section-title">2. Tren Penambahan Konten ke Platform</div>
            <div class="section-subtitle">Kapan konten diakuisisi & ditambahkan ke server Netflix (date_added)</div></div>
        </div>""", unsafe_allow_html=True
    )

    at = df.groupby(['year_added', 'type']).size().reset_index(name='count')
    at = at[at['year_added'] >= 2008]
    fig_area = px.area(at, x='year_added', y='count', color='type',
                       color_discrete_map={'Movie': RED, 'TV Show': '#A0A0A0'}, markers=True)
    style_fig(fig_area, "Tren Pertumbuhan Penambahan Konten Netflix Berdasarkan Tahun")
    fig_area.update_xaxes(title_text="Tahun Ditambahkan ke Netflix")
    fig_area.update_yaxes(title_text="Jumlah Konten Baru")
    st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Durasi
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">⏱️</div>
            <div><div class="section-title">3. Karakteristik Durasi Konten</div>
            <div class="section-subtitle">Sebaran menit film & distribusi musim serial TV</div></div>
        </div>""", unsafe_allow_html=True
    )

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        mdf = df[df['type'] == 'Movie'].copy()
        fig_hist = px.histogram(mdf, x='duration_int', nbins=40, color_discrete_sequence=[RED])
        avg_d = mdf['duration_int'].mean()
        med_d = mdf['duration_int'].median()
        fig_hist.add_vline(x=avg_d, line_dash="dash", line_color=WHITE,
                           annotation_text=f"Mean: {avg_d:.0f}m", annotation_position="top right")
        fig_hist.add_vline(x=med_d, line_dash="dot", line_color="#FFA500",
                           annotation_text=f"Median: {med_d:.0f}m", annotation_position="top left")
        style_fig(fig_hist, "Distribusi Durasi Film (Movie Duration in Minutes)")
        fig_hist.update_xaxes(title_text="Durasi Film (Menit)")
        fig_hist.update_yaxes(title_text="Jumlah Judul Film")
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption(f"💡 Rata-rata: **{avg_d:.1f} menit**, Median: **{med_d:.0f} menit** · Film terpanjang: **{mdf.loc[mdf['duration_int'].idxmax(),'title']}** ({mdf['duration_int'].max()} menit)")

    with col_d2:
        tdf = df[df['type'] == 'TV Show'].copy()
        sc  = tdf['duration_int'].value_counts().reset_index()
        sc.columns = ['seasons', 'count']
        sc  = sc.sort_values('seasons')
        fig_seas = px.bar(sc, x='seasons', y='count', text='count',
                          color='count', color_continuous_scale=['#1a1a1a','#660000', RED])
        fig_seas.update_traces(textposition='outside', textfont=dict(color=WHITE, size=11))
        fig_seas.update_coloraxes(showscale=False)
        style_fig(fig_seas, "Distribusi Jumlah Musim (TV Show Seasons)")
        fig_seas.update_xaxes(title_text="Jumlah Musim (Season)", tickmode='linear', dtick=1)
        fig_seas.update_yaxes(title_text="Jumlah Serial TV")
        st.plotly_chart(fig_seas, use_container_width=True)
        tv1_pct = (tdf['duration_int'] == 1).sum() / len(tdf) * 100
        longest_tv = tdf.loc[tdf['duration_int'].idxmax()]
        st.caption(f"💡 **{tv1_pct:.1f}%** serial TV hanya memiliki 1 Season · Terpanjang: **{longest_tv['title']}** ({longest_tv['duration_int']} Seasons)")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — GENRE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif "Genre Analysis" in menu:

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Taxonomy &amp; Category Breakdown</span>
            <h1 class="hero-title">GENRE <span>ANALYSIS</span></h1>
            <p class="hero-subtitle">Eksplorasi Persebaran Tema, Genre Terpopuler, Komparasi Tipe Konten, &amp; Evolusi Waktu</p>
        </div>
        """, unsafe_allow_html=True
    )

    # 1. Top 10 Genre
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">🏆</div>
            <div><div class="section-title">1. Top 10 Genre Netflix Teratas</div>
            <div class="section-subtitle">Frekuensi kemunculan genre setelah pemisahan multi-genre (exploding)</div></div>
        </div>""", unsafe_allow_html=True
    )
    cg1, cg2 = st.columns([1.4, 1])
    with cg1:
        t10g = df_genres['genre'].value_counts().head(10).reset_index()
        t10g.columns = ['genre', 'count']
        t10g = t10g.sort_values('count', ascending=True)
        fig_t10g = px.bar(t10g, x='count', y='genre', orientation='h', text='count',
                          color='count', color_continuous_scale=['#2a2a2a','#8b0000', RED])
        fig_t10g.update_traces(textposition='outside')
        fig_t10g.update_coloraxes(showscale=False)
        style_fig(fig_t10g, "Top 10 Genre Netflix Berdasarkan Frekuensi Judul", height=430)
        fig_t10g.update_xaxes(title_text="Jumlah Judul")
        fig_t10g.update_yaxes(title_text="")
        st.plotly_chart(fig_t10g, use_container_width=True)

    with cg2:
        # Build insight text dynamically
        int_mov_val = t10g[t10g['genre'] == 'International Movies']['count'].values
        dramas_val  = t10g[t10g['genre'] == 'Dramas']['count'].values
        comedy_val  = t10g[t10g['genre'] == 'Comedies']['count'].values
        int_mov_str  = f"{int_mov_val[0]:,}" if len(int_mov_val) else "N/A"
        dramas_str   = f"{dramas_val[0]:,}"  if len(dramas_val)  else "N/A"
        comedy_str   = f"{comedy_val[0]:,}"  if len(comedy_val)  else "N/A"
        st.markdown(
            f"""
            <div class="content-card" style="height:430px;overflow:auto;">
                <div class="content-card-title">📌 Analisis Taksonomi Genre</div>
                <p style="color:{GRAY};font-size:0.85rem;line-height:1.65;margin-top:12px;">
                    Netflix menggunakan skema kategorisasi <b>multi-label</b> dimana satu judul dapat memiliki 1 hingga 3 genre sekaligus.
                </p>
                <div class="sb-id-divider"></div>
                <div style="display:flex;flex-direction:column;gap:10px;margin-top:4px;">
                    <div class="insight-box" style="margin-bottom:0;">
                        <div class="insight-tag">PERINGKAT #1</div>
                        <div class="insight-title">International Movies</div>
                        <div class="insight-metric-pill">{int_mov_str} judul</div>
                        <p class="insight-desc">Membuktikan pilar utama diversifikasi konten internasional non-Hollywood.</p>
                    </div>
                    <div class="insight-box" style="margin-bottom:0;">
                        <div class="insight-tag">PERINGKAT #2–3</div>
                        <div class="insight-title">Dramas &amp; Comedies</div>
                        <div class="insight-metric-pill">{dramas_str} · {comedy_str} judul</div>
                        <p class="insight-desc">Dua genre naratif fiksi terpopuler di seluruh format konten Netflix.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Movie vs TV Show Genre Comparison
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">⚖️</div>
            <div><div class="section-title">2. Perbandingan Genre: Movie vs TV Show</div>
            <div class="section-subtitle">Top 8 genre dominan per format konten</div></div>
        </div>""", unsafe_allow_html=True
    )
    cgm, cgt = st.columns(2)
    with cgm:
        mg = df_genres[df_genres['type'] == 'Movie']['genre'].value_counts().head(8).reset_index()
        mg.columns = ['genre', 'count']
        mg = mg.sort_values('count', ascending=True)
        fig_mg = px.bar(mg, x='count', y='genre', orientation='h', text='count',
                        color_discrete_sequence=[RED])
        fig_mg.update_traces(textposition='outside')
        style_fig(fig_mg, "Top 8 Genre Khusus Movies")
        fig_mg.update_xaxes(title_text="Jumlah Film")
        fig_mg.update_yaxes(title_text="")
        st.plotly_chart(fig_mg, use_container_width=True)

    with cgt:
        tg2 = df_genres[df_genres['type'] == 'TV Show']['genre'].value_counts().head(8).reset_index()
        tg2.columns = ['genre', 'count']
        tg2 = tg2.sort_values('count', ascending=True)
        fig_tg2 = px.bar(tg2, x='count', y='genre', orientation='h', text='count',
                         color_discrete_sequence=['#D1D5DB'])
        fig_tg2.update_traces(textposition='outside', textfont=dict(color=WHITE))
        style_fig(fig_tg2, "Top 8 Genre Khusus TV Shows")
        fig_tg2.update_xaxes(title_text="Jumlah Serial")
        fig_tg2.update_yaxes(title_text="")
        st.plotly_chart(fig_tg2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Heatmap Genre × Tahun
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">🔥</div>
            <div><div class="section-title">3. Heatmap Genre Terpopuler × Tahun Rilis</div>
            <div class="section-subtitle">Intensitas rilis genre dalam 10 tahun terakhir (2012–2021)</div></div>
        </div>""", unsafe_allow_html=True
    )
    top8_names  = df_genres['genre'].value_counts().head(8).index.tolist()
    recent_g    = df_genres[
        (df_genres['genre'].isin(top8_names)) &
        (df_genres['release_year'] >= 2012) &
        (df_genres['release_year'] <= 2021)
    ]
    hmap_data = recent_g.groupby(['genre', 'release_year']).size().unstack(fill_value=0)
    fig_heat  = px.imshow(hmap_data,
                          color_continuous_scale=['#0d0d0d','#4a0d10','#b81d24', RED, '#ff8080'],
                          text_auto=True, aspect="auto")
    style_fig(fig_heat, "Intensitas Rilis Genre Populer per Tahun (2012–2021)", height=460)
    fig_heat.update_xaxes(title_text="Tahun Rilis")
    fig_heat.update_yaxes(title_text="Genre")
    st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — COUNTRY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif "Country Analysis" in menu:

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Geographic Intelligence &amp; Global Reach</span>
            <h1 class="hero-title">COUNTRY <span>ANALYSIS</span></h1>
            <p class="hero-subtitle">Pemetaan Kontribusi Produksi Konten Berdasarkan Negara &amp; Wilayah Global</p>
        </div>
        """, unsafe_allow_html=True
    )

    vc = df_countries[~df_countries['country'].isin(['Unknown Country', ''])]
    top_cname = vc['country'].value_counts().index[0]
    top_cval  = vc['country'].value_counts().iloc[0]

    cck1, cck2, cck3, cck4 = st.columns(4)
    cck1.metric("Total Negara", f"{vc['country'].nunique():,}")
    cck2.metric("Negara #1",    top_cname, f"{top_cval:,} Judul")
    cck3.metric("Asia Selatan", "India",   f"{(vc['country']=='India').sum():,} Judul")
    cck4.metric("Asia Timur",   "Jepang",  f"{(vc['country']=='Japan').sum():,} Judul")

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Choropleth Map
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">🗺️</div>
            <div><div class="section-title">1. Peta Distribusi Produksi Konten Global</div>
            <div class="section-subtitle">Peta interaktif 122 negara produsen konten Netflix</div></div>
        </div>""", unsafe_allow_html=True
    )
    cc = vc['country'].value_counts().reset_index()
    cc.columns = ['country', 'count']
    fig_map = px.choropleth(
        cc, locations='country', locationmode='country names', color='count',
        hover_name='country', hover_data={'count': ':,', 'country': False},
        color_continuous_scale=['#141414','#4a0d10','#8b0000', RED, '#ff4444'],
        labels={'count': 'Jumlah Konten'}
    )
    fig_map.update_geos(bgcolor='#0a0a0a', showocean=True, oceancolor='#070707',
                        showland=True, landcolor='#141414', showlakes=True, lakecolor='#070707',
                        showcoastlines=True, coastlinecolor='#2a2a2a',
                        showcountries=True, countrycolor='#242424')
    fig_map.update_coloraxes(colorbar=dict(
        title=dict(text="Judul", font=dict(color=WHITE)),
        tickfont=dict(color=GRAY)
    ))
    style_fig(fig_map, "Peta Sebaran Konten Netflix di Seluruh Dunia", height=500)
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Country Type Breakdown
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">📊</div>
            <div><div class="section-title">2. Top 10 Negara: Komposisi Movie vs TV Show</div>
            <div class="section-subtitle">Preferensi produksi per format konten di tiap negara</div></div>
        </div>""", unsafe_allow_html=True
    )
    top10c   = vc['country'].value_counts().head(10).index.tolist()
    t10df    = vc[vc['country'].isin(top10c)]
    ctb      = t10df.groupby(['country', 'type']).size().reset_index(name='count')
    c_order  = vc['country'].value_counts().head(10).index.tolist()
    fig_ctb  = px.bar(ctb, x='country', y='count', color='type', barmode='group',
                      category_orders={'country': c_order},
                      color_discrete_map={'Movie': RED, 'TV Show': '#D1D5DB'})
    style_fig(fig_ctb, "Perbandingan Movie vs TV Show pada Top 10 Negara Produsen")
    fig_ctb.update_xaxes(title_text="Negara")
    fig_ctb.update_yaxes(title_text="Jumlah Konten")
    st.plotly_chart(fig_ctb, use_container_width=True)

    # Spotlight cards
    st.markdown("#### 🌟 Sorotan Negara Produsen Utama")
    sc1, sc2, sc3 = st.columns(3)
    for col, tag, name, pill, desc in [
        (sc1,"HUB #1 AMERIKA UTARA","United States","3,690 Judul (~41.9%)","Pasar utama dan basis operasi orisinal Netflix dengan portofolio seimbang blockbuster dan serial global."),
        (sc2,"HUB #2 ASIA SELATAN","India (Bollywood)","1,046 Judul (88% Movie)","Didominasi film layar lebar Bollywood & regional. India merupakan produsen terbesar kedua setelah AS."),
        (sc3,"HUB #3 ASIA TIMUR","Japan & South Korea","318 + 231 Judul","Rasio TV Show tertinggi secara global, didorong popularitas Anime & K-Drama yang masif."),
    ]:
        with col:
            st.markdown(
                f"""<div class="insight-box">
                    <div class="insight-tag">{tag}</div>
                    <div class="insight-title">{name}</div>
                    <div class="insight-metric-pill">{pill}</div>
                    <p class="insight-desc">{desc}</p>
                </div>""",
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — RATING ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif "Rating Analysis" in menu:

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Audience Demographics &amp; Age Classification</span>
            <h1 class="hero-title">RATING <span>ANALYSIS</span></h1>
            <p class="hero-subtitle">Distribusi Klasifikasi Usia Konten &amp; Segmentasi Audiens Sasaran Netflix</p>
        </div>
        """, unsafe_allow_html=True
    )

    # 1. Bar + Donut
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">🎯</div>
            <div><div class="section-title">1. Distribusi Klasifikasi Usia</div>
            <div class="section-subtitle">Frekuensi rating konten &amp; proporsi segmentasi audiens</div></div>
        </div>""", unsafe_allow_html=True
    )
    rc1, rc2 = st.columns([1.2, 1])

    with rc1:
        rc = df['rating'].value_counts().reset_index()
        rc.columns = ['rating', 'count']
        fig_rb = px.bar(rc, x='rating', y='count', text='count',
                        color='count', color_continuous_scale=['#1a1a1a','#660000', RED])
        fig_rb.update_traces(textposition='outside')
        fig_rb.update_coloraxes(showscale=False)
        style_fig(fig_rb, "Frekuensi Konten Berdasarkan Klasifikasi Usia (Rating)")
        fig_rb.update_xaxes(title_text="Rating")
        fig_rb.update_yaxes(title_text="Jumlah Judul")
        st.plotly_chart(fig_rb, use_container_width=True)

    with rc2:
        def group_demo(r):
            if r in ['TV-MA','R','NC-17']:            return 'Dewasa (Mature)'
            elif r in ['TV-14','PG-13']:              return 'Remaja (13-14+)'
            elif r in ['TV-PG','PG']:                 return 'Bimbingan Ortu'
            elif r in ['TV-Y','TV-Y7','TV-Y7-FV','G','TV-G']: return 'Anak-anak & Keluarga'
            else:                                     return 'Lainnya / NR'
        df_d = df.copy()
        df_d['demographic'] = df_d['rating'].apply(group_demo)
        dc = df_d['demographic'].value_counts().reset_index()
        dc.columns = ['demographic', 'count']
        fig_rd = px.pie(dc, names='demographic', values='count', hole=0.58,
                        color='demographic',
                        color_discrete_map={
                            'Dewasa (Mature)': RED,
                            'Remaja (13-14+)': '#FFA07A',
                            'Bimbingan Ortu': '#D1D5DB',
                            'Anak-anak & Keluarga': '#71717A',
                            'Lainnya / NR': '#2a2a2a'
                        })
        fig_rd.update_traces(textinfo='percent+label', textfont=dict(size=11),
                             hovertemplate="<b>%{label}</b><br>%{value:,} judul<br>%{percent}<extra></extra>")
        style_fig(fig_rd, "Segmentasi Demografi Audiens")
        st.plotly_chart(fig_rd, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Rating by Type
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">📊</div>
            <div><div class="section-title">2. Perbandingan Rating: Movie vs TV Show</div>
            <div class="section-subtitle">Distribusi klasifikasi usia per format konten</div></div>
        </div>""", unsafe_allow_html=True
    )
    rt     = df.groupby(['rating','type']).size().reset_index(name='count')
    top8r  = df['rating'].value_counts().head(8).index.tolist()
    fig_rt = px.bar(rt[rt['rating'].isin(top8r)], x='rating', y='count', color='type', barmode='group',
                    color_discrete_map={'Movie': RED, 'TV Show': '#D1D5DB'})
    style_fig(fig_rt, "Perbandingan Rating Mayoritas: Movie vs TV Show")
    fig_rt.update_xaxes(title_text="Klasifikasi Usia (Rating)")
    fig_rt.update_yaxes(title_text="Jumlah Judul")
    st.plotly_chart(fig_rt, use_container_width=True)

    # 3. Rating reference table
    st.markdown(
        """<div class="section-header" style="margin-top:16px;">
            <div class="section-icon">📖</div>
            <div><div class="section-title">3. Panduan Klasifikasi Usia Netflix</div>
            <div class="section-subtitle">Referensi makna resmi rating konten</div></div>
        </div>""", unsafe_allow_html=True
    )
    st.markdown(
        """
        | Rating | Audiens Sasaran | Deskripsi | Jumlah Katalog |
        | :--- | :--- | :--- | :--- |
        | **TV-MA** | Dewasa (17/18+) | Konten eksplisit — bahasa kasar, kekerasan, tema dewasa | **3,207** (~36.4%) |
        | **TV-14** | Remaja (14+) | Materi mungkin tidak sesuai anak di bawah 14 tahun | **2,160** (~24.5%) |
        | **TV-PG** | Panduan Ortu | Memerlukan bimbingan orang tua bagi anak kecil | **863** (~9.8%) |
        | **R** | 17+ (Restricted) | Khusus bioskop dewasa tanpa pendamping | **799** (~9.1%) |
        | **PG-13** | 13+ | Diperingatkan bagi anak di bawah 13 tahun | **490** (~5.6%) |
        | **TV-Y / Y7** | Anak-Anak | Khusus untuk balita hingga usia 7 tahun ke atas | **639** (~7.3%) |
        """
    )

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 — DATA EXPLORER
# ─────────────────────────────────────────────────────────────────────────────
elif "Data Explorer" in menu:

    st.markdown(
        """
        <div class="hero-banner">
            <span class="hero-badge">Interactive Exploration &amp; Export</span>
            <h1 class="hero-title">DATA <span>EXPLORER</span></h1>
            <p class="hero-subtitle">Cari, Filter, Telusuri, dan Unduh Dataset Netflix secara Dinamis &amp; Interaktif</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Filter Panel
    st.markdown('<div class="filter-panel"><div class="filter-panel-title">⚙️ Panel Filter Interaktif</div>', unsafe_allow_html=True)

    ff1, ff2 = st.columns([2, 1])
    with ff1:
        search_query = st.text_input("🔍 Cari Judul, Sutradara, atau Pemeran:",
                                     placeholder="Contoh: Stranger Things, Inception, Squid Game, Christopher Nolan...")
    with ff2:
        type_filter = st.selectbox("Format Konten:", ["Semua Tipe", "Movie", "TV Show"])

    ff3, ff4, ff5 = st.columns(3)
    with ff3:
        yr_min = int(df['release_year'].min())
        yr_max = int(df['release_year'].max())
        sel_years = st.slider("Rentang Tahun Rilis:", min_value=yr_min, max_value=yr_max, value=(yr_min, yr_max))
    with ff4:
        avail_ratings = ["Semua Rating"] + sorted(df['rating'].dropna().unique().tolist())
        sel_rating = st.selectbox("Klasifikasi Usia (Rating):", avail_ratings)
    with ff5:
        all_genres = sorted(df_genres['genre'].dropna().unique().tolist())
        sel_genres = st.multiselect("Genre Konten:", all_genres, default=[])

    all_ctrs = sorted(_valid_c['country'].unique().tolist())
    sel_ctrs = st.multiselect("Negara Asal Produksi:", all_ctrs, default=[])

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    fdf = df.copy()
    if search_query:
        q = search_query.lower()
        fdf = fdf[
            fdf['title'].astype(str).str.lower().str.contains(q, na=False) |
            fdf['director'].astype(str).str.lower().str.contains(q, na=False) |
            fdf['cast'].astype(str).str.lower().str.contains(q, na=False) |
            fdf['description'].astype(str).str.lower().str.contains(q, na=False)
        ]
    if type_filter != "Semua Tipe":
        fdf = fdf[fdf['type'] == type_filter]
    fdf = fdf[(fdf['release_year'] >= sel_years[0]) & (fdf['release_year'] <= sel_years[1])]
    if sel_rating != "Semua Rating":
        fdf = fdf[fdf['rating'] == sel_rating]
    if sel_genres:
        matched_ids = df_genres[df_genres['genre'].isin(sel_genres)]['show_id'].unique()
        fdf = fdf[fdf['show_id'].isin(matched_ids)]
    if sel_ctrs:
        matched_cids = df_countries[df_countries['country'].isin(sel_ctrs)]['show_id'].unique()
        fdf = fdf[fdf['show_id'].isin(matched_cids)]

    # Result Bar
    total_r  = len(df)
    filt_r   = len(fdf)
    filt_pct = filt_r / total_r * 100 if total_r else 0
    st.markdown(
        f"""
        <div class="result-bar">
            <div>Menampilkan <span class="result-bar-count">{filt_r:,}</span>
                 dari total <b>{total_r:,}</b> judul &nbsp;·&nbsp; {filt_pct:.1f}% dari keseluruhan data</div>
            <div class="result-bar-status">{'Filter Aktif' if filt_r < total_r else 'Semua Data'}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Download
    csv_bytes = fdf.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Dataset Hasil Filter (CSV)",
        data=csv_bytes,
        file_name="netflix_filtered_dataset.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Data Table
    display_cols = ['show_id','type','title','director','country','release_year','rating','duration','listed_in']
    st.dataframe(
        fdf[display_cols],
        use_container_width=True,
        height=460,
        column_config={
            "show_id":       st.column_config.TextColumn("ID",             width="small"),
            "type":          st.column_config.TextColumn("Tipe",           width="small"),
            "title":         st.column_config.TextColumn("Judul",          width="large"),
            "director":      st.column_config.TextColumn("Sutradara",      width="medium"),
            "country":       st.column_config.TextColumn("Negara",         width="medium"),
            "release_year":  st.column_config.NumberColumn("Tahun", format="%d", width="small"),
            "rating":        st.column_config.TextColumn("Rating",         width="small"),
            "duration":      st.column_config.TextColumn("Durasi",         width="small"),
            "listed_in":     st.column_config.TextColumn("Genre",          width="large"),
        }
    )

    # Title Inspector
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """<div class="section-header">
            <div class="section-icon">🔎</div>
            <div><div class="section-title">Detail Inspector</div>
            <div class="section-subtitle">Pilih judul untuk melihat sinopsis &amp; detail produksi lengkap</div></div>
        </div>""", unsafe_allow_html=True
    )

    if not fdf.empty:
        sel_title = st.selectbox("Pilih Judul:", fdf['title'].tolist()[:200])
        if sel_title:
            it = fdf[fdf['title'] == sel_title].iloc[0]
            st.markdown(
                f"""
                <div class="title-inspector">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;">
                        <div>
                            <span class="hero-badge">{it['type']}</span>
                            <h2 style="color:{WHITE};margin:8px 0 4px;font-size:1.4rem;font-weight:800;">{it['title']}</h2>
                            <span style="color:{GRAY};font-size:0.85rem;">
                                📅 {it['release_year']} &nbsp;|&nbsp;
                                ⏱️ {it['duration']} &nbsp;|&nbsp;
                                🎯 <b style="color:{RED};">{it['rating']}</b>
                            </span>
                        </div>
                        <div style="text-align:right;color:#3f3f46;font-size:0.7rem;">
                            ID: {it['show_id']}<br>
                            Ditambahkan: {it['date_added']}
                        </div>
                    </div>
                    <p style="color:#e4e4e7;font-size:0.9rem;line-height:1.65;margin:14px 0;">
                        <b>Sinopsis:</b><br>{it['description']}
                    </p>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;
                                padding-top:14px;border-top:1px solid {DARK_GRAY};font-size:0.82rem;">
                        <div><div style="color:#52525b;margin-bottom:3px;">🎬 Sutradara</div>
                             <div style="color:{WHITE};">{it['director']}</div></div>
                        <div><div style="color:#52525b;margin-bottom:3px;">🌍 Negara Asal</div>
                             <div style="color:{WHITE};">{it['country']}</div></div>
                        <div><div style="color:#52525b;margin-bottom:3px;">🎭 Pemeran</div>
                             <div style="color:{WHITE};">{it['cast']}</div></div>
                        <div><div style="color:#52525b;margin-bottom:3px;">🏷️ Genre</div>
                             <div style="color:{WHITE};">{it['listed_in']}</div></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Tidak ada konten yang sesuai dengan filter yang Anda tentukan.")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown(
    """
    <div class="app-footer">
        <strong>Netflix Content Analytics Dashboard</strong> &bull; Proyek Ujian Tengah Semester (UTS) Visualisasi Data<br>
        Ayu Maesaroh · 241041010 · Manajemen Informatika &bull;
        Dibangun dengan Python, Streamlit, Pandas &amp; Plotly
    </div>
    """,
    unsafe_allow_html=True
)
