import time
import random

# Sentences for testing
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great programming language.",
    "Typing speed tests help improve your skills.",
    "Artificial intelligence is changing the world.",
    "Stay focused and keep practicing every day."
]

def calculate_accuracy(original, typed):
    correct = 0
    for i in range(min(len(original), len(typed))):
        if original[i] == typed[i]:
            correct += 1
    accuracy = (correct / len(original)) * 100
    return accuracy

def typing_test():
    sentence = random.choice(sentences)
    print("\n--- Typing Speed Test ---")
    print("Type the following sentence:\n")
    print(">>>", sentence)
    input("\nPress Enter when you're ready to start...")

    start_time = time.time()
    typed_input = input("\nStart typing:\n>>> ")
    end_time = time.time()

    time_taken = end_time - start_time
    time_taken_minutes = time_taken / 60

    words_typed = len(typed_input.split())
    wpm = words_typed / time_taken_minutes if time_taken_minutes > 0 else 0
    accuracy = calculate_accuracy(sentence, typed_input)

    print("\n--- Results ---")
    print(f"Time Taken: {time_taken:.2f} seconds")
    print(f"Words Per Minute (WPM): {wpm:.2f}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    typing_test()

