import streamlit as st
import os
import shutil
from page_details import module_page  # your existing function
import re
ICON = "/code/images/MULTIVOL_LOGO.png"
ICON_HEADER = "/code/images/multivol_header.png"
ICON_FAVICON = "/code/images/multivol_favicon.png"
st.set_page_config(layout="wide",page_title='MultiVol',page_icon=ICON_FAVICON)
base_path = "../shared_volume"
def get_subdirectories(path):
    try:
        return [f.name for f in os.scandir(path) if f.is_dir()]
    except Exception as e:
        st.error(str(e))
        return []

def clean_string_for_module_title(input_str):
    # Step 1: Remove 'vol2_' and 'vol3'
    cleaned = input_str.replace("vol2_", "").replace("vol3", "").replace("windows","")
    
    # Step 2: Extract only words containing a-z (case-insensitive)
    words = re.findall(r'[a-zA-Z]+', cleaned)
    
    # Step 3: Deduplicate case-insensitively, preserving first occurrence
    seen = set()
    unique_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word not in seen:
            seen.add(lower_word)
            unique_words.append(lower_word)  # You can use word instead if you want original case
    
    return ' '.join(unique_words)

# Session for selected module
if "selected_page" not in st.session_state:
    st.session_state.selected_page = None

# Sidebar UI
with st.sidebar:
    st.header("Navigation")

    # 🗑️ Folder Management Section
    with st.expander("🗑️ Manage Folders", expanded=False):
        all_folders = get_subdirectories(base_path)
        folder_to_delete = st.selectbox("Select folder to delete", all_folders)

        if st.button("❌ Delete Selected Folder"):
            folder_path = os.path.join(base_path, folder_to_delete)
            try:
                shutil.rmtree(folder_path)
                st.success(f"Deleted folder '{folder_to_delete}'")
                st.rerun()  # Refresh after deletion
            except Exception as e:
                st.error(f"Failed to delete folder: {e}")

    # Navigation Expanders
    for dump_name in get_subdirectories(base_path):
        with st.expander(f"📁 {dump_name}", expanded=False):
            dump_path = os.path.join(base_path, dump_name)
            for module_name in get_subdirectories(dump_path):
                url_path = f"{dump_name}_{module_name}".lower().replace(" ", "_")
                st.session_state.setdefault("page_functions", {})[url_path] = module_page(dump_name, module_name)
                module_title = clean_string_for_module_title(module_name)
                if st.button(f"{module_title}", key=url_path):
                    st.session_state.selected_page = url_path

# Load selected page
page_functions = st.session_state.get("page_functions", {})
selected_page = st.session_state.selected_page
if selected_page and selected_page in page_functions:
    page_functions[selected_page]()
else:
    st.title("MultiVol By BobNewz & Sp00kySkelet0n")
    st.write("📂 **Select a module from the sidebar**")
    #st.divider()
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image(ICON,width=550)

    with col3:
        st.write("")

full_url = os.getenv("FULL_URL")
if full_url:
    st.logo(image=ICON_HEADER,size="large",link=full_url)
else:
    st.logo(image=ICON_HEADER,size="large")