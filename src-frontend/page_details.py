import streamlit as st
import importlib

def module_page(dump_name, module_name):
    def page():
        try:
            if module_name.startswith("vol2_"):
                # Example: vol2_bash_output → module_pages.vol2.vol2_bash_output
                template_path = "module_pages.template.templating"
                mod_path = f"module_pages.vol2.{module_name}"
                try:
                    specific_module = importlib.import_module(mod_path)
                    specific_module_func = getattr(specific_module, "main")
                    specific_module_func(dump_name, module_name)
                except Exception as e:
                    templating_module = importlib.import_module(template_path)
                    templating_module_func = getattr(templating_module, "main")
                    templating_module_func(dump_name, module_name)

            elif module_name.startswith("vol3_") or module_name.startswith("vol3.windows"):
                # Example: vol3_windows.netstat.NetStat → module_pages.vol3.vol3_netstat
                parts = module_name.split(".")
                vol_ver = parts[0][:4]  # 'vol3'
                base_module = parts[1]  # e.g., 'netstat'
                mod_path = f"module_pages.{vol_ver}.{vol_ver}_{base_module}"
                template_path = "module_pages.template.templating"
                try:
                    specific_module = importlib.import_module(mod_path)
                    specific_module_func = getattr(specific_module, "main")
                    specific_module_func(dump_name, module_name)
                except:
                    templating_module = importlib.import_module(template_path)
                    templating_module_func = getattr(templating_module, "main")
                    templating_module_func(dump_name, module_name)
            else:
                st.warning("Unknown module format.")

        except ModuleNotFoundError as e:
            st.error(f"Module not found: {e}")
        except AttributeError:
            st.error("Main function not found in module.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

    return page
