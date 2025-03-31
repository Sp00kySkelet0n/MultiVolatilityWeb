import streamlit as st
import pandas as pd
import json
from st_aggrid import StAggridTheme, AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

# Load JSON data
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Template to render any JSON list of dicts
def render_json_table(json_data, title="Table Viewer", search_keys=None, update_on=None):
    st.title(title)

    # Convert to DataFrame
    df = pd.DataFrame(json_data)
    custom_theme = (
        StAggridTheme(base="quartz")
        .withParams(
            fontSize=13,
            rowBorder=False,
            backgroundColor="#FFFFFF"
        )
        .withParts('iconSetAlpine', 'colorSchemeDark')
    )
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, autoHeight=False, wrapText=False,filter=True)
    grid_options = gb.build()

    AgGrid(
        df,
        gridOptions=grid_options,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        theme=custom_theme,
        fit_columns_on_grid_load=True,
        height=700,
        editable=True,
        update_on=update_on or [],
    )

# Main entry point
def main(dump_name, module_name):
    if "vol2" in module_name:
        module_title = module_name.strip("vol2_")
    elif "vol3" in module_name:
        module_title = module_name.strip("vol3_")
    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    json_data = load_json(json_file_path)

    # If structured like Volatility output
    if isinstance(json_data, dict) and "rows" in json_data and "columns" in json_data:
        df = pd.DataFrame(json_data["rows"], columns=json_data["columns"])
        render_json_table(df.to_dict(orient="records"), title=f"{module_title} Output")
    # If it's already a flat list of dicts
    elif isinstance(json_data, list):
        render_json_table(json_data, title=f"{module_title} Output")
    else:
        st.error("Unsupported JSON structure.")
