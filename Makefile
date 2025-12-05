.PHONY: run demo install

run:
	python3 hangman.py

demo:
	python3 hangman.py --demo

install:
	chmod +x hangman.py
