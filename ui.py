import streamlit as st
import requests
import time
import json

st.set_page_config(page_title="Social Support AI", layout="wide")

st.title("🤖 Govt Social Support AI Agent")
st.markdown("### Automated Eligibility & Risk Assessment System")

uploaded_file = st.file_uploader("Upload Applicant Documents (PDF/Image/Excel)", type=["pdf", "jpg", "png", "csv", "xlsx"])
user_name = st.text_input("Applicant Name", "Mohamed Hammad")

if st.button("Submit Application") and uploaded_file:
    with st.spinner("Uploading and starting AI Workflow..."):
        files = {"file": uploaded_file.getvalue()}
        data = {"user_name": user_name}
        
        try:
            response = requests.post("http://127.0.0.1:8000/submit-application", files={"file": uploaded_file}, data=data)
            
            if response.status_code == 200:
                task_id = response.json().get("task_id")
                st.success(f"Application Submitted! Tracking ID: {task_id}")
                
                status_placeholder = st.empty()
                result_placeholder = st.empty()
                
                while True:
                    status_res = requests.get(f"http://127.0.0.1:8000/result/{task_id}")
                    status_data = status_res.json()
                    
                    if status_data["status"] == "COMPLETED":
                        status_placeholder.success("✅ Analysis Complete!")
                        final_output = status_data["result"]["final_decision"]
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📋 Decision")
                            status = final_output.get("status", "UNKNOWN")
                            if status == "APPROVED":
                                st.success(f"DECISION: {status}")
                            elif status == "REJECTED":
                                st.error(f"DECISION: {status}")
                            else:
                                st.warning(f"DECISION: {status}")
                            
                            st.write(f"**Reason:** {final_output.get('reasoning')}")
                            st.metric("Financial Support", f"{final_output.get('financial_support_amount', 0)} AED")

                        with col2:
                            st.subheader("🚀 Enablement Plan")
                            st.info(final_output.get("enablement_recommendation"))

                        with st.expander("See Raw Extraction & Risk Data"):
                            st.json(status_data["result"])
                        
                        break
                    else:
                        status_placeholder.info("⏳ AI Agents are working... (OCR -> Extraction -> Risk ML -> RAG -> Decision)")
                        time.sleep(2)
            else:
                st.error("Failed to submit application.")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")