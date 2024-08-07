import streamlit as st
import pandas as pd
import re
import io

# Dictionnaire des thématiques et mots-clés (combinaison des anciens et nouveaux)
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux', 'terriers', 'veterinary', 'breed', 'wildlife', 'dog', 'cat', 'bird', 'fish', 'monde marin', 'faune', 'sauvage', 'domestique', 'poisson', 'oiseau'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant', 'chef', 'gastronomy', 'dining', 'eatery', 'kitchen', 'bakery', 'catering', 'madeleine', 'plat', 'traiteur', 'aliment', 'repas', 'gourmet', 'nourriture', 'cuisinier', 'pizza', 'grill'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services', 'firm', 'industry', 'commerce', 'trade', 'venture', 'market', 'publicity', 'entreprise', 'affaires', 'gestion', 'service', 'industrie', 'commerce', 'publicité'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier', 'fortune', 'credit', 'money', 'invest', 'mortgage', 'loan', 'tax', 'insurance', 'wealth', 'argent', 'prêt', 'hypothèque', 'impôt', 'assurance', 'richesse'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'research', 'graphics', 'solution', 'hardware', 'programming', 'coding', 'digital', 'cyber', 'web', 'hack', 'forum', 'apps', 'digital', 'open media', 'email', 'AI', 'machine learning', 'competence', 'informatique', 'technologie', 'ordinateur', 'logiciel', 'jeu vidéo', 'recherche', 'solution', 'matériel', 'programmation', 'codage', 'numérique', 'cybernétique', 'hacking', 'intelligence artificielle', 'apprentissage automatique'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux', 'solar', 'energy', 'decor', 'furniture', 'property', 'apartment', 'condo', 'villa', '4piecesetplus', 'maison', 'jardinage', 'décoration', 'aménagement', 'travaux', 'énergie', 'décor', 'meuble', 'propriété', 'appartement', 'condo', 'villa', '4piècesetplus'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping', 'style', 'clothing', 'accessories', 'women', 'hat', 'jewelry', 'makeup', 'designer', 'boutique', 'shopping', 'runway', 'model', 'mode', 'beauté', 'bien-être', 'style de vie', 'vêtements', 'accessoires', 'chapeau', 'bijoux', 'maquillage', 'styliste', 'boutique', 'défilé', 'modèle', 'robe', 'vintage'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors', 'baby', 'therapy', 'massage', 'biochimie', 'skincare', 'santé', 'fitness', 'bien-être', 'médical', 'hôpital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'santé', 'aînés', 'bébé', 'thérapie', 'massage', 'biochimie', 'soins de la peau'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo', 'cricket', 'gym', 'athletic', 'team', 'league', 'club', 'cycling', 'surf', 'trail', 'marathon', 'tango', 'sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'vélo', 'cricket', 'gym', 'athlétique', 'équipe', 'ligue', 'club', 'cyclisme', 'surf', 'sentier', 'marathon', 'tango'],
    'TOURISME': [
        'travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping',
        'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'sauna',
        'expat', 'visit', 'explore', 'adventure', 'destination', 'hotel',
        'resort', 'photo', 'document', 'wave', 'land', 'fries', 'voyage',
        'trip', 'journey', 'escape', 'getaway', 'tourisme', 'vacances',
        'voyage', 'sauna', 'expatrié', 'visite', 'explorer', 'aventure',
        'destination', 'hôtel', 'resort', 'photo', 'document', 'vague',
        'terre', 'frites', 'voyage', 'excursion', 'voyage', 'évasion',
        's\'échapper'
    ],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture', 'formula', 'drive', 'racing', 'garage', 'repair', 'dealership', 'rental', 'taxi', 'bus', 'train', 'plane', 'aviation', 'véhicule', 'voiture', 'auto', 'bike', 'bicyclette', 'moto', 'produits', 'sécurité', 'voiture', 'formule', 'conduite', 'course', 'garage', 'réparation', 'concessionnaire', 'location', 'taxi', 'bus', 'train', 'avion', 'aviation']
}

# Mots clés pour exclure des domaines (combinaison des anciens et nouveaux)
excluded_keywords = [
    'religion', 'sex', 'voyance', 'escort', 'jesus', 'porn', 'teen', 'adult',
    'White Pussy', 'Black Cocks', 'youtube', 'instagram', 'pinterest', 'forex',
    'trading', 'invest', 'broker', 'stock', 'market', 'finance', 'avocat', 'avocats',
    'fuck', 'poker'
]

# Mots clés pour exclure des domaines liés au sexe
sex_keywords = [
    'fuck', 'sex', 'porn', 'pussy', 'cock', 'adult', 'teen', 'escort', 'White Pussy', 'Black Cocks'
]

excluded_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, excluded_keywords)), re.IGNORECASE)
sex_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, sex_keywords)), re.IGNORECASE)
year_regex = re.compile(r'\b(19[0-9]{2}|20[0-9]{2})\b')
name_regex = re.compile(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b')
brand_regex = re.compile(r'\b(samsung|atari|longchamp)\b', re.IGNORECASE)
geographic_regex = re.compile(r'\b(louisville|quercy|france|ferney)\b', re.IGNORECASE)
publicity_regex = re.compile(r'\bpublicity\b', re.IGNORECASE)
transport_regex = re.compile(r'\btransport\b', re.IGNORECASE)

def classify_domain(domain, categories):
    domain_lower = domain.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in domain_lower:
                # Prioritize certain keywords over others
                if category == 'SANTE' and 'skincare' in domain_lower:
                    return 'SANTE'
                # Exclude domains that contain 'land' if 'ecole' is present
                if category == 'TOURISME' and 'land' in domain_lower and 'ecole' in domain_lower:
                    return 'EXCLU'
                return category
    # Special cases
    if 'nomad' in domain_lower and 'map' in domain_lower:
        return 'TOURISME'
    if 'apache' in domain_lower and 'mag' in domain_lower:
        return 'INFORMATIQUE'
    if 'fitness' in domain_lower:
        return 'SPORT'
    if 'chateau' in domain_lower:
        return 'TOURISME'
    if 'competences' in domain_lower:
        return 'ENTREPRISE'
    if 'rando' in domain_lower and 'decouverte' in domain_lower:
        return 'TOURISME'
    if 'carotte' in domain_lower:
        return 'CUISINE'
    if 'carpet' in domain_lower or 'stains' in domain_lower:
        return 'MAISON'
    if 'training' in domain_lower:
        return 'SPORT'
    if 'entrepreneur' in domain_lower:
        return 'ENTREPRISE'
    return 'NON UTILISÉ'

def is_excluded(domain):
    if sex_regex.search(domain) or excluded_regex.search(domain) or year_regex.search(domain):
        return True
    if name_regex.search(domain):
        return True
    if any(word in domain.lower() for word in ['pas cher', 'bas prix']):
        return True
    if re.search(r'\b[a-z]+[A-Z][a-z]+\b', domain):  # Noms propres probables
        return True
    if len(domain.split('.')[0]) <= 3:  # Domaines très courts
        return True
    if brand_regex.search(domain):  # Marques
        return True
    if geographic_regex.search(domain):  # Géographique
        return True
    if publicity_regex.search(domain) and not transport_regex.search(domain):
        return True
    if re.search(r'\d', domain):  # Domaines contenant des nombres
        return True
    if 'marijuana' in domain.lower():
        return True
    if 'denuncia' in domain.lower():
        return True
    if 'hunter' in domain.lower():
        return True
    return False

def has_meaning(domain):
    clean_domain = re.sub(r'\.(com|net|org|info|biz|fr|de|uk|es|it)$', '', domain.lower())
    clean_domain = ''.join(char for char in clean_domain if char.isalnum())
    words = re.findall(r'\b\w{3,}\b', clean_domain)
    return len(words) > 0

def main():
    st.title("Classification des noms de domaine par thématique")

    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")

    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]
            classified_domains = []
            excluded_domains = []

            for domain in domaines:
                try:
                    if is_excluded(domain):
                        excluded_domains.append((domain, 'EXCLU'))
                    else:
                        category = classify_domain(domain, thematique_dict)
                        if category == 'NON UTILISÉ' and not has_meaning(domain):
                            excluded_domains.append((domain, 'EXCLU (pas de sens)'))
                        elif category == 'NON UTILISÉ':
                            excluded_domains.append((domain, category))
                        else:
                            classified_domains.append((domain, category))
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse du domaine {domain}: {e}")

            df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category'])
            df_excluded = pd.DataFrame(excluded_domains, columns=['Domain', 'Category'])

            st.subheader("Prévisualisation des résultats")
            st.write(df_classified)
            st.write(df_excluded)

            def convert_df_to_excel(df1, df2):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df1.to_excel(writer, index=False, sheet_name='Classified')
                    df2.to_excel(writer, index=False, sheet_name='Excluded')
                output.seek(0)
                return output

            st.download_button(
                label="Télécharger les résultats en Excel",
                data=convert_df_to_excel(df_classified, df_excluded),
                file_name="domaines_classes_resultats.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Veuillez entrer au moins un nom de domaine.")

if __name__ == "__main__":
    main()
