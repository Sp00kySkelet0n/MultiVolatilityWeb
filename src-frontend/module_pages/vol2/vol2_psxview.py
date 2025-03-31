import streamlit as st
import pandas as pd
import json

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name, module_name):
    

    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(json_data["rows"], columns=json_data["columns"])

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    search_term = st.sidebar.text_input("Search by Process Name")
    hide_exited = st.sidebar.checkbox("Hide Exited Processes (with ExitTime)", value=False)

    filtered_df = df.copy()
    if search_term:
        filtered_df = filtered_df[filtered_df["Name"].str.contains(search_term, case=False, na=False)]

    if hide_exited:
        filtered_df = filtered_df[filtered_df["ExitTime"].astype(str).str.strip() == ""]

    # --- Main Page ---
    st.title("Process Summary - psxview")
    st.write("Displays a cross-view of running processes from multiple scanning techniques.")

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.caption("Tip: Use the filters in the sidebar to refine the list. Rows showing 'False' in any column might indicate hidden or suspicious processes.")

if __name__ == "__main__":
    main("sample", "psxview")