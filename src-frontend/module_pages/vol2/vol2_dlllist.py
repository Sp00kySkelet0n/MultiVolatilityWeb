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

# Streamlit UI
def main(dump_name, module_name):
    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert to DataFrame
    df = pd.DataFrame(json_data["rows"], columns=json_data["columns"])

    # Load previous session state
    search_pid = st.session_state.get("search_pid", "")
    search_path = st.session_state.get("search_path", "")

    # Filter logic
    filtered_df = df.copy()

    if search_pid:
        filtered_df = filtered_df[filtered_df["Pid"].astype(str).str.contains(search_pid, case=False, na=False)]

    if search_path:
        filtered_df = filtered_df[filtered_df["Path"].astype(str).str.contains(search_path, case=False, na=False)]

    templating.render_json_table(filtered_df, f"{module_name} Output", module_name)
    st.caption("Tip: Use the filters below to refine by PID or path. Rows with errors will still appear.")


    # Filters below the table
    new_search_pid = st.text_input("Search by PID", value=search_pid, key="search_pid_input")
    new_search_path = st.text_input("Search by Path", value=search_path, key="search_path_input")

    # Update session state and rerun if changed
    if new_search_pid != search_pid or new_search_path != search_path:
        st.session_state.search_pid = new_search_pid
        st.session_state.search_path = new_search_path
        st.rerun()