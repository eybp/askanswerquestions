import tkinter as tk
from tkinter import ttk
import json

questions_file = 'questions.json'

class QuestionAnswerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Question Answering GUI")
        self.questions = []

        # Create and place widgets
        self.create_widgets()
        self.load_questions()

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="Select a question to answer:")
        self.question_label.pack()

        self.question_dropdown = ttk.Combobox(self.root)
        self.question_dropdown.pack()
        self.question_dropdown.bind("<<ComboboxSelected>>", self.on_question_selected)

        self.answer_label = tk.Label(self.root, text="Enter your answer:")
        self.answer_label.pack()

        self.answer_text = tk.Text(self.root, height=5, width=50)
        self.answer_text.pack()

        self.submit_button = tk.Button(self.root, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack()

    def load_questions(self):
        try:
            with open(questions_file, 'r') as f:
                content = f.read()
                if not content:
                    self.questions = []
                else:
                    self.questions = json.loads(content)
                    # Filter out unanswered questions
                    unanswered_questions = [q for q in self.questions if not q['answer']]
                    self.update_dropdown(unanswered_questions)
        except FileNotFoundError:
            self.questions = []
        except json.JSONDecodeError:
            self.questions = []

    def update_dropdown(self, questions):
        self.question_dropdown['values'] = [q['question'] for q in questions]
        if questions:
            self.question_dropdown.set(questions[0]['question'])

    def on_question_selected(self, event):
        selected_question = self.question_dropdown.get()
        for q in self.questions:
            if q['question'] == selected_question:
                self.answer_text.delete(1.0, tk.END)
                self.answer_text.insert(tk.END, q['answer'])
                break

    def submit_answer(self):
        selected_question = self.question_dropdown.get()
        answer = self.answer_text.get(1.0, tk.END).strip()

        for q in self.questions:
            if q['question'] == selected_question:
                q['answer'] = answer
                break

        with open(questions_file, 'w') as f:
            json.dump(self.questions, f)

        self.load_questions()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionAnswerGUI(root)
    root.mainloop()
