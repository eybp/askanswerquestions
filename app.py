from flask import Flask, request, jsonify, render_template
import json
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
questions_file = 'questions.json'

# Ensure the questions file exists
if not os.path.exists(questions_file):
    with open(questions_file, 'w') as f:
        f.write('[]')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_question', methods=['POST'])
def submit_question():
    app.logger.debug('Received POST request to /submit_question')
    question = request.form.get('question')
    if question:
        with open(questions_file, 'r+') as f:
            questions = json.load(f)
            questions.append({"question": question, "answer": ""})
            f.seek(0)
            json.dump(questions, f)
        app.logger.debug('Question added successfully')
        return jsonify({"success": True})
    app.logger.debug('Failed to add question')
    return jsonify({"success": False})

@app.route('/fetch_questions')
def fetch_questions():
    try:
        with open(questions_file, 'r') as f:
            content = f.read()
            if not content:
                questions = []
            else:
                questions = json.loads(content)
                # Filter out unanswered questions
                questions = [q for q in questions if q['answer']]
    except FileNotFoundError:
        questions = []
    except json.JSONDecodeError:
        questions = []
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True)
