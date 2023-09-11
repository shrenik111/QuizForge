import streamlit as st
import openai
import json

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
# openai.api_key = st.secrets["OPENAPIKEY"]




def main():
    st.title("OpenAI Streamlit App")

    # Get the topic input from the user
    topic = st.text_input("Please choose topic:")

    number_of_ques = st.selectbox(
    'Number of questions?',
    ('1', '2', '3', '4', '5'))

    number_of_options = st.selectbox(
    'Number of Options?',
    ('2', '3', '4', '5'))

    difficulty_level = st.selectbox(
    'Difficulty of the quiz?',
    ('Easy', 'Medium', 'Hard', 'Expert'))
    if "questions_data" not in st.session_state:
        st.session_state['questions_data'] = []
        st.session_state["total_questions"] = 0
    user_score = 0
    correct_ans_arr = []

    user_answers = {}  # Store user answers
    questions = {}
    # Create a button to trigger the response generation
    if st.button("Generate Response"):
        if topic:
            # Call the generate_response function to get the output
            response = generate_response(topic, number_of_ques, number_of_options, difficulty_level)
            questions = json.loads(response)
            st.session_state['questions_data'] = questions
            st.session_state["total_questions"] = len(questions)

    for idx, question_data in enumerate(st.session_state['questions_data']):
        question = question_data["question"]
        options = question_data["options"]
        correct_ans_arr.append(question_data["correct_option"])
        st.write(f"**Question {idx+1}/{st.session_state['total_questions']}:** {question}")


        
    st.write(st.session_state)
                
            
if __name__ == "__main__":

    main()

