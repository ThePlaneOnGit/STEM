#!/usr/bin/env python3
"""
uae_history_quiz.py — small interactive, terminal-based quiz about the history of the UAE.

Make executable:
    chmod +x test/uae_history_quiz.py

Run:
    ./test/uae_history_quiz.py

The quiz presents multiple-choice questions, validates input, randomizes question order,
shows explanations for incorrect answers, and prints a final score.
"""

import random
import sys

QUESTIONS = [
    {
        "question": "When is the United Arab Emirates National Day celebrated (the date the union was founded)?",
        "options": {
            "A": "January 1, 1971",
            "B": "June 18, 1971",
            "C": "December 2, 1971",
            "D": "February 7, 1972",
        },
        "answer": "C",
        "explanation": "The UAE was formed on December 2, 1971. This date is celebrated as National Day."
    },
    {
        "question": "Who is widely recognized as the 'Founding Father' of the UAE?",
        "options": {
            "A": "Sheikh Rashid bin Saeed Al Maktoum",
            "B": "Sheikh Zayed bin Sultan Al Nahyan",
            "C": "Sheikh Khalifa bin Zayed Al Nahyan",
            "D": "Sheikh Saud bin Rashid Al Mualla",
        },
        "answer": "B",
        "explanation": "Sheikh Zayed bin Sultan Al Nahyan of Abu Dhabi played the leading role in founding the UAE."
    },
    {
        "question": "How many emirates originally joined the federation on December 2, 1971?",
        "options": {
            "A": "Five",
            "B": "Six",
            "C": "Seven",
            "D": "Four",
        },
        "answer": "B",
        "explanation": "Six emirates formed the federation on December 2, 1971 (Abu Dhabi, Dubai, Sharjah, Ajman, Umm al-Quwain, and Fujairah). Ras Al Khaimah joined in early 1972, bringing the total to seven."
    },
    {
        "question": "Before the federation, what was the collective name used for the group of sheikhdoms on the southeastern Persian Gulf coast under British treaties?",
        "options": {
            "A": "Trucial States",
            "B": "Gulf Sultanates",
            "C": "Eastern Emirates",
            "D": "Maritime Confederation",
        },
        "answer": "A",
        "explanation": "They were commonly known as the Trucial States due to a series of truces and treaty relationships with Britain."
    },
    {
        "question": "Which emirate is the capital of the UAE?",
        "options": {
            "A": "Dubai",
            "B": "Sharjah",
            "C": "Abu Dhabi",
            "D": "Ajman",
        },
        "answer": "C",
        "explanation": "Abu Dhabi is the capital of the UAE and is the seat of the federal government."
    },
    {
        "question": "In which decade were commercial oil exports first discovered and developed in the area that became the UAE?",
        "options": {
            "A": "1910s",
            "B": "1930s",
            "C": "1950s",
            "D": "1970s",
        },
        "answer": "C",
        "explanation": "Significant oil discoveries in the region occurred in the 1950s and 1960s, accelerating economic and social change."
    },
    {
        "question": "Which city is famous for rapid trade and later turned into a global business and tourism hub, notably under the leadership of Sheikh Rashid bin Saeed Al Maktoum?",
        "options": {
            "A": "Al Ain",
            "B": "Dubai",
            "C": "Fujairah",
            "D": "Ras Al Khaimah",
        },
        "answer": "B",
        "explanation": "Dubai developed rapidly from a trading port into an international center for business and tourism."
    },
    {
        "question": "What is the official language of the United Arab Emirates?",
        "options": {
            "A": "English",
            "B": "Persian",
            "C": "Arabic",
            "D": "Urdu",
        },
        "answer": "C",
        "explanation": "Arabic is the official language of the UAE."
    },
    {
        "question": "Which body is the UAE's highest constitutional authority, composed of the rulers of the emirates?",
        "options": {
            "A": "Federal National Council",
            "B": "Council of Ministers",
            "C": "Federal Supreme Council",
            "D": "Consultative Assembly",
        },
        "answer": "C",
        "explanation": "The Federal Supreme Council, made up of the rulers of the emirates, is the highest constitutional authority."
    },
    {
        "question": "Which emirate joined the UAE after the initial formation in December 1971, completing the seven emirates?",
        "options": {
            "A": "Ras Al Khaimah",
            "B": "Sharjah",
            "C": "Fujairah",
            "D": "Ajman",
        },
        "answer": "A",
        "explanation": "Ras Al Khaimah joined the federation in February 1972."
    }
]


def ask_question(qnum, qdata):
    print(f"\nQuestion {qnum}: {qdata['question']}")
    for key in sorted(qdata["options"].keys()):
        print(f"  {key}. {qdata['options'][key]}")
    while True:
        ans = input("Your answer (A/B/C/D) > ").strip().upper()
        if ans in qdata["options"]:
            return ans
        if ans in ("QUIT", "EXIT"):
            print("Exiting quiz. Goodbye!")
            sys.exit(0)
        print("Please enter one of A, B, C, or D (or type 'quit' to exit).")


def run_quiz(num_questions=None):
    qpool = QUESTIONS[:]
    random.shuffle(qpool)
    if num_questions is None or num_questions <= 0 or num_questions > len(qpool):
        num_questions = len(qpool)
    selected = qpool[:num_questions]

    print("Welcome to the United Arab Emirates — History Quiz!")
    print(f"There are {num_questions} questions. Type 'quit' to exit at any time.\n")

    score = 0
    wrong = []

    for i, q in enumerate(selected, start=1):
        user_ans = ask_question(i, q)
        correct = q["answer"].upper()
        if user_ans == correct:
            print("Correct! \u2705")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct}.")
            wrong.append((i, q, user_ans))

    percent = (score / num_questions) * 100
    print("\nQuiz complete!")
    print(f"Score: {score}/{num_questions} ({percent:.1f}%)")

    if wrong:
        print("\nReview of incorrect answers:")
        for idx, q, given in wrong:
            print(f"\nQuestion {idx}: {q['question']}")
            print(f"  Your answer: {given} — {q['options'].get(given, 'N/A')}")
            correct = q['answer']
            print(f"  Correct: {correct} — {q['options'][correct]}")
            if q.get("explanation"):
                print(f"  Explanation: {q['explanation']}")

    if percent == 100:
        print("\nExcellent! You got a perfect score.")
    elif percent >= 70:
        print("\nWell done — good knowledge of UAE history.")
    else:
        print("\nKeep studying — history is full of fascinating details to learn!")

    # Offer retry
    while True:
        again = input("\nWould you like to try again? (y/n) > ").strip().lower()
        if again in ("y", "yes"):
            print("\nRestarting the quiz...\n")
            run_quiz(num_questions)
            return
        if again in ("n", "no"):
            print("Thanks for playing — goodbye!")
            return
        print("Please answer 'y' or 'n'.")


def parse_args(argv):
    # Very simple argument parsing: allow a single optional integer to limit number of questions
    if len(argv) <= 1:
        return None
    if argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    try:
        n = int(argv[1])
        return n
    except ValueError:
        print("Usage: uae_history_quiz.py [number_of_questions]")
        print("Example: ./uae_history_quiz.py 5")
        sys.exit(1)


if __name__ == "__main__":
    try:
        num = parse_args(sys.argv)
        run_quiz(num)
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
