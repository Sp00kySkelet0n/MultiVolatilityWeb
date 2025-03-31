import streamlit as st
import pandas as pd
import json

# Function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def main(dump_name,module_name):
    
    
    # Update with your actual file path
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)
    
    # Convert JSON data to a DataFrame
    df = pd.DataFrame(json_data)
    
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    search_user = st.sidebar.text_input("Search User")
    
    filtered_df = df.copy()
    if search_user:
        filtered_df = df[df["User"].str.contains(search_user, case=False, na=False)]
    
    st.title("User Accounts Explorer")
    st.write("Explore user account details. Click on 'Show Details' to reveal more information.")
    
    # --- Card View using st.metric and st.expander ---
    records = filtered_df.to_dict(orient="records")
    num_cols = 2  # Adjust the number of columns per row as desired
    
    for i in range(0, len(records), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(records):
                record = records[i + j]
                with col:
                    # Display the user name and RID using st.metric
                    st.metric(label=record["User"], value=f"RID: {record['rid']}")
                    # Expandable section to show additional details
                    with st.expander("Show Details"):
                        st.write("**LM Hash:**", record["lmhash"])
                        st.write("**NT Hash:**", record["nthash"])
                        st.write("**RID:**", record["rid"])
    
    # --- Complete Data Table at the Bottom ---
    st.write("### Complete Data Table")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.caption("Tip: Use the sidebar filter to refine the user list.")

if __name__ == "__main__":
    main()
