import streamlit as st
import openai
import json

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = st.secrets["OPENAPIKEY"]


def generate_response(topic, no_of_ques, no_of_options, diff_level):
    # Number of ques, options number, difficulty level
    json_format = [
        {
                "question":  "sample question1 ?",
                "options": [
                    "answer option 1", 
                "correct answer option 2",
                    "answer option 3",
                    "answer option 4"
                ],
                "correct_option": 1,
                },

                {
                "question":  "sample question2?",
                "options": [
                    "answer option 1",
                    "answer option 2",
                    "correct answer option 3",
                    "answer option 4"
                ],
                "correct_option": 2
                }
                ]
    my_prompt = "Generate a {0} level quiz for the topic: {1}, {2} questions {3} options each, in pure JSON format like {4}".format(diff_level, topic, no_of_ques, no_of_options,str(json_format))
    print("Its here ")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": my_prompt}],
            temperature=0,
            max_tokens=3000
        )
        ans = response['choices'][0].message
        
        return ans["content"]

    except Exception as e:
        return f"Error: {e}"


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

        user_answer = st.selectbox("Choose an option:", options)
        
        st.session_state[f"Q{int(idx) + 1}"] = user_answer
        st.session_state[f"A{int(idx) + 1}"] = question_data["correct_option"]

    if st.button("Submit Quiz"):
        
        st.write(f"Your score: {user_score}/{st.session_state['total_questions']}")
        st.write("Your answers:", user_answers)
        
    st.write(st.session_state)
                
            
if __name__ == "__main__":

    main()

