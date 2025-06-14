# streamlit_app.py
import streamlit as st
from startup_idea_val_agent import graph

# Replace 'your_module' with the actual name of your file/module
from langchain_core.messages import AIMessage
# import markdown

# --- Streamlit UI ---

st.set_page_config(page_title="Startup Intelligence Agent", page_icon="🚀")

st.title("🚀 Startup Intelligence Agent")
st.subheader("End-to-end analysis and reporting for your startup idea")
st.markdown(
    """
This assistant refines your startup idea, performs market research, competitor analysis,
and produces a professional report in markdown format.
"""
)

st.write(
    "E.g., A marketplace for Christmas Ornaments made from leather")
# --- Input Area ---
startup_idea = st.text_area(
    "💡 Enter your startup idea below:",
    placeholder="E.g., A marketplace for Christmas Ornaments made from leather",
    height=75,
)

if st.button("Generate Report"):
    if not startup_idea.strip():
        st.warning("🚨 Please enter a startup idea to proceed.")
    else:
        with st.spinner(
            "🛠️ Generating your startup report... This may take a moment ⏳"
        ):
            try:
                state = graph.invoke({"startup_idea": startup_idea})
                final_report = state.get("final_report", "")

                st.success("✅ Report generated successfully!")

                st.markdown("---")
                st.markdown(
                    """
                    <div style="font-size: 26px; font-weight: 700; color: #333;">
                        📄 Final Startup Report
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

                # Styled Markdown container
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; font-size: 16px; line-height: 1.6; color: #222;">
                        {final_report}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"❌ An error occurred while generating the report: {str(e)}")
