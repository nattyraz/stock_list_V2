
import streamlit as st
import pandas as pd

# Title
st.title("Moteur de recherche pour le stock")

uploaded_file = st.file_uploader("Importez votre fichier Excel", type=['xlsx'])

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    cleaned_data = data[(data["Kalkuleret Kostpris (RV)"].notna()) & (data["Lager.1"].notna()) & (data["Lager.1"] > 0)]
    
    # Search input
    search_term = st.text_input("Entrez votre recherche (Beskrivelse, Nummer, or Produktgruppekode)")

    # Filter by brand
    brands = st.multiselect("Choisissez une marque", options=cleaned_data["Producent Kode"].unique().tolist(), default=cleaned_data["Producent Kode"].unique().tolist())

    # Filter by price
    min_price, max_price = st.slider("Sélectionnez une plage de prix", int(cleaned_data["Kalkuleret Kostpris (RV)"].min()), int(cleaned_data["Kalkuleret Kostpris (RV)"].max()), (int(cleaned_data["Kalkuleret Kostpris (RV)"].min()), int(cleaned_data["Kalkuleret Kostpris (RV)"].max())))

    # Filter results
    filtered_data = cleaned_data[cleaned_data["Producent Kode"].isin(brands) & (cleaned_data["Kalkuleret Kostpris (RV)"] >= min_price) & (cleaned_data["Kalkuleret Kostpris (RV)"] <= max_price)]

    if search_term:
        filtered_data = filtered_data[filtered_data["Beskrivelse.1"].str.contains(search_term, case=False) | filtered_data["Nummer"].str.contains(search_term, case=False) | filtered_data["Produktgruppekode"].str.contains(search_term, case=False)]

    # Display results
    for index, row in filtered_data.iterrows():
        st.write(f'**Description:** {row["Beskrivelse.1"]}')
        st.write(f'**Numéro:** {row["Nummer"]}')
        st.write(f'**Prix:** {row["Kalkuleret Kostpris (RV)"]}')
        st.write(f'**Quantité:** {row["Lager.1"]}')
        st.write(f'**Lien:** [Cliquez ici]({row["Web URL"]})')
        st.write("---")
