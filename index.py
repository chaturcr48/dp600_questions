from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open('questions.json', 'r') as file:
    questions_data = json.load(file)

@app.route('/')
def quiz():
    import random
    random.shuffle(questions_data['questions'])
    return render_template('quiz.html', questions=questions_data['questions'], length=len(questions_data['questions']))

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    score = 0
    total_questions = len(questions_data['questions'])
    print(total_questions)
    user_answers = {}
    for question in questions_data['questions']:
        if question['id']+"[]" in request.form:
            user_answers[question['id']] = request.form.getlist(question['id']+"[]")
        else:
            user_answers[question['id']] = [request.form[question['id']]]
    
    for question in questions_data['questions']:
        if question['id'] in user_answers:
            user_selected = set(user_answers[question['id']])
            # print(user_selected)
            correct_answers = set(question.get('correct_answers', [question.get('answer')]))
            # print(correct_answers)
            if user_selected == correct_answers:
                score += 1
    
    return render_template('score.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
