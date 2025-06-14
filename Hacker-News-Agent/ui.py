import streamlit as st
from main import Article, hn_team
st.set_page_config(page_title="HackerNews Article Generator", layout="wide")
st.title("🧠 HackerNews Intelligence Synthesizer")

st.markdown("Enter a topic ")

query = st.text_input(
    "Query", value="Write an article about the top 2 stories on hackernews"
)

if st.button("Generate Article"):
    with st.spinner("🧠 Thinking..."):
        try:
            article = hn_team.run(query )

            # st.subheader("📝 Title")
            # st.markdown(f"**{article.title}**")

            st.subheader("📚 Response")
            st.markdown(article.content)
            # st.write_stream(hn_team.run(query, stream=True))

            # st.subheader("🔗 Reference Links")
            # for link in article.reference_links:
            #     st.markdown(f"- [{link}]({link})")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
