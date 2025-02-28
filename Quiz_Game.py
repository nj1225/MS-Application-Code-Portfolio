def run_quiz(questions):
    # Initialize score to track correct answers
    score = 0

    # Loop through each question in the provided list
    for question in questions:
        print(question["prompt"])  # Display the question text
        
        # Display answer choices
        for option in question["options"]:
            print(option)
        
        # Get user input and convert to uppercase for consistency
        answer = input("Enter your answer (A, B, C, or D): ").upper()

        # Check if the user's answer is correct
        if answer == question["answer"]:
            print("Correct!\n")
            score += 1  # Increase score for correct answers
        else:
            print("Wrong! The correct answer was", question["answer"], "\n")

    # Display final score after all questions are answered
    print(f"You got {score} out of {len(questions)} questions correct.")

# List of quiz questions. Each question is a dictionary.
questions = [
    {
        "prompt": "What is the largest planet in our solar system?",
        "options": ["A. Earth", "B. Jupiter", "C. Saturn", "D. Mars"],
        "answer": "B"
    },
    {
        "prompt": "Which element has the chemical symbol 'O'?",
        "options": ["A. Oxygen", "B. Gold", "C. Silver", "D. Hydrogen"],
        "answer": "A"
    },
    {
        "prompt": "Who painted the Mona Lisa?",
        "options": ["A. Vincent van Gogh", "B. Pablo Picasso", "C. Leonardo da Vinci", "D. Claude Monet"],
        "answer": "C"
    },
    {
        "prompt": "What is the square root of 64?",
        "options": ["A. 6", "B. 7", "C. 8", "D. 9"],
        "answer": "C"
    }
]

# Run the quiz
run_quiz(questions)
