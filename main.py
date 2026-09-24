import tkinter as tk
from tkinter import messagebox
import requests
import json
import threading

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:latest"


class AIStudyAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)
        self.root.configure(bg="#f8fafc")

        self.subject = "General Study"
        self.topic = "General"
        self.history = []
        self.busy = False

        self.subjects = {
            "🐍 Python": ["Variables", "Data Types", "Loops", "Functions", "Lists", "OOP"],
            "🧱 Data Structures": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Searching"],
            "🗄 DBMS": ["SQL", "ER Model", "Normalization", "Transactions", "Joins", "Data Warehouse"],
            "🌐 Computer Networks": ["OSI Model", "TCP/IP", "IP Addressing", "DNS", "HTTP", "Network Security"],
            "💻 Operating Systems": ["Processes", "Threads", "CPU Scheduling", "Deadlocks", "Memory", "File Systems"]
        }

        self.quiz_questions = []
        self.quiz_index = 0
        self.quiz_score = 0
        self.home()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, title):
        bar = tk.Frame(self.root, bg="#172554", height=65)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Button(
            bar, text="◀ Back", command=self.home,
            bg="#334155", fg="white", relief="flat",
            font=("Arial", 10, "bold"), padx=14
        ).pack(side="left", padx=10, pady=12)

        tk.Label(
            bar, text=title, bg="#172554", fg="white",
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=10)

        tk.Button(
            bar, text="🏠 Home", command=self.home,
            bg="#334155", fg="white", relief="flat",
            font=("Arial", 10, "bold"), padx=14
        ).pack(side="right", padx=10, pady=12)

    def home(self):
        if self.busy:
            return
        self.clear()

        top = tk.Frame(self.root, bg="#172554", height=75)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top, text="🎓 AI Study Assistant",
            bg="#172554", fg="white",
            font=("Arial", 22, "bold")
        ).pack(side="left", padx=25)

        tk.Label(
            top, text="Gemma 3 • Ollama",
            bg="#172554", fg="#bfdbfe",
            font=("Arial", 10)
        ).pack(side="right", padx=25)

        tk.Label(
            self.root, text="Welcome MJ! 👋",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 27, "bold")
        ).pack(pady=(25, 2))

        tk.Label(
            self.root, text="Learn • Practice • Ask AI",
            bg="#f8fafc", fg="#64748b",
            font=("Arial", 13)
        ).pack(pady=(0, 20))

        main = tk.Frame(self.root, bg="#f8fafc")
        main.pack(fill="both", expand=True, padx=35)

        left = tk.Frame(main, bg="#f8fafc")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            left, text="📚 Subjects",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 8))

        for subject in self.subjects:
            tk.Button(
                left, text=subject,
                command=lambda s=subject: self.subject_page(s),
                bg="white", fg="#0f172a",
                activebackground="#dbeafe",
                relief="flat", font=("Arial", 12, "bold"),
                anchor="w", padx=18, pady=12
            ).pack(fill="x", pady=4)

        right = tk.Frame(main, bg="#f8fafc")
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(
            right, text="🛠 Study Tools",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 17, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.tool_button(right, "🤖 AI Chat", "Ask Gemma 3 anything", self.chat_page)
        self.tool_button(right, "📝 Notes", "Write and save your study notes", self.notes_page)
        self.tool_button(right, "🧠 AI Quiz", "Generate questions using Gemma 3", self.quiz_page)
        self.tool_button(right, "🔍 Search", "Search subjects and topics", self.search_page)

    def tool_button(self, parent, title, subtitle, command):
        frame = tk.Frame(parent, bg="white", highlightbackground="#dbeafe", highlightthickness=1)
        frame.pack(fill="x", pady=7)

        tk.Label(
            frame, text=title, bg="white", fg="#0f172a",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 2))

        tk.Label(
            frame, text=subtitle, bg="white", fg="#64748b",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)

        tk.Button(
            frame, text="Open →", command=command,
            bg="#2563eb", fg="white", relief="flat",
            font=("Arial", 10, "bold"), padx=18, pady=7
        ).pack(anchor="e", padx=15, pady=10)

    def subject_page(self, subject):
        self.subject = subject
        self.clear()
        self.header("📚 " + subject)

        tk.Label(
            self.root, text="Choose a Topic",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 5))

        box = tk.Frame(self.root, bg="#f8fafc")
        box.pack(fill="both", expand=True, padx=60)

        for topic in self.subjects[subject]:
            tk.Button(
                box, text="📖  " + topic,
                command=lambda t=topic: self.open_topic(t),
                anchor="w", bg="white", fg="#0f172a",
                activebackground="#dbeafe", relief="flat",
                font=("Arial", 12, "bold"), padx=18, pady=12
            ).pack(fill="x", pady=4)

    def open_topic(self, topic):
        self.topic = topic
        self.chat_page()
        self.entry.insert(0, "Explain " + topic + " in simple terms.")
        self.entry.focus()

    def notes_page(self):
        self.clear()
        self.header("📝 Study Notes")

        tk.Label(
            self.root, text="Write Your Study Notes",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 21, "bold")
        ).pack(pady=(20, 5))

        self.notes_text = tk.Text(
            self.root, bg="white", fg="#111827",
            font=("Arial", 12), wrap="word",
            relief="flat", padx=15, pady=15
        )
        self.notes_text.pack(fill="both", expand=True, padx=40, pady=10)

        bottom = tk.Frame(self.root, bg="#f8fafc")
        bottom.pack(fill="x", padx=40, pady=10)

        tk.Button(
            bottom, text="💾 Save Notes", command=self.save_notes,
            bg="#16a34a", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=20, pady=9
        ).pack(side="left")

        tk.Button(
            bottom, text="🗑 Clear",
            command=lambda: self.notes_text.delete("1.0", "end"),
            bg="#64748b", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=20, pady=9
        ).pack(side="right")

    def save_notes(self):
        content = self.notes_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Notes", "Please write something first.")
            return
        try:
            with open("study_notes.txt", "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Saved", "Notes saved successfully! ✅")
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def chat_page(self):
        self.clear()
        self.header("🤖 AI Chat")

        main = tk.Frame(self.root, bg="#f8fafc")
        main.pack(fill="both", expand=True, padx=12, pady=10)

        self.chat = tk.Text(
            main, bg="white", fg="#111827",
            font=("Arial", 12), wrap="word",
            relief="flat", padx=15, pady=15,
            state="disabled"
        )
        self.chat.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(main, command=self.chat.yview)
        scroll.pack(side="right", fill="y")
        self.chat.configure(yscrollcommand=scroll.set)

        if not self.history:
            self.write(
                "🤖 AI:\nHey MJ! 👋\n"
                "I'm your local AI Study Assistant.\n"
                "Ask me anything about your studies.\n\n"
            )
        else:
            for item in self.history:
                self.write(item)

        bottom = tk.Frame(self.root, bg="#e2e8f0", height=72)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        self.entry = tk.Entry(
            bottom, font=("Arial", 13),
            bg="white", fg="#111827", relief="flat"
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=12)
        self.entry.bind("<Return>", lambda event: self.ask())

        tk.Button(
            bottom, text="Clear", command=self.clear_chat,
            bg="#64748b", fg="white", relief="flat",
            font=("Arial", 10, "bold"), padx=12
        ).pack(side="right", padx=5, pady=12)

        self.send_button = tk.Button(
            bottom, text="SEND 🚀", command=self.ask,
            bg="#2563eb", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=22
        )
        self.send_button.pack(side="right", padx=8, pady=12)
        self.entry.focus()

    def write(self, text):
        if not hasattr(self, "chat"):
            return
        self.chat.config(state="normal")
        self.chat.insert("end", text)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def ask(self):
        if self.busy:
            return

        question = self.entry.get().strip()
        if not question:
            return

        self.entry.delete(0, "end")
        self.write("\n🧑 You:\n" + question + "\n\n🤖 AI:\n")

        self.busy = True
        self.send_button.config(state="disabled", text="Thinking...")
        self.entry.config(state="disabled")

        threading.Thread(
            target=self.ollama,
            args=(question,),
            daemon=True
        ).start()

    def ollama(self, question):
        prompt = f"""
You are MJ's personal AI Study Assistant.

Be friendly and helpful.
If MJ writes Telugu-English, reply naturally in Telugu-English.
If MJ writes English, reply in English.
Keep simple questions short.
For difficult topics, explain step by step.
For programming questions, give clean working code.

Subject: {self.subject}
Topic: {self.topic}
Question: {question}

Answer:
"""

        answer = ""

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "temperature": 0.2,
                        "num_ctx": 2048,
                        "num_predict": 450
                    }
                },
                stream=True,
                timeout=120
            )

            if response.status_code != 200:
                self.root.after(0, self.error, "Ollama error: " + str(response.status_code))
                return

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    part = data.get("response", "")
                    if part:
                        answer += part
                        self.root.after(0, self.write, part)
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue

            if answer.strip():
                self.history.append(
                    "🧑 You:\n" + question +
                    "\n\n🤖 AI:\n" + answer + "\n\n"
                )
                self.history = self.history[-6:]

        except requests.exceptions.ConnectionError:
            self.root.after(0, self.error, "❌ Ollama is not running.\nPlease start Ollama.")
        except requests.exceptions.Timeout:
            self.root.after(0, self.error, "⏳ AI took too long to respond.")
        except Exception as error:
            self.root.after(0, self.error, "❌ Error:\n" + str(error))
        finally:
            self.root.after(0, self.finished)

    def finished(self):
        self.busy = False

        if hasattr(self, "send_button"):
            self.send_button.config(state="normal", text="SEND 🚀")

        if hasattr(self, "entry"):
            self.entry.config(state="normal")
            self.entry.focus()

        self.write("\n\n")

    def error(self, message):
        self.write("\n\n" + message + "\n\n")

    def clear_chat(self):
        if self.busy:
            return
        self.history.clear()
        self.chat_page()

    def search_page(self):
        self.clear()
        self.header("🔍 Search")

        tk.Label(
            self.root, text="Search Subjects & Topics",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 10))

        search_frame = tk.Frame(self.root, bg="#f8fafc")
        search_frame.pack(fill="x", padx=50)

        self.search_entry = tk.Entry(
            search_frame, font=("Arial", 13),
            bg="white", fg="#111827", relief="flat"
        )
        self.search_entry.pack(
            side="left", fill="x", expand=True,
            ipady=10, padx=(0, 8)
        )
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

        tk.Button(
            search_frame, text="Search 🔍",
            command=self.perform_search,
            bg="#2563eb", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=20, pady=8
        ).pack(side="right")

        self.search_results = tk.Frame(self.root, bg="#f8fafc")
        self.search_results.pack(fill="both", expand=True, padx=50, pady=20)
        self.search_entry.focus()

    def perform_search(self):
        query = self.search_entry.get().strip().lower()

        for widget in self.search_results.winfo_children():
            widget.destroy()

        if not query:
            return

        found = False

        for subject in self.subjects:
            if query in subject.lower():
                found = True
                tk.Button(
                    self.search_results, text=subject + " →",
                    command=lambda s=subject: self.subject_page(s),
                    anchor="w", bg="white", fg="#0f172a",
                    relief="flat", font=("Arial", 12, "bold"),
                    padx=15, pady=12
                ).pack(fill="x", pady=4)

            for topic in self.subjects[subject]:
                if query in topic.lower():
                    found = True
                    tk.Button(
                        self.search_results,
                        text="📖 " + topic + " (" + subject + ")",
                        command=lambda s=subject, t=topic: self.open_search_topic(s, t),
                        anchor="w", bg="white", fg="#0f172a",
                        relief="flat", font=("Arial", 11),
                        padx=15, pady=10
                    ).pack(fill="x", pady=3)

        if not found:
            tk.Label(
                self.search_results, text="No results found 😕",
                bg="#f8fafc", fg="#64748b",
                font=("Arial", 13)
            ).pack(pady=30)

    def open_search_topic(self, subject, topic):
        self.subject = subject
        self.topic = topic
        self.chat_page()
        self.entry.insert(0, "Explain " + topic + " in simple terms.")
        self.entry.focus()

    # =====================================================
    # AI QUIZ
    # =====================================================

    def quiz_page(self):
        self.clear()
        self.header("🧠 AI Quiz")

        tk.Label(
            self.root, text="Choose Quiz Subject",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 23, "bold")
        ).pack(pady=(35, 10))

        tk.Label(
            self.root,
            text="Gemma 3 will generate fresh questions",
            bg="#f8fafc", fg="#64748b",
            font=("Arial", 12)
        ).pack(pady=(0, 20))

        box = tk.Frame(self.root, bg="#f8fafc")
        box.pack(fill="both", expand=True, padx=100)

        quiz_subjects = [
            ("🐍 Python", "Python"),
            ("🧱 Data Structures", "Data Structures"),
            ("🗄 DBMS", "DBMS"),
            ("🌐 Computer Networks", "Computer Networks"),
            ("💻 Operating Systems", "Operating Systems")
        ]

        for title, subject in quiz_subjects:
            tk.Button(
                box, text=title,
                command=lambda s=subject: self.quiz_topic_page(s),
                bg="white", fg="#0f172a",
                activebackground="#dbeafe",
                relief="flat", font=("Arial", 13, "bold"),
                pady=13
            ).pack(fill="x", pady=5)

    def quiz_topic_page(self, subject):
        self.clear()
        self.header("🧠 " + subject + " Quiz")
        self.quiz_selected_subject = subject

        tk.Label(
            self.root, text="Choose Topic",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 22, "bold")
        ).pack(pady=(30, 10))

        box = tk.Frame(self.root, bg="#f8fafc")
        box.pack(fill="both", expand=True, padx=80)

        for topic in self.subject_topics_for_quiz(subject):
            tk.Button(
                box, text="🧠 " + topic,
                command=lambda t=topic: self.generate_quiz(subject, t),
                bg="white", fg="#0f172a",
                activebackground="#dbeafe",
                relief="flat", font=("Arial", 12, "bold"),
                anchor="w", padx=18, pady=12
            ).pack(fill="x", pady=4)

    def subject_topics_for_quiz(self, subject):
        for key in self.subjects:
            clean_key = key[2:].strip()
            if clean_key == subject:
                return self.subjects[key]
        return []

    def generate_quiz(self, subject, topic):
        if self.busy:
            return

        self.quiz_subject = subject
        self.quiz_topic = topic
        self.clear()
        self.header("🤖 Generating AI Quiz")

        tk.Label(
            self.root,
            text="🧠 Gemma 3 is creating your questions...",
            bg="#f8fafc", fg="#2563eb",
            font=("Arial", 16, "bold")
        ).pack(pady=80)

        tk.Label(
            self.root,
            text="Subject: " + subject + "\nTopic: " + topic,
            bg="#f8fafc", fg="#64748b",
            font=("Arial", 12)
        ).pack(pady=10)

        self.busy = True

        threading.Thread(
            target=self.generate_quiz_thread,
            args=(subject, topic),
            daemon=True
        ).start()

    def generate_quiz_thread(self, subject, topic):
        prompt = f"""
Create a multiple-choice quiz for a college CSE student.

Subject: {subject}
Topic: {topic}

Create exactly 5 questions.
Every question must have exactly 4 options.
Only one option must be correct.

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option text"
    }}
  ]
}}

Do not add markdown or explanations.
"""

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": 0.2,
                        "num_ctx": 4096,
                        "num_predict": 1400
                    }
                },
                timeout=180
            )

            if response.status_code != 200:
                self.root.after(
                    0, self.quiz_generation_error,
                    "Ollama error: " + str(response.status_code)
                )
                return

            data = response.json()
            raw_answer = data.get("response", "")
            quiz = self.extract_quiz_json(raw_answer)
            quiz = self.validate_quiz(quiz)

            if not quiz:
                self.root.after(
                    0, self.quiz_generation_error,
                    "AI returned an invalid quiz format."
                )
                return

            self.root.after(0, self.quiz_ready, quiz)

        except requests.exceptions.ConnectionError:
            self.root.after(
                0, self.quiz_generation_error,
                "❌ Ollama is not running.\n\nStart Ollama and try again."
            )
        except requests.exceptions.Timeout:
            self.root.after(
                0, self.quiz_generation_error,
                "⏳ Quiz generation took too long."
            )
        except Exception as error:
            self.root.after(
                0, self.quiz_generation_error,
                "❌ Quiz generation error:\n" + str(error)
            )

    def extract_quiz_json(self, text):
        text = text.strip()

        try:
            data = json.loads(text)
            if isinstance(data, dict) and "questions" in data:
                return data["questions"]
            if isinstance(data, list):
                return data
        except Exception:
            pass

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            try:
                data = json.loads(text[start:end + 1])
                if isinstance(data, dict):
                    return data.get("questions", [])
            except Exception:
                pass

        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1:
            try:
                data = json.loads(text[start:end + 1])
                if isinstance(data, list):
                    return data
            except Exception:
                pass

        return []

    def validate_quiz(self, quiz):
        valid = []

        if not isinstance(quiz, list):
            return valid

        for item in quiz:
            if not isinstance(item, dict):
                continue

            question = str(item.get("question", "")).strip()
            options = item.get("options", [])
            answer = str(item.get("answer", "")).strip()

            if not isinstance(options, list):
                continue

            options = [str(x).strip() for x in options if str(x).strip()]

            if not question or len(options) != 4 or not answer:
                continue

            matching_answer = None

            for option in options:
                if option.lower() == answer.lower():
                    matching_answer = option
                    break

            if matching_answer is None:
                continue

            valid.append({
                "question": question,
                "options": options,
                "answer": matching_answer
            })

            if len(valid) == 5:
                break

        return valid

    def quiz_ready(self, quiz):
        self.busy = False
        self.quiz_questions = quiz
        self.quiz_index = 0
        self.quiz_score = 0
        self.show_ai_quiz_question()

    def quiz_generation_error(self, message):
        self.busy = False
        self.clear()
        self.header("❌ Quiz Error")

        tk.Label(
            self.root, text="Quiz could not be generated",
            bg="#f8fafc", fg="#dc2626",
            font=("Arial", 22, "bold")
        ).pack(pady=(80, 20))

        tk.Label(
            self.root, text=message,
            bg="#f8fafc", fg="#475569",
            font=("Arial", 12),
            justify="center", wraplength=750
        ).pack(pady=10)

        tk.Button(
            self.root, text="🔄 Try Again",
            command=lambda: self.generate_quiz(
                self.quiz_subject, self.quiz_topic
            ),
            bg="#2563eb", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=25, pady=10
        ).pack(pady=20)

        tk.Button(
            self.root, text="🏠 Home", command=self.home,
            bg="#64748b", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=25, pady=9
        ).pack()

    def show_ai_quiz_question(self):
        self.clear()
        self.header("🧠 " + self.quiz_subject + " • " + self.quiz_topic)

        if self.quiz_index >= len(self.quiz_questions):
            self.show_ai_quiz_result()
            return

        question = self.quiz_questions[self.quiz_index]

        tk.Label(
            self.root,
            text=f"Question {self.quiz_index + 1} of {len(self.quiz_questions)}",
            bg="#f8fafc", fg="#64748b",
            font=("Arial", 12, "bold")
        ).pack(pady=(30, 10))

        tk.Label(
            self.root, text=question["question"],
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 18, "bold"),
            wraplength=820, justify="center"
        ).pack(padx=40, pady=25)

        options_frame = tk.Frame(self.root, bg="#f8fafc")
        options_frame.pack(fill="x", padx=100)

        for option in question["options"]:
            tk.Button(
                options_frame, text=option,
                command=lambda selected=option: self.answer_ai_quiz(selected),
                bg="white", fg="#0f172a",
                activebackground="#dbeafe",
                relief="flat", font=("Arial", 12, "bold"),
                pady=13
            ).pack(fill="x", pady=5)

    def answer_ai_quiz(self, selected):
        question = self.quiz_questions[self.quiz_index]
        correct = question["answer"]

        if selected == correct:
            self.quiz_score += 1
            messagebox.showinfo(
                "Correct! 🎉",
                "Excellent MJ!\n\nYour answer is correct."
            )
        else:
            messagebox.showinfo(
                "Wrong ❌",
                "Correct answer:\n\n" + correct
            )

        self.quiz_index += 1
        self.show_ai_quiz_question()

    def show_ai_quiz_result(self):
        self.clear()
        self.header("🏆 AI Quiz Result")

        total = len(self.quiz_questions)
        percentage = int((self.quiz_score / total) * 100)

        tk.Label(
            self.root, text="🎉 Quiz Complete!",
            bg="#f8fafc", fg="#0f172a",
            font=("Arial", 28, "bold")
        ).pack(pady=(70, 15))

        tk.Label(
            self.root,
            text=self.quiz_subject + " • " + self.quiz_topic,
            bg="#f8fafc", fg="#64748b",
            font=("Arial", 14)
        ).pack(pady=5)

        tk.Label(
            self.root,
            text=f"{self.quiz_score} / {total}",
            bg="#f8fafc", fg="#2563eb",
            font=("Arial", 34, "bold")
        ).pack(pady=15)

        tk.Label(
            self.root,
            text=f"Score: {percentage}%",
            bg="#f8fafc", fg="#16a34a",
            font=("Arial", 20, "bold")
        ).pack(pady=5)

        if percentage >= 80:
            result_text = "🔥 Excellent performance, MJ!"
        elif percentage >= 60:
            result_text = "👍 Good job! Keep practicing."
        else:
            result_text = "📚 Keep studying. You can improve!"

        tk.Label(
            self.root, text=result_text,
            bg="#f8fafc", fg="#475569",
            font=("Arial", 13)
        ).pack(pady=10)

        tk.Button(
            self.root, text="🤖 Generate New Quiz",
            command=lambda: self.generate_quiz(
                self.quiz_subject, self.quiz_topic
            ),
            bg="#2563eb", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=25, pady=10
        ).pack(pady=20)

        tk.Button(
            self.root, text="📚 Choose Another Topic",
            command=self.quiz_page,
            bg="#64748b", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=25, pady=9
        ).pack()

        tk.Button(
            self.root, text="🏠 Home", command=self.home,
            bg="#334155", fg="white", relief="flat",
            font=("Arial", 11, "bold"), padx=25, pady=9
        ).pack(pady=8)


if __name__ == "__main__":
    root = tk.Tk()
    app = AIStudyAssistant(root)
    root.mainloop()