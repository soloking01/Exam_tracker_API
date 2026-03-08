import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Exam & Job Tracker", page_icon="🎯", layout="wide")
st.title(" Application & Exam Tracker Dashboard")
st.markdown("Track your government exams, software engineering applications, and interview schedules in one place.")

try:
    metrics_response = requests.get(f"{API_URL}/items")
    all_data = metrics_response.json() if metrics_response.status_code == 200 else []
except:
    all_data = []
    st.error("Cannot connect to backend server. Is FastAPI running?")

if all_data:
    col1, col2, col3, col4 = st.columns(4)
    total_apps = len(all_data)
    
    gov_exams = len([d for d in all_data if str(d.get("category")).lower() == "government exam"])
    sde_roles = len([d for d in all_data if str(d.get("category")).lower() == "software engineer role"])
    admit_cards = len([d for d in all_data if str(d.get("status")).lower() == "admit card received"])
    
    col1.metric("Total Tracked", total_apps)
    col2.metric("Govt Exams", gov_exams)
    col3.metric("SDE Roles", sde_roles)
    col4.metric("Admit Cards Ready", admit_cards)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 View & Search", "➕ Add New Target", "✏️ Update Entry", "🗑️ Delete Entry"])

with tab1:
    st.subheader("Search & Filter Applications")
    
    c1, c2 = st.columns(2)
    with c1:
        filter_category = st.selectbox("Filter by Category", ["All", "Government Exam", "Software Engineer Role", "Other"], key="f_cat")
    with c2:
        filter_status = st.selectbox("Filter by Status", ["All", "Not Applied", "Applied", "Preparing", "Admit Card Received", "Interview Scheduled", "Completed", "Rejected"], key="f_stat")
    
    query_params = {}
    if filter_category != "All": query_params["category"] = filter_category
    if filter_status != "All": query_params["status"] = filter_status
    
    if st.button("🔄 Refresh Data"):
        st.rerun()

    try:
        res = requests.get(f"{API_URL}/items", params=query_params)
        if res.status_code == 200 and res.json():
            df = pd.DataFrame(res.json())
            df = df[["id", "title", "category", "status", "notes"]]
            # Streamlit's new dataframe UI is very sleek
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No applications match your current filters. Try changing them or add a new one!")
    except:
        pass

with tab2:
    st.subheader("Add a New Target")
    with st.form("add_form", clear_on_submit=True):
        new_title = st.text_input("Title (e.g., SSC CGL, Backend Developer Intern)")
        new_category = st.selectbox("Category", ["Government Exam", "Software Engineer Role", "Other"])
        new_status = st.selectbox("Status", ["Not Applied", "Applied", "Preparing", "Admit Card Received", "Interview Scheduled", "Completed", "Rejected"])
        new_notes = st.text_area("Notes (Optional)")
        
        if st.form_submit_button("Save to Database"):
            if not new_title.strip():
                st.error("Please enter a title.")
            else:
                payload = {"title": new_title, "category": new_category, "status": new_status, "notes": new_notes}
                r = requests.post(f"{API_URL}/items", json=payload)
                if r.status_code == 200:
                    st.success(f"Successfully added '{new_title}'!")
                    st.rerun()

with tab3:
    st.subheader("Update an Existing Record")
    st.info("Look up the ID of the record in the 'View' tab, then enter its new details here.")
    
    with st.form("update_form"):
        upd_id = st.number_input("Record ID to Update", min_value=1, step=1)
        upd_title = st.text_input("Updated Title")
        upd_category = st.selectbox("Updated Category", ["Government Exam", "Software Engineer Role", "Other"], key="u_cat")
        upd_status = st.selectbox("Updated Status", ["Not Applied", "Applied", "Preparing", "Admit Card Received", "Interview Scheduled", "Completed", "Rejected"], key="u_stat")
        upd_notes = st.text_area("Updated Notes (Optional)", key="u_notes")
        
        if st.form_submit_button("Update Record"):
            if not upd_title.strip():
                st.error("Please enter the updated title.")
            else:
                payload = {"title": upd_title, "category": upd_category, "status": upd_status, "notes": upd_notes}
                r = requests.put(f"{API_URL}/items/{upd_id}", json=payload)
                if r.status_code == 200:
                    st.success(f"Record {upd_id} updated successfully!")
                    st.rerun()
                elif r.status_code == 404:
                    st.error(f"Record with ID {upd_id} not found.")

with tab4:
    st.subheader("Delete a Record")
    st.warning("Warning: This action permanently removes the entry from the database.")
    
    col_del1, col_del2 = st.columns([1, 3])
    with col_del1:
        del_id = st.number_input("Enter ID to Delete", min_value=1, step=1, key="del_id")
    with col_del2:
        st.write("") 
        st.write("")
        if st.button("🗑️ Delete Record"):
            r = requests.delete(f"{API_URL}/items/{del_id}")
            if r.status_code == 200:
                st.success(f"Record {del_id} deleted successfully.")
                st.rerun()
            elif r.status_code == 404:
                st.error(f"Record with ID {del_id} not found.")