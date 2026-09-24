import json
import threading
from pathlib import Path

import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

OLLAMA_URL = "http://10.241.203.21:11434/api/generate"
MODEL = "gemma3:latest"

SUBJECTS = {
    "🐍 Python": ["Variables", "Data Types", "Loops", "Functions", "Lists", "OOP"],
    "🧱 Data Structures": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Searching"],
    "🗄 DBMS": ["SQL", "ER Model", "Normalization", "Transactions", "Joins", "Data Warehouse"],
    "🌐 Computer Networks": ["OSI Model", "TCP/IP", "IP Addressing", "DNS", "HTTP", "Network Security"],
    "💻 Operating Systems": ["Processes", "Threads", "CPU Scheduling", "Deadlocks", "Memory", "File Systems"],
}


def clean_subject(name):
    return name[2:].strip() if len(name) > 2 else name


class BaseScreen(Screen):
    def add_title(self, title):
        bar = BoxLayout(size_hint_y=None, height=dp(58), padding=dp(8), spacing=dp(8))
        back = Button(text="◀ Back", size_hint_x=None, width=dp(85))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "home"))
        bar.add_widget(back)
        bar.add_widget(Label(text=title, font_size="20sp", bold=True))
        home = Button(text="🏠", size_hint_x=None, width=dp(60))
        home.bind(on_release=lambda *_: setattr(self.manager, "current", "home"))
        bar.add_widget(home)
        self.add_widget(bar)


class HomeScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_title("🎓 AI Study Assistant")
        body = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        body.add_widget(Label(text="Welcome MJ! 👋", font_size="28sp", bold=True, size_hint_y=None, height=dp(55)))
        body.add_widget(Label(text="Learn • Practice • Ask AI", font_size="16sp", size_hint_y=None, height=dp(35)))

        scroll = ScrollView()
        grid = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for subject in SUBJECTS:
            b = Button(text=subject, font_size="16sp", size_hint_y=None, height=dp(55))
            b.bind(on_release=lambda btn, s=subject: self.open_subject(s))
            grid.add_widget(b)

        for text, target in [
            ("🤖 AI Chat", "chat"),
            ("📝 Notes", "notes"),
            ("🧠 AI Quiz", "quiz_subject"),
            ("🔍 Search", "search"),
        ]:
            b = Button(text=text, font_size="16sp", size_hint_y=None, height=dp(55))
            b.bind(on_release=lambda btn, t=target: setattr(self.manager, "current", t))
            grid.add_widget(b)

        scroll.add_widget(grid)
        body.add_widget(scroll)
        self.add_widget(body)

    def open_subject(self, subject):
        app = App.get_running_app()
        app.selected_subject = subject
        self.manager.current = "topics"


class TopicsScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        subject = app.selected_subject
        self.add_title("📚 " + subject)

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(8))
        layout.add_widget(Label(text="Choose a Topic", font_size="23sp", bold=True, size_hint_y=None, height=dp(50)))

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        for topic in SUBJECTS.get(subject, []):
            b = Button(text="📖 " + topic, size_hint_y=None, height=dp(52), font_size="15sp")
            b.bind(on_release=lambda btn, t=topic: self.open_topic(t))
            box.add_widget(b)

        scroll.add_widget(box)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_topic(self, topic):
        app = App.get_running_app()
        app.selected_topic = topic
        self.manager.current = "chat"
        Clock.schedule_once(lambda *_: self.manager.get_screen("chat").prefill(
            f"Explain {topic} in simple terms."
        ), 0.1)


class ChatScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_title("🤖 AI Chat")

        root = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        self.chat = Label(
            text="🤖 AI:\nHey MJ! 👋\nI'm your local AI Study Assistant.\nAsk me anything about your studies.\n",
            size_hint_y=None,
            halign="left",
            valign="top",
            text_size=(dp(340), None),
        )
        self.chat.bind(texture_size=self._chat_size)
        scroll = ScrollView()
        scroll.add_widget(self.chat)
        self.scroll = scroll
        root.add_widget(scroll)

        bottom = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        self.entry = TextInput(hint_text="Ask your question...", multiline=False)
        self.entry.bind(on_text_validate=lambda *_: self.ask())
        send = Button(text="SEND 🚀", size_hint_x=None, width=dp(105))
        send.bind(on_release=lambda *_: self.ask())
        bottom.add_widget(self.entry)
        bottom.add_widget(send)
        root.add_widget(bottom)
        self.add_widget(root)

    def _chat_size(self, *_):
        self.chat.text_size = (self.chat.parent.width - dp(15), None)

    def prefill(self, text):
        if hasattr(self, "entry"):
            self.entry.text = text
            self.entry.focus = True

    def append(self, text):
        self.chat.text += text
        Clock.schedule_once(lambda *_: setattr(self.scroll, "scroll_y", 0), 0.05)

    def ask(self):
        question = self.entry.text.strip()
        if not question:
            return
        self.entry.text = ""
        self.append(f"\n\n🧑 You:\n{question}\n\n🤖 AI:\n")
        app = App.get_running_app()
        threading.Thread(target=app.ask_ollama, args=(question, self), daemon=True).start()


class NotesScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_title("📝 Study Notes")

        root = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        root.add_widget(Label(text="Write Your Study Notes", font_size="22sp", bold=True, size_hint_y=None, height=dp(45)))
        self.notes = TextInput(multiline=True, hint_text="Type your notes here...")
        root.add_widget(self.notes)

        buttons = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        save = Button(text="💾 Save Notes")
        clear = Button(text="🗑 Clear")
        save.bind(on_release=lambda *_: self.save())
        clear.bind(on_release=lambda *_: setattr(self.notes, "text", ""))
        buttons.add_widget(save)
        buttons.add_widget(clear)
        root.add_widget(buttons)
        self.add_widget(root)

    def save(self):
        Path("study_notes.txt").write_text(self.notes.text, encoding="utf-8")


class QuizSubjectScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_title("🧠 AI Quiz")
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(8))
        root.add_widget(Label(text="Choose Quiz Subject", font_size="23sp", bold=True, size_hint_y=None, height=dp(50)))

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        for key in SUBJECTS:
            b = Button(text=key, size_hint_y=None, height=dp(55), font_size="15sp")
            b.bind(on_release=lambda btn, s=key: self.select(s))
            box.add_widget(b)
        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def select(self, subject):
        App.get_running_app().quiz_subject = clean_subject(subject)
        self.manager.current = "quiz_topic"


class QuizTopicScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        subject = app.quiz_subject
        self.add_title("🧠 " + subject + " Quiz")

        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(8))
        root.add_widget(Label(text="Choose Topic", font_size="22sp", bold=True, size_hint_y=None, height=dp(50)))

        scroll = ScrollView()
        box = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))
        key = next((k for k in SUBJECTS if clean_subject(k) == subject), "")
        for topic in SUBJECTS.get(key, []):
            b = Button(text="🧠 " + topic, size_hint_y=None, height=dp(52))
            b.bind(on_release=lambda btn, t=topic: app.generate_quiz(subject, t))
            box.add_widget(b)
        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)


class QuizScreen(BaseScreen):
    def on_pre_enter(self):
        self.show_question()

    def show_question(self):
        self.clear_widgets()
        app = App.get_running_app()
        self.add_title(f"🧠 {app.quiz_subject} • {app.quiz_topic}")

        if app.quiz_index >= len(app.quiz_questions):
            self.show_result()
            return

        q = app.quiz_questions[app.quiz_index]
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        root.add_widget(Label(
            text=f"Question {app.quiz_index + 1} of {len(app.quiz_questions)}",
            font_size="14sp", size_hint_y=None, height=dp(35)
        ))
        root.add_widget(Label(text=q["question"], font_size="19sp", bold=True, halign="center"))
        for option in q["options"]:
            b = Button(text=option, size_hint_y=None, height=dp(55))
            b.bind(on_release=lambda btn, o=option: app.answer_quiz(o))
            root.add_widget(b)
        self.add_widget(root)

    def show_result(self):
        app = App.get_running_app()
        total = len(app.quiz_questions)
        percent = int(app.quiz_score / total * 100) if total else 0
        self.clear_widgets()
        self.add_title("🏆 AI Quiz Result")
        root = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(12))
        root.add_widget(Label(text="🎉 Quiz Complete!", font_size="28sp", bold=True))
        root.add_widget(Label(text=f"{app.quiz_score} / {total}\nScore: {percent}%", font_size="25sp"))
        again = Button(text="🤖 Generate New Quiz", size_hint_y=None, height=dp(55))
        again.bind(on_release=lambda *_: setattr(self.manager, "current", "quiz_topic"))
        home = Button(text="🏠 Home", size_hint_y=None, height=dp(55))
        home.bind(on_release=lambda *_: setattr(self.manager, "current", "home"))
        root.add_widget(again)
        root.add_widget(home)
        self.add_widget(root)


class SearchScreen(BaseScreen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_title("🔍 Search")
        root = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(8))
        self.search = TextInput(hint_text="Search subjects or topics...", multiline=False, size_hint_y=None, height=dp(50))
        self.search.bind(on_text_validate=lambda *_: self.perform())
        root.add_widget(self.search)
        go = Button(text="Search 🔍", size_hint_y=None, height=dp(50))
        go.bind(on_release=lambda *_: self.perform())
        root.add_widget(go)
        self.results = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.results)
        root.add_widget(scroll)
        self.add_widget(root)

    def perform(self):
        self.results.clear_widgets()
        q = self.search.text.lower().strip()
        if not q:
            return
        for subject, topics in SUBJECTS.items():
            if q in subject.lower():
                b = Button(text=subject, size_hint_y=None, height=dp(50))
                b.bind(on_release=lambda *_: setattr(self.manager, "current", "topics"))
                self.results.add_widget(b)
            for topic in topics:
                if q in topic.lower():
                    b = Button(text=f"📖 {topic} ({subject})", size_hint_y=None, height=dp(50))
                    b.bind(on_release=lambda btn, s=subject, t=topic: self.open_topic(s, t))
                    self.results.add_widget(b)

        if not self.results.children:
            self.results.add_widget(Label(text="No results found 😕", size_hint_y=None, height=dp(50)))

    def open_topic(self, subject, topic):
        app = App.get_running_app()
        app.selected_subject = subject
        app.selected_topic = topic
        self.manager.current = "chat"
        Clock.schedule_once(lambda *_: self.manager.get_screen("chat").prefill(
            f"Explain {topic} in simple terms."
        ), 0.1)


class AIStudyAssistantApp(App):
    selected_subject = "General Study"
    selected_topic = "General"
    quiz_subject = ""
    quiz_topic = ""
    quiz_questions = []
    quiz_index = 0
    quiz_score = 0

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TopicsScreen(name="topics"))
        sm.add_widget(ChatScreen(name="chat"))
        sm.add_widget(NotesScreen(name="notes"))
        sm.add_widget(QuizSubjectScreen(name="quiz_subject"))
        sm.add_widget(QuizTopicScreen(name="quiz_topic"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(SearchScreen(name="search"))
        return sm

    def ask_ollama(self, question, screen):
        prompt = f"""You are MJ's personal AI Study Assistant.
Be friendly and helpful.
If MJ writes Telugu-English, reply naturally in Telugu-English.
If MJ writes English, reply in English.
Keep simple questions short. For difficult topics, explain step by step.
For programming questions, give clean working code.

Subject: {self.selected_subject}
Topic: {self.selected_topic}
Question: {question}

Answer:"""
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"temperature": 0.2, "num_ctx": 2048, "num_predict": 450},
                },
                stream=True,
                timeout=120,
            )
            if response.status_code != 200:
                raise RuntimeError(f"Ollama error: {response.status_code}")
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    part = data.get("response", "")
                    if part:
                        Clock.schedule_once(lambda dt, p=part: screen.append(p))
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            Clock.schedule_once(lambda dt, err=str(e): screen.append(f"\n\n❌ {err}\n"))

    def generate_quiz(self, subject, topic):
        self.quiz_subject = subject
        self.quiz_topic = topic
        self.quiz_questions = []
        self.quiz_index = 0
        self.quiz_score = 0
        threading.Thread(target=self._quiz_thread, daemon=True).start()
        self.root.current = "quiz"

    def _quiz_thread(self):
        prompt = f"""Create exactly 5 multiple-choice questions for a college CSE student.
Subject: {self.quiz_subject}
Topic: {self.quiz_topic}
Every question must have exactly 4 options and one correct answer.
Return ONLY valid JSON:
{{"questions":[{{"question":"Question","options":["A","B","C","D"],"answer":"Correct option text"}}]}}"""
        try:
            r = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0.2, "num_ctx": 4096, "num_predict": 1400},
                },
                timeout=180,
            )
            r.raise_for_status()
            data = r.json()
            raw = data.get("response", "")
            parsed = json.loads(raw)
            questions = parsed.get("questions", []) if isinstance(parsed, dict) else []
            valid = []
            for item in questions:
                if not isinstance(item, dict):
                    continue
                q = str(item.get("question", "")).strip()
                opts = [str(x).strip() for x in item.get("options", []) if str(x).strip()]
                ans = str(item.get("answer", "")).strip()
                match = next((o for o in opts if o.lower() == ans.lower()), None)
                if q and len(opts) == 4 and match:
                    valid.append({"question": q, "options": opts, "answer": match})
                if len(valid) == 5:
                    break
            if not valid:
                raise ValueError("AI returned an invalid quiz.")
            self.quiz_questions = valid
            Clock.schedule_once(lambda *_: setattr(self.root, "current", "quiz"))
            Clock.schedule_once(lambda *_: self.root.get_screen("quiz").show_question())
        except Exception:
            self.quiz_questions = []
            Clock.schedule_once(lambda *_: setattr(self.root, "current", "quiz"))
            Clock.schedule_once(lambda *_: self.root.get_screen("quiz").show_error())

    def answer_quiz(self, selected):
        q = self.quiz_questions[self.quiz_index]
        if selected == q["answer"]:
            self.quiz_score += 1
        self.quiz_index += 1
        self.root.get_screen("quiz").show_question()


# Add a simple error screen method dynamically.
def show_error(self):
    self.clear_widgets()
    self.add_title("❌ Quiz Error")
    box = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(12))
    box.add_widget(Label(text="Quiz could not be generated.\nCheck that Ollama is running.", font_size="18sp"))
    retry = Button(text="🔄 Try Again", size_hint_y=None, height=dp(55))
    retry.bind(on_release=lambda *_: setattr(self.manager, "current", "quiz_topic"))
    box.add_widget(retry)
    self.add_widget(box)


QuizScreen.show_error = show_error

if __name__ == "__main__":
    AIStudyAssistantApp().run()
