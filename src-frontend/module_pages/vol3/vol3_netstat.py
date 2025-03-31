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

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name, module_name):
    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert JSON to DataFrame
    df = pd.DataFrame(json_data)

    # Ensure required columns exist
    if "Proto" not in df.columns or "LocalAddr" not in df.columns:
        st.error("Error: Required columns ('Proto' or 'LocalAddr') not found in JSON data.")
        return

    # Normalize columns
    df["Proto"] = df["Proto"].astype(str).str.strip().str.upper()
    df["LocalAddr"] = df["LocalAddr"].astype(str)

    # Load filter states
    search_term = st.session_state.get("search_localaddr", "")
    remove_udp = st.session_state.get("remove_udp", False)

    # Apply filters
    filtered_df = df.copy()

    if remove_udp:
        filtered_df = filtered_df[~filtered_df["Proto"].str.contains("UDP", case=False, na=False)]

    if search_term:
        filtered_df = filtered_df[filtered_df["LocalAddr"].str.contains(search_term, case=False, na=False)]

    # Show filtered table using templating renderer
    templating.render_json_table(filtered_df, f"{module_name} Output", module_name)
    st.caption("Tip: Click column headers to sort. Use the controls below to filter results.")

    # Input filters (below the table)
    new_search_term = st.text_input("Search (Local Address)", value=search_term, key="search_localaddr_input")
    new_remove_udp = st.checkbox("Hide UDP Entries", value=remove_udp, key="remove_udp_input")

    # Update session state and rerun if changed
    if new_search_term != search_term or new_remove_udp != remove_udp:
        st.session_state.search_localaddr = new_search_term
        st.session_state.remove_udp = new_remove_udp
        st.rerun()

