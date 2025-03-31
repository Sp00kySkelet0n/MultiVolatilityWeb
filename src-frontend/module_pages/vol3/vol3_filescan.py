import streamlit as st
import pandas as pd
import json
import os
import sys

# Get the path to the ../template directory relative to this script
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'template'))

# Add it to sys.path
if template_dir not in sys.path:
    sys.path.insert(0, template_dir)

import templating

# Load JSON data from file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Streamlit UI
def main(dump_name, module_name):
    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert JSON to DataFrame
    df = pd.DataFrame(json_data)

    # Initialize session state variables if they don't exist
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ''
    if 'keep_users' not in st.session_state:
        st.session_state.keep_users = False

    # Apply filters
    filtered_df = df.copy()
    if st.session_state.keep_users:
        filtered_df = filtered_df[filtered_df["Name"].str.contains("Users", case=False, na=False)]
    if st.session_state.search_term:
        filtered_df = filtered_df[filtered_df["Name"].str.contains(st.session_state.search_term, case=False, na=False)]

    # Render table
    templating.render_json_table(filtered_df, f"{module_name} Output", module_name)
    st.caption("Tip: Click on column headers to sort, and use the search box to filter results.")

    # Inputs below the table
    with st.form(key='filter_form'):
        search_term = st.text_input("Search Arguments", value=st.session_state.search_term)
        keep_users = st.checkbox("Show Only 'Users' Entries", value=st.session_state.keep_users)
        submit_button = st.form_submit_button(label='Apply Filters')

    # Update session state and rerun if filters have changed
    if submit_button:
        st.session_state.search_term = search_term
        st.session_state.keep_users = keep_users
        st.rerun()

