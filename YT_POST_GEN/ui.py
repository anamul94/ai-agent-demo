import streamlit as st
from agnets import graph  # Import your graph instance
from agno_agent import agent

# App title
st.title("YouTube Blog Generator")
st.subheader("Turn YouTube Videos into Blog Posts")

# Input field for YouTube URL
url = st.text_input(
    "Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=..."
)

# Submit button
if st.button("Generate Blog"):
    if url:
        with st.spinner("Processing video..."):
            try:
                # Invoke your graph with the URL
                # result = graph.invoke({"url": url})
                result = agent.run(url)

                # Display results
                st.subheader("Blog")
                # st.write(result.get("response", "No response found"))
                st.write(result.content)
                
                
                st.subheader("Metrics")
                st.json(result.metrics)

                # Show additional metadata if available
                # if "metrics" in result:
                #     with st.expander("Detailed Metadata"):
                #         st.json(result)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a YouTube URL")
