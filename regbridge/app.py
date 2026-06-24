"""
RegBridge Compliance Advisors
Plateforme SaaS de conseil et d'intelligence réglementaire
Caraïbes & Afrique — LCB-FT, GAFI, OFAC, TRACFIN/DGT, Bâle III
"""

import streamlit as st
import pandas as pd
import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "platform_data")

st.set_page_config(
    page_title="RegBridge Compliance Advisors",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# CSS — CHARTE INSTITUTIONNELLE
# Stratégie : forcer TOUT en sombre sur fond blanc.
# Les dropdowns Streamlit utilisent un thème système qu'on
# neutralise via les sélecteurs data-baseweb et stSelectbox.
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --navy:   #1c2b4a;
    --gold:   #b8975a;
    --slate:  #5a6a7a;
    --border: #e4e8ed;
    --bg:     #f5f7fa;
    --white:  #ffffff;
    --red:    #b91c1c;
    --orange: #c2410c;
    --green:  #15803d;
    --yellow: #a16207;
    --text:   #1c2b4a;
    --sub:    #4a5568;
}

/* ── FOND GLOBAL BLANC ── */
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container { background-color: var(--bg) !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── TOUT LE TEXTE EN SOMBRE ── */
html, body, .stApp, .main,
p, span, div, li, td, th, label, a,
[data-testid="stMarkdownContainer"] *,
[data-testid="stHeadingWithActionElements"] *,
.stMarkdown *, .element-container * {
    color: var(--text) !important;
}
h1, h2, h3, h4, h5, h6 {
    color: var(--navy) !important;
    font-family: 'Playfair Display', Georgia, serif !important;
}

/* ── INPUTS : fond blanc, texte sombre ── */
input, textarea,
.stTextInput input,
.stTextArea textarea {
    background-color: var(--white) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* ── SELECTBOX & MULTISELECT : forcer fond blanc texte sombre ── */
/* Conteneur dropdown */
[data-baseweb="select"] > div,
[data-baseweb="select"] > div > div,
[data-baseweb="popover"] *,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"],
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background-color: var(--white) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
    border-radius: 4px !important;
}
/* Texte dans le select */
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="select"] input {
    color: var(--text) !important;
    background-color: transparent !important;
}
/* Liste déroulante options */
[data-baseweb="menu"],
[data-baseweb="menu"] ul,
[data-baseweb="menu"] li,
[data-baseweb="option"] {
    background-color: var(--white) !important;
    color: var(--text) !important;
}
[data-baseweb="option"]:hover {
    background-color: #eef2ff !important;
}
/* Labels widgets */
.stSelectbox label, .stMultiSelect label,
.stTextInput label, .stTextArea label,
.stDateInput label, .stFileUploader label,
.stCheckbox label, .stRadio label {
    color: var(--navy) !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.2px !important;
}
/* Tags multiselect sélectionnés */
[data-baseweb="tag"] {
    background-color: var(--navy) !important;
}
[data-baseweb="tag"] span { color: white !important; }

/* ── DATE INPUT ── */
[data-testid="stDateInput"] input {
    background: white !important;
    color: var(--text) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] section {
    background: white !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 4px !important;
}
[data-testid="stFileUploader"] * { color: var(--text) !important; }

/* ── SIDEBAR : fond navy, tout blanc ── */
section[data-testid="stSidebar"] {
    background-color: var(--navy) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {
    color: #c8d6e8 !important;
    background-color: transparent !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] b,
section[data-testid="stSidebar"] strong { color: #ffffff !important; }
/* Radio buttons sidebar */
section[data-testid="stSidebar"] .stRadio label {
    color: #c8d6e8 !important;
    font-weight: 400 !important;
    font-size: 0.88rem !important;
    padding: 0.3rem 0 !important;
}
section[data-testid="stSidebar"] [aria-checked="true"] ~ div p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── NAVBAR ── */
.rb-nav {
    background-color: var(--navy);
    border-bottom: 3px solid var(--gold);
    padding: 0.85rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 0;
}
.rb-nav-name {
    font-family: 'Playfair Display', Georgia, serif;
    color: #ffffff;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.2px;
    white-space: nowrap;
}
.rb-nav-sep { color: rgba(255,255,255,0.25); font-size: 1rem; margin: 0 0.2rem; }
.rb-nav-sub {
    font-family: 'Inter', sans-serif;
    color: #8ba3c0;
    font-size: 0.7rem;
    font-weight: 300;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── HERO ZONE ── */
.rb-hero {
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 1.8rem 2rem 1.6rem;
    margin-bottom: 1.8rem;
}
.rb-hero-label {
    font-size: 0.62rem;
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 700;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
}
.rb-hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--navy);
    font-size: 1.55rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    line-height: 1.3;
}
.rb-hero-desc {
    color: var(--sub);
    font-size: 0.87rem;
    margin: 0 0 1rem;
    line-height: 1.65;
    max-width: 700px;
}
.rb-hero-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.rb-tag {
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--navy);
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.25rem 0.7rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    border-radius: 2px;
}

/* ── ICON CARDS (3 colonnes) ── */
.ic-card {
    background: #eef2f8;
    border: 1px solid var(--border);
    padding: 1.6rem 1.4rem;
    height: 100%;
}
.ic-icon {
    width: 46px; height: 46px;
    background: var(--navy);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 1rem;
}
.ic-title {
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--navy);
    font-size: 0.97rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    line-height: 1.35;
}
.ic-text { color: var(--sub); font-size: 0.82rem; line-height: 1.65; }

/* ── METRIC BOXES ── */
.metric-box {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 3px solid var(--navy);
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.metric-box .label {
    font-size: 0.67rem; color: var(--slate);
    text-transform: uppercase; letter-spacing: 1.5px;
    font-weight: 700; margin-bottom: 0.4rem;
}
.metric-box .value { font-size: 1.05rem; font-weight: 700; color: var(--navy); }
.metric-box .sub { font-size: 0.74rem; color: var(--sub); margin-top: 0.25rem; line-height: 1.4; }

/* ── BADGES ── */
.badge {
    display: inline-block; padding: 0.2rem 0.6rem;
    font-size: 0.69rem; font-weight: 700;
    letter-spacing: 0.8px; text-transform: uppercase; border-radius: 2px;
}
.badge-critique { background:#fee2e2; color:#991b1b !important; border:1px solid #fca5a5; }
.badge-eleve    { background:#ffedd5; color:#9a3412 !important; border:1px solid #fdba74; }
.badge-moyen    { background:#fef9c3; color:#854d0e !important; border:1px solid #fde047; }
.badge-faible   { background:#dcfce7; color:#166534 !important; border:1px solid #86efac; }
.badge-noir     { background:#1e293b; color:#f1f5f9 !important; }
.badge-gris     { background:#f1f5f9; color:#475569 !important; border:1px solid #cbd5e1; }
.badge-conforme { background:#dcfce7; color:#166534 !important; border:1px solid #86efac; }

/* ── ALERTES ── */
.alert-box {
    background:#fffbfb;
    border-left:4px solid var(--red);
    border:1px solid #fecaca; border-left:4px solid var(--red);
    padding:1.1rem 1.4rem; margin:0.7rem 0;
}
.alert-box .alert-title { color:var(--red) !important; font-size:0.92rem; font-weight:700; margin-bottom:0.5rem; }
.alert-box td, .alert-box th { color: var(--sub) !important; font-size: 0.82rem; }
.alert-clean {
    background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid var(--green);
    padding:0.9rem 1.3rem; color:var(--green) !important; font-weight:600; font-size:0.87rem;
}

/* ── STEP CARDS AUDIT ── */
.step-card {
    background: var(--white); border:1px solid var(--border);
    border-left:4px solid var(--navy); padding:1.2rem 1.5rem; margin:0.6rem 0;
}
.step-num {
    background:var(--navy); color:white !important;
    border-radius:50%; width:28px; height:28px;
    display:inline-flex; align-items:center; justify-content:center;
    font-weight:700; font-size:0.82rem; margin-right:0.6rem; vertical-align:middle;
}

/* ── SECTION CARDS ── */
.section-card {
    background:var(--white); border:1px solid var(--border);
    padding:1.4rem 1.6rem; margin-bottom:0.9rem;
}
.section-card h3 {
    font-family:'Playfair Display',Georgia,serif !important;
    color:var(--navy) !important; font-size:0.97rem !important;
    font-weight:700 !important; margin-bottom:0.9rem !important;
    padding-bottom:0.5rem; border-bottom:1px solid var(--border);
}

/* ── BOUTONS ── */
.stButton > button {
    background: var(--navy) !important; color: white !important;
    border: none !important; border-radius: 2px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    letter-spacing: 0.4px !important; padding: 0.5rem 1.3rem !important;
}
.stButton > button:hover { background: var(--gold) !important; }
[data-testid="stDownloadButton"] button {
    background: white !important; color: var(--navy) !important;
    border: 1.5px solid var(--navy) !important; border-radius: 2px !important;
    font-size: 0.81rem !important; font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: var(--navy) !important; color: white !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--border) !important;
    background: transparent !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--slate) !important;
    font-weight: 500 !important; font-size: 0.84rem !important;
    padding: 0.65rem 1.2rem !important; border-radius: 0 !important;
    border-bottom: 2px solid transparent !important; margin-bottom: -2px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--navy) !important; font-weight: 700 !important;
    border-bottom: 2px solid var(--navy) !important;
}
.stTabs [data-baseweb="tab"] * { color: inherit !important; }

/* ── EXPANDERS ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important; background: white !important;
    margin-bottom: 0.4rem !important;
}
[data-testid="stExpander"] summary { color: var(--navy) !important; font-weight: 600 !important; }
[data-testid="stExpander"] summary * { color: var(--navy) !important; }

/* ── DIVIDER ── */
.rb-divider { border:none; border-top:1px solid var(--border); margin:1.3rem 0; }

/* ── INFO BOX API READY ── */
.api-notice {
    background: #fffbeb; border-left: 4px solid var(--gold);
    border: 1px solid #fde68a; border-left: 4px solid var(--gold);
    padding: 0.75rem 1.1rem; font-size: 0.82rem;
    color: var(--navy); margin-bottom: 1.2rem; border-radius: 2px;
}

/* ── LIEN EXTERNE ── */
.ext-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    color: var(--navy) !important; font-size: 0.82rem; font-weight: 600;
    border: 1px solid var(--navy); padding: 0.35rem 0.9rem;
    border-radius: 2px; text-decoration: none; margin: 0.2rem;
    background: white;
}
.ext-link:hover { background: var(--navy); color: white !important; }

/* ── FOOTER ── */
.rb-footer {
    background: var(--navy); border-top: 3px solid var(--gold);
    padding: 1.4rem 2rem; margin-top: 2.5rem;
}
.rb-footer p { color: #8ba3c0 !important; font-size: 0.77rem !important; text-align:center; margin:0.2rem 0; }
.rb-footer b { color: white !important; }

/* ── SUCCESS / WARNING ── */
[data-testid="stSuccess"] { background: #f0fdf4 !important; }
[data-testid="stSuccess"] * { color: #166534 !important; }
[data-testid="stWarning"] { background: #fffbeb !important; }
[data-testid="stWarning"] * { color: #92400e !important; }
[data-testid="stInfo"] { background: #eff6ff !important; }
[data-testid="stInfo"] * { color: var(--navy) !important; }
[data-testid="stError"] { background: #fef2f2 !important; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Erreur de chargement : {filename} — {e}")
        return pd.DataFrame()

df_gafi       = load_csv("reg_matrix_gafi.csv")
df_ofac       = load_csv("reg_matrix_ofac.csv")
df_tracfin    = load_csv("reg_matrix_tracfin_dgt.csv")
df_bale       = load_csv("normes_prudentielles_bale.csv")
df_caraib     = load_csv("country_risk_caribbean.csv")
df_africa     = load_csv("country_risk_africa.csv")
df_pep        = load_csv("pep_sanctions_profiles.csv")
df_corridors  = load_csv("mta_diaspora_corridors.csv")
df_audit      = load_csv("audit_procedures_framework.csv")
df_consulting = load_csv("appointments_consulting_schema.csv")


# ─────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────
def badge_html(niveau):
    mapping = {
        "Critique":"critique","critique":"critique",
        "Élevé":"eleve","élevé":"eleve","Eleve":"eleve",
        "Moyen":"moyen","moyen":"moyen",
        "Faible":"faible","faible":"faible",
        "Liste Noire":"noir","Liste Grise":"gris","Conforme":"conforme",
    }
    cls = mapping.get(str(niveau), "moyen")
    return f'<span class="badge badge-{cls}">{niveau}</span>'

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")

def fake_pdf(title, lines):
    content = ["REGBRIDGE COMPLIANCE ADVISORS",
                f"Rapport — {datetime.date.today().strftime('%d/%m/%Y')}","",
                f"=== {title} ===",""] + lines + ["","— Fin du rapport —"]
    return "\n".join(content).encode("utf-8")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.4rem 1rem 0.5rem;">
        <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:1.3rem;">
            <span style="font-size:1.5rem;">⚖️</span>
            <div>
                <div style="font-weight:700;font-size:0.92rem;color:#ffffff;line-height:1.2;">RegBridge</div>
                <div style="font-size:0.6rem;color:#b8975a;letter-spacing:2px;text-transform:uppercase;font-weight:600;">Compliance Advisors</div>
            </div>
        </div>
        <div style="height:1px;background:rgba(255,255,255,0.08);margin-bottom:1.2rem;"></div>
        <div style="font-size:0.6rem;color:#b8975a;text-transform:uppercase;letter-spacing:2.5px;font-weight:700;margin-bottom:0.7rem;">Menu</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("", options=[
        "📅 Cabinet & Prestations",
        "🏛️ Environnement Pays",
        "🔍 Screening PEP / Sanctions",
        "💸 Diaspora & Transferts",
        "📋 Audit & Référentiels",
    ], label_visibility="collapsed")

    st.markdown("""
    <div style="padding:0 1rem 1.5rem;">
        <div style="height:1px;background:rgba(255,255,255,0.08);margin:1.2rem 0 1rem;"></div>
        <div style="font-size:0.6rem;color:#b8975a;text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:0.7rem;">Sources</div>
        <div style="font-size:0.78rem;color:#8ba3c0;line-height:2;">
            GAFI &nbsp;·&nbsp; OFAC SDN<br>
            TRACFIN &nbsp;·&nbsp; DGT<br>
            Bâle II / III &nbsp;·&nbsp; GIABA<br>
            OpenSanctions
        </div>
        <div style="height:1px;background:rgba(255,255,255,0.08);margin:1rem 0;"></div>
        <div style="font-size:0.72rem;color:#8ba3c0;">Base <b style="color:#c8d6e8;">2024 – 2025</b></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="rb-nav">
    <span style="font-size:1.2rem;">⚖️</span>
    <span class="rb-nav-name">RegBridge Compliance Advisors</span>
    <span class="rb-nav-sep">|</span>
    <span class="rb-nav-sub">Intelligence Réglementaire &nbsp;·&nbsp; Caraïbes &amp; Afrique</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ONGLET 1 : CABINET & PRESTATIONS (en premier)
# ═══════════════════════════════════════════════════════════
if menu == "📅 Cabinet & Prestations":
    st.markdown("""
    <div class="rb-hero">
        <div class="rb-hero-label">Cabinet — Contact &amp; Services</div>
        <div class="rb-hero-title">Prise de Rendez-Vous &amp; Catalogue de Prestations</div>
        <div class="rb-hero-desc">
            Réservez une mission de conseil, soumettez vos documents de contrôle interne en toute confidentialité,
            et découvrez l'offre complète du cabinet RegBridge.
        </div>
        <div class="rb-hero-tags">
            <span class="rb-tag">Audit Environnement</span>
            <span class="rb-tag">KYC Remédiation</span>
            <span class="rb-tag">Formation MLRO</span>
            <span class="rb-tag">Screening API</span>
            <span class="rb-tag">Abonnement SaaS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Cartes de valeur ──
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="ic-card"><div class="ic-icon">🛡️</div>
        <div class="ic-title">Protection &amp; Remédiation</div>
        <div class="ic-text">Accompagnement complet pour la mise en conformité LCB-FT et la remédiation KYC face aux exigences des banques correspondantes américaines et européennes.</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="ic-card"><div class="ic-icon">⚖️</div>
        <div class="ic-title">Approche Sur-Mesure</div>
        <div class="ic-text">Chaque institution a des besoins spécifiques. Nos experts conçoivent des plans d'action adaptés à votre environnement réglementaire local et aux standards internationaux.</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="ic-card"><div class="ic-icon">🌍</div>
        <div class="ic-title">Expertise Caraïbes &amp; Afrique</div>
        <div class="ic-text">Présence et connaissance terrain des marchés caribéens et africains. Maîtrise des enjeux GAFI, OFAC et de-risking spécifiques à ces juridictions sous pression.</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("""<div class="section-card"><h3>📋 Formulaire de Contact &amp; Réservation</h3>""", unsafe_allow_html=True)

        type_client = st.selectbox("Nature de l'organisation", [
            "Banque Commerciale", "Maison de Transfert d'Argent (MTA)",
            "Banque Centrale / Régulateur", "Gouvernement / Ministère",
            "ONG Internationale", "Cabinet d'Audit / Conseil", "Autre"])

        col_n1, col_n2 = st.columns(2)
        with col_n1:
            nom = st.text_input("Nom du contact *")
        with col_n2:
            email = st.text_input("Email professionnel *")

        org = st.text_input("Nom de l'organisation / Institution *")
        pays_client = st.text_input("Pays d'opération principal")

        if not df_consulting.empty:
            prestations = df_consulting["Titre_Prestation"].tolist()
            prest_sel = st.selectbox("Prestation souhaitée *", prestations)
            if prest_sel:
                r = df_consulting[df_consulting["Titre_Prestation"] == prest_sel].iloc[0]
                st.markdown(f"""
                <div style="background:#f0f4f9;border-left:3px solid var(--gold);padding:0.7rem 1rem;
                            font-size:0.82rem;color:var(--navy);margin:0.4rem 0 0.8rem;border-radius:2px;">
                    💰 <b>{r.get('Prix_EUR','N/A')} € HT</b> &nbsp;·&nbsp;
                    ⏱️ <b>{r.get('Duree_Jours','N/A')} jours</b> &nbsp;·&nbsp;
                    📦 {r.get('Livrable_Principal','N/A')}
                </div>""", unsafe_allow_html=True)

        date_rdv = st.date_input("Date souhaitée", min_value=datetime.date.today())
        format_rdv = st.selectbox("Format", ["Visioconférence", "Présentiel Paris", "Appel téléphonique"])
        message = st.text_area("Contexte & Besoins", height=110,
            placeholder="Décrivez votre situation réglementaire (de-risking, audit en cours, inspection prochaine...)")
        urgence = st.checkbox("⚡ Demande urgente — réponse sous 24h")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("✉️ Envoyer la demande", use_container_width=True):
                if nom and email and org:
                    st.success(f"✅ Demande envoyée. Nous vous recontacterons sous 48h, {nom}.")
                    if urgence:
                        st.warning("⚡ Urgence prise en compte — réponse garantie sous 24h.")
                else:
                    st.error("Merci de compléter les champs obligatoires (*)")
        with col_b2:
            if st.button("💳 Paiement Stripe", use_container_width=True):
                if not df_consulting.empty and prest_sel:
                    stripe_id = df_consulting[df_consulting["Titre_Prestation"] == prest_sel]["Stripe_Price_ID"].iloc[0]
                    st.info(f"🔌 Stripe Price ID : `{stripe_id}` — Intégration en cours.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("""<div class="section-card"><h3>📎 Dépôt Documentaire Sécurisé</h3>""", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#fffbeb;border:1px solid #fde68a;border-left:3px solid var(--gold);
                    padding:0.7rem 1rem;font-size:0.81rem;color:var(--navy);margin-bottom:1rem;border-radius:2px;">
            🔒 <b>Transmission sécurisée :</b> Chiffrement TLS 1.3 en transit. Accès exclusif aux analystes RegBridge habilités.
        </div>""", unsafe_allow_html=True)

        uploaded = st.file_uploader("Déposer vos documents", accept_multiple_files=True,
            type=["pdf","xlsx","csv","docx","txt"],
            help="PDF, Excel, Word — 50 MB max par fichier")
        if uploaded:
            for f in uploaded:
                size = len(f.read()) / 1024
                f.seek(0)
                st.markdown(f"""<div style="background:white;border:1px solid var(--border);border-left:3px solid var(--green);
                    padding:0.45rem 0.8rem;margin:0.25rem 0;font-size:0.8rem;border-radius:2px;">
                    📄 <b>{f.name}</b> — {size:.0f} KB &nbsp;<span style="color:var(--green);float:right;font-weight:600;">✓ Reçu</span>
                    </div>""", unsafe_allow_html=True)
            st.success(f"✅ {len(uploaded)} document(s) reçu(s).")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""<div class="section-card" style="margin-top:1rem;"><h3>🏛️ Coordonnées du Cabinet</h3>
        <div style="font-size:0.84rem;line-height:2;color:var(--sub);">
            <b style="color:var(--navy);">RegBridge Compliance Advisors</b><br>
            📍 Paris, France<br>
            📧 contact@regbridge-compliance.com<br>
            📞 +33 (0)1 XX XX XX XX<br>
            🌐 <a href="https://regbridge-compliance.com" target="_blank" style="color:var(--navy);">regbridge-compliance.com</a>
        </div>
        <div style="height:1px;background:var(--border);margin:0.8rem 0;"></div>
        <div style="font-size:0.75rem;color:var(--sub);">Lun–Ven 09:00–18:00 CET<br>Ligne urgence 24/7 pour clients sous audit</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="section-card" style="margin-top:1rem;"><h3>💼 Catalogue des Prestations</h3>""", unsafe_allow_html=True)
        if not df_consulting.empty:
            for _, r in df_consulting.iterrows():
                with st.expander(f"{r.get('Code_Prestation','')} — {r.get('Titre_Prestation','')}"):
                    st.markdown(f"""
                    **Prix :** {r.get('Prix_EUR','N/A')} € HT &nbsp;|&nbsp; **Durée :** {r.get('Duree_Jours','N/A')} j
                    &nbsp;|&nbsp; **Format :** {r.get('Format_RDV','N/A')}

                    **Public :** {r.get('Public_Cible','N/A')}

                    **Livrable :** {r.get('Livrable_Principal','N/A')}

                    **Disponibilité :** {r.get('Disponibilite','N/A')}
                    """)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ONGLET 2 : ENVIRONNEMENT PAYS
# ═══════════════════════════════════════════════════════════
elif menu == "🏛️ Environnement Pays":
    st.markdown("""
    <div class="rb-hero">
        <div class="rb-hero-label">Module — Analyse Juridictionnelle</div>
        <div class="rb-hero-title">Vision Environnement Pays</div>
        <div class="rb-hero-desc">
            Fiche de risque réglementaire complète par juridiction : statut GAFI, exposition OFAC,
            indice de de-risking, score de corruption et vulnérabilités structurelles.
        </div>
        <div class="rb-hero-tags">
            <span class="rb-tag">GAFI</span><span class="rb-tag">OFAC SDN</span>
            <span class="rb-tag">De-risking</span><span class="rb-tag">Corruption TI</span>
            <span class="rb-tag">Correspondance Bancaire</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cartes
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="ic-card"><div class="ic-icon">🛡️</div>
        <div class="ic-title">Statut GAFI &amp; Listes</div>
        <div class="ic-text">Positionnement de la juridiction (liste grise, noire ou conforme) et plan de sortie recommandé.</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="ic-card"><div class="ic-icon">⚖️</div>
        <div class="ic-title">Exposition OFAC</div>
        <div class="ic-text">Programmes de sanctions américains actifs, désignations SDN et niveau de risque de contrepartie.</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="ic-card"><div class="ic-icon">📊</div>
        <div class="ic-title">Indice De-Risking</div>
        <div class="ic-text">Pression sur les relations de correspondance bancaire et score de corruption Transparency International.</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    col_r, col_p = st.columns([1, 2])
    with col_r:
        region = st.selectbox("Région", ["Caraïbes", "Afrique"])
    df_region = df_caraib if region == "Caraïbes" else df_africa
    with col_p:
        pays_list = df_region["Nom_Pays"].tolist() if not df_region.empty else []
        pays_sel = st.selectbox("Pays", pays_list)

    if pays_sel and not df_region.empty:
        row = df_region[df_region["Nom_Pays"] == pays_sel].iloc[0]
        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        colA, colB = st.columns([1, 3])
        with colA:
            st.markdown(f"""
            <div style="background:white;border:1px solid var(--border);padding:1.5rem;text-align:center;">
                <div style="font-size:3.5rem;line-height:1;">{row.get('Emoji_Drapeau','🌍')}</div>
                <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1.1rem;
                            color:var(--navy);margin-top:0.6rem;">{pays_sel}</div>
                <div style="font-size:0.72rem;color:var(--sub);margin-top:0.2rem;">
                    {row.get('Code_ISO','')} &nbsp;·&nbsp; {region}</div>
            </div>""", unsafe_allow_html=True)

        with colB:
            c1, c2, c3 = st.columns(3)
            statut = row.get("Statut_GAFI","N/A")
            top_color = '#b91c1c' if 'Noire' in str(statut) else ('#5a6a7a' if 'Grise' in str(statut) else '#15803d')
            badge_cls = "badge-noir" if "Noire" in str(statut) else ("badge-gris" if "Grise" in str(statut) else "badge-conforme")
            with c1:
                st.markdown(f"""<div class="metric-box" style="border-top-color:{top_color}">
                    <div class="label">Statut GAFI</div>
                    <div class="value"><span class="badge {badge_cls}">{statut}</span></div>
                    <div class="sub">{str(row.get('Liste_GAFI_Detail',''))[:90]}...</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="metric-box" style="border-top-color:#c2410c">
                    <div class="label">Risque De-Risking</div>
                    <div class="value">{row.get('Indice_Derisking','N/A')}</div>
                    <div class="sub">Pression sur la correspondance bancaire</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                ofac = row.get("Risque_OFAC","N/A")
                ofac_col = {"Critique":"#b91c1c","Élevé":"#c2410c","Moyen":"#a16207","Faible":"#15803d"}.get(str(ofac),"#5a6a7a")
                st.markdown(f"""<div class="metric-box" style="border-top-color:{ofac_col}">
                    <div class="label">Vulnérabilité OFAC</div>
                    <div class="value">{badge_html(ofac)}</div>
                    <div class="sub">Sanctions actives : {row.get('Sanctions_OFAC_Actives','N/A')}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="section-card"><h3>📊 Indicateurs Macro-Financiers</h3>""", unsafe_allow_html=True)
            st.markdown(f"""
| Indicateur | Valeur |
|---|---|
| Niveau de risque global | {badge_html(row.get('Niveau_Risque_Global','N/A'))} |
| Score Corruption TI | **{row.get('Score_Corruption_TI','N/A')} / 100** |
| Correspondants bancaires | {row.get('Banques_Correspondantes_Maintenues','N/A')} |
| Population | {row.get('Population_Millions','N/A')} M hab. |
| PIB | {row.get('PIB_USD_Milliards','N/A')} Mds USD |
""", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="section-card"><h3>⚠️ Vulnérabilités Clés</h3>""", unsafe_allow_html=True)
            for v in str(row.get("Principales_Vulnerabilites","")).split(","):
                st.markdown(f"— {v.strip()}")
            st.markdown(f"<br><i style='color:var(--sub);font-size:0.82rem;'>{row.get('Note_Macro','')}</i>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        col_e1, col_e2, _ = st.columns([1,1,2])
        with col_e1:
            st.download_button("⬇️ Fiche CSV",
                data=to_csv_bytes(df_region[df_region["Nom_Pays"]==pays_sel]),
                file_name=f"fiche_{pays_sel.replace(' ','_')}.csv", mime="text/csv")
        with col_e2:
            pdf_lines = [f"PAYS : {pays_sel}", f"STATUT GAFI : {row.get('Statut_GAFI','')}",
                f"RISQUE OFAC : {row.get('Risque_OFAC','')}",
                f"INDICE DE-RISKING : {row.get('Indice_Derisking','')}",
                f"SCORE CORRUPTION : {row.get('Score_Corruption_TI','')}/100",
                f"VULNERABILITES : {row.get('Principales_Vulnerabilites','')}"]
            st.download_button("📄 Rapport PDF (sim.)",
                data=fake_pdf(f"Fiche Pays — {pays_sel}", pdf_lines),
                file_name=f"rapport_{pays_sel.replace(' ','_')}.txt", mime="text/plain")


# ═══════════════════════════════════════════════════════════
# ONGLET 3 : SCREENING PEP / SANCTIONS
# ═══════════════════════════════════════════════════════════
elif menu == "🔍 Screening PEP / Sanctions":
    st.markdown("""
    <div class="rb-hero">
        <div class="rb-hero-label">Module — Criblage</div>
        <div class="rb-hero-title">Moteur de Screening PEP / Sanctions</div>
        <div class="rb-hero-desc">
            Criblage instantané contre les listes consolidées mondiales. Détection des PEP,
            désignations SDN OFAC, gels d'avoirs DGT et alertes OpenSanctions.
        </div>
        <div class="rb-hero-tags">
            <span class="rb-tag">OFAC SDN</span><span class="rb-tag">DGT Gel Avoirs</span>
            <span class="rb-tag">OpenSanctions</span><span class="rb-tag">PEP</span><span class="rb-tag">Interpol</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="api-notice">
        🔌 <b>API Ready :</b> Ce module est conçu pour se connecter à <b>OpenSanctions API</b>,
        <b>OFAC API</b> et <b>DGT Gel des Avoirs</b> en remplacement du fichier CSV local.
        &nbsp;→&nbsp; <a href="https://www.opensanctions.org/api/" target="_blank" style="color:var(--navy);font-weight:600;">OpenSanctions API</a>
        &nbsp;·&nbsp; <a href="https://ofac.treasury.gov/api" target="_blank" style="color:var(--navy);font-weight:600;">OFAC API</a>
    </div>
    """, unsafe_allow_html=True)

    query = st.text_input("🔎 Nom de la personne à cribler",
        placeholder="Ex : Duvalier, Belmokhtar, Moïse...")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_type = st.multiselect("Filtrer par type de risque",
            options=df_pep["Type_Risque"].unique().tolist() if not df_pep.empty else [])
    with col_f2:
        f_statut = st.multiselect("Filtrer par statut",
            options=df_pep["Statut_Actuel"].unique().tolist() if not df_pep.empty else [])

    df_s = df_pep.copy()
    if f_type:   df_s = df_s[df_s["Type_Risque"].isin(f_type)]
    if f_statut: df_s = df_s[df_s["Statut_Actuel"].isin(f_statut)]

    if query:
        mask = (df_s["Nom_Complet"].str.contains(query, case=False, na=False) |
                df_s["Alias"].str.contains(query, case=False, na=False))
        results = df_s[mask]
        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        if results.empty:
            st.markdown(f'<div class="alert-clean">✅ Aucune correspondance pour <b>"{query}"</b> dans la base locale.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"### 🚨 {len(results)} alerte(s) — **\"{query}\"**")
            for _, r in results.iterrows():
                niv = str(r.get("Niveau_Alerte",""))
                bc = "#b91c1c" if "Rouge" in niv else ("#c2410c" if "Orange" in niv else "#a16207")
                alias = f' ({r["Alias"]})' if str(r.get("Alias","")) not in ["N/A","nan"] else ""
                st.markdown(f"""
                <div class="alert-box" style="border-left-color:{bc}">
                    <div class="alert-title">⚠️ {r['Nom_Complet']}{alias}</div>
                    <table style="width:100%;border-collapse:collapse;font-size:0.82rem;">
                        <tr><td style="color:var(--sub);width:120px;padding:2px 0;"><b>Type</b></td><td>{r.get('Type_Risque','')}</td>
                            <td style="color:var(--sub);width:100px;padding:2px 1rem;"><b>Nationalité</b></td><td>{r.get('Nationalite','')}</td></tr>
                        <tr><td style="color:var(--sub);padding:2px 0;"><b>Source</b></td><td>{r.get('Source_Alerte','')}</td>
                            <td style="color:var(--sub);padding:2px 1rem;"><b>Statut</b></td>
                            <td><b style="color:{bc}">{r.get('Statut_Actuel','')}</b></td></tr>
                        <tr><td style="color:var(--sub);padding:4px 0;vertical-align:top;"><b>Programmes</b></td>
                            <td colspan="3">{r.get('Programmes_Sanctions','')}</td></tr>
                        <tr><td style="color:var(--sub);padding:4px 0;vertical-align:top;"><b>Infraction</b></td>
                            <td colspan="3" style="font-style:italic;">{str(r.get('Description_Infraction',''))[:280]}...</td></tr>
                    </table>
                </div>""", unsafe_allow_html=True)
            st.download_button("⬇️ Exporter les alertes (CSV)",
                data=to_csv_bytes(results),
                file_name=f"alertes_{query.replace(' ','_')}.csv", mime="text/csv")
    else:
        st.markdown(f"""
        <div style="background:white;border:1px solid var(--border);padding:1.2rem 1.5rem;
                    border-left:3px solid var(--gold);margin-top:1rem;font-size:0.85rem;">
            <b>{len(df_s)} profils</b> dans la base locale · Saisissez un nom pour lancer le criblage.
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ONGLET 4 : DIASPORA & TRANSFERTS
# ═══════════════════════════════════════════════════════════
elif menu == "💸 Diaspora & Transferts":
    st.markdown("""
    <div class="rb-hero">
        <div class="rb-hero-label">Module — MTA &amp; Remises de Fonds</div>
        <div class="rb-hero-title">Diaspora &amp; Maisons de Transfert d'Argent</div>
        <div class="rb-hero-desc">
            Cartographie des risques par corridor de transfert · Mesures compensatoires réglementaires ·
            Transaction Monitoring et contrôles KYC adaptés aux flux de la diaspora.
        </div>
        <div class="rb-hero-tags">
            <span class="rb-tag">TRACFIN</span><span class="rb-tag">FinCEN</span>
            <span class="rb-tag">Transaction Monitoring</span><span class="rb-tag">KYC Diaspora</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_corridors.empty:
        st.error("Données corridors non disponibles.")
    else:
        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="metric-box"><div class="label">Corridors</div>
            <div class="value">{len(df_corridors)}</div><div class="sub">Cartographiés 2024</div></div>""", unsafe_allow_html=True)
        with c2:
            crit = len(df_corridors[df_corridors["Criticite_OFAC"]=="Critique"])
            st.markdown(f"""<div class="metric-box" style="border-top-color:#b91c1c"><div class="label">OFAC Critiques</div>
            <div class="value" style="color:#b91c1c;">{crit}</div><div class="sub">Exposition sanctions US</div></div>""", unsafe_allow_html=True)
        with c3:
            vol = df_corridors[df_corridors["Volume_Annuel_USD_M"]>0]["Volume_Annuel_USD_M"].sum()
            st.markdown(f"""<div class="metric-box"><div class="label">Volume annuel</div>
            <div class="value">{vol/1000:.1f} Mds $</div><div class="sub">Flux légitimes monitored</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-box" style="border-top-color:#1e293b"><div class="label">Bloqués</div>
            <div class="value">1</div><div class="sub">Embargo total (Cuba)</div></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            fc = st.multiselect("Criticité OFAC", df_corridors["Criticite_OFAC"].unique().tolist())
        with col_f2:
            fg = st.multiselect("Criticité GAFI", df_corridors["Criticite_GAFI"].unique().tolist())

        df_c = df_corridors.copy()
        if fc: df_c = df_c[df_c["Criticite_OFAC"].isin(fc)]
        if fg: df_c = df_c[df_c["Criticite_GAFI"].isin(fg)]

        for _, r in df_c.iterrows():
            score_str = str(r.get("Score_Risque_Global","5"))
            try: sv = float(score_str.split("/")[0])
            except: sv = 5.0
            ic = "🚨" if sv>=9 else ("⚠️" if sv>=7 else "✅")
            with st.expander(f"{ic}  **{r['Corridor']}**  ·  {r.get('Volume_Annuel_USD_M','N/A')} M USD/an  ·  Score {score_str}"):
                cc1, cc2 = st.columns(2)
                with cc1:
                    st.markdown(f"""
                    **Criticités :**
                    - OFAC : {badge_html(r.get('Criticite_OFAC',''))}
                    - GAFI : {badge_html(r.get('Criticite_GAFI',''))}
                    - TRACFIN : {badge_html(r.get('Criticite_TRACFIN',''))}

                    **MTA actifs :** {r.get('Nombre_MTA_Actifs','N/A')}
                    **% PIB dest. :** {r.get('Part_PIB_Destination_Pct','N/A')}%
                    **Tendance :** {r.get('Tendance_Volume','N/A')}
                    """, unsafe_allow_html=True)
                with cc2:
                    st.info(f"🛡️ **Remédiation :** {r.get('Mesures_Remediation','N/A')}")
                    st.warning(f"⚙️ **Contrôles :** {r.get('Controles_Compensatoires','N/A')}")
                    st.markdown(f"_⚡ {r.get('Defis_Specifiques','N/A')}_")

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        st.download_button("⬇️ Exporter la cartographie (CSV)",
            data=to_csv_bytes(df_c), file_name="corridors_diaspora.csv", mime="text/csv")


# ═══════════════════════════════════════════════════════════
# ONGLET 5 : AUDIT & RÉFÉRENTIELS
# ═══════════════════════════════════════════════════════════
elif menu == "📋 Audit & Référentiels":
    st.markdown("""
    <div class="rb-hero">
        <div class="rb-hero-label">Module — Méthodologie &amp; Normes</div>
        <div class="rb-hero-title">Démarche d'Audit &amp; Référentiels Réglementaires</div>
        <div class="rb-hero-desc">
            Méthodologie d'audit RegBridge en 5 phases séquentielles. Accès aux référentiels
            GAFI, OFAC, TRACFIN/DGT et Bâle II/III — exportables pour vos missions.
        </div>
        <div class="rb-hero-tags">
            <span class="rb-tag">GAFI 40 Rec.</span><span class="rb-tag">OFAC</span>
            <span class="rb-tag">TRACFIN / DGT</span><span class="rb-tag">Bâle III</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Liens officiels
    st.markdown("""
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1.5rem;">
        <a class="ext-link" href="https://www.fatf-gafi.org/fr/recommandations.html" target="_blank">↗ GAFI — Recommandations officielles</a>
        <a class="ext-link" href="https://ofac.treasury.gov/sanctions-list-search" target="_blank">↗ OFAC SDN List Search</a>
        <a class="ext-link" href="https://www.tracfin.gouv.fr" target="_blank">↗ TRACFIN</a>
        <a class="ext-link" href="https://www.tresor.economie.gouv.fr/Fiches-pays/sanctions-financieres" target="_blank">↗ DGT Gel des Avoirs</a>
        <a class="ext-link" href="https://www.bis.org/bcbs/basel3.htm" target="_blank">↗ Bâle III — BIS</a>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔵 Démarche Audit", "📘 GAFI", "🔴 OFAC", "🇫🇷 TRACFIN/DGT", "🏦 Bâle II/III"
    ])

    with tab1:
        st.markdown("#### Méthodologie RegBridge — 5 Phases")
        if not df_audit.empty:
            for _, r in df_audit.iterrows():
                st.markdown(f"""
                <div class="step-card">
                    <span class="step-num">{int(r.get('Numero_Etape',0))}</span>
                    <b style="color:var(--navy);font-size:0.97rem;">{r.get('Phase','')}</b>
                    <span style="color:var(--sub);font-size:0.84rem;"> — {r.get('Titre_Etape','')}</span>
                    <p style="margin:0.6rem 0 0.4rem;color:var(--sub);font-size:0.84rem;">
                        {str(r.get('Description_Complete',''))[:280]}...
                    </p>
                    <div style="font-size:0.77rem;color:var(--sub);display:flex;gap:1.5rem;flex-wrap:wrap;">
                        <span>⏱️ <b>{r.get('Duree_Estimee_Jours','')} j</b></span>
                        <span>👥 {r.get('Intervenants','')}</span>
                        <span>✅ {r.get('Criteres_Validation','')}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.download_button("⬇️ Télécharger la méthodologie (CSV)",
                data=to_csv_bytes(df_audit), file_name="methodologie_audit.csv", mime="text/csv")

    with tab2:
        st.markdown("#### Recommandations GAFI — 40 Normes LCB-FT")
        st.markdown("_Source officielle : [fatf-gafi.org](https://www.fatf-gafi.org/fr/recommandations.html)_")
        if not df_gafi.empty:
            for _, r in df_gafi.iterrows():
                with st.expander(f"**{r.get('Code_Norme','')}** — {r.get('Titre','')}"):
                    st.markdown(f"""
                    **Catégorie :** {r.get('Categorie','')} &nbsp;·&nbsp; **Niveau :** {badge_html(r.get('Niveau_Risque',''))}

                    {r.get('Description','')}

                    **Obligation clé :** _{r.get('Obligation_Clef','')}_
                    """, unsafe_allow_html=True)
            st.download_button("⬇️ Référentiel GAFI (CSV)",
                data=to_csv_bytes(df_gafi), file_name="referentiel_gafi.csv", mime="text/csv")

    with tab3:
        st.markdown("#### Programmes de Sanctions OFAC")
        st.markdown("_Source : [ofac.treasury.gov](https://ofac.treasury.gov)_")
        if not df_ofac.empty:
            for _, r in df_ofac.iterrows():
                with st.expander(f"**{r.get('Code_Programme','')}** — {r.get('Type_Sanction','')} · {r.get('Pays_Region_Vise','')}"):
                    st.markdown(f"""
                    **Impact MTA :** {badge_html(r.get('Niveau_Impact_MTA',''))} &nbsp;·&nbsp; **Autorité :** {r.get('Autorite_Gestion','')}

                    {r.get('Description','')}

                    **Critères de gel :** _{r.get('Criteres_Gel','')}_
                    """, unsafe_allow_html=True)
            st.download_button("⬇️ Référentiel OFAC (CSV)",
                data=to_csv_bytes(df_ofac), file_name="referentiel_ofac.csv", mime="text/csv")

    with tab4:
        st.markdown("#### Obligations TRACFIN & DGT — Dispositif Français LCB-FT")
        st.markdown("_Sources : [tracfin.gouv.fr](https://www.tracfin.gouv.fr) · [tresor.economie.gouv.fr](https://www.tresor.economie.gouv.fr)_")
        if not df_tracfin.empty:
            for _, r in df_tracfin.iterrows():
                with st.expander(f"**{r.get('Code_Texte','')}** — {r.get('Titre','')}"):
                    st.markdown(f"""
                    **Organisme :** {r.get('Organisme','')} &nbsp;·&nbsp; **Délai :** {r.get('Delai_Execution','')}

                    {r.get('Description','')}

                    **Sanction max :** _{r.get('Sanction_Max','')}_
                    """, unsafe_allow_html=True)
            st.download_button("⬇️ Référentiel TRACFIN/DGT (CSV)",
                data=to_csv_bytes(df_tracfin), file_name="referentiel_tracfin_dgt.csv", mime="text/csv")

    with tab5:
        st.markdown("#### Normes Prudentielles Bâle II / III")
        st.markdown("_Source : [bis.org](https://www.bis.org/bcbs/basel3.htm)_")
        if not df_bale.empty:
            piliers = st.multiselect("Filtrer par Pilier", df_bale["Pilier"].unique().tolist())
            df_b = df_bale[df_bale["Pilier"].isin(piliers)] if piliers else df_bale
            for _, r in df_b.iterrows():
                with st.expander(f"**{r.get('Code_Ratio','')}** — {r.get('Titre','')} · Seuil : {r.get('Seuil_Minimum','')}"):
                    st.markdown(f"""
                    **Cadre :** {r.get('Cadre','')} &nbsp;·&nbsp; **Pilier :** {r.get('Pilier','')} &nbsp;·&nbsp;
                    **Statut :** {r.get('Statut_Implementation','')}

                    {r.get('Description','')}

                    **Formule :** `{r.get('Formule_Calcul','')}`
                    """, unsafe_allow_html=True)
            st.download_button("⬇️ Référentiel Bâle (CSV)",
                data=to_csv_bytes(df_b), file_name="referentiel_bale.csv", mime="text/csv")


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="rb-footer">
    <p><b>RegBridge Compliance Advisors</b> &nbsp;—&nbsp; Conseil stratégique en conformité financière internationale</p>
    <p>GAFI &nbsp;·&nbsp; OFAC &nbsp;·&nbsp; TRACFIN / DGT &nbsp;·&nbsp; Bâle III &nbsp;·&nbsp; OpenSanctions &nbsp;·&nbsp; GIABA</p>
    <p style="margin-top:0.8rem;font-size:0.7rem;color:#3d5470 !important;">
        Les informations fournies sont à titre informatif et professionnel uniquement. Elles ne constituent pas un avis juridique.
        © 2025 RegBridge Compliance Advisors.
    </p>
</div>
""", unsafe_allow_html=True)
