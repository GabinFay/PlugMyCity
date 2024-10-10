import streamlit as st

# Titre du formulaire
st.title("New Accommodation Form")

# Formulaire pour recueillir les données
with st.form(key="new_accommodation_form"):
    # Champs du formulaire
    annee_construction = st.number_input("Année de construction", min_value=1800, max_value=2024, step=1)
    superficie_terrain = st.number_input("Superficie terrain (en m²)", min_value=1, step=1)
    nombre_pieces = st.number_input("Nombre de pièces", min_value=1, step=1)
    superficie_habitable = st.number_input("Superficie habitable (en m²)", min_value=1, step=1)
    annee_acquisition = st.number_input("Année d'acquisition", min_value=1800, max_value=2024, step=1)
    montant_acquisition = st.number_input("Montant d'acquisition (€)", min_value=1.0, step=1000.0)
    type_achat = st.selectbox("Type d'achat", ["Neuf", "Ancien", "Investissement", "Résidence principale"])

    # Bouton de validation du formulaire
    submit_button = st.form_submit_button(label="Valider")

# Vérification des informations soumises et affichage
if submit_button:
    st.write("### Informations soumises :")
    st.write(f"**Année de construction** : {annee_construction}")
    st.write(f"**Superficie du terrain** : {superficie_terrain} m²")
    st.write(f"**Nombre de pièces** : {nombre_pieces}")
    st.write(f"**Superficie habitable** : {superficie_habitable} m²")
    st.write(f"**Année d'acquisition** : {annee_acquisition}")
    st.write(f"**Montant d'acquisition** : {montant_acquisition} €")
    st.write(f"**Type d'achat** : {type_achat}")

    # Appeler une fonction pour créer un NFT
    st.write("Création du NFT en cours...")

