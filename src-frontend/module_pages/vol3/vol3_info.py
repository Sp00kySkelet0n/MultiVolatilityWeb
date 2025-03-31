import streamlit as st
import pandas as pd
import json

# Load JSON data from file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Streamlit UI
def main(dump_name,module_name):
    
    
    # Load JSON data
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)
    
    # Convert JSON data to a DataFrame
    df = pd.DataFrame(json_data)
    
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    search_variable = st.sidebar.text_input("Search Variable Name")
    search_value = st.sidebar.text_input("Search Value")
    
    # Apply filters to the DataFrame
    filtered_df = df.copy()
    if search_variable:
        filtered_df = filtered_df[filtered_df["Variable"].str.contains(search_variable, case=False, na=False)]
    if search_value:
        filtered_df = filtered_df[filtered_df["Value"].str.contains(search_value, case=False, na=False)]
    
    st.title("Windows System Info Explorer")
    st.write("Explore Windows system information using the filters in the sidebar. The metrics below display individual info items.")
    
    # --- Card View using st.metric ---
    records = filtered_df.to_dict(orient="records")
    num_cols = 3  # Change this number to adjust how many metrics per row
    for i in range(0, len(records), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(records):
                record = records[i + j]
                # st.metric displays the Variable as the label and the Value as the main value
                with col:
                    st.metric(label=record["Variable"], value=record["Value"])

if __name__ == "__main__":
    main()
