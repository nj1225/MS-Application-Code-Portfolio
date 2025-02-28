import random

# List of words to guess
words = ['python', 'java', 'kotlin', 'javascript', 'ruby', 'swift']

# Randomly choose a word from the list
chosen_word = random.choice(words)
word_display = ['_' for _ in chosen_word]  # Create a list of underscores
attempts = 8  # Number of allowed attempts
guessed_letters = set()  # Store letters that the user has already guessed

print("Welcome to Hangman!")

while attempts > 0 and '_' in word_display:
    print("\n" + ' '.join(word_display))
    
    # Take input and validate it
    guess = input("Guess a letter: ").lower()

    # 🔹 Input validation: Ensure only a single alphabetic character is entered
    if len(guess) != 1 or not guess.isalpha():
        print("⚠️ Invalid input! Please enter only a single letter.")
        continue

    # 🔹 Check if the letter has already been guessed
    if guess in guessed_letters:
        print("⚠️ You have already guessed this letter. Try a different one.")
        continue

    guessed_letters.add(guess)  # Add letter to guessed set

    # Check if the guessed letter is in the chosen word
    if guess in chosen_word:
        for index, letter in enumerate(chosen_word):
            if letter == guess:
                word_display[index] = guess  # Reveal the letter
    else:
        print("❌ That letter doesn't appear in the word.")
        attempts -= 1

# Game conclusion
if '_' not in word_display:
    print("\n🎉 You guessed the word!")
    print(' '.join(word_display))
    print("🏆 You survived!")
else:
    print("\n💀 You ran out of attempts. The word was:", chosen_word)
    print("Game over!")
