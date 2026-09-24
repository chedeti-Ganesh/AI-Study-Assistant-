import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import json
import random
import threading
import urllib.request
import urllib.error
import webbrowser

APP_TITLE = "AI Study Assistant V6"
BG = "#071426"
PANEL = "#0b1d34"
CARD = "#102846"
CARD2 = "#14345a"
TEXT = "#f4f8ff"
MUTED = "#9bb0c9"
CYAN = "#38bdf8"
BLUE = "#2563eb"
BLUE_DARK = "#1d4ed8"
PURPLE = "#9b7cff"
GREEN = "#25d366"
ORANGE = "#fb923c"
RED = "#ef4444"
BORDER = "#24517f"

BASE_DIR = Path(__file__).resolve().parent
USER_FILE = BASE_DIR / "ai_study_users.json"
PROGRESS_FILE = BASE_DIR / "ai_study_progress.json"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODELS = ("gemma3:latest", "llama3.2:3b")

SUBJECTS = {
    "Programming": ["Python Programming", "C Programming", "C++ Programming", "Java Programming", "Data Structures", "Algorithms"],
    "Core CSE": ["Database Management Systems", "Operating Systems", "Computer Networks", "Computer Organization", "Object Oriented Programming", "Software Engineering", "Theory of Computation", "Compiler Design"],
    "Web Development": ["HTML", "CSS", "JavaScript", "SQL", "Git & GitHub"],
    "AI & Data": ["Artificial Intelligence", "Machine Learning", "Data Science", "Generative AI"],
}

# Each subject has theory, lessons, Q&A and a practice task. This is intentionally local-first for fast answers.
DATA = {
"Python Programming": {"icon":"🐍", "intro":"Python is a high-level, general-purpose language focused on readable syntax and rapid development.", "topics":["Syntax & Variables","Data Types","Operators","Conditions","Loops","Functions","Lists & Tuples","Dictionaries & Sets","Exceptions","OOP"], "qa":[
("What is Python?","Python is a high-level, general-purpose programming language. It uses dynamic typing and indentation-based block structure and has a large standard library and ecosystem."),
("What are Python data types?","Common built-in types include int, float, complex, bool, str, list, tuple, set and dict. Python variables refer to objects rather than storing a fixed declared type."),
("What is a function?","A function is a reusable block of code defined with def. It can accept parameters and return a value with return."),
("What is a list?","A list is an ordered, mutable collection. It supports indexing, slicing and methods such as append, insert, remove and sort."),
("What is a dictionary?","A dictionary stores key-value pairs. Keys must be hashable and values can be any Python object."),
("What is exception handling?","Python uses try, except, else and finally to handle runtime exceptions without abruptly terminating the program."),
], "code":"def add(a, b):\n    return a + b\n\nprint(add(10, 20))"},
"C Programming": {"icon":"C", "intro":"C is a procedural language used for systems programming and for learning memory, pointers and low-level concepts.", "topics":["Program Structure","Data Types","Operators","Control Flow","Functions","Arrays","Pointers","Strings","Structures","Dynamic Memory"], "qa":[
("What is C?","C is a procedural, compiled programming language. It provides direct memory access through pointers and is widely used for systems software."),
("What is a pointer?","A pointer is an object that stores the address of another object or function. The * operator can dereference a pointer and & obtains an address."),
("What is an array?","An array stores a fixed number of elements of the same type in contiguous memory."),
("What is malloc?","malloc allocates a requested number of bytes from dynamic memory and returns a pointer to the allocated block, or NULL on failure."),
], "code":"#include <stdio.h>\nint main(void) {\n    int a = 10, b = 20;\n    printf(\"%d\\n\", a + b);\n    return 0;\n}"},
"C++ Programming": {"icon":"C++", "intro":"C++ combines procedural programming with object-oriented and generic programming features.", "topics":["Classes","Objects","Constructors","Inheritance","Polymorphism","Templates","STL","Exceptions"], "qa":[
("What is a class?","A class is a user-defined type that groups data members and member functions. Objects are instances of a class."),
("What is inheritance?","Inheritance lets a derived class reuse and extend members of a base class. C++ supports public, protected and private inheritance."),
("What is polymorphism?","Polymorphism means one interface can represent different implementations. In C++, compile-time examples include overloading and run-time polymorphism can use virtual functions."),
], "code":"class Student {\npublic:\n    string name;\n};"},
"Java Programming": {"icon":"☕", "intro":"Java is a class-based language commonly used for enterprise, Android and backend development.", "topics":["JVM & JRE","Variables","Classes","Objects","Inheritance","Interfaces","Exceptions","Collections"], "qa":[
("What is JVM?","The Java Virtual Machine executes Java bytecode and provides a platform-independent execution environment."),
("What is an interface?","An interface defines a contract of methods and can also contain default and static methods. A class implements an interface."),
("What is exception handling?","Java uses try, catch, finally, throw and throws to manage exceptional conditions."),
], "code":"public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello MJ\");\n    }\n}"},
"Data Structures": {"icon":"🌳", "intro":"Data structures organize data so operations such as search, insertion and deletion can be performed efficiently.", "topics":["Arrays","Linked Lists","Stacks","Queues","Trees","Graphs","Hashing","Heaps","Complexity"], "qa":[
("What is a data structure?","A data structure is an organized representation of data together with operations for accessing or modifying it."),
("What is a stack?","A stack follows LIFO: the most recently inserted item is removed first. Push and pop are its basic operations."),
("What is a queue?","A queue follows FIFO: the earliest inserted item is removed first. Enqueue adds an item and dequeue removes one."),
("What is a binary search tree?","A binary search tree is a binary tree in which values in the left subtree are ordered before the node and values in the right subtree after it, subject to the chosen duplicate policy."),
], "code":"stack = []\nstack.append(10)\nstack.append(20)\nprint(stack.pop())"},
"Algorithms": {"icon":"⚙", "intro":"Algorithms are finite, well-defined procedures for solving problems.", "topics":["Complexity","Searching","Sorting","Recursion","Greedy","Divide & Conquer","Dynamic Programming","Graphs"], "qa":[
("What is an algorithm?","An algorithm is a finite sequence of precise steps that transforms input into output to solve a problem."),
("What is time complexity?","Time complexity describes how an algorithm's running time grows as input size increases. Big-O gives an asymptotic upper bound in common analysis."),
("What is binary search?","Binary search works on sorted data by comparing the target with the middle element and discarding half the search interval after each comparison."),
("What is dynamic programming?","Dynamic programming solves overlapping subproblems by storing solutions so the same subproblem does not need to be solved repeatedly."),
], "code":"def binary_search(a, x):\n    lo, hi = 0, len(a)-1\n    while lo <= hi:\n        mid = (lo + hi)//2\n        if a[mid] == x: return mid\n        if a[mid] < x: lo = mid + 1\n        else: hi = mid - 1\n    return -1"},
"Database Management Systems": {"icon":"🗄", "intro":"DBMS concepts cover data models, relational algebra, SQL, normalization, transactions and recovery.", "topics":["DBMS Basics","ER Model","Relational Model","Keys","SQL","Normalization","Transactions","Concurrency","Indexing"], "qa":[
("What is DBMS?","A Database Management System is software used to define, create, store, retrieve, update and control access to databases."),
("What is a primary key?","A primary key is a candidate key selected to uniquely identify tuples in a relation. Its values must be unique and not NULL in the relational model."),
("What is normalization?","Normalization organizes relations to reduce redundancy and update anomalies by decomposing tables according to functional dependencies and normal-form rules."),
("What is a transaction?","A transaction is a logical unit of database work. ACID properties are atomicity, consistency, isolation and durability."),
("What is SQL?","SQL is a language used to define, query and manipulate relational data. Common categories include DDL, DML, DQL and transaction/control statements."),
], "code":"SELECT name, marks\nFROM students\nWHERE marks >= 70\nORDER BY marks DESC;"},
"Operating Systems": {"icon":"🖥", "intro":"Operating systems manage hardware resources and provide services to application programs.", "topics":["OS Services","Processes","Threads","CPU Scheduling","Synchronization","Deadlocks","Memory Management","Virtual Memory","File Systems"], "qa":[
("What is an operating system?","An operating system manages hardware resources and provides common services such as process management, memory management, file management and I/O control."),
("What is a process?","A process is a program in execution together with its current state, address space and allocated resources."),
("What is a thread?","A thread is a unit of execution within a process. Threads in the same process can share its address space and resources."),
("What is deadlock?","Deadlock is a state in which a set of processes are permanently waiting for resources held by one another. The four classic necessary conditions are mutual exclusion, hold-and-wait, no preemption and circular wait."),
("What is virtual memory?","Virtual memory gives processes an abstraction of a large logical address space using secondary storage together with mechanisms such as paging."),
], "code":"# CPU scheduling concept\nprocesses = ['P1', 'P2', 'P3']\nfor p in processes:\n    print('Running', p)"},
"Computer Networks": {"icon":"🌐", "intro":"Computer Networks studies communication between devices, layered protocols, addressing, routing and reliable delivery.", "topics":["Network Basics","OSI Model","TCP/IP Model","Physical & Data Link","IP Addressing","ARP","Routing","TCP","UDP","DNS","HTTP/HTTPS"], "qa":[
("What is a computer network?","A computer network is a collection of interconnected devices that exchange data using communication links and protocols."),
("What is the OSI model?","The OSI reference model divides communication into seven layers: Physical, Data Link, Network, Transport, Session, Presentation and Application."),
("What is the Transport layer?","The Transport layer provides process-to-process delivery. TCP provides connection-oriented reliable delivery, while UDP provides connectionless datagrams with lower protocol overhead."),
("What is TCP?","TCP is a connection-oriented transport protocol that uses sequencing, acknowledgements, retransmission and flow/congestion-control mechanisms to provide reliable ordered delivery."),
("What is UDP?","UDP is a connectionless transport protocol with a small header. It does not provide TCP-style reliability, ordering or connection setup."),
("What is IP?","Internet Protocol provides logical addressing and packet forwarding across interconnected networks. IPv4 uses 32-bit addresses and IPv6 uses 128-bit addresses."),
("What is DNS?","DNS maps domain names to resource records such as IP addresses. It uses a distributed hierarchical naming system."),
("What is HTTP?","HTTP is an application-layer request/response protocol used by web clients and servers. HTTPS is HTTP carried over a secure TLS connection."),
("What is routing?","Routing selects paths for packets between networks using routing information maintained by routers and routing protocols."),
], "code":"# Simplified layered view\n# Application -> Transport -> Internet -> Link"},
"Computer Organization": {"icon":"🔧", "intro":"Computer organization explains how CPU, memory, I/O and instruction execution work together.", "topics":["CPU","ALU","Control Unit","Registers","Memory Hierarchy","Cache","Instructions","I/O"], "qa":[
("What is ALU?","The Arithmetic Logic Unit performs arithmetic and logical operations on data."),
("What is cache memory?","Cache is small, high-speed memory placed close to the processor to reduce average access time by exploiting locality."),
("What is a register?","A register is a small, fast storage location inside the processor used for operands, addresses, instructions or intermediate results."),
], "code":"# Instruction cycle\n# Fetch -> Decode -> Execute -> Memory access -> Write back"},
"Object Oriented Programming": {"icon":"🧩", "intro":"OOP models software using objects that combine state and behavior.", "topics":["Classes","Objects","Encapsulation","Inheritance","Abstraction","Polymorphism","Interfaces"], "qa":[
("What is OOP?","Object-oriented programming organizes software around objects containing state and behavior. Common principles include encapsulation, abstraction, inheritance and polymorphism."),
("What is encapsulation?","Encapsulation combines related state and behavior and controls how internal state is accessed or changed."),
("What is abstraction?","Abstraction focuses on essential behavior while hiding implementation details that are not required by the user of an abstraction."),
], "code":"class Student:\n    def __init__(self, name):\n        self.name = name\n\ns = Student('MJ')"},
"Software Engineering": {"icon":"🛠", "intro":"Software engineering applies systematic processes to requirements, design, development, testing and maintenance.", "topics":["SDLC","Requirements","Architecture","Design","Testing","Agile","Version Control","Maintenance"], "qa":[
("What is SDLC?","Software Development Life Cycle is a structured set of activities for requirements, planning, design, implementation, testing, deployment and maintenance."),
("What is software testing?","Testing evaluates software behavior to find defects and provide evidence that specified requirements are satisfied."),
("What is Agile?","Agile is a family of iterative and incremental development approaches emphasizing frequent delivery, feedback and adaptation."),
], "code":"# Typical flow\n# Requirements -> Design -> Development -> Testing -> Deployment -> Maintenance"},
"Theory of Computation": {"icon":"Σ", "intro":"Theory of Computation studies mathematical models of computation and formal languages.", "topics":["DFA","NFA","Regular Languages","CFG","PDA","Turing Machines","Decidability"], "qa":[
("What is DFA?","A deterministic finite automaton has a finite set of states and exactly one transition for each state and input symbol."),
("What is NFA?","A nondeterministic finite automaton may have zero, one or multiple possible transitions for a state and symbol. NFAs and DFAs recognize the same class of regular languages."),
("What is a context-free grammar?","A CFG consists of variables, terminals, production rules and a start symbol and is used to describe context-free languages."),
], "code":"# Automaton idea\n# current_state + input_symbol -> next_state"},
"Compiler Design": {"icon":"⚙", "intro":"Compiler design covers translation from source programs to target or intermediate representations.", "topics":["Lexical Analysis","Parsing","AST","Semantic Analysis","Intermediate Code","Optimization","Code Generation"], "qa":[
("What is a compiler?","A compiler translates a source program into another representation, commonly machine code or an intermediate representation, while reporting errors."),
("What is lexical analysis?","Lexical analysis converts a character stream into tokens such as identifiers, keywords, operators and literals."),
("What is parsing?","Parsing checks whether the token sequence follows a grammar and constructs a syntactic structure such as a parse tree or AST."),
], "code":"# Source -> Lexer -> Parser -> Semantic Analysis -> IR -> Optimization -> Code Generation"},
"HTML": {"icon":"<> ", "intro":"HTML defines the structure and semantics of web documents.", "topics":["Elements","Attributes","Links","Images","Forms","Tables","Semantic HTML","Accessibility"], "qa":[
("What is HTML?","HTML is the standard markup language for structuring content on web pages."),
("What is semantic HTML?","Semantic HTML uses elements whose names describe their purpose, such as header, nav, main, article, section and footer."),
("What is a form?","An HTML form collects user input through controls such as input, select, textarea and button and can submit data to a server."),
], "code":"<!doctype html>\n<html>\n<body>\n  <h1>Hello MJ</h1>\n</body>\n</html>"},
"CSS": {"icon":"#", "intro":"CSS controls presentation, layout and responsive behavior of web pages.", "topics":["Selectors","Box Model","Colors","Flexbox","Grid","Responsive Design","Transitions"], "qa":[
("What is CSS?","CSS is a stylesheet language used to describe presentation and layout of HTML and other document trees."),
("What is the box model?","The CSS box model represents an element as content surrounded by padding, border and margin."),
("What is Flexbox?","Flexbox is a one-dimensional layout system for arranging items along a main axis and a cross axis."),
], "code":".card {\n  padding: 20px;\n  display: flex;\n  gap: 12px;\n}"},
"JavaScript": {"icon":"JS", "intro":"JavaScript is a programming language widely used to add behavior and interactivity to web applications.", "topics":["Variables","Functions","Arrays","Objects","DOM","Events","Async JavaScript","Fetch API"], "qa":[
("What is JavaScript?","JavaScript is a dynamic programming language used in browsers and many server/runtime environments."),
("What is the DOM?","The Document Object Model represents an HTML document as a tree of objects that scripts can inspect and modify."),
("What is a Promise?","A Promise represents the eventual completion or failure of an asynchronous operation and its resulting value."),
], "code":"const button = document.querySelector('#btn');\nbutton.addEventListener('click', () => {\n  console.log('Clicked');\n});"},
"SQL": {"icon":"SQL", "intro":"SQL is used to define, query and manipulate data in relational database systems.", "topics":["SELECT","WHERE","JOIN","GROUP BY","Subqueries","INSERT/UPDATE/DELETE","Constraints","Transactions"], "qa":[
("What is SELECT?","SELECT retrieves rows and expressions from one or more tables or query sources."),
("What is a JOIN?","A JOIN combines rows from tables using a matching condition or another join rule. Common types include INNER, LEFT, RIGHT and FULL joins, depending on the DBMS."),
("What is GROUP BY?","GROUP BY forms groups of rows so aggregate functions such as COUNT, SUM, AVG, MIN and MAX can be calculated per group."),
], "code":"SELECT department, COUNT(*) AS total\nFROM students\nGROUP BY department;"},
"Git & GitHub": {"icon":"git", "intro":"Git tracks changes to files; GitHub hosts Git repositories and collaboration workflows.", "topics":["Repository","Commit","Branch","Merge","Pull","Push","Clone","Pull Request"], "qa":[
("What is Git?","Git is a distributed version-control system that records changes to files in a repository."),
("What is a commit?","A commit records a snapshot of selected repository changes together with metadata and a message."),
("What is a branch?","A branch is a movable reference to commits that lets developers work on lines of development independently."),
], "code":"git init\ngit add .\ngit commit -m \"first commit\"\ngit branch -M main\ngit remote add origin <URL>\ngit push -u origin main"},
"Artificial Intelligence": {"icon":"AI", "intro":"Artificial Intelligence studies systems that perform tasks associated with perception, reasoning, learning and decision making.", "topics":["AI Basics","Agents","Search","Knowledge Representation","Reasoning","Machine Learning","NLP","Computer Vision","Generative AI"], "qa":[
("What is Artificial Intelligence?","AI is the field of computing concerned with building systems that perform tasks involving capabilities such as perception, reasoning, learning, language understanding or decision making."),
("What is an intelligent agent?","An agent perceives its environment through sensors and acts through actuators. A rational agent chooses actions according to a performance measure and available information."),
("What is machine learning?","Machine learning is a branch of AI in which systems learn patterns or decision rules from data rather than relying only on explicitly programmed rules."),
("What is NLP?","Natural Language Processing deals with computational processing of human language, including tasks such as classification, extraction, translation and generation."),
], "code":"# Simple rule-based agent\nif temperature > 30:\n    action = 'turn_on_cooling'"},
"Machine Learning": {"icon":"ML", "intro":"Machine learning learns useful patterns from data for prediction, classification, generation or decision support.", "topics":["Supervised Learning","Unsupervised Learning","Regression","Classification","Clustering","Overfitting","Evaluation","Neural Networks"], "qa":[
("What is supervised learning?","Supervised learning trains a model using labeled examples containing inputs and target outputs."),
("What is classification?","Classification predicts a discrete class label, such as spam/not-spam or one of several categories."),
("What is regression?","Regression predicts a numeric quantity such as price, temperature or demand."),
("What is overfitting?","Overfitting occurs when a model fits training data too closely and generalizes poorly to unseen data. Regularization, more data and appropriate model complexity can help."),
], "code":"# ML workflow\n# data -> split -> train -> validate -> evaluate -> deploy"},
"Data Science": {"icon":"DS", "intro":"Data science combines statistics, programming, data management and domain knowledge to extract useful information from data.", "topics":["Data Collection","Cleaning","EDA","Statistics","Visualization","Feature Engineering","Modeling","Communication"], "qa":[
("What is EDA?","Exploratory Data Analysis uses summaries and visualizations to understand distributions, relationships, missing values and unusual observations."),
("Why clean data?","Cleaning addresses problems such as missing values, duplicates, inconsistent formats and invalid records so downstream analysis is more reliable."),
("What is a feature?","A feature is an input variable used to describe an observation for analysis or model training."),
], "code":"import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())\nprint(df.describe())"},
"Generative AI": {"icon":"✦", "intro":"Generative AI models learn patterns from data and generate new text, images, audio, code or other content.", "topics":["LLMs","Tokens","Prompts","Embeddings","RAG","Fine-tuning","Agents","Evaluation"], "qa":[
("What is a large language model?","An LLM is a neural language model trained on large amounts of text to model sequences of tokens and generate language based on context."),
("What is a token?","A token is a unit used by a language model to represent text for processing. Tokenization may split text into words, subwords or other pieces."),
("What is RAG?","Retrieval-Augmented Generation retrieves relevant external documents and supplies their content to a generative model so the answer can be grounded in those sources."),
], "code":"# RAG concept\n# question -> retrieve relevant documents -> prompt model -> grounded answer"},
}

# Aliases let the AI answer common abbreviations such as CN, OS and DBMS.
ALIASES = {
    "cn":"Computer Networks", "computer network":"Computer Networks", "networks":"Computer Networks", "networking":"Computer Networks",
    "os":"Operating Systems", "operating system":"Operating Systems", "operating systems":"Operating Systems",
    "dbms":"Database Management Systems", "database":"Database Management Systems", "sql":"SQL",
    "ai":"Artificial Intelligence", "ml":"Machine Learning", "ds":"Data Science", "genai":"Generative AI",
    "oops":"Object Oriented Programming", "oop":"Object Oriented Programming", "dsa":"Data Structures",
    "js":"JavaScript", "html":"HTML", "css":"CSS", "git":"Git & GitHub", "toc":"Theory of Computation", "cd":"Compiler Design",
}

# Extra bulk questions for quiz / important-question sections.
EXTRA_QA = [
("What is a protocol?","A protocol is a defined set of rules and message formats used by communicating systems."),
("What is an IP address?","An IP address is a logical address used to identify an interface or endpoint at the Internet Protocol layer."),
("What is a router?","A router forwards packets between networks based on routing information."),
("What is a switch?","A network switch forwards frames within a local network, commonly using MAC address information."),
("What is HTTP?","HTTP is an application-layer protocol used for request/response communication on the Web."),
("What is a process state?","A process may move through states such as new, ready, running, waiting/blocked and terminated, depending on the OS model."),
("What is paging?","Paging divides logical memory into fixed-size pages and physical memory into frames, allowing non-contiguous allocation."),
("What is a foreign key?","A foreign key is an attribute or set of attributes in one relation that references a candidate/primary key in another relation."),
("What is an index in DBMS?","An index is an auxiliary data structure that can speed up selected queries at the cost of extra storage and maintenance work."),
("What is normalization 1NF?","First Normal Form requires each relation cell to contain a single atomic value under the usual relational interpretation."),
("What is inheritance?","Inheritance is a mechanism in object-oriented programming in which a derived type reuses or specializes behavior from a base type."),
("What is abstraction?","Abstraction exposes relevant concepts while hiding implementation details that are not needed by the client."),
("What is recursion?","Recursion is a technique in which a function solves a problem by calling itself on smaller instances, with a base case stopping recursion."),
("What is Big-O notation?","Big-O describes an asymptotic upper bound on the growth rate of a function and is commonly used for algorithm complexity."),
("What is an API?","An API is an interface through which one software component can request operations or data from another component according to defined rules."),
]


def all_subjects():
    return [s for group in SUBJECTS.values() for s in group]


def normalize(text):
    return " ".join((text or "").lower().replace("?", " ").replace("-", " ").split())


def subject_for_query(q):
    nq = normalize(q)
    for alias, subject in sorted(ALIASES.items(), key=lambda x: -len(x[0])):
        if alias in nq:
            return subject
    for subject in all_subjects():
        if normalize(subject) in nq:
            return subject
    return None


def save_json(path, data):
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def load_json(path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


class ScrollFrame(tk.Frame):
    """Reliable Tk Canvas + Frame scrolling with mouse wheel, scrollbar and drag scrolling."""
    def __init__(self, parent, bg=PANEL):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.bar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.bar.set)
        self.bar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._sync_region)
        self.canvas.bind("<Configure>", self._sync_width)
        for widget in (self, self.canvas, self.inner):
            widget.bind("<Enter>", self._enter, add="+")
            widget.bind("<Leave>", self._leave, add="+")
            widget.bind("<ButtonPress-1>", self._mark, add="+")
            widget.bind("<B1-Motion>", self._drag, add="+")
        self._wheel_active = False

    def _sync_region(self, _=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _sync_width(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)
        self.after_idle(self._sync_region)

    def _enter(self, _=None):
        self._wheel_active = True
        self.canvas.focus_set()

    def _leave(self, _=None):
        self._wheel_active = False

    def _wheel(self, event):
        if not self._wheel_active:
            return
        if getattr(event, "delta", 0):
            step = -1 * int(event.delta / 120) if abs(event.delta) >= 120 else (-1 if event.delta > 0 else 1)
            self.canvas.yview_scroll(step, "units")
        elif getattr(event, "num", None) == 4:
            self.canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            self.canvas.yview_scroll(3, "units")
        return "break"

    def _mark(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def activate_wheel(self):
        # bind_all is deliberate: wheel events often land on a Label/Button child
        # rather than the Canvas itself. We scroll only when the pointer is inside
        # this ScrollFrame.
        self.canvas.bind_all("<MouseWheel>", self._wheel_global, add="+")
        self.canvas.bind_all("<Button-4>", self._wheel_global, add="+")
        self.canvas.bind_all("<Button-5>", self._wheel_global, add="+")

    def _wheel_global(self, event):
        try:
            x, y = event.x_root, event.y_root
            left = self.canvas.winfo_rootx()
            top = self.canvas.winfo_rooty()
            right = left + self.canvas.winfo_width()
            bottom = top + self.canvas.winfo_height()
            if left <= x <= right and top <= y <= bottom:
                return self._wheel(event)
        except tk.TclError:
            return None
        return None


class AIStudyAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1220x800")
        self.root.minsize(1000, 680)
        self.root.configure(bg=BG)
        self.font_scale = 1.0
        self.user = None
        self.history = []
        self.current_screen = None
        self.selected_subject = None
        self.progress = load_json(PROGRESS_FILE, {})
        self.chat_history = []
        self.content = None
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.login_screen()

    def fs(self, size, bold=False):
        return ("Segoe UI", max(9, int(size * self.font_scale)), "bold" if bold else "normal")

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def card(self, parent, padx=18, pady=16):
        return tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)

    def label(self, parent, text="", size=11, fg=TEXT, bold=False, bg=None, **kwargs):
        return tk.Label(parent, text=text, fg=fg, bg=bg if bg is not None else parent.cget("bg"), font=self.fs(size, bold), **kwargs)

    def button(self, parent, text, command, width=None, bg=CARD2, fg=TEXT, **kwargs):
        b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground=BLUE_DARK, activeforeground="white", relief="flat", bd=0, cursor="hand2", font=self.fs(10, True), padx=12, pady=8, **kwargs)
        if width:
            b.configure(width=width)
        return b

    def title_bar(self, parent, title, subtitle="", back=True):
        bar = tk.Frame(parent, bg=PANEL, height=70)
        bar.pack(fill="x")
        if back and self.history:
            self.button(bar, "← Back", self.go_back, bg=CARD2).pack(side="left", padx=14, pady=14)
        self.label(bar, title, 18, TEXT, True, bg=PANEL).pack(side="left", padx=8)
        if subtitle:
            self.label(bar, subtitle, 10, MUTED, False, bg=PANEL).pack(side="left", padx=8)
        return bar

    def set_screen(self, builder, title="", push=True):
        if push and self.current_screen is not None:
            self.history.append(self.current_screen)
        self.current_screen = builder
        self.clear_root()
        builder()

    def go_back(self):
        if self.history:
            builder = self.history.pop()
            self.current_screen = builder
            self.clear_root()
            builder()
        else:
            self.show_home(push=False)

    def go_home(self):
        self.history.clear()
        self.show_home(push=False)

    def shell(self, title, subtitle="", back=True):
        self.clear_root()
        top = tk.Frame(self.root, bg=PANEL, height=64)
        top.pack(fill="x")
        if back and self.history:
            self.button(top, "← Back", self.go_back, bg=CARD2).pack(side="left", padx=12, pady=12)
        self.label(top, "✦  AI Study Assistant", 16, TEXT, True, bg=PANEL).pack(side="left", padx=10)
        self.label(top, title, 12, CYAN, True, bg=PANEL).pack(side="left", padx=8)
        if self.user:
            self.label(top, self.user.get("name", "Student"), 10, TEXT, True, bg=PANEL).pack(side="right", padx=14)
        self.label(self.root, subtitle, 10, MUTED, False, bg=BG).pack(anchor="w", padx=24, pady=(12, 4))
        body = ScrollFrame(self.root, BG)
        body.pack(fill="both", expand=True, padx=18, pady=(4, 12))
        body.activate_wheel()
        self.content = body.inner
        return body.inner

    # ---------------- authentication ----------------
    def login_screen(self):
        self.clear_root()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)
        panel = tk.Frame(outer, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.46, relheight=0.70)
        self.label(panel, "✦", 34, CYAN, True, bg=PANEL).pack(pady=(28, 4))
        self.label(panel, "AI Study Assistant", 23, TEXT, True, bg=PANEL).pack()
        self.label(panel, "Sign in to continue your study journey", 10, MUTED, bg=PANEL).pack(pady=(4, 22))
        form = tk.Frame(panel, bg=PANEL)
        form.pack(fill="x", padx=44)
        self.label(form, "Name or Email", 10, MUTED, True, bg=PANEL).pack(anchor="w")
        self.login_user = tk.Entry(form, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", font=self.fs(12), bd=0)
        self.login_user.pack(fill="x", ipady=11, pady=(5, 12))
        self.label(form, "Password", 10, MUTED, True, bg=PANEL).pack(anchor="w")
        self.login_pass = tk.Entry(form, show="•", bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", font=self.fs(12), bd=0)
        self.login_pass.pack(fill="x", ipady=11, pady=(5, 14))
        self.button(form, "Login", self.login, bg=BLUE, width=20).pack(fill="x", pady=4)
        self.button(form, "Create Account", self.signup_screen, bg=CARD2).pack(fill="x", pady=6)
        self.button(form, "Continue with Google", self.google_login, bg="#17395e").pack(fill="x", pady=6)
        self.label(panel, "Local account data stays on this PC. Google button opens the official sign-in page; full OAuth needs a backend.", 8, MUTED, bg=PANEL, wraplength=420, justify="center").pack(padx=35, pady=18)
        self.login_user.focus_set()
        self.root.bind("<Return>", lambda e: self.login())

    def users(self):
        return load_json(USER_FILE, {})

    def login(self):
        key = self.login_user.get().strip().lower()
        pw = self.login_pass.get()
        users = self.users()
        if not key or not pw:
            messagebox.showwarning("Login", "Enter your name/email and password.")
            return
        record = users.get(key)
        if not record or record.get("password") != pw:
            messagebox.showerror("Login", "Account not found or password is incorrect. Create an account first.")
            return
        self.user = record
        self.root.unbind("<Return>")
        self.go_home()

    def signup_screen(self):
        self.clear_root()
        panel = tk.Frame(self.root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.48, relheight=0.72)
        self.label(panel, "Create your account", 22, TEXT, True, bg=PANEL).pack(pady=(28, 20))
        form = tk.Frame(panel, bg=PANEL); form.pack(fill="x", padx=44)
        entries = {}
        for key, text in (("name","Full Name"),("email","Email"),("password","Password")):
            self.label(form, text, 10, MUTED, True, bg=PANEL).pack(anchor="w")
            e = tk.Entry(form, show="•" if key == "password" else "", bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", font=self.fs(12), bd=0)
            e.pack(fill="x", ipady=11, pady=(5, 12)); entries[key] = e
        def create():
            name = entries["name"].get().strip(); email = entries["email"].get().strip().lower(); pw = entries["password"].get()
            if not name or not email or not pw:
                messagebox.showwarning("Sign up", "Fill all fields."); return
            users = self.users()
            if email in users:
                messagebox.showerror("Sign up", "That email already has an account."); return
            users[email] = {"name": name, "email": email, "password": pw}
            save_json(USER_FILE, users)
            self.user = users[email]
            self.go_home()
        self.button(form, "Create Account", create, bg=BLUE).pack(fill="x", pady=4)
        self.button(form, "← Back to Login", self.login_screen, bg=CARD2).pack(fill="x", pady=8)

    def google_login(self):
        webbrowser.open("https://accounts.google.com/")
        messagebox.showinfo("Google Sign-in", "The official Google sign-in page was opened. Automatic OAuth account linking requires a backend service, so this desktop version does not pretend that the web page completed authentication.")

    # ---------------- home / navigation ----------------
    def nav(self, parent):
        bar = tk.Frame(parent, bg=PANEL, height=58); bar.pack(fill="x", side="bottom")
        for text, cmd in (("Home", self.go_home), ("Subjects", lambda: self.show_subjects()), ("Notes", lambda: self.show_notes()), ("Questions", lambda: self.show_questions()), ("Quiz", lambda: self.show_quiz()), ("AI", lambda: self.show_ai()), ("Settings", lambda: self.show_settings())):
            self.button(bar, text, cmd, bg=PANEL, fg=MUTED).pack(side="left", expand=True, fill="x", padx=2, pady=5)

    def show_home(self, push=False):
        if push: self.set_screen(lambda: self.show_home(False), "Home", True); return
        self.history.clear(); self.current_screen = lambda: self.show_home(False); self.clear_root()
        top = tk.Frame(self.root, bg=PANEL, height=66); top.pack(fill="x")
        self.label(top, "✦  AI Study Assistant", 17, TEXT, True, bg=PANEL).pack(side="left", padx=20, pady=18)
        self.label(top, "V6", 10, CYAN, True, bg=PANEL).pack(side="left")
        search = tk.Entry(top, textvariable=self.search_var, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", font=self.fs(11), bd=0)
        search.pack(side="left", fill="x", expand=True, padx=25, ipady=9)
        search.bind("<Return>", lambda e: self.perform_search())
        self.button(top, "Search", self.perform_search, bg=BLUE).pack(side="left", padx=5)
        self.button(top, "⚙", lambda: self.show_settings(), bg=PANEL).pack(side="right", padx=6)
        self.label(top, self.user.get("name", "Student"), 10, TEXT, True, bg=PANEL).pack(side="right", padx=10)
        body = ScrollFrame(self.root, BG); body.pack(fill="both", expand=True, padx=16, pady=10); body.activate_wheel(); c=body.inner
        greet = self.card(c); greet.pack(fill="x", padx=8, pady=8)
        self.label(greet, f"Hello {self.user.get('name','Student')} 👋", 24, TEXT, True, bg=CARD).pack(anchor="w", padx=22, pady=(22, 4))
        self.label(greet, "Learn • Practice • Revise • Grow", 11, MUTED, bg=CARD).pack(anchor="w", padx=22, pady=(0,22))
        self.label(c, "Main Subjects", 17, TEXT, True, bg=BG).pack(anchor="w", padx=12, pady=(12,8))
        grid=tk.Frame(c,bg=BG); grid.pack(fill="x", padx=8)
        for i,(group, subs) in enumerate(SUBJECTS.items()):
            f=self.card(grid); f.grid(row=i//2,column=i%2,sticky="nsew",padx=6,pady=6); grid.grid_columnconfigure(i%2,weight=1)
            self.label(f, f"{SUBJECTS and {'Programming':'</>','Core CSE':'▣','Web Development':'◎','AI & Data':'✦'}[group]}  {group}", 15, CYAN, True, bg=CARD).pack(anchor="w",padx=18,pady=(16,5))
            self.label(f, " • ".join(subs[:4]) + (" • more" if len(subs)>4 else ""), 10, MUTED, bg=CARD, wraplength=420, justify="left").pack(anchor="w",padx=18,pady=4)
            self.button(f,"Open →",lambda g=group:self.show_group(g),bg=BLUE_DARK).pack(anchor="w",padx=18,pady=(8,16))
        self.label(c, f"Progress: {len(self.progress)} completed topics", 12, GREEN, True, bg=BG).pack(anchor="w", padx=14, pady=16)
        self.nav(self.root)

    def show_group(self, group):
        self.set_screen(lambda g=group: self._group_screen(g), group, True)
    def _group_screen(self, group):
        c=self.shell(group,"Choose a subject. Every subject has lessons, theory, questions, quiz and practice.")
        for subject in SUBJECTS[group]:
            d=DATA.get(subject,{}); f=self.card(c); f.pack(fill="x",padx=8,pady=6)
            self.label(f,d.get("icon","•")+"  "+subject,15,CYAN,True,bg=CARD).pack(anchor="w",padx=18,pady=(14,3))
            self.label(f,d.get("intro","Core concepts and exam preparation."),10,MUTED,bg=CARD,wraplength=850,justify="left").pack(anchor="w",padx=18,pady=4)
            self.button(f,"Open Subject →",lambda s=subject:self.show_subject(s),bg=BLUE_DARK).pack(anchor="w",padx=18,pady=(6,14))

    def show_subjects(self): self.set_screen(self._subjects_screen,"Subjects",True)
    def _subjects_screen(self):
        c=self.shell("Main Subjects","Select a subject to open the full learning hub.")
        for group in SUBJECTS:
            self.button(c, f"{group}  →", lambda g=group:self.show_group(g), bg=CARD2).pack(fill="x",padx=8,pady=5)

    def show_subject(self, subject):
        self.selected_subject=subject
        self.set_screen(lambda s=subject:self._subject_screen(s), subject, True)
    def _subject_screen(self, subject):
        d=DATA[subject]; c=self.shell(subject,d["intro"])
        f=self.card(c); f.pack(fill="x",padx=8,pady=8)
        self.label(f,"Learning Hub",16,TEXT,True,bg=CARD).pack(anchor="w",padx=18,pady=(16,8))
        for text,cmd in (("📖 Lessons & Theory",lambda s=subject:self.show_lessons(s)),("❓ Important Questions + Answers",lambda s=subject:self.show_subject_questions(s)),("🧠 Quiz",lambda s=subject:self.show_quiz(s)),("💻 Coding Practice",lambda s=subject:self.show_coding(s))):
            self.button(f,text,cmd,bg=CARD2).pack(fill="x",padx=18,pady=5)
        self.label(f,"Topics: "+" • ".join(d["topics"]),10,MUTED,bg=CARD,wraplength=850,justify="left").pack(anchor="w",padx=18,pady=(10,16))

    # ---------------- lessons / notes / questions ----------------
    def show_lessons(self, subject): self.set_screen(lambda s=subject:self._lessons(s),"Lessons",True)
    def _lessons(self, subject):
        d=DATA[subject]; c=self.shell(f"{subject} — Lessons","Click a topic. The theory opens on the same scrollable page.")
        for topic in d["topics"]:
            f=self.card(c); f.pack(fill="x",padx=8,pady=5)
            self.label(f,topic,13,TEXT,True,bg=CARD).pack(side="left",padx=16,pady=14)
            self.button(f,"Open lesson →",lambda s=subject,t=topic:self.show_lesson(s,t),bg=BLUE_DARK).pack(side="right",padx=12,pady=8)
    def show_lesson(self,subject,topic): self.set_screen(lambda s=subject,t=topic:self._lesson(s,t),"Lesson",True)
    def _lesson(self,subject,topic):
        d=DATA[subject]; c=self.shell(f"{subject} — {topic}","Exam-friendly theory with definitions, key points and a quick check.")
        f=self.card(c); f.pack(fill="x",padx=8,pady=8)
        text=self.lesson_text(subject,topic)
        self.label(f,text,12,TEXT,bg=CARD,wraplength=900,justify="left").pack(fill="x",padx=20,pady=20)
        self.button(c,"Mark topic completed ✓",lambda:self.mark_progress(subject,topic),bg=GREEN,fg="#06210e").pack(anchor="w",padx=10,pady=8)
        related=[q for q,a in d["qa"] if normalize(topic) in normalize(q) or normalize(topic).split()[0] in normalize(q)]
        if related:
            self.label(c,"Related questions",15,TEXT,True,bg=BG).pack(anchor="w",padx=10,pady=(18,6))
            for q,a in d["qa"][:4]: self.qa_card(c,q,a)
    def lesson_text(self,subject,topic):
        base={
        "OSI Model":"The OSI reference model divides network communication into seven conceptual layers: Physical, Data Link, Network, Transport, Session, Presentation and Application. Each layer provides services to the layer above and uses services below.",
        "TCP/IP Model":"The TCP/IP architecture groups communication into Link, Internet, Transport and Application layers. IP provides internetwork packet delivery, while TCP and UDP provide different transport services.",
        "Transport Layer":"The Transport layer provides process-to-process communication. Important ideas include port numbers, segmentation, multiplexing, flow control, reliability and congestion control. TCP is reliable and connection-oriented; UDP is connectionless with less protocol overhead.",
        "TCP":"TCP establishes a logical connection, numbers bytes, acknowledges received data and retransmits data when necessary. It also uses flow and congestion control to regulate transmission.",
        "UDP":"UDP sends independent datagrams with a small header. It does not guarantee delivery, ordering or duplicate suppression at the protocol level, making it useful where low overhead or application-controlled reliability is desirable.",
        "DNS":"DNS is a hierarchical distributed naming system. A resolver can obtain records from DNS servers, and common records include A, AAAA, CNAME and MX.",
        "HTTP":"HTTP uses requests and responses. A request has a method such as GET or POST, a target and headers, while a response contains a status code, headers and optional content. HTTPS adds TLS protection.",
        "Deadlocks":"Deadlock requires a set of conditions traditionally described as mutual exclusion, hold-and-wait, no preemption and circular wait. Operating systems can prevent, avoid, detect/recover from, or ignore deadlocks depending on the design.",
        "Processes":"A process is a program in execution. The OS maintains process state and resources and schedules runnable processes on CPUs. Context switching saves one execution context and restores another.",
        "Normalization":"Normalization decomposes relations using dependency information to reduce redundancy and modification anomalies. Normal forms such as 1NF, 2NF, 3NF and BCNF impose progressively stronger structural conditions.",
        "Transactions":"A transaction is a logical unit of database work. ACID means atomicity, consistency, isolation and durability. Concurrency control helps preserve correctness when transactions overlap.",
        "SQL":"SQL supports querying and data manipulation through statements such as SELECT, INSERT, UPDATE and DELETE. Constraints such as PRIMARY KEY, FOREIGN KEY, UNIQUE and CHECK help enforce data rules.",
        "Functions":"Functions package reusable behavior. Good functions have a clear purpose, explicit inputs and predictable outputs; they reduce duplication and make programs easier to test.",
        "Loops":"Loops repeat a block of code. Common patterns include for loops over iterables and while loops controlled by a condition. A loop should have a condition or iteration mechanism that eventually makes progress toward termination.",
        "Classes":"A class defines a type containing data and behavior. An object is an instance of a class. Encapsulation and well-defined interfaces help keep object responsibilities manageable.",
        }
        if topic in base: return base[topic]
        return f"{topic} is an important part of {subject}. Study its definition, purpose, working steps, key components, examples, advantages, limitations and common exam questions. For revision, write the definition first, then a small diagram or flow, followed by 3–5 key points and one example."

    def mark_progress(self,subject,topic):
        self.progress[f"{subject}::{topic}"]=True; save_json(PROGRESS_FILE,self.progress); messagebox.showinfo("Progress","Topic marked complete.")
    def qa_card(self,parent,q,a):
        f=self.card(parent); f.pack(fill="x",padx=8,pady=5)
        self.label(f,"Q. "+q,12,TEXT,True,bg=CARD,wraplength=880,justify="left").pack(anchor="w",padx=16,pady=(13,5))
        self.label(f,"A. "+a,11,MUTED,bg=CARD,wraplength=880,justify="left").pack(anchor="w",padx=16,pady=(0,13))
    def show_subject_questions(self,subject): self.set_screen(lambda s=subject:self._subject_questions(s),"Questions",True)
    def _subject_questions(self,subject):
        c=self.shell(f"{subject} — Important Questions","Use these for 2/5/10-mark preparation.")
        for q,a in DATA[subject]["qa"]: self.qa_card(c,q,a)
        for q,a in EXTRA_QA[:8]: self.qa_card(c,q,a)
    def show_notes(self): self.set_screen(self._notes,"Notes",True)
    def _notes(self):
        c=self.shell("Notes","Theory is stored locally so it opens instantly. Choose a subject, then a lesson.")
        for group,subs in SUBJECTS.items():
            self.label(c,group,15,CYAN,True,bg=BG).pack(anchor="w",padx=8,pady=(10,5))
            for s in subs:
                self.button(c,s,lambda x=s:self.show_lessons(x),bg=CARD).pack(fill="x",padx=8,pady=3)

    # ---------------- quiz ----------------
    def quiz_bank(self, subject=None):
        pool=[]
        if subject:
            pool.extend(DATA[subject]["qa"])
        else:
            for s in all_subjects(): pool.extend(DATA[s]["qa"])
        pool.extend(EXTRA_QA)
        # generate variants so repeated sessions do not show the exact same short set
        return pool
    def show_quiz(self,subject=None): self.set_screen(lambda s=subject:self._quiz_menu(s),"Quiz",True)
    def _quiz_menu(self,subject=None):
        c=self.shell("Quiz","Choose a subject or mixed quiz. New questions are randomized each session.")
        if subject:
            self.button(c,f"Start {subject} Quiz →",lambda:self.start_quiz(subject),bg=BLUE).pack(fill="x",padx=8,pady=8)
        else:
            self.button(c,"Mixed CSE Quiz →",lambda:self.start_quiz(None),bg=BLUE).pack(fill="x",padx=8,pady=8)
            for g,subs in SUBJECTS.items():
                self.label(c,g,14,CYAN,True,bg=BG).pack(anchor="w",padx=8,pady=(14,4))
                for s in subs: self.button(c,s,lambda x=s:self.start_quiz(x),bg=CARD).pack(fill="x",padx=8,pady=2)
    def start_quiz(self,subject=None):
        bank=self.quiz_bank(subject)
        random.shuffle(bank)
        questions=bank[:min(12,len(bank))]
        state={"subject":subject,"questions":questions,"i":0,"score":0}
        self.set_screen(lambda st=state:self._quiz_question(st),"Quiz",True)
    def _quiz_question(self,state):
        if state["i"]>=len(state["questions"]):
            self.quiz_result(state); return
        q,a=state["questions"][state["i"]]
        c=self.shell("Quiz Question",f"Question {state['i']+1} of {len(state['questions'])} • Score {state['score']}")
        f=self.card(c); f.pack(fill="x",padx=8,pady=8)
        self.label(f,q,17,TEXT,True,bg=CARD,wraplength=900,justify="left").pack(anchor="w",padx=20,pady=20)
        # create MCQ by mixing correct answer with other answers
        answers=[a]
        others=[x[1] for x in self.quiz_bank(state["subject"]) if x[1]!=a]
        random.shuffle(others); answers += others[:3]; random.shuffle(answers)
        for ans in answers:
            self.button(c,ans,lambda x=ans,correct=a,st=state:self.answer_quiz(st,x,correct),bg=CARD2).pack(fill="x",padx=12,pady=4)
    def answer_quiz(self,state,chosen,correct):
        if chosen==correct: state["score"]+=1; messagebox.showinfo("Correct","Correct answer ✓")
        else: messagebox.showinfo("Answer",f"Not quite.\n\nCorrect answer:\n{correct}")
        state["i"]+=1
        self.current_screen=lambda st=state:self._quiz_question(st)
        self.clear_root(); self._quiz_question(state)
    def quiz_result(self,state):
        c=self.shell("Quiz Result","Session complete")
        total=len(state["questions"]); pct=round(state["score"]*100/total) if total else 0
        f=self.card(c); f.pack(fill="x",padx=8,pady=10)
        self.label(f,f"{state['score']} / {total}",30,CYAN,True,bg=CARD).pack(pady=(25,5))
        self.label(f,f"Score: {pct}%",16,TEXT,True,bg=CARD).pack(pady=5)
        self.button(f,"Try another quiz",lambda:self.start_quiz(state["subject"]),bg=BLUE).pack(pady=18)

    # ---------------- coding ----------------
    def show_coding(self,subject=None): self.set_screen(lambda s=subject:self._coding(s),"Coding Practice",True)
    def _coding(self,subject=None):
        c=self.shell("Coding Practice","Choose a language/task. The model solution is always available locally.")
        tasks=[
            ("Python","Write a function that returns the sum of two numbers.","def add(a, b):\n    return a + b"),
            ("C","Print the sum of two integers.","#include <stdio.h>\nint main(void) {\n    int a=10, b=20;\n    printf(\"%d\\n\", a+b);\n    return 0;\n}"),
            ("Java","Create a class Student with a name field.","class Student {\n    String name;\n    Student(String name) { this.name = name; }\n}"),
            ("HTML","Create a heading and a paragraph.","<h1>AI Study Assistant</h1>\n<p>Learn every day.</p>"),
            ("CSS","Create a card with padding and rounded corners.",".card { padding: 20px; border-radius: 12px; }"),
            ("JavaScript","Print a message when a button is clicked.","document.querySelector('#btn').addEventListener('click', () => {\n  console.log('Clicked');\n});"),
            ("SQL","Select students with marks 70 or above.","SELECT * FROM students WHERE marks >= 70;"),
            ("Git","Show the basic first-commit workflow.","git init\ngit add .\ngit commit -m \"first commit\""),
        ]
        for lang,task,solution in tasks:
            f=self.card(c); f.pack(fill="x",padx=8,pady=6)
            self.label(f,f"{lang} • Practice",14,CYAN,True,bg=CARD).pack(anchor="w",padx=16,pady=(14,4))
            self.label(f,task,11,TEXT,bg=CARD,wraplength=880,justify="left").pack(anchor="w",padx=16,pady=4)
            self.button(f,"Open Practice →",lambda l=lang,t=task,s=solution:self.coding_editor(l,t,s),bg=BLUE_DARK).pack(anchor="w",padx=16,pady=(7,14))
    def coding_editor(self,lang,task,solution):
        self.set_screen(lambda:self._coding_editor(lang,task,solution),"Code Editor",True)
    def _coding_editor(self,lang,task,solution):
        c=self.shell(f"{lang} Practice","Write your solution, then compare it with the model solution.")
        f=self.card(c); f.pack(fill="both",expand=True,padx=8,pady=8)
        self.label(f,"Task: "+task,12,TEXT,True,bg=CARD,wraplength=880,justify="left").pack(anchor="w",padx=16,pady=14)
        editor=tk.Text(f,bg="#06111f",fg=TEXT,insertbackground=CYAN,font=("Consolas",12),relief="flat",height=12,wrap="none")
        editor.pack(fill="both",expand=True,padx=16,pady=8)
        editor.insert("1.0",solution)
        actions=tk.Frame(f,bg=CARD); actions.pack(fill="x",padx=16,pady=8)
        self.button(actions,"Reset",lambda:(editor.delete("1.0","end"),editor.insert("1.0",solution)),bg=CARD2).pack(side="left",padx=4)
        self.button(actions,"Model Solution",lambda:self.show_solution(lang,solution),bg=BLUE).pack(side="left",padx=4)
        self.button(actions,"Copy",lambda:self.copy_text(editor),bg=GREEN,fg="#06210e").pack(side="left",padx=4)
        self.label(f,"Note: this V6 desktop practice editor does not execute arbitrary code. It is intentionally a safe editor + model-solution comparison.",9,MUTED,bg=CARD,wraplength=850,justify="left").pack(anchor="w",padx=16,pady=(4,16))
    def show_solution(self,lang,solution):
        win=tk.Toplevel(self.root); win.title("Model Solution — "+lang); win.geometry("760x500"); win.configure(bg=BG)
        self.label(win,"Model Solution",17,CYAN,True,bg=BG).pack(anchor="w",padx=18,pady=12)
        t=tk.Text(win,bg="#06111f",fg=TEXT,font=("Consolas",11),wrap="none",relief="flat"); t.pack(fill="both",expand=True,padx=18,pady=8); t.insert("1.0",solution); t.configure(state="disabled")
        self.button(win,"Close",win.destroy,bg=BLUE).pack(pady=10)
    def copy_text(self,widget):
        self.root.clipboard_clear(); self.root.clipboard_append(widget.get("1.0","end-1c")); self.root.update(); messagebox.showinfo("Copied","Code copied to clipboard.")

    # ---------------- AI assistant ----------------
    def show_ai(self): self.set_screen(self._ai,"AI Assistant",True)
    def _ai(self):
        c=self.shell("AI Assistant","Ask any academic question: CN, OS, DBMS, AI, Python, HTML, DSA, or general study topics.")
        chat=tk.Frame(c,bg=BG); chat.pack(fill="x",padx=8,pady=5)
        self.ai_output=tk.Text(chat,bg="#06111f",fg=TEXT,font=self.fs(11),wrap="word",height=22,relief="flat",state="disabled")
        self.ai_output.pack(fill="both",expand=True)
        input_box=tk.Frame(c,bg=BG); input_box.pack(fill="x",padx=8,pady=8)
        self.ai_entry=tk.Entry(input_box,bg=CARD,fg=TEXT,insertbackground=TEXT,font=self.fs(12),relief="flat",bd=0)
        self.ai_entry.pack(side="left",fill="x",expand=True,ipady=11,padx=(0,8)); self.ai_entry.bind("<Return>",lambda e:self.ask_ai())
        self.button(input_box,"Ask →",self.ask_ai,bg=BLUE).pack(side="right")
        self.ai_entry.focus_set()
        if not self.chat_history:
            self.append_ai("AI", "Hi! Ask me something like: 'Explain CN', 'What is TCP?', 'Explain normalization', or any other study question.")
        else:
            for role,text in self.chat_history[-12:]: self.append_ai(role,text)
    def append_ai(self,role,text):
        self.ai_output.configure(state="normal"); self.ai_output.insert("end",f"{role}:\n{text}\n\n"); self.ai_output.see("end"); self.ai_output.configure(state="disabled")
    def ask_ai(self):
        q=self.ai_entry.get().strip()
        if not q: return
        self.ai_entry.delete(0,"end")
        self.chat_history.append(("You",q)); self.append_ai("You",q)
        local=self.local_answer(q)
        if local:
            self.chat_history.append(("AI",local)); self.append_ai("AI",local); return
        self.append_ai("AI","Thinking…")
        threading.Thread(target=self._ollama_worker,args=(q,),daemon=True).start()
    def local_answer(self,q):
        nq=normalize(q)
        subject=subject_for_query(nq)
        # Exact/near exact local Q&A is instant.
        best=None; best_score=0
        corpus=[]
        for s in all_subjects():
            for question,answer in DATA[s]["qa"]: corpus.append((s,question,answer))
        corpus += [("General",q,a) for q,a in EXTRA_QA]
        words=set(nq.split())
        for s,question,answer in corpus:
            qwords=set(normalize(question).split())
            score=len(words & qwords)
            if subject==s: score += 2
            if normalize(question) in nq or nq in normalize(question): score += 8
            if score>best_score and score>=2: best_score=score; best=(s,question,answer)
        if best:
            s,question,answer=best
            return f"{s}\n\n{answer}\n\nExam tip: Start with the definition, then explain the working/components, followed by a small example or diagram."
        # Topic-only questions such as "explain cn".
        if subject:
            d=DATA[subject]
            return f"{subject}\n\n{d['intro']}\n\nKey topics: {', '.join(d['topics'])}.\n\nAsk a specific topic such as '{d['topics'][0]}' or 'What is TCP?' for a focused answer."
        return None
    def _ollama_worker(self,q):
        answer=self.ollama_answer(q)
        self.root.after(0,lambda:self.finish_ollama(q,answer))
    def finish_ollama(self,q,answer):
        # rebuild output to remove the Thinking line cleanly
        if self.current_screen != self._ai and self.ai_output.winfo_exists():
            pass
        try:
            self.ai_output.configure(state="normal"); self.ai_output.delete("1.0","end"); self.ai_output.configure(state="disabled")
            for role,text in self.chat_history[-12:]: self.append_ai(role,text)
            self.append_ai("AI",answer); self.chat_history.append(("AI",answer))
        except tk.TclError: pass
    def ollama_answer(self,q):
        prompt=("You are a fast college study assistant. Answer clearly and accurately. "
                "If the user asks a Computer Networks, OS, DBMS, AI, programming or web topic, give definition, key working points, example and exam tip. "
                "Do not claim an answer is from a textbook unless source text was supplied. Keep the answer concise.\n\nQuestion: "+q)
        for model in OLLAMA_MODELS:
            payload={"model":model,"messages":[{"role":"user","content":prompt}],"stream":False,"keep_alive":"5m"}
            try:
                req=urllib.request.Request(OLLAMA_URL,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
                with urllib.request.urlopen(req,timeout=12) as response:
                    data=json.loads(response.read().decode("utf-8"))
                text=data.get("message",{}).get("content","").strip()
                if text: return text
            except Exception:
                continue
        return "I couldn't reach the local AI model right now. But I can answer from the built-in study knowledge. Try a topic such as 'Explain CN', 'What is TCP?', 'What is DBMS?', or open the subject's Lessons/Questions section."

    # ---------------- search ----------------
    def perform_search(self):
        q=self.search_var.get().strip()
        if not q: return
        self.set_screen(lambda query=q:self._search_results(query),"Search",True)
    def _search_results(self,q):
        c=self.shell("Search Results",f"Results for: {q}")
        nq=normalize(q); found=[]
        for s in all_subjects():
            d=DATA[s]
            hay=normalize(s+" "+d["intro"]+" "+" ".join(d["topics"])+" "+" ".join(x[0] for x in d["qa"]))
            if any(w in hay for w in nq.split()): found.append(s)
        for s in found[:20]: self.button(c,s+" →",lambda x=s:self.show_subject(x),bg=CARD).pack(fill="x",padx=8,pady=4)
        # Q&A results
        shown=0
        for s in all_subjects():
            for question,answer in DATA[s]["qa"]:
                if any(w in normalize(question+" "+answer) for w in nq.split()):
                    self.qa_card(c,question,answer); shown+=1
                    if shown>=20: break
            if shown>=20: break
        if not found and not shown: self.label(c,"No local result. Try the AI Assistant for a generated explanation.",12,MUTED,bg=BG).pack(padx=12,pady=25)

    # ---------------- settings / progress ----------------
    def show_settings(self): self.set_screen(self._settings,"Settings",True)
    def _settings(self):
        c=self.shell("Settings","Controls are active and saved locally.")
        f=self.card(c); f.pack(fill="x",padx=8,pady=8)
        self.label(f,"Account",15,CYAN,True,bg=CARD).pack(anchor="w",padx=18,pady=(16,5))
        self.label(f,f"Name: {self.user.get('name')}\nEmail: {self.user.get('email')}",11,MUTED,bg=CARD,justify="left").pack(anchor="w",padx=18,pady=5)
        self.button(f,"Logout",self.logout,bg=RED).pack(anchor="w",padx=18,pady=(8,16))
        f2=self.card(c); f2.pack(fill="x",padx=8,pady=8)
        self.label(f2,"Display Size",15,CYAN,True,bg=CARD).pack(anchor="w",padx=18,pady=(16,6))
        for text,scale in (("Small",0.9),("Normal",1.0),("Large",1.1),("Extra Large",1.2)):
            self.button(f2,text,lambda x=scale:self.change_scale(x),bg=CARD2).pack(side="left",padx=5,pady=(4,16))
        f3=self.card(c); f3.pack(fill="x",padx=8,pady=8)
        self.label(f3,"Progress",15,CYAN,True,bg=CARD).pack(anchor="w",padx=18,pady=(16,6))
        self.label(f3,f"Completed topics: {len(self.progress)}",11,MUTED,bg=CARD).pack(anchor="w",padx=18,pady=4)
        self.button(f3,"Reset Progress",self.reset_progress,bg=RED).pack(anchor="w",padx=18,pady=(8,16))
    def change_scale(self,scale):
        self.font_scale=scale
        self.show_settings()
    def reset_progress(self):
        if messagebox.askyesno("Reset", "Reset all local progress?"):
            self.progress={}; save_json(PROGRESS_FILE,self.progress); self.show_settings()
    def logout(self): self.user=None; self.history.clear(); self.login_screen()


def main():
    root=tk.Tk()
    app=AIStudyAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
