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
    columns_to_keep = [
        "Console Process",
        "Console PID",
        "Title",
        "Attached Process Name",
        "Command History Applications",
        "Command History Command String"
    ]
    filtered_df = df[columns_to_keep]

    templating.render_json_table(filtered_df, f"Filtered {module_name} Output", module_name)

    st.divider()

    templating.render_json_table(df, f"Full {module_name} Output", module_name)
