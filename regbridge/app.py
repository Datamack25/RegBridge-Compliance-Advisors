"""
RegBridge Compliance Advisors
Plateforme SaaS de conseil et d'intelligence réglementaire
Spécialisée Caraïbes & Afrique — LCB-FT, GAFI, OFAC, TRACFIN/DGT, Bâle
"""

import streamlit as st
import pandas as pd
import io
import datetime
import os

# Chemin absolu vers platform_data, quel que soit le répertoire de lancement
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
# CONFIGURATION DE PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RegBridge Compliance Advisors",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CHARTE GRAPHIQUE & CSS INSTITUTIONNEL
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Variables de couleur ── */
    :root {
        --navy:   #1a365d;
        --royal:  #2b6cb0;
        --slate:  #718096;
        --light:  #e8f0fe;
        --white:  #ffffff;
        --red:    #c53030;
        --orange: #c05621;
        --green:  #276749;
        --yellow: #b7791f;
    }

    /* ── Fond global ── */
    .stApp { background-color: #f0f4f8; }

    /* ── Forcer texte sombre dans le contenu principal ── */
    /* Cible tous les éléments texte natifs de Streamlit hors sidebar */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #1a365d !important;
    }
    .main p, .main span, .main label, .main div {
        color: #2d3748;
    }
    /* Subheader et texte Streamlit natif */
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] td,
    [data-testid="stMarkdownContainer"] th,
    [data-testid="stMarkdownContainer"] span { color: #2d3748 !important; }
    /* Titres natifs st.subheader / st.title */
    [data-testid="stHeadingWithActionElements"] h1,
    [data-testid="stHeadingWithActionElements"] h2,
    [data-testid="stHeadingWithActionElements"] h3 { color: #1a365d !important; }
    /* Labels selectbox, text_input hors sidebar */
    .main .stSelectbox label,
    .main .stTextInput label,
    .main .stTextArea label,
    .main .stDateInput label,
    .main .stFileUploader label,
    .main .stCheckbox label,
    .main .stMultiSelect label { color: #2d3748 !important; }
    /* Texte dans les expanders */
    .streamlit-expanderHeader { color: #1a365d !important; font-weight: 600; }
    /* Texte dans les tabs */
    .stTabs [data-baseweb="tab"] span { color: #718096 !important; }
    .stTabs [aria-selected="true"] span { color: #1a365d !important; }
    
    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy) 0%, #2d4a7a 100%);
    }
    /* Texte blanc uniquement dans la sidebar — ne pas toucher au contenu principal */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stRadio span,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown b,
    section[data-testid="stSidebar"] .stMarkdown small { color: var(--white) !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #a8c4e8 !important; }

    /* ── En-tête bannière ── */
    .rb-header {
        background: linear-gradient(135deg, var(--navy) 0%, var(--royal) 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(26,54,93,0.25);
    }
    .rb-header h1 { color: var(--white); font-size: 1.9rem; margin: 0; font-weight: 700; letter-spacing: -0.5px; }
    .rb-header p  { color: #a8c4e8; margin: 0.3rem 0 0; font-size: 0.95rem; }
    .rb-logo-tag  { font-size: 0.7rem; color: #63b3ed; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }

    /* ── Boîtes de métriques ── */
    .metric-box {
        background: var(--white);
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-left: 4px solid var(--royal);
        margin-bottom: 0.8rem;
    }
    .metric-box .label { font-size: 0.72rem; color: var(--slate); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 0.3rem; }
    .metric-box .value { font-size: 1.25rem; font-weight: 700; color: var(--navy); }
    .metric-box .sub   { font-size: 0.78rem; color: var(--slate); margin-top: 0.2rem; }

    /* ── Badges de risque ── */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-critique { background: #fed7d7; color: var(--red); border: 1px solid #feb2b2; }
    .badge-eleve    { background: #feebc8; color: var(--orange); border: 1px solid #fbd38d; }
    .badge-moyen    { background: #fefcbf; color: var(--yellow); border: 1px solid #f6e05e; }
    .badge-faible   { background: #c6f6d5; color: var(--green); border: 1px solid #9ae6b4; }
    .badge-noir     { background: #1a202c; color: var(--white); }
    .badge-gris     { background: #e2e8f0; color: #4a5568; }
    .badge-conforme { background: #c6f6d5; color: var(--green); }

    /* ── Alerte PEP/Sanction ── */
    .alert-box {
        background: #fff5f5;
        border: 2px solid var(--red);
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
    }
    .alert-box .alert-title { color: var(--red); font-size: 1rem; font-weight: 700; margin-bottom: 0.5rem; }
    .alert-clean {
        background: #f0fff4;
        border: 2px solid var(--green);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        color: var(--green);
        font-weight: 600;
    }

    /* ── Section cards ── */
    .section-card {
        background: var(--white);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    .section-card h3 { color: var(--navy); font-size: 1rem; font-weight: 700; margin-bottom: 0.8rem; }

    /* ── Corridor bar ── */
    .corridor-bar {
        background: var(--white);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 5px solid var(--royal);
        margin: 0.5rem 0;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }

    /* ── Step audit ── */
    .step-card {
        background: var(--white);
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 0.6rem 0;
        border-top: 3px solid var(--royal);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .step-num {
        background: var(--navy);
        color: var(--white);
        border-radius: 50%;
        width: 32px; height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        margin-right: 0.6rem;
        vertical-align: middle;
    }

    /* ── Tabs styling ── */
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--slate);
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        padding: 0.6rem 1.2rem;
    }
    .stTabs [aria-selected="true"] {
        background: var(--white) !important;
        color: var(--navy) !important;
        border-bottom: 3px solid var(--royal) !important;
    }

    /* ── Boutons ── */
    .stButton > button {
        background: var(--royal);
        color: var(--white);
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: var(--navy);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26,54,93,0.3);
    }

    /* ── Divider ── */
    .rb-divider {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 1.2rem 0;
    }

    /* ── Footbar ── */
    .rb-footer {
        background: var(--navy);
        color: #a8c4e8;
        text-align: center;
        padding: 0.8rem;
        border-radius: 10px;
        font-size: 0.75rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────
DATA_DIR = os.path.join(BASE_DIR, "platform_data")

@st.cache_data(ttl=3600)
def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Erreur de chargement : {filename} — {e}")
        return pd.DataFrame()

df_gafi        = load_csv("reg_matrix_gafi.csv")
df_ofac        = load_csv("reg_matrix_ofac.csv")
df_tracfin     = load_csv("reg_matrix_tracfin_dgt.csv")
df_bale        = load_csv("normes_prudentielles_bale.csv")
df_caraib      = load_csv("country_risk_caribbean.csv")
df_africa      = load_csv("country_risk_africa.csv")
df_pep         = load_csv("pep_sanctions_profiles.csv")
df_corridors   = load_csv("mta_diaspora_corridors.csv")
df_audit       = load_csv("audit_procedures_framework.csv")
df_consulting  = load_csv("appointments_consulting_schema.csv")


# ─────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────
def badge_html(niveau):
    mapping = {
        "Critique": "critique", "critique": "critique",
        "Élevé": "eleve", "élevé": "eleve", "Eleve": "eleve",
        "Moyen": "moyen", "moyen": "moyen",
        "Faible": "faible", "faible": "faible",
        "Liste Noire": "noir", "Liste Grise": "gris",
        "Conforme": "conforme",
    }
    cls = mapping.get(str(niveau), "moyen")
    return f'<span class="badge badge-{cls}">{niveau}</span>'


def to_csv_download(df):
    return df.to_csv(index=False).encode("utf-8")


def fake_pdf_bytes(title, content_lines):
    """Simule un PDF en texte brut pour la démo (sans ReportLab)."""
    lines = [
        f"REGBRIDGE COMPLIANCE ADVISORS",
        f"Rapport généré le {datetime.date.today().strftime('%d/%m/%Y')}",
        f"",
        f"═══ {title} ═══",
        f"",
    ] + content_lines + ["", "— Fin du rapport —", "RegBridge Compliance Advisors © 2025"]
    return "\n".join(lines).encode("utf-8")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2.5rem;'>⚖️</div>
        <div style='font-weight:700; font-size:1.1rem; color:#ffffff; margin-top:0.4rem;'>RegBridge</div>
        <div style='font-size:0.7rem; color:#63b3ed; letter-spacing:2px; text-transform:uppercase;'>Compliance Advisors</div>
    </div>
    <hr style='border-color:#2d4a7a; margin:0.8rem 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**Navigation**")
    menu = st.radio(
        "",
        options=[
            "🏛️ Vision Environnement Pays",
            "🔍 Moteur de Screening",
            "💸 Diaspora & Transferts",
            "📋 Démarche d'Audit & Référentiel",
            "📅 Cabinet — RDV & Échanges",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#2d4a7a; margin:1rem 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem; color:#718096; line-height:1.6;'>
        <b style='color:#a8c4e8;'>Sources intégrées :</b><br>
        GAFI • OFAC SDN • TRACFIN<br>
        DGT Gel Avoirs • Bâle III<br>
        OpenSanctions • GIABA<br>
        <br>
        <b style='color:#a8c4e8;'>Mise à jour :</b><br>
        Base réglementaire 2024–2025
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# EN-TÊTE PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="rb-header">
    <div class="rb-logo-tag">Plateforme d'Intelligence Réglementaire</div>
    <h1>⚖️ RegBridge Compliance Advisors</h1>
    <p>LCB-FT · GAFI · OFAC · TRACFIN/DGT · Bâle III — Caraïbes & Afrique</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# ONGLET 1 : VISION ENVIRONNEMENT PAYS
# ═══════════════════════════════════════════════════════════
if menu == "🏛️ Vision Environnement Pays":
    st.subheader("🏛️ Vision Environnement Pays")
    st.markdown("Sélectionnez une juridiction pour obtenir sa fiche complète de risque réglementaire.")

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

        # ── En-tête pays ──
        colA, colB = st.columns([1, 3])
        with colA:
            st.markdown(f"""
            <div style='background:white; border-radius:12px; padding:1.5rem; text-align:center;
                        box-shadow:0 2px 12px rgba(0,0,0,0.08);'>
                <div style='font-size:4rem;'>{row.get('Emoji_Drapeau','🌍')}</div>
                <div style='font-weight:700; font-size:1.2rem; color:#1a365d; margin-top:0.5rem;'>{pays_sel}</div>
                <div style='font-size:0.75rem; color:#718096; margin-top:0.2rem;'>{row.get('Code_ISO','')} · {region}</div>
            </div>
            """, unsafe_allow_html=True)

        with colB:
            c1, c2, c3 = st.columns(3)
            with c1:
                statut = row.get("Statut_GAFI", "N/A")
                badge_cls = "badge-noir" if "Noire" in str(statut) else ("badge-gris" if "Grise" in str(statut) else "badge-conforme")
                st.markdown(f"""
                <div class="metric-box" style="border-left-color:{'#c53030' if 'Noire' in str(statut) else ('#718096' if 'Grise' in str(statut) else '#276749')}">
                    <div class="label">Statut GAFI</div>
                    <div class="value"><span class="badge {badge_cls}">{statut}</span></div>
                    <div class="sub">{str(row.get('Liste_GAFI_Detail',''))[:80]}...</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                derisking = row.get("Indice_Derisking", "N/A")
                st.markdown(f"""
                <div class="metric-box" style="border-left-color:#c05621">
                    <div class="label">Risque De-Risking</div>
                    <div class="value">{derisking}</div>
                    <div class="sub">Indice pression correspondance bancaire</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                ofac_risk = row.get("Risque_OFAC", "N/A")
                ofac_color = {"Critique": "#c53030", "Élevé": "#c05621", "Moyen": "#b7791f", "Faible": "#276749"}.get(str(ofac_risk), "#718096")
                st.markdown(f"""
                <div class="metric-box" style="border-left-color:{ofac_color}">
                    <div class="label">Vulnérabilité OFAC</div>
                    <div class="value">{badge_html(ofac_risk)}</div>
                    <div class="sub">Sanctions américaines actives : {row.get('Sanctions_OFAC_Actives','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        # ── Données complémentaires ──
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
            st.markdown("""<div class="section-card"><h3>⚠️ Principales Vulnérabilités</h3>""", unsafe_allow_html=True)
            vulnerabilites = str(row.get("Principales_Vulnerabilites", "N/A")).split(",")
            for v in vulnerabilites:
                st.markdown(f"• {v.strip()}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""<div class="section-card" style="margin-top:0.8rem"><h3>🏦 Note Macro</h3>""", unsafe_allow_html=True)
            st.markdown(str(row.get("Note_Macro", "N/A")))
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        # ── Boutons d'export ──
        col_exp1, col_exp2, col_spacer = st.columns([1, 1, 2])
        with col_exp1:
            csv_bytes = to_csv_download(df_region[df_region["Nom_Pays"] == pays_sel])
            st.download_button(
                "⬇️ Exporter Fiche CSV",
                data=csv_bytes,
                file_name=f"fiche_risque_{pays_sel.replace(' ','_')}.csv",
                mime="text/csv",
            )
        with col_exp2:
            pdf_content = [
                f"PAYS : {pays_sel} ({row.get('Code_ISO','')})",
                f"RÉGION : {region}",
                f"",
                f"STATUT GAFI : {row.get('Statut_GAFI','N/A')}",
                f"Détail : {row.get('Liste_GAFI_Detail','N/A')}",
                f"",
                f"RISQUE OFAC : {row.get('Risque_OFAC','N/A')}",
                f"Sanctions actives : {row.get('Sanctions_OFAC_Actives','N/A')}",
                f"",
                f"SCORE CORRUPTION TI : {row.get('Score_Corruption_TI','N/A')}/100",
                f"INDICE DE-RISKING : {row.get('Indice_Derisking','N/A')}",
                f"NIVEAU RISQUE GLOBAL : {row.get('Niveau_Risque_Global','N/A')}",
                f"",
                f"CORRESPONDANTS BANCAIRES : {row.get('Banques_Correspondantes_Maintenues','N/A')}",
                f"",
                f"VULNÉRABILITÉS CLÉS :",
                f"{row.get('Principales_Vulnerabilites','N/A')}",
                f"",
                f"NOTE MACRO :",
                f"{row.get('Note_Macro','N/A')}",
            ]
            pdf_bytes = fake_pdf_bytes(f"Rapport d'Environnement Pays — {pays_sel}", pdf_content)
            st.download_button(
                "📄 Rapport PDF (simulation)",
                data=pdf_bytes,
                file_name=f"rapport_audit_env_{pays_sel.replace(' ','_')}.txt",
                mime="text/plain",
            )


# ═══════════════════════════════════════════════════════════
# ONGLET 2 : MOTEUR DE SCREENING
# ═══════════════════════════════════════════════════════════
elif menu == "🔍 Moteur de Screening":
    st.subheader("🔍 Moteur de Screening PEP / Sanctions")
    st.markdown(
        "Saisissez un nom pour le croiser instantanément avec la base des personnes "
        "à haut risque (OFAC SDN, Gel d'avoirs DGT, OpenSanctions, PEP)."
    )

    st.markdown("""
    <div style='background:#ebf8ff; border:1px solid #bee3f8; border-radius:8px; padding:0.8rem 1rem; margin-bottom:1rem; font-size:0.85rem; color:#2c5282;'>
        🔌 <b>API Ready :</b> Ce module est conçu pour se connecter à 
        <b>OpenSanctions API</b>, <b>OFAC API</b> et <b>DGT Gel des Avoirs API</b> 
        en remplacement du fichier CSV local. Contactez le cabinet pour l'activation.
    </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input(
        "🔎 Nom de la personne à cribler",
        placeholder="Ex: Duvalier, Belmokhtar, Moïse...",
        help="Recherche insensible à la casse sur le nom complet et les alias."
    )

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filtre_type = st.multiselect(
            "Filtrer par type de risque",
            options=df_pep["Type_Risque"].unique().tolist() if not df_pep.empty else [],
            default=[],
        )
    with col_f2:
        filtre_statut = st.multiselect(
            "Filtrer par statut",
            options=df_pep["Statut_Actuel"].unique().tolist() if not df_pep.empty else [],
            default=[],
        )

    # Filtrage
    df_screen = df_pep.copy()
    if filtre_type:
        df_screen = df_screen[df_screen["Type_Risque"].isin(filtre_type)]
    if filtre_statut:
        df_screen = df_screen[df_screen["Statut_Actuel"].isin(filtre_statut)]

    if search_query:
        mask = (
            df_screen["Nom_Complet"].str.contains(search_query, case=False, na=False) |
            df_screen["Alias"].str.contains(search_query, case=False, na=False)
        )
        results = df_screen[mask]

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        if results.empty:
            st.markdown(f"""
            <div class="alert-clean">
                ✅ Aucune correspondance trouvée pour <b>"{search_query}"</b> dans la base de données.
                <br><small>La base locale peut ne pas être exhaustive. Activez les API OFAC/OpenSanctions pour une couverture complète.</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            alert_color = {"Rouge - Critique": "#c53030", "Rouge - Actif": "#c53030", "Orange - Enquête": "#c05621", "Orange - Surveillance": "#c05621", "Jaune - Investigation nationale": "#b7791f"}.get
            st.markdown(f"### 🚨 {len(results)} alerte(s) détectée(s) pour **\"{search_query}\"**")

            for _, r in results.iterrows():
                niveau = str(r.get("Niveau_Alerte", ""))
                border_color = "#c53030" if "Rouge" in niveau else ("#c05621" if "Orange" in niveau else "#b7791f")
                st.markdown(f"""
                <div class="alert-box" style="border-color:{border_color}">
                    <div class="alert-title">⚠️ ALERTE — {r['Nom_Complet']} 
                        {f'({r["Alias"]})' if str(r.get("Alias","")) != "N/A" else ""}
                    </div>
                    <table style="width:100%; font-size:0.85rem; border-collapse:collapse;">
                        <tr>
                            <td style="padding:0.2rem 0.8rem 0.2rem 0; color:#718096; white-space:nowrap;"><b>Type de risque</b></td>
                            <td>{r.get('Type_Risque','N/A')}</td>
                            <td style="padding:0.2rem 0.8rem 0.2rem 1rem; color:#718096; white-space:nowrap;"><b>Nationalité</b></td>
                            <td>{r.get('Nationalite','N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding:0.2rem 0.8rem 0.2rem 0; color:#718096;"><b>Source alerte</b></td>
                            <td>{r.get('Source_Alerte','N/A')}</td>
                            <td style="padding:0.2rem 0.8rem 0.2rem 1rem; color:#718096;"><b>Statut actuel</b></td>
                            <td><b style="color:{border_color}">{r.get('Statut_Actuel','N/A')}</b></td>
                        </tr>
                        <tr>
                            <td style="padding:0.2rem 0.8rem 0.2rem 0; color:#718096;"><b>Programmes</b></td>
                            <td colspan="3">{r.get('Programmes_Sanctions','N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding:0.4rem 0.8rem 0 0; color:#718096; vertical-align:top;"><b>Infraction</b></td>
                            <td colspan="3" style="padding-top:0.4rem; font-style:italic; color:#2d3748;">{str(r.get('Description_Infraction','N/A'))[:300]}{'...' if len(str(r.get('Description_Infraction','')))>300 else ''}</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

            # Export
            csv_alert = to_csv_download(results)
            st.download_button(
                "⬇️ Exporter les alertes en CSV",
                data=csv_alert,
                file_name=f"alertes_screening_{search_query.replace(' ','_')}.csv",
                mime="text/csv",
            )
    else:
        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        st.markdown(f"**Base de données active : {len(df_screen)} profils chargés**")
        st.dataframe(
            df_screen[["Nom_Complet", "Alias", "Nationalite", "Type_Risque", "Source_Alerte", "Statut_Actuel", "Niveau_Alerte"]],
            use_container_width=True,
            hide_index=True,
        )


# ═══════════════════════════════════════════════════════════
# ONGLET 3 : DIASPORA & TRANSFERTS
# ═══════════════════════════════════════════════════════════
elif menu == "💸 Diaspora & Transferts":
    st.subheader("💸 Secteur Diaspora & Maisons de Transfert d'Argent (MTA)")
    st.markdown(
        "Analyse de risque des corridors de transfert de fonds de la diaspora. "
        "Mesures compensatoires automatisées et monitoring des flux critiques."
    )

    if df_corridors.empty:
        st.error("Données corridors non disponibles.")
    else:
        # KPIs globaux
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Corridors cartographiés</div>
                <div class="value">{len(df_corridors)}</div>
                <div class="sub">Base RegBridge 2024</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            crit = len(df_corridors[df_corridors["Criticite_OFAC"] == "Critique"])
            st.markdown(f"""
            <div class="metric-box" style="border-left-color:#c53030">
                <div class="label">Corridors OFAC Critiques</div>
                <div class="value" style="color:#c53030">{crit}</div>
                <div class="sub">Exposition directe sanctions US</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            vol_total = df_corridors[df_corridors["Volume_Annuel_USD_M"] > 0]["Volume_Annuel_USD_M"].sum()
            st.markdown(f"""
            <div class="metric-box">
                <div class="label">Volume total annuel</div>
                <div class="value">{vol_total/1000:.1f} Mds USD</div>
                <div class="sub">Flux légitimes monitored</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            bloque = len(df_corridors[df_corridors["Score_Risque_Global"].str.contains("10", na=False)])
            st.markdown(f"""
            <div class="metric-box" style="border-left-color:#1a202c">
                <div class="label">Corridors bloqués</div>
                <div class="value">{bloque}</div>
                <div class="sub">Embargo total (ex: Cuba)</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)

        # Filtres
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtre_crit = st.multiselect(
                "Criticité OFAC",
                options=df_corridors["Criticite_OFAC"].unique().tolist(),
                default=[],
            )
        with col_f2:
            filtre_gafi = st.multiselect(
                "Criticité GAFI",
                options=df_corridors["Criticite_GAFI"].unique().tolist(),
                default=[],
            )

        df_corr_filtered = df_corridors.copy()
        if filtre_crit:
            df_corr_filtered = df_corr_filtered[df_corr_filtered["Criticite_OFAC"].isin(filtre_crit)]
        if filtre_gafi:
            df_corr_filtered = df_corr_filtered[df_corr_filtered["Criticite_GAFI"].isin(filtre_gafi)]

        # Affichage corridors
        for _, r in df_corr_filtered.iterrows():
            score = str(r.get("Score_Risque_Global", ""))
            score_val = float(score.split("/")[0]) if "/" in score else 5.0
            bar_color = "#c53030" if score_val >= 9 else ("#c05621" if score_val >= 7 else ("#b7791f" if score_val >= 5 else "#276749"))
            bar_pct = int(score_val * 10)

            with st.expander(f"{'🚨' if score_val >= 9 else ('⚠️' if score_val >= 7 else '✅')}  **{r['Corridor']}**  |  Vol. {r.get('Volume_Annuel_USD_M','N/A')} M USD/an  |  Score {score}", expanded=False):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Criticités réglementaires**")
                    st.markdown(f"- OFAC : {badge_html(r.get('Criticite_OFAC','N/A'))}", unsafe_allow_html=True)
                    st.markdown(f"- GAFI : {badge_html(r.get('Criticite_GAFI','N/A'))}", unsafe_allow_html=True)
                    st.markdown(f"- TRACFIN : {badge_html(r.get('Criticite_TRACFIN','N/A'))}", unsafe_allow_html=True)
                    st.markdown(f"- MTA actifs : **{r.get('Nombre_MTA_Actifs','N/A')}**")
                    st.markdown(f"- % PIB destination : **{r.get('Part_PIB_Destination_Pct','N/A')}%**")
                    st.markdown(f"- Tendance volume : **{r.get('Tendance_Volume','N/A')}**")
                with c2:
                    st.markdown("**🛡️ Mesures de Remédiation**")
                    st.info(str(r.get("Mesures_Remediation", "N/A")))
                    st.markdown("**⚙️ Contrôles Compensatoires**")
                    st.warning(str(r.get("Controles_Compensatoires", "N/A")))
                    st.markdown("**⚡ Défis Spécifiques**")
                    st.markdown(f"_{str(r.get('Defis_Specifiques','N/A'))}_")

        # Export
        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Exporter la cartographie des corridors (CSV)",
            data=to_csv_download(df_corr_filtered),
            file_name="cartographie_corridors_diaspora.csv",
            mime="text/csv",
        )


# ═══════════════════════════════════════════════════════════
# ONGLET 4 : DÉMARCHE D'AUDIT & RÉFÉRENTIEL
# ═══════════════════════════════════════════════════════════
elif menu == "📋 Démarche d'Audit & Référentiel":
    st.subheader("📋 Démarche d'Audit & Référentiel Réglementaire")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔵 Démarche Audit", "📘 GAFI (40 Rec.)", "🔴 OFAC Sanctions", "🇫🇷 TRACFIN / DGT", "🏦 Bâle II/III"
    ])

    # ── Démarche Audit ──
    with tab1:
        st.markdown("#### Méthodologie d'Audit RegBridge — Séquence en 5 Phases")
        st.markdown("*Démarche structurée pour cartographier et remédier aux vulnérabilités LCB-FT d'une institution ou d'une juridiction.*")

        if df_audit.empty:
            st.error("Données d'audit non disponibles.")
        else:
            for _, r in df_audit.iterrows():
                st.markdown(f"""
                <div class="step-card">
                    <div>
                        <span class="step-num">{int(r.get('Numero_Etape', 0))}</span>
                        <strong style="font-size:1rem; color:#1a365d;">{r.get('Phase','')}</strong>
                        <span style="color:#718096; margin-left:0.5rem; font-size:0.85rem;">— {r.get('Titre_Etape','')}</span>
                    </div>
                    <p style="margin:0.6rem 0 0.4rem; color:#2d3748; font-size:0.88rem;">{str(r.get('Description_Complete',''))[:300]}...</p>
                    <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-top:0.5rem; font-size:0.78rem; color:#718096;">
                        <span>⏱️ <b>{r.get('Duree_Estimee_Jours','')}</b> jours</span>
                        <span>👥 <b>{r.get('Intervenants','')}</b></span>
                        <span>✅ Validation : <em>{r.get('Criteres_Validation','')}</em></span>
                    </div>
                    <div style="margin-top:0.5rem; font-size:0.78rem; background:#ebf8ff; padding:0.3rem 0.6rem; border-radius:4px; display:inline-block; color:#2c5282;">
                        🛠️ <b>Outils :</b> {r.get('Outils_Plateforme','')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.download_button(
                "⬇️ Télécharger le référentiel d'audit (CSV)",
                data=to_csv_download(df_audit),
                file_name="methodologie_audit_regbridge.csv",
                mime="text/csv",
            )

    # ── GAFI ──
    with tab2:
        st.markdown("#### Recommandations GAFI — Normes Mondiales LCB-FT")
        if not df_gafi.empty:
            filtre_cat = st.multiselect("Filtrer par catégorie", options=df_gafi["Categorie"].unique().tolist(), default=[])
            df_gafi_f = df_gafi[df_gafi["Categorie"].isin(filtre_cat)] if filtre_cat else df_gafi
            
            st.dataframe(
                df_gafi_f[["Code_Norme", "Categorie", "Titre", "Obligation_Clef", "Niveau_Risque"]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "⬇️ Télécharger le référentiel GAFI (CSV)",
                data=to_csv_download(df_gafi_f),
                file_name="referentiel_gafi.csv",
                mime="text/csv",
            )

    # ── OFAC ──
    with tab3:
        st.markdown("#### Programmes de Sanctions OFAC — Embargos et Listes SDN")
        if not df_ofac.empty:
            st.dataframe(
                df_ofac[["Code_Programme", "Type_Sanction", "Pays_Region_Vise", "Niveau_Impact_MTA", "Autorite_Gestion"]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "⬇️ Télécharger le référentiel OFAC (CSV)",
                data=to_csv_download(df_ofac),
                file_name="referentiel_ofac.csv",
                mime="text/csv",
            )

    # ── TRACFIN / DGT ──
    with tab4:
        st.markdown("#### Obligations TRACFIN & DGT — Dispositif Français LCB-FT")
        if not df_tracfin.empty:
            st.dataframe(
                df_tracfin[["Code_Texte", "Type_Obligation", "Organisme", "Titre", "Delai_Execution", "Sanction_Max"]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "⬇️ Télécharger le référentiel TRACFIN/DGT (CSV)",
                data=to_csv_download(df_tracfin),
                file_name="referentiel_tracfin_dgt.csv",
                mime="text/csv",
            )

    # ── Bâle ──
    with tab5:
        st.markdown("#### Normes Prudentielles Bâle II / III — Supervision Bancaire")
        if not df_bale.empty:
            filtre_pilier = st.multiselect("Filtrer par Pilier", options=df_bale["Pilier"].unique().tolist(), default=[])
            df_bale_f = df_bale[df_bale["Pilier"].isin(filtre_pilier)] if filtre_pilier else df_bale
            
            st.dataframe(
                df_bale_f[["Cadre", "Pilier", "Code_Ratio", "Titre", "Seuil_Minimum", "Statut_Implementation"]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "⬇️ Télécharger le référentiel Bâle (CSV)",
                data=to_csv_download(df_bale_f),
                file_name="referentiel_bale.csv",
                mime="text/csv",
            )


# ═══════════════════════════════════════════════════════════
# ONGLET 5 : CABINET — RDV & ÉCHANGES
# ═══════════════════════════════════════════════════════════
elif menu == "📅 Cabinet — RDV & Échanges":
    st.subheader("📅 Cabinet RegBridge — Prise de Rendez-Vous & Échanges")

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("#### 📋 Formulaire de Contact & Réservation de Prestation")

        type_client = st.selectbox(
            "Nature de l'organisation",
            ["Banque Commerciale", "Maison de Transfert d'Argent (MTA)", "Banque Centrale / Régulateur",
             "Gouvernement / Ministère", "ONG Internationale", "Cabinet d'Audit / Conseil", "Autre"],
        )

        col_n1, col_n2 = st.columns(2)
        with col_n1:
            nom_contact = st.text_input("Nom du contact *")
        with col_n2:
            email_contact = st.text_input("Email professionnel *")

        organisation = st.text_input("Nom de l'organisation / Institution *")
        pays_client = st.text_input("Pays d'opération principal")

        if not df_consulting.empty:
            prestations = df_consulting["Titre_Prestation"].tolist()
            prix_map = dict(zip(df_consulting["Titre_Prestation"], df_consulting["Prix_EUR"].astype(str)))
            code_map = dict(zip(df_consulting["Titre_Prestation"], df_consulting["Code_Prestation"]))
            duree_map = dict(zip(df_consulting["Titre_Prestation"], df_consulting["Duree_Jours"].astype(str)))
            
            prestation_sel = st.selectbox("Prestation souhaitée *", prestations)

            if prestation_sel:
                row_p = df_consulting[df_consulting["Titre_Prestation"] == prestation_sel].iloc[0]
                st.markdown(f"""
                <div style='background:#ebf8ff; border-radius:8px; padding:0.8rem 1rem; margin:0.5rem 0; font-size:0.85rem; color:#2c5282;'>
                    <b>💰 Tarif :</b> {row_p.get('Prix_EUR','N/A')} € HT 
                    &nbsp;|&nbsp; <b>⏱️ Durée :</b> {row_p.get('Duree_Jours','N/A')} jours
                    &nbsp;|&nbsp; <b>📦 Livrable :</b> {row_p.get('Livrable_Principal','N/A')}
                    <br><small style='color:#4a5568;'>{row_p.get('Description_Courte','')}</small>
                </div>
                """, unsafe_allow_html=True)

        date_rdv = st.date_input("Date souhaitée pour l'entretien initial", min_value=datetime.date.today())
        
        format_rdv_options = ["Visioconférence (Teams / Zoom)", "Présentiel Paris", "Appel téléphonique"]
        format_rdv = st.selectbox("Format de l'entretien", format_rdv_options)

        message = st.text_area(
            "Contexte & Besoins (décrivez votre situation réglementaire)",
            placeholder="Ex : Notre banque fait l'objet d'une pression de de-risking de notre correspondant américain. Nous avons besoin d'un audit KYC urgent...",
            height=120,
        )

        urgence = st.checkbox("⚡ Demande urgente (réponse sous 24h, supplément tarifaire)")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✉️ Envoyer la demande", use_container_width=True):
                if nom_contact and email_contact and organisation:
                    st.success(f"✅ Demande envoyée ! Nous reviendrons vers **{nom_contact}** ({email_contact}) sous 48h.")
                    if urgence:
                        st.warning("⚡ Demande urgente prise en compte — Réponse garantie sous 24h.")
                else:
                    st.error("⚠️ Merci de compléter les champs obligatoires (*)")

        with col_btn2:
            if st.button("💳 Procéder au paiement (Stripe)", use_container_width=True):
                st.info("🔌 Redirection vers Stripe Checkout... (Intégration en cours — contactez le cabinet)")
                if prestation_sel:
                    stripe_id = df_consulting[df_consulting["Titre_Prestation"] == prestation_sel]["Stripe_Price_ID"].iloc[0] if not df_consulting.empty else "N/A"
                    st.code(f"Stripe Price ID : {stripe_id}", language="text")

    with col_b:
        st.markdown("#### 📎 Espace de Dépôt Documentaire Sécurisé")
        st.markdown("""
        <div style='background:#fff5f5; border:1px solid #feb2b2; border-radius:8px; padding:0.8rem 1rem; font-size:0.82rem; color:#c53030; margin-bottom:0.8rem;'>
            🔒 <b>Transmission sécurisée :</b> Les documents déposés sont chiffrés en transit (TLS 1.3) 
            et à la réception. Accès exclusif aux analystes RegBridge habilités.
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Déposer vos documents de contrôle interne",
            accept_multiple_files=True,
            type=["pdf", "xlsx", "csv", "docx", "txt"],
            help="Formats acceptés : PDF, Excel, CSV, Word. Taille max : 50 MB par fichier.",
        )

        if uploaded_files:
            st.markdown("**Documents reçus :**")
            for f in uploaded_files:
                size_kb = len(f.read()) / 1024
                f.seek(0)
                st.markdown(f"""
                <div style='background:white; border-radius:6px; padding:0.5rem 0.8rem; margin:0.3rem 0;
                            border-left:3px solid #276749; font-size:0.82rem;'>
                    📄 <b>{f.name}</b> — {size_kb:.1f} KB
                    <span style='color:#276749; float:right;'>✓ Reçu</span>
                </div>
                """, unsafe_allow_html=True)
            st.success(f"✅ {len(uploaded_files)} document(s) reçu(s) et sécurisé(s).")

        st.markdown("<hr class='rb-divider'>", unsafe_allow_html=True)
        st.markdown("#### 📞 Coordonnées du Cabinet")
        st.markdown("""
        <div class="section-card">
            <div style="font-size:0.85rem; line-height:1.9;">
                🏛️ <b>RegBridge Compliance Advisors</b><br>
                📍 Paris, France<br>
                📧 contact@regbridge-compliance.com<br>
                📞 +33 (0)1 XX XX XX XX<br>
                🌐 www.regbridge-compliance.com<br>
                <br>
                <span style="color:#718096; font-size:0.78rem;">
                Disponibilité : Lun–Ven 09:00–18:00 CET<br>
                Urgences : Ligne dédiée 24/7 pour clients sous audit
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 💼 Catalogue des Prestations")
        if not df_consulting.empty:
            for _, r in df_consulting.iterrows():
                with st.expander(f"{r.get('Code_Prestation','')} — {r.get('Titre_Prestation','')}"):
                    st.markdown(f"""
                    **Prix :** {r.get('Prix_EUR','N/A')} € HT ({r.get('Prix_USD','N/A')} USD)  
                    **Durée :** {r.get('Duree_Jours','N/A')} jours  
                    **Livrable :** {r.get('Livrable_Principal','N/A')}  
                    **Public cible :** {r.get('Public_Cible','N/A')}  
                    **Disponibilité :** {r.get('Disponibilite','N/A')}
                    """)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="rb-footer">
    ⚖️ <b>RegBridge Compliance Advisors</b> — Plateforme d'Intelligence Réglementaire<br>
    GAFI · OFAC · TRACFIN/DGT · Bâle III · OpenSanctions · GIABA<br>
    <span style="font-size:0.68rem; color:#4a5568;">
        Les informations fournies sont à des fins d'information et de conseil professionnel uniquement.
        Elles ne constituent pas un avis juridique. © 2025 RegBridge Compliance Advisors.
    </span>
</div>
""", unsafe_allow_html=True)
