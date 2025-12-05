#!/usr/bin/env python3
"""Simple terminal Hangman game.

Features:
- Shows the mystery word with correctly guessed letters placed in their slots.
- Displays letters already guessed (correct and wrong).
- Supports phrases (spaces and punctuation are shown as-is).
- Interactive play plus a non-interactive `--demo` mode for quick verification.
"""
import random
import argparse
import sys

WORD_LIST = [
    "python",
    "hello world",
    "openai",
    "final exam",
    "hangman",
    "data science",
    "unit test",
]


def mask_word(word: str, guesses: set) -> str:
    """Return the masked display of the word using guesses.

    Letters present in `guesses` (case-insensitive) are shown; other letters
    are replaced with underscores. Spaces and non-letter characters are preserved.
    """
    out = []
    for ch in word:
        if ch.isalpha():
            if ch.lower() in guesses:
                out.append(ch)
            else:
                out.append("_")
        else:
            out.append(ch)
    return "".join(out)


def display_state(word: str, guesses: set, wrong: set, max_wrong: int) -> None:
    masked = mask_word(word, guesses)
    print("\nMystery: ", " ".join(masked))
    all_guessed = sorted(set(list(guesses) + list(wrong)))
    print("Guessed letters:", ", ".join(all_guessed) if all_guessed else "(none yet)")
    print(f"Wrong guesses ({len(wrong)}/{max_wrong}): {', '.join(sorted(wrong)) if wrong else '(none)'}")


def play_interactive(word: str):
    word_lower = word.lower()
    guesses = set()
    wrong = set()
    max_wrong = 6

    while True:
        display_state(word, guesses, wrong, max_wrong)

        if '_' not in mask_word(word, guesses):
            print("\nYou win! The word was:\n", word)
            break

        if len(wrong) >= max_wrong:
            print("\nOut of guesses. You lose. The word was:\n", word)
            break

        user = input("Enter a letter, or type the full word to guess: ").strip()
        if not user:
            print("Please enter something.")
            continue

        # Full-word guess
        if len(user) > 1:
            if user.lower() == word_lower:
                print("Correct! You guessed the full word:", word)
                break
            else:
                print("That's not the word.")
                # penalize one wrong guess for a wrong full-word guess
                wrong.add(user[0].lower())
                continue

        # Single letter guess
        letter = user[0].lower()
        if not letter.isalpha():
            print("Please enter a letter (a-z).")
            continue

        if letter in guesses or letter in wrong:
            print("You already guessed that letter.")
            continue

        if letter in word_lower:
            print("Good guess!")
            guesses.add(letter)
        else:
            print("Nope.")
            wrong.add(letter)


def demo_run():
    # deterministic demo for quick verification
    word = "hello world"
    print("Demo mode: mystery word is:", word)
    guesses = []
    wrong = []
    max_wrong = 6
    # a sequence of guesses to demonstrate reveals
    sequence = ["e", "x", "o", "l", "h", "w", "r", "d"]
    for g in sequence:
        if len(g) == 1:
            if g in word:
                guesses.append(g)
            else:
                wrong.append(g)
        print("\nAfter guessing:", g)
        display_state(word, set(guesses), set(wrong), max_wrong)

    if '_' not in mask_word(word, set(guesses)):
        print("\nDemo result: win")
    else:
        print("\nDemo result: still hidden")


def main():
    parser = argparse.ArgumentParser(description="Play Hangman in the terminal.")
    parser.add_argument("--demo", action="store_true", help="Run non-interactive demo and exit")
    args = parser.parse_args()

    if args.demo:
        demo_run()
        return

    word = random.choice(WORD_LIST)
    try:
        play_interactive(word)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
