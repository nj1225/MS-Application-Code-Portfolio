import random
import sqlite3

# Italian-English words categorized by difficulty
words = {
    "Beginner": [
        {"italian": "ciao", "english": "hello"},
        {"italian": "grazie", "english": "thank you"},
        {"italian": "amico", "english": "friend"},
        {"italian": "scuola", "english": "school"},
        {"italian": "libro", "english": "book"},
    ],
    "Intermediate": [
        {"italian": "mangiare", "english": "to eat"},
        {"italian": "bere", "english": "to drink"},
        {"italian": "felice", "english": "happy"},
        {"italian": "triste", "english": "sad"},
        {"italian": "famiglia", "english": "family"},
    ],
    "Advanced": [
        {"italian": "pensare", "english": "to think"},
        {"italian": "dimenticare", "english": "to forget"},
        {"italian": "insegnare", "english": "to teach"},
        {"italian": "soddisfatto", "english": "satisfied"},
        {"italian": "preoccupato", "english": "worried"},
    ]
}

# Database setup
def setup_database():
    conn = sqlite3.connect("quiz_scores.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            difficulty TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to save user scores
def save_score(username, score, difficulty):
    conn = sqlite3.connect("quiz_scores.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (username, score, difficulty) VALUES (?, ?, ?)", 
                   (username, score, difficulty))
    conn.commit()
    conn.close()

# Function to retrieve user scores
def show_scores():
    conn = sqlite3.connect("quiz_scores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, score, difficulty FROM scores ORDER BY score DESC LIMIT 5")
    scores = cursor.fetchall()
    conn.close()

    print("\n🏆 High Scores:")
    if scores:
        for idx, (user, score, difficulty) in enumerate(scores, 1):
            print(f"{idx}. {user}: {score} points ({difficulty} level)")
    else:
        print("No scores recorded yet.")

# Function to determine difficulty level based on past performance
def get_difficulty_level(score):
    if score < 3:
        return "Beginner"
    elif score < 6:
        return "Intermediate"
    else:
        return "Advanced"

# Function to run the quiz
def quiz_user(username):
    """Quiz the user with adaptive difficulty."""
    print("\nStarting Quiz... Answer the questions correctly to increase difficulty!")

    score = 0
    difficulty = "Beginner"  # Start at Beginner level

    for i in range(5):  # Ask 5 questions
        word_list = words[difficulty]  # Get words based on difficulty level
        word = random.choice(word_list)  # Pick a random word from the category
        correct_answer = word["english"]

        # Generate multiple-choice options
        options = random.sample([w["english"] for w in word_list if w != word], 3)
        options.append(correct_answer)
        random.shuffle(options)

        # Display the question
        print(f"\nWhat is the English translation of '{word['italian']}'?")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        try:
            user_choice = int(input("Enter the number of your answer: ")) - 1
            if options[user_choice] == correct_answer:
                print("✅ Correct!\n")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer is '{correct_answer}'.\n")
        except (ValueError, IndexError):
            print(f"⚠️ Invalid choice! The correct answer was '{correct_answer}'.\n")

        # Adjust difficulty based on score
        difficulty = get_difficulty_level(score)

    print(f"🎉 Quiz complete, {username}! Your final score: {score}/5 (Final Level: {difficulty})")
    save_score(username, score, difficulty)

# Main function
def main():
    setup_database()
    print("Welcome to the Italian-English Vocabulary Quiz!")
    username = input("Enter your name: ").strip()

    while True:
        print("\nWhat would you like to do?")
        print("1. Start Quiz")
        print("2. View High Scores")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            quiz_user(username)
        elif choice == "2":
            show_scores()
        elif choice == "3":
            print("Goodbye! Grazie for playing!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
