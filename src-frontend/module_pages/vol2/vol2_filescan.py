import streamlit as st
import pandas as pd
import json
import os, sys

# Get the path to the ../template directory relative to this script
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'template'))
if template_dir not in sys.path:
    sys.path.insert(0, template_dir)

import templating

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name, module_name):
    # Load JSON
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)
    df = pd.DataFrame(json_data["rows"], columns=["Offset", "RefCount", "ShadowCount", "Permissions", "Path"])

    # Initialize state if needed
    if "filters_applied" not in st.session_state:
        st.session_state.search_path_term = ""
        st.session_state.keep_users = False
        st.session_state.filters_applied = True
        st.rerun()

    # Read current filter values
    search_term = st.session_state.search_path_term
    keep_users = st.session_state.keep_users

    # Apply filters
    filtered_df = df.copy()
    if keep_users:
        filtered_df = filtered_df[filtered_df["Path"].str.contains("Users", case=False, na=False)]
    if search_term:
        filtered_df = filtered_df[filtered_df["Path"].str.contains(search_term, case=False, na=False)]

    templating.render_json_table(filtered_df.to_dict(orient="records"), title=f"{module_name} Output")
    st.caption("Tip: Use the filters below to refine entries. Columns can be sorted.")

    # --- Inputs below the table ---
    new_search_term = st.text_input("Search Path", value=search_term)
    new_keep_users = st.checkbox("Show Only 'Users' Entries", value=keep_users)

    # Handle state change on next run
    if new_search_term != search_term or new_keep_users != keep_users:
        st.session_state.search_path_term = new_search_term
        st.session_state.keep_users = new_keep_users
        st.session_state.filters_applied = False
        st.rerun()
