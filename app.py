import streamlit as st
import pandas as pd
import re
import io

# Function to standardize column names
def standardize_columns(df, column_mapping):
    return df.rename(columns=column_mapping)

# Function to check if geography is present in the local government file using regex
def check_geography_presence(geography, lg_df, geography_column):
    # Normalize the input and the DataFrame column for comparison
    geography_normalized = geography.strip().lower()
    lg_df[geography_column] = lg_df[geography_column].str.strip().str.lower()
    
    # Check if the geography is in the column
    if geography_normalized in lg_df[geography_column].values:
        return "Found in Local Government File"
    else:
        return "Missing in Local Government File"


# Load the local government file 
lg_file_path = "MOLG.xlsx"

try:

    lg_df = pd.read_excel(lg_file_path)
    st.write("Local Government File Loaded Successfully.")

except Exception as e:
    st.error(f"Error loading local government file: {e}")

st.title("Geography Consistency Checking")

# Load the census 2024 file
census_file = st.file_uploader("Please Upload Census Excel or CSV file", type=['xlsx', 'csv'], key='census')

if census_file is not None:
    if census_file.name.endswith('.xlsx'):
        census_df = pd.read_excel(census_file)
    elif census_file.name.endswith('.csv'):
        census_df = pd.read_csv(census_file)
    st.write("Census File Uploaded Successfully.")

    # Standardize column names for the census file
    census_df = standardize_columns(census_df, {
        '_id': 'id',
        'region': 'region',
        'district': 'district',
        'dcode': 'division_code',
        'county': 'county',
        'ccode': 'constituency_code',
        'const': 'constituency',
        'sub_county': 'sub_county',
        'scode': 'sub_county_code',
        'parish': 'parish',
        'pcode': 'parish_code',
        'lci': 'lci',
        'lccode': 'lc_code',
        'eaname': 'electoral_area_name',
        'eacode': 'electoral_area_code',
        'fullcode': 'full_code',
        'actualcode': 'actual_code'
    })

    # # User input to check geograhy
    # st.subheader("Check Geography Presence")
    # geography_type = st.selectbox("Select Geography:", ["District", "Sub-County", "Parish", "LCI"])
    # geography_value = st.text_input(f"Enter {geography_type} Name:")

    # if geography_value:
    #     if geography_type == "District":
    #         result = check_geography_presence_regex(geography_value, lg_df, 'district')
    #     elif geography_type == "Sub-county":
    #         result = check_geography_presence_regex(geography_value, lg_df, 'sub_county')
    #     elif geography_type == "Parish":
    #         result = check_geography_presence_regex(geography_value, lg_df, 'parish')
    #     elif geography_type == "LCI":
    #         result = check_geography_presence_regex(geography_value, lg_df, 'lci')
        
    #     st.write(result)

    # Process the entire census file
    processed_df = census_df.copy()
    for geography_type in ['district', 'sub_county', 'parish', 'lci']:
        processed_df[geography_type + '_status'] = processed_df.apply(lambda row: check_geography_presence(row[geography_type], lg_df, geography_type), axis=1)

    # Add download buttons for processed files
    st.download_button(
        label="Download Processed File",
        data=processed_df.to_csv(index=False),
        file_name="processed_geography_data.csv",
        mime="text/csv"
    )

    st.download_button(
        label=f"Download Processed {geography_type.lower()} Data",
        data=processed_df.to_csv(index=False),
        file_name=f"processed_{geography_type.lower()}_data.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload the census file for comparison.")