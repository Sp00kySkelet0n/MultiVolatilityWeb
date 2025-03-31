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

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name,module_name):
    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert to DataFrame
    df = pd.DataFrame(json_data)

    # Basic sanity check
    if df.empty or "Name" not in df.columns:
        st.error("Error: JSON data missing or doesn't contain expected fields.")
        return

    # Load previous state
    search_name = st.session_state.get("search_name", "")

    # Filter
    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search_name, case=False, na=False) |
            filtered_df["Process"].str.contains(search_name, case=False, na=False)
        ]
    
    templating.render_json_table(
        filtered_df[["Name", "Process", "PID", "Path", "Base", "Size", "LoadTime", "File output"]],
        f"{module_name} Output",
        module_name
    )

    st.caption("Tip: Use the filter below to search by module or process name. Columns are sortable.")

    # Input filter (below the table)
    new_search_name = st.text_input("Search by Module or Process Name", value=search_name, key="search_name_input")

    # Update session state and rerun if changed
    if new_search_name != search_name:
        st.session_state.search_name = new_search_name
        st.rerun()
