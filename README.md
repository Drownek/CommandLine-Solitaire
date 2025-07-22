# Solitaire

## Screenshots
<img width="879" height="539" alt="image" src="https://github.com/user-attachments/assets/2344115a-13de-41cb-9d0b-a1528f11af15" />
<img width="1539" height="752" alt="image" src="https://github.com/user-attachments/assets/46cac2ad-f4d1-4e71-80eb-fa05556e1dee" />

## How to Run the Project

To run the game, follow these steps:

1. Make sure you have Python version 3.12 or newer installed.
2. Install the required packages:

```bash
    pip install -r .\requirements.txt
```

3. Run the game using the following command from the main folder (PasjansGigathon) (tested on Windows PowerShell and Command Prompt):

```bash
   py main.py
```

## Gameplay Instructions

### Keys

* **n** - New game
* **u** - Undo
* **?** - Help
* **q** - Quit
* **c** - Change Theme

### Controls

* Click a hidden card from the stack to reveal it.
* Click the top card to select it.
* Click a card below the top to select all cards from the top one to the selected one.
* When one card is selected, if the rules allow, it can be moved:

  * to the foundation pile by clicking it
  * to another card in a different stack by clicking the top card
* When multiple cards are selected, they can only be moved to another column by clicking the top card of that column.

### Game Rules

The goal of the game is to arrange all the cards into four foundation piles by suit and in ascending order (from Ace to King).
Cards can be arranged in the tableau columns in descending order and alternating colors.

## Module and Class Description

### Main Classes

* **Game** – the main application class that manages the entire game
* **GameGrid** – class responsible for displaying the board
* **Card** – representation of a playing card
* **CardHolder** – empty slot for a card
* **Tableau** – class representing the main tableau of the game
* **Foundation** – class representing the foundation piles
* **StashWaste** – class representing the deck and discard pile

### Styling System

The project uses the Textual CSS library for styling the user interface. The `pasjans.tcss` file contains style definitions for all UI elements.
The project is implemented as a console application using the Textual library, which provides an interactive terminal user interface.
