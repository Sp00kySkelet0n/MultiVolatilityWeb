import streamlit as st
import pandas as pd
import json

# Load and parse hashes
def load_and_parse_hashes(file_path):
    with open(file_path, "r") as file:
        json_data = json.load(file)

    parsed_rows = []
    for row in json_data["rows"]:
        parts = row[0].split(":")
        if len(parts) >= 4:
            parsed_rows.append({
                "User": parts[0],
                "rid": parts[1],
                "lmhash": parts[2],
                "nthash": parts[3]
            })
    return pd.DataFrame(parsed_rows)

# Streamlit UI
def main(dump_name, module_name):
    

    # Load JSON and parse hashes
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    df = load_and_parse_hashes(json_file_path)

    # Sidebar filter
    st.sidebar.header("Filter Options")
    search_user = st.sidebar.text_input("Search User")

    filtered_df = df.copy()
    if search_user:
        filtered_df = filtered_df[filtered_df["User"].str.contains(search_user, case=False, na=False)]

    # --- Main Display ---
    st.title("User Hash Explorer")
    st.write("View extracted user account hashes. Use the sidebar to filter.")

    # Metric + Expander Cards
    records = filtered_df.to_dict(orient="records")
    num_cols = 2

    for i in range(0, len(records), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(records):
                record = records[i + j]
                with col:
                    st.metric(label=record["User"], value=f"RID: {record['rid']}")
                    with st.expander("Show Details"):
                        st.write("**LM Hash:**", record["lmhash"])
                        st.write("**NT Hash:**", record["nthash"])
                        st.write("**RID:**", record["rid"])
