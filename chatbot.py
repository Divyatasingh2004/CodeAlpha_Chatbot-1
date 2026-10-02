import tkinter as tk
from tkinter import ttk
import difflib
import threading
import random
import datetime

class AuroraAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Divyata")
        self.root.geometry("720x860")
        self.root.config(bg="#060b19")

        self.user_name = "Friend"
        self.is_typing = False

        # --- Top Header Bar (Glassmorphic Style) ---
        header_frame = tk.Frame(root, bg="#0b1229", pady=16, padx=20)
        header_frame.pack(fill=tk.X)
        
        # Back / Menu Icon
        tk.Label(header_frame, text="←", font=("Segoe UI", 14, "bold"), bg="#0b1229", fg="#94a3b8", cursor="hand2").pack(side=tk.LEFT, padx=(0, 10))

        # Simulated AI Avatar Icon with Glow Effect
        avatar_container = tk.Frame(header_frame, bg="#3b82f6", padx=2, pady=2)
        avatar_container.pack(side=tk.LEFT)
        tk.Label(avatar_container, text="✨", font=("Segoe UI", 10), bg="#0f172a", fg="#38bdf8", padx=6, pady=2).pack()
        
        title_container = tk.Frame(header_frame, bg="#0b1229")
        title_container.pack(side=tk.LEFT, padx=12)
        
        tk.Label(title_container, text="AURORA NEURAL AI", font=("Segoe UI", 11, "bold"), bg="#0b1229", fg="#ffffff").pack(anchor=tk.W)
        
        status_row = tk.Frame(title_container, bg="#0b1229")
        status_row.pack(anchor=tk.W)
        tk.Label(status_row, text="●", font=("Segoe UI", 8), bg="#0b1229", fg="#22c55e").pack(side=tk.LEFT)
        self.status_lbl = tk.Label(status_row, text=" Online • Neural Engine Active", font=("Segoe UI", 8), bg="#0b1229", fg="#64748b")
        self.status_lbl.pack(side=tk.LEFT)

        # --- Quick Action Pill Buttons Bar ---
        action_bar = tk.Frame(root, bg="#060b19", pady=8, padx=20)
        action_bar.pack(fill=tk.X)

        actions = ["⚡ Capabilities", "🛠️ Code Assistant", "🚀 Project Help", "💡 Clear Chat"]
        for act in actions:
            btn = tk.Button(action_bar, text=act, font=("Segoe UI", 9), 
                            bg="#111c38", fg="#93c5fd", activebackground="#1e293b", activeforeground="#ffffff",
                            relief=tk.FLAT, bd=0, padx=12, pady=6, cursor="hand2",
                            command=lambda a=act: self.handle_quick_action(a))
            btn.pack(side=tk.LEFT, padx=4)

        # --- Main Scrollable Chat Container (Bubble UI) ---
        self.chat_container = tk.Canvas(root, bg="#060b19", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.chat_container.yview)
        
        self.scrollable_frame = tk.Frame(self.chat_container, bg="#060b19")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.chat_container.configure(scrollregion=self.chat_container.bbox("all"))
        )

        self.chat_container.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.chat_container.configure(yscrollcommand=self.scrollbar.set)

        self.chat_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Bottom Input Control Bar ---
        input_wrapper = tk.Frame(root, bg="#060b19", pady=15, padx=20)
        input_wrapper.pack(fill=tk.X, side=tk.BOTTOM)

        input_pill = tk.Frame(input_wrapper, bg="#0f172a", highlightbackground="#1e3a8a", highlightthickness=1)
        input_pill.pack(fill=tk.X, ipady=8, ipadx=12)

        mic_btn = tk.Button(input_pill, text="🎙️", font=("Segoe UI", 11), bg="#0f172a", fg="#38bdf8", 
                            relief=tk.FLAT, bd=0, activebackground="#0f172a", cursor="hand2",
                            command=lambda: self.add_message("AURORA", "Voice module is in standby mode. Type your query below!"))
        mic_btn.pack(side=tk.LEFT, padx=(2, 6))

        att_btn = tk.Button(input_pill, text="📎", font=("Segoe UI", 11), bg="#0f172a", fg="#64748b", 
                            relief=tk.FLAT, bd=0, activebackground="#0f172a", cursor="hand2")
        att_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.user_entry = tk.Entry(input_pill, font=("Segoe UI", 11), bg="#0f172a", fg="#ffffff", 
                                  insertbackground="#38bdf8", relief=tk.FLAT, bd=0)
        self.user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.user_entry.bind("<Return>", lambda event: self.handle_user_message())
        
        send_btn = tk.Button(input_pill, text="➔", font=("Segoe UI", 12, "bold"), 
                             bg="#2563eb", fg="#ffffff", activebackground="#1d4ed8", activeforeground="#ffffff",
                             relief=tk.FLAT, padx=14, pady=4, cursor="hand2", command=self.handle_user_message)
        send_btn.pack(side=tk.RIGHT, padx=2)

        # --- Initial Welcome Sequence ---
        self.start_intro()

    def start_intro(self):
        self.add_message("AURORA", "✨ Initializing Neural Core... Hello! I am AURORA, your advanced AI assistant.")
        self.root.after(1000, lambda: self.add_message("AURORA", "Before we begin, what should I call you? (Type your name below)"))

    def add_message(self, sender, text):
        msg_row = tk.Frame(self.scrollable_frame, bg="#060b19", pady=6)
        msg_row.pack(fill=tk.X, expand=True)

        if sender == "USER":
            bubble = tk.Frame(msg_row, bg="#1d4ed8", padx=16, pady=12)
            bubble.pack(side=tk.RIGHT, anchor=tk.E, padx=(60, 0))
            lbl = tk.Label(bubble, text=text, font=("Segoe UI", 10), bg="#1d4ed8", fg="#ffffff", wraplength=420, justify=tk.LEFT)
            lbl.pack()
        else:
            bubble = tk.Frame(msg_row, bg="#0f172a", padx=16, pady=12, highlightbackground="#1e293b", highlightthickness=1)
            bubble.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 60))
            lbl = tk.Label(bubble, text=text, font=("Segoe UI", 10), bg="#0f172a", fg="#e2e8f0", wraplength=420, justify=tk.LEFT)
            lbl.pack()

        self.chat_container.update_idletasks()
        self.chat_container.yview_moveto(1.0)
        return lbl

    def stream_response(self, full_text):
        """Streams response letter by letter like modern AI interfaces"""
        msg_row = tk.Frame(self.scrollable_frame, bg="#060b19", pady=6)
        msg_row.pack(fill=tk.X, expand=True)

        bubble = tk.Frame(msg_row, bg="#0f172a", padx=16, pady=12, highlightbackground="#1e293b", highlightthickness=1)
        bubble.pack(side=tk.LEFT, anchor=tk.W, padx=(0, 60))
        
        lbl = tk.Label(bubble, text="", font=("Segoe UI", 10), bg="#0f172a", fg="#e2e8f0", wraplength=420, justify=tk.LEFT)
        lbl.pack()

        self.status_lbl.config(text=" Speaking...", fg="#38bdf8")

        def append_char(index=0):
            if index <= len(full_text):
                lbl.config(text=full_text[:index])
                self.chat_container.update_idletasks()
                self.chat_container.yview_moveto(1.0)
                self.root.after(12, lambda: append_char(index + 1))
            else:
                self.status_lbl.config(text=" Online • Neural Engine Active", fg="#64748b")
                self.is_typing = False

        append_char()

    def handle_quick_action(self, action_text):
        if self.is_typing: return
        if "Capabilities" in action_text:
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, "What are your core capabilities?")
            self.handle_user_message()
        elif "Code Assistant" in action_text:
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, "Help me write Python code.")
            self.handle_user_message()
        elif "Project Help" in action_text:
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, "I need project architecture help.")
            self.handle_user_message()
        elif "Clear Chat" in action_text:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.start_intro()

    def generate_response(self, query):
        q = query.lower().strip()
        
        # Capture name if it's the first turn or name setting
        if any(w in q for w in ["my name is", "i am", "call me"]) or len(q.split()) == 1 and not any(k in q for k in ["hi", "hello", "bye", "help", "time"]):
            words = q.split()
            potential_name = words[-1].capitalize()
            if potential_name not in ["Hi", "Hello", "Hey", "Bot", "Aurora"]:
                self.user_name = potential_name
                return f"Got it, {self.user_name}! I've stored your name in my neural memory. How can I help you today?"

        if any(w in q for w in ["hi", "hello", "hey", "greetings", "hii"]):
            return f"Hello there, {self.user_name}! It's great to interact with you. How can I assist your workflow today?"
        if any(w in q for w in ["how are you", "aur batao"]):
            return f"All neural networks are operating at 100% capacity, {self.user_name}! Ready to build amazing things."
        if any(w in q for w in ["bye", "exit", "quit", "goodbye"]):
            return f"Goodbye, {self.user_name}! Shutting down active threads. Have an incredible day!"
        if any(w in q for w in ["thank", "thanks", "thx"]):
            return f"You're very welcome, {self.user_name}! Let me know if you need any other code or assistance."
        if any(w in q for w in ["time", "date"]):
            current_time = datetime.datetime.now().strftime('%I:%M %p, %A, %B %d, %Y')
            return f"System clock time: {current_time} 🕒"

        faqs = {
            "capabilities": "I specialize in full-stack code architecture, Python scripting, UI/UX design, debugging complex algorithms, and rapid prototyping.",
            "code assistant": "Drop your snippet or describe your bug. I can assist in Python, JavaScript, C#, Java, and Tkinter UI development!",
            "project help": "I can structure your project folders, write modular code, help with Git workflows, or assist with database and frontend design.",
            "return policy": "You can return any product within 30 days of purchase for a full refund, provided it is in original packaging.",
            "track order": "Once dispatched, you will receive an SMS and email containing your live tracking link.",
            "reset password": "Click on 'Forgot Password' on the login screen, enter your registered email, and follow the secure reset link."
        }

        for key, ans in faqs.items():
            if key in q:
                return ans

        matches = difflib.get_close_matches(q, list(faqs.keys()), n=1, cutoff=0.3)
        if matches:
            return f"Did you mean to ask about {matches[0]}? Here is the info: {faqs[matches[0]]}"

        return f"That's a fascinating query, {self.user_name}. I'm continuously learning—could you rephrase or ask about programming, debugging, or our core services?"

    def handle_user_message(self):
        if self.is_typing:
            return
            
        text = self.user_entry.get()
        if not text.strip():
            return
        
        self.add_message("USER", text)
        self.user_entry.delete(0, tk.END)
        self.is_typing = True
        
        # Show "Thinking..." status indicator
        self.status_lbl.config(text=" Processing query...", fg="#f59e0b")

        def process_reply():
            response = self.generate_response(text)
            # Use root.after to safely update UI from thread
            self.root.after(600, lambda: self.stream_response(response))

        threading.Thread(target=process_reply, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuroraAIApp(root)
    root.mainloop()