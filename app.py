import os
import streamlit as st
from src.fact_checker import FactChecker
import json

# Disable file watcher to prevent torch errors
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

# Initialize fact checker
fc = FactChecker()

# UI Configuration
st.set_page_config(
    page_title="🕵️‍♂️ LLM-Powered Fact Checker",
    page_icon="✅",
    layout="centered"
)

# App Header
st.title("🕵️‍♂️ LLM-Powered Fact Checker")
st.markdown("Verify news or social media claims using trusted facts and LLM reasoning.")

# Main Form
with st.form("fact_form"):
    input_text = st.text_area(
        "🔎 Enter a claim or news statement to verify:",
        height=150,
        placeholder="e.g. The Indian government has announced free electricity to all farmers starting July 2025.",
        key="claim_input"
    )
    
    submitted = st.form_submit_button(
        "Check Fact",
        use_container_width=True
    )

# Results Display
if submitted and input_text:
    with st.spinner("🔍 Analyzing and verifying..."):
        result = fc.check(input_text)
        
        for item in result:
            # Claim Display
            st.divider()
            st.markdown(f"### ✅ Claim: \n> *{item['claim']}*")
            
            # Verdict Display
            col1, col2 = st.columns([1, 4])
            with col1:
                verdict = item["verdict"].lower()
                if verdict == "true":
                    st.success("✅ Likely True", icon="✅")
                elif verdict == "false":
                    st.error("❌ Likely False", icon="❌")
                else:
                    st.warning("❓ Unverifiable", icon="⚠️")
            
            with col2:
                st.markdown(f"**Confidence:** {item.get('confidence', 'N/A')}")
            
            # Reasoning Display
            st.markdown("### 🧠 Reasoning")
            st.info(f"> {item.get('reasoning', 'No reasoning provided')}")
            
            # Evidence Display
            if item.get("evidence"):
                with st.expander("📚 View Supporting Evidence", expanded=False):
                    for i, fact in enumerate(item["evidence"], 1):
                        st.markdown(f"{i}. {fact}")
            else:
                st.markdown("> *No supporting evidence found*")
    
    # Footer
    st.divider()
    st.caption("This is a demo system powered by Google Gemini + RAG pipeline. Verdicts are AI-generated and should be verified by humans.")