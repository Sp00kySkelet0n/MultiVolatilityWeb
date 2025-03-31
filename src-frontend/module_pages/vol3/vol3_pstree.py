import streamlit as st
import json
import os

# Function to load JSON data from file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Recursive function to build markdown tree
def render_process_tree(process, indent=0):
    indent_str = "    " * indent
    line = f"{indent_str}- **{process['ImageFileName']}** (PID: {process['PID']}, PPID: {process['PPID']})"
    lines = [line]
    for child in process.get("__children", []):
        lines.extend(render_process_tree(child, indent + 1))
    return lines

def main(dump_name, module_name):

    json_file_path = f"/shared_volume/{dump_name}/{module_name}/output.json"
    if not os.path.exists(json_file_path):
        st.error("File not found: " + json_file_path)
        return

    json_data = load_json(json_file_path)

    st.title("Process Tree Viewer")
    st.markdown("Browse a hierarchical view of the process tree.")

    # Display each root process
    for process in json_data:
        tree_lines = render_process_tree(process)
        tree_md = "\n".join(tree_lines)
        st.markdown(tree_md)
