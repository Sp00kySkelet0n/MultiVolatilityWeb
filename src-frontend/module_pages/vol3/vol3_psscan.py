import streamlit as st
import pandas as pd
import json
import os, sys

# Get the path to the ../template directory relative to this script
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'template'))

# Add it to sys.path
if template_dir not in sys.path:
    sys.path.insert(0, template_dir)

import templating

# Load JSON from file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name, module_name):
    # Load the JSON file
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert JSON list of dicts to DataFrame
    df = pd.DataFrame(json_data)

    # Sanity check
    if df.empty or "ImageFileName" not in df.columns:
        st.error("Error: Required data not found in JSON.")
        return

    # Load filter states
    search_term = st.session_state.get("search_process", "")
    show_running_only = st.session_state.get("show_running_only", False)
    show_exited_only = st.session_state.get("show_exited_only", False)

    # Apply filters
    filtered_df = df.copy()

    if search_term:
        filtered_df = filtered_df[filtered_df["ImageFileName"].str.contains(search_term, case=False, na=False)]

    if show_running_only and not show_exited_only:
        filtered_df = filtered_df[filtered_df["ExitTime"].isnull()]
    elif show_exited_only and not show_running_only:
        filtered_df = filtered_df[filtered_df["ExitTime"].notnull()]
    # If both or neither are checked, show all

    templating.render_json_table(filtered_df, f"{module_name} Output", module_name)
    st.caption("Tip: Use column headers to sort and the controls below to filter for specific process names or running state.")

    # Filters below the table
    new_search_term = st.text_input("Search Process Name", value=search_term, key="search_process_input")
    new_show_running_only = st.checkbox("Show Only Running Processes (Hide Exited)", value=show_running_only, key="show_running_only_input")
    new_show_exited_only = st.checkbox("Show Only Exited Processes (Hide Running)", value=show_exited_only, key="show_exited_only_input")

    # Update session state and rerun if changed
    if (new_search_term != search_term or
        new_show_running_only != show_running_only or
        new_show_exited_only != show_exited_only):
        st.session_state.search_process = new_search_term
        st.session_state.show_running_only = new_show_running_only
        st.session_state.show_exited_only = new_show_exited_only
        st.rerun()