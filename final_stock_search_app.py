
import streamlit as st
import pandas as pd

# Title
st.title("Moteur de recherche optimisé pour le stock")

uploaded_file = st.file_uploader("Importez votre fichier Excel", type=['xlsx'])

if uploaded_file:
    # Read only the 'Varekategorikode.1' column to get the main categories
    main_categories = pd.read_excel(uploaded_file, usecols=["Varekategorikode.1"])["Varekategorikode.1"].unique().tolist()
    
    selected_main_category = st.selectbox("Sélectionnez une catégorie principale", main_categories)
    
    # Load the data for the selected main category
    data = pd.read_excel(uploaded_file)
    main_category_data = data[data["Varekategorikode.1"] == selected_main_category]
    
    # Allow user to filter further by 'Produktgruppekode'
    sub_categories = main_category_data["Produktgruppekode"].unique().tolist()
    selected_sub_category = st.selectbox("Sélectionnez une sous-catégorie", sub_categories)
    
    filtered_data_by_sub_category = main_category_data[main_category_data["Produktgruppekode"] == selected_sub_category]
    
    # Search input
    search_term = st.text_input("Entrez votre recherche (Beskrivelse, Nummer)")

    # Filter by brand
    brands = st.multiselect("Choisissez une marque", options=filtered_data_by_sub_category["Producent Kode"].unique().tolist(), default=filtered_data_by_sub_category["Producent Kode"].unique().tolist())

    # Filter by price
    min_price, max_price = st.slider("Sélectionnez une plage de prix", int(filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"].min()), int(filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"].max()), (int(filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"].min()), int(filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"].max())))

    # Filter results
    final_filtered_data = filtered_data_by_sub_category[filtered_data_by_sub_category["Producent Kode"].isin(brands) & (filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"] >= min_price) & (filtered_data_by_sub_category["Kalkuleret Kostpris (RV)"] <= max_price)]

    if search_term:
        final_filtered_data = final_filtered_data[final_filtered_data["Beskrivelse.1"].str.contains(search_term, case=False) | final_filtered_data["Nummer"].str.contains(search_term, case=False)]

    # Display results
    for index, row in final_filtered_data.iterrows():
        st.write(f'**Description:** {row["Beskrivelse.1"]}')
        st.write(f'**Numéro:** {row["Nummer"]}')
        st.write(f'**Prix:** {row["Kalkuleret Kostpris (RV)"]}')
        st.write(f'**Quantité:** {row["Lager.1"]}')
        st.write(f'**Lien:** [Cliquez ici]({row["Web URL"]})')
        st.write("---")
