import streamlit as st
from agnets import graph  # Import your graph instance

# App title
st.title("YouTube Content Summarizer")

# Input field for YouTube URL
url = st.text_input(
    "Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=..."
)

# Submit button
if st.button("Summarize"):
    if url:
        with st.spinner("Processing video..."):
            try:
                # Invoke your graph with the URL
                result = graph.invoke({"url": url})

                # Display results
                st.subheader("Summarized Results")
                st.write(result.get("response", "No response found"))

                # Show additional metadata if available
                if "metadata" in result:
                    with st.expander("Detailed Metadata"):
                        st.json(result["metadata"])

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a YouTube URL")
