#!/usr/bin/env python3
"""
uae_history_quiz_gui.py — simple Tkinter GUI for the UAE history quiz.

This version imports the QUESTIONS data from the CLI script (uae_history_quiz.py)
so questions stay in a single place.

Run:
    python3 test/uae_history_quiz_gui.py

If the GUI script is placed in the same directory as uae_history_quiz.py, it will
import QUESTIONS directly. If you run it from another directory, it will attempt
to load uae_history_quiz.py by path next to this file.
"""
import random
import sys
import os
import importlib.util
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Try a normal import first (works if running from the same directory or package)
try:
    from uae_history_quiz import QUESTIONS  # type: ignore
except Exception:
    # Fallback: load by path relative to this file
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(this_dir, "uae_history_quiz.py")
    if not os.path.exists(candidate):
        raise ImportError(
            "Could not import QUESTIONS from uae_history_quiz.py. "
            f"Checked {candidate}"
        )
    spec = importlib.util.spec_from_file_location("uae_history_quiz", candidate)
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)  # type: ignore
    QUESTIONS = getattr(module, "QUESTIONS")


class QuizGUI(tk.Tk):
    def __init__(self, questions):
        super().__init__()
        self.title("UAE History Quiz")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Quiz state
        self.all_questions = questions[:]
        random.shuffle(self.all_questions)
        self.num_questions = len(self.all_questions)
        self.current_index = 0
        self.score = 0
        self.wrong = []  # list of tuples (index, question, given_answer)

        # Selected answer variable
        self.selected = tk.StringVar(value="")  # "", "A", "B", "C", "D"

        # UI elements
        self._build_widgets()
        self._load_question()

    def _build_widgets(self):
        pad = {"padx": 10, "pady": 8}
        header = ttk.Label(self, text="United Arab Emirates — History Quiz", font=("Segoe UI", 14, "bold"))
        header.grid(row=0, column=0, columnspan=2, **pad)

        self.progress_label = ttk.Label(self, text="")
        self.progress_label.grid(row=1, column=0, columnspan=2)

        self.question_label = ttk.Label(self, text="", wraplength=480, justify="left", font=("Segoe UI", 11))
        self.question_label.grid(row=2, column=0, columnspan=2, sticky="w", **pad)

        self.radio_frame = ttk.Frame(self)
        self.radio_frame.grid(row=3, column=0, columnspan=2, sticky="w", **pad)

        # Create radio buttons for options A-D
        self.option_vars = {}
        for i, opt_key in enumerate(("A", "B", "C", "D")):
            rb = ttk.Radiobutton(
                self.radio_frame,
                text="",
                variable=self.selected,
                value=opt_key,
            )
            rb.grid(row=i, column=0, sticky="w", pady=2)
            self.option_vars[opt_key] = rb

        self.feedback_label = ttk.Label(self, text="", foreground="blue", wraplength=480, justify="left")
        self.feedback_label.grid(row=4, column=0, columnspan=2, sticky="w", **pad)

        self.next_button = ttk.Button(self, text="Submit", command=self._on_next)
        self.next_button.grid(row=5, column=0, sticky="e", padx=10, pady=(0, 12))

        self.restart_button = ttk.Button(self, text="Restart", command=self._on_restart)
        self.restart_button.grid(row=5, column=1, sticky="w", padx=10, pady=(0, 12))

    def _load_question(self):
        """Load current question into the UI."""
        self.selected.set("")
        self.feedback_label.config(text="")
        q = self.all_questions[self.current_index]
        idx = self.current_index + 1
        self.progress_label.config(text=f"Question {idx} of {self.num_questions}")
        self.question_label.config(text=q["question"])

        # Update radio text labels
        for key, rb in self.option_vars.items():
            text = f"{key}. {q['options'].get(key, '')}"
            rb.config(text=text, state="normal")

        self.next_button.config(text="Submit", state="normal")

    def _on_next(self):
        """Handles Submit -> evaluate -> change to Next, and Next -> advance."""
        if self.next_button.cget("text") == "Submit":
            chosen = self.selected.get()
            if not chosen:
                messagebox.showinfo("Choose an answer", "Please select A, B, C, or D before submitting.")
                return
            self._evaluate_answer(chosen)
            self.next_button.config(text="Next")
            # disable radiobuttons after submit
            for rb in self.option_vars.values():
                rb.config(state="disabled")
        else:  # Next
            self.current_index += 1
            if self.current_index >= self.num_questions:
                self._show_results()
            else:
                self._load_question()

    def _evaluate_answer(self, chosen):
        q = self.all_questions[self.current_index]
        correct = q["answer"].upper()
        if chosen == correct:
            self.score += 1
            self.feedback_label.config(text="Correct! ✓", foreground="green")
        else:
            self.feedback_label.config(
                text=f"Incorrect. Correct answer: {correct}. {q.get('explanation','')}",
                foreground="red"
            )
            self.wrong.append((self.current_index + 1, q, chosen))

    def _show_results(self):
        percent = (self.score / self.num_questions) * 100 if self.num_questions else 0
        msg = f"Quiz complete!\nScore: {self.score}/{self.num_questions} ({percent:.1f}%)"
        messagebox.showinfo("Results", msg)
        # Open a review window
        review = tk.Toplevel(self)
        review.title("Review of incorrect answers")
        review.geometry("560x360")
        txt = scrolledtext.ScrolledText(review, wrap="word", padx=10, pady=10, state="normal")
        txt.pack(expand=True, fill="both")
        if not self.wrong:
            txt.insert("end", "You answered all questions correctly. Well done!\n")
        else:
            for idx, q, given in self.wrong:
                correct = q["answer"]
                txt.insert("end", f"Question {idx}: {q['question']}\n")
                txt.insert("end", f"  Your answer: {given} — {q['options'].get(given, 'N/A')}\n")
                txt.insert("end", f"  Correct: {correct} — {q['options'][correct]}\n")
                if q.get("explanation"):
                    txt.insert("end", f"  Explanation: {q['explanation']}\n")
                txt.insert("end", "\n")
        txt.config(state="disabled")

        # Offer to restart from results window too
        def restart_from_review():
            review.destroy()
            self._on_restart()

        btn_frame = ttk.Frame(review)
        btn_frame.pack(fill="x", pady=6)
        ttk.Button(btn_frame, text="Restart Quiz", command=restart_from_review).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Close", command=review.destroy).pack(side="right", padx=8)

    def _on_restart(self):
        """Reset state and reshuffle questions."""
        if messagebox.askyesno("Restart", "Do you want to restart the quiz?"):
            random.shuffle(self.all_questions)
            self.current_index = 0
            self.score = 0
            self.wrong = []
            self._load_question()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.destroy()


def main():
    app = QuizGUI(QUESTIONS)
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
