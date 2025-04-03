import streamlit as st
import json
import random
from datetime import datetime

st.set_page_config(
    page_title="QuizGenius - Python Quiz",
    page_icon="🧠",
    layout="wide",
)
# Load questions from JSON file
def load_questions():
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: questions.json file not found!")
        return []
    except json.JSONDecodeError:
        st.error("Error: Invalid JSON format in questions.json!")
        return []

questions = load_questions()

# Initialize session state
def initialize_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.start_time = None
        st.session_state.user_answers = []
        st.session_state.show_results = False
        st.session_state.selected_option = None
        st.session_state.questions = questions.copy()
        random.shuffle(st.session_state.questions)

initialize_state()

def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.start_time = datetime.now()
    st.session_state.current_question = 0
    st.session_state.selected_option = None
    st.session_state.user_answers = []
    st.session_state.score = 0
    st.session_state.show_results = False
    st.session_state.questions = questions.copy()
    random.shuffle(st.session_state.questions)

def show_question():
    q = st.session_state.questions[st.session_state.current_question]
    
    # Question header with progress
    st.progress((st.session_state.current_question + 1) / len(st.session_state.questions))
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
    st.markdown(f"#### {q['question']}")
    
    options = q["options"]
    letters = ['A', 'B', 'C', 'D'][:len(options)]
    
    # Show radio buttons for answer selection
    selected_option = st.radio(
        "Select your answer:",
        options,
        format_func=lambda x: f"{letters[options.index(x)]}. {x}",
        index=None
    )
    
    st.session_state.selected_option = selected_option

    if st.button("Submit Answer"):
        if selected_option is not None:
            is_correct = selected_option == q["answer"]
            st.session_state.user_answers.append({
                "question": q['question'],
                "selected": selected_option,
                "correct": q['answer'],
                "is_correct": is_correct
            })
            if is_correct:
                st.session_state.score += 1
            
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                st.session_state.current_question += 1
            else:
                st.session_state.show_results = True
            
            st.rerun()
        else:
            st.warning("⚠️ Please select an answer before submitting!")

def show_results():
    time_taken = datetime.now() - st.session_state.start_time
    minutes, seconds = divmod(time_taken.seconds, 60)
    
    st.balloons()
    st.success("### 🎉 Quiz Completed!")
    st.markdown(f"""
    **Your Score:** {st.session_state.score}/{len(st.session_state.questions)}  
    **Percentage:** {(st.session_state.score/len(st.session_state.questions))*100:.1f}%  
    **Time Taken:** {minutes}m {seconds}s
    """)
    
    with st.expander("📝 View Detailed Results"):
        for i, answer in enumerate(st.session_state.user_answers):
            st.markdown(f"#### Q{i+1}: {answer['question']}")
            if answer['selected']:
                status = "✅" if answer['is_correct'] else "❌"
                st.write(f"{status} Your answer: {answer['selected']}")
                if not answer['is_correct']:
                    st.write(f"Correct answer: {answer['correct']}")
            else:
                st.write("⏭️ You skipped this question")
                st.write(f"Correct answer: {answer['correct']}")
            st.markdown("---")
    
    if st.button("🔄 Restart Quiz"):
        start_quiz()
        st.rerun()

# Main App
st.title("QuizGenius - Test Your Knowledge Like a Pro! 🧠")
st.markdown("QuizGenius is an interactive and engaging quiz app designed to challenge and enhance your knowledge in Python. Whether you’re a beginner or a pro, this app helps you test your skills and track your progress efficiently.")

if not st.session_state.quiz_started:
    st.markdown(f"""
    ### Quiz Features:
    - 📊 {len(questions)} multiple-choice questions
    - ⏱️ Timed completion tracking
    - 📝 Detailed answer review
    - 📈 Score percentage calculation
    """)
    if st.button("🚀 Start Quiz", type="primary"):
        start_quiz()
        st.rerun()
else:
    if st.session_state.show_results:
        show_results()
    else:
        show_question()

with st.sidebar:
    st.header("Quiz Info")
    if st.session_state.quiz_started and not st.session_state.show_results:
        st.write(f"**Progress:** {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
        st.write(f"**Score:** {st.session_state.score}")
    st.markdown("---")
    st.markdown("""
   **How to play:**
    1. Read each question carefully
    2. Select your answer
    3. Click Submit to confirm your answer
    4. Review your score and answers at the end
    """)
    if st.session_state.quiz_started and not st.session_state.show_results:
        if st.button("🔴 End Quiz Early"):
            st.session_state.show_results = True
            st.rerun()
    # footer

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center;">
    <small>Built with ❤️ by Dua Fatima</small><br>
    <small>Copyright © 2025- All Rights Reserved</small>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <small>Built with ❤️ by Dua Fatima</small><br>
    <small>Copyright © 2025- All Rights Reserved</small>
</div>
""", unsafe_allow_html=True)
