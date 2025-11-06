# High-Low-Game-In-Python-
A probabilistic game that depends on complete randomness, this project includes event driven programming concepts and game state management.

# How To Run
pip install pillow
python main.py

# Key Features
Feature	Description
🎨 User-Friendly GUI	Developed using Tkinter with clean layout
🃏 Realistic Cards	Uses actual card image assets
📊 Probability Multipliers	Dynamic multiplier based on card rank probability
🔄 Smooth Card Transition	Current card shifts visually each round
💰 Virtual Balance System	Increase or lose based on prediction outcome
🧠 Smart Ace/King Logic	Strict handling for edge cases (A = 1, K = 13)

🎮 Gameplay Logic
- You start with a balance.
- A card is shown.
- Choose HIGH or LOW.
- Next card is revealed.
- If prediction is correct → balance increases based on multiplier.
- If incorrect → balance resets to zero.
- You can return to the menu anytime.
