import streamlit as st
from main import nutrition_agent

st.set_page_config(page_title="NutriPlan Pro", layout="wide")
st.title("🥗 NutriPlan Pro")

st.markdown(
    "A sophisticated nutritional planning assistant that creates personalized meal plans and dietary recommendations. "
    "NutriPlan Pro analyzes individual health profiles, calculates precise nutritional requirements, and designs "
    "customized meal plans considering regional food availability, health conditions, and dietary preferences."
)

query = st.text_area(
    "🍽️ Nutrition Plan Request",
    value=(
        "I need a nutrition plan for a 35-year-old male, 175cm, 82kg, moderately active with type 2 diabetes. "
        "He lives in southern India and is vegetarian. He wants to lose weight gradually while managing his blood sugar. "
        "Please consider locally available foods and traditional cooking methods."
    ),
    height=100,
)

if st.button("Generate Nutrition Plan"):
    with st.spinner("🧠 Analyzing nutritional needs..."):
        try:
            nutrition_plan = nutrition_agent.run(query)

            st.subheader("📝 Personalized Nutrition Plan")
            st.markdown(nutrition_plan.content)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add sidebar with helpful tips
with st.sidebar:
    st.header("How to Get the Best Results")
    st.markdown("""
    ### Include in your request:
    - Age, gender, height, and weight
    - Activity level and exercise routine
    - Health conditions or concerns
    - Dietary preferences or restrictions
    - Location (for regional food availability)
    - Specific goals (weight loss, muscle gain, etc.)
    - Any food allergies or intolerances
    """)
    
    st.header("Example Requests")
    example1 = "Create a nutrition plan for weight loss for a 28-year-old woman in Mexico City who is moderately active, 165cm, 75kg, and prefers low-carb options"
    example2 = "Design a meal plan for a 60-year-old with kidney disease (CKD stage 3) in Japan who needs to limit protein and mineral intake"
    example3 = "Develop a high-protein nutrition strategy for a marathon runner during training in Kenya, male, 30 years old, 70kg, 180cm"
    
    if st.button("Example 1"):
        st.session_state.example_query = example1
        
    if st.button("Example 2"):
        st.session_state.example_query = example2
        
    if st.button("Example 3"):
        st.session_state.example_query = example3
        
    # Display citation and disclaimer
    st.markdown("---")
    st.caption("**Disclaimer:** This tool provides nutritional guidance based on general principles and should not replace professional medical advice. Always consult with healthcare providers before making significant dietary changes.")