# ⚖️ RegBridge Compliance Advisors

**Plateforme SaaS d'Intelligence Réglementaire — LCB-FT, GAFI, OFAC, TRACFIN/DGT, Bâle III**

Spécialisée Caraïbes & Afrique | Lutte contre le De-Risking

---

## 🗂️ Structure du projet

```
regbridge/
├── app.py                          # Application principale Streamlit
├── requirements.txt                # Dépendances Python
└── platform_data/                  # Base d'intelligence (10 fichiers CSV)
    ├── reg_matrix_gafi.csv         # 40 Recommandations GAFI
    ├── reg_matrix_ofac.csv         # Programmes de sanctions OFAC/SDN
    ├── reg_matrix_tracfin_dgt.csv  # Obligations françaises LCB-FT & Gel avoirs
    ├── normes_prudentielles_bale.csv # Piliers Bâle II/III, ratios prudentiels
    ├── country_risk_caribbean.csv  # Risque pays — Caraïbes (12 juridictions)
    ├── country_risk_africa.csv     # Risque pays — Afrique (12 juridictions)
    ├── pep_sanctions_profiles.csv  # Base screening PEP & sanctions (11 profils)
    ├── mta_diaspora_corridors.csv  # Corridors de transfert diaspora (12 corridors)
    ├── audit_procedures_framework.csv # Méthodologie audit en 5 étapes
    └── appointments_consulting_schema.csv # Catalogue de prestations & tarifs
```

## 🚀 Déploiement Streamlit Community Cloud

1. Forker ce dépôt sur GitHub
2. Connecter à [share.streamlit.io](https://share.streamlit.io)
3. Pointer sur `app.py`
4. Déployer — aucune variable d'environnement requise pour la version de base

## 📡 Évolutions prévues

- **Intégration API OFAC** : connexion temps réel à api.ofac.us
- **OpenSanctions API** : remplacement du CSV PEP par l'API officielle
- **DGT Gel des Avoirs** : flux JSON de la Direction Générale du Trésor
- **ReportLab / WeasyPrint** : génération PDF réelle des rapports d'audit
- **Stripe Checkout** : tunnel de paiement pour réservation des prestations

## 🔒 Sources réglementaires intégrées

| Source | Couverture |
|--------|-----------|
| GAFI / FATF | 40 Recommandations — normes mondiales LCB-FT |
| OFAC (US Treasury) | Listes SDN, SSI, embargos par pays |
| TRACFIN | Déclarations de soupçon, obligations françaises |
| DGT France | Gel des avoirs, arrêtés ministériels |
| Bâle II/III (BIS) | Ratios CET1, LCR, NSFR, Levier |
| OpenSanctions | Screening multi-source consolidé |
| GIABA / UEMOA | Évaluations Afrique de l'Ouest |

---

*© 2025 RegBridge Compliance Advisors — Contact : contact@regbridge-compliance.com*
