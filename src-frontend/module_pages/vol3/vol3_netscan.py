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

    # Convert to DataFrame
    df = pd.DataFrame(json_data)

    # Ensure required columns exist
    for col in ["Owner", "Proto", "LocalPort"]:
        if col not in df.columns:
            st.error(f"Error: Required column '{col}' not found in JSON data.")
            return

    # Normalize columns
    df["Proto"] = df["Proto"].astype(str).str.strip().str.upper()
    df["Owner"] = df["Owner"].astype(str)

    # Load filter states
    search_owner = st.session_state.get("search_owner", "")
    proto_filter = st.session_state.get("proto_filter", [])
    port_filter = st.session_state.get("port_filter", 0)

    # Apply filters
    filtered_df = df.copy()

    if search_owner:
        filtered_df = filtered_df[filtered_df["Owner"].str.contains(search_owner, case=False, na=False)]

    if proto_filter:
        filtered_df = filtered_df[filtered_df["Proto"].isin(proto_filter)]

    if port_filter > 0:
        filtered_df = filtered_df[filtered_df["LocalPort"] == port_filter]

    templating.render_json_table(filtered_df, f"{module_name} Output", module_name)
    st.caption("Tip: Click column headers to sort. Use the filters below to find suspicious ports, protocols, or processes.")

    # Filters below the table
    new_search_owner = st.text_input("Search by Owner", value=search_owner, key="search_owner_input")
    new_proto_filter = st.multiselect("Protocol", sorted(df["Proto"].unique()), default=proto_filter, key="proto_filter_input")
    new_port_filter = st.number_input("Filter by Local Port", value=port_filter, step=1, key="port_filter_input")

    # Update session state and rerun if changed
    if (new_search_owner != search_owner or
        new_proto_filter != proto_filter or
        new_port_filter != port_filter):
        st.session_state.search_owner = new_search_owner
        st.session_state.proto_filter = new_proto_filter
        st.session_state.port_filter = new_port_filter
        st.rerun()