import streamlit as st
import httpx
from datetime import date

st.set_page_config(page_title="Legal Docket Deadline Calculator", page_icon="📅")

st.title("📅 Legal Docket Deadline Calculator")

# --- Form input ---
with st.form("deadline_form"):
    st.subheader("Enter Case Information")

    jurisdiction = st.selectbox("Jurisdiction", ["California", "Virginia"])
    case_type = st.selectbox("Case Type", ["Civil"])

    # Trigger event options per jurisdiction
    trigger_event_options = {
        "California": ["Complaint Filed"],
        "Virginia": ["Complaint Filed", "Answer Filed"]
    }

    trigger_event = st.selectbox(
        "Trigger Event",
        trigger_event_options.get(jurisdiction, [])
    )

    trigger_date = st.date_input("Trigger Date", value=date.today())
    submitted = st.form_submit_button("Generate Deadlines")

# --- On submit ---
if submitted:
    with st.spinner("Calculating..."):
        payload = {
            "jurisdiction": jurisdiction,
            "case_type": case_type,
            "trigger_event": trigger_event,
            "trigger_date": str(trigger_date)
        }

        try:
            response = httpx.post("http://localhost:8000/generate-deadlines/", json=payload)
            response.raise_for_status()

            deadlines = response.json()["deadlines"]

            if deadlines:
                st.success("✅ Deadlines generated!")
                for d in deadlines:
                    st.write(f"📌 **{d['name']}** → `{d['due_date']}` (_{d['rule_applied']}_)")
            else:
                st.warning("⚠️ No matching rules found for the selected event.")

        except Exception as e:
            st.error(f"❌ Failed to generate deadlines: {e}")
