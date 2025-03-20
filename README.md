# Reinforcement Learning Agent for Twenty-Nine Card Game

This project implements a **reinforcement learning environment** for the **Twenty-Nine** card game, a popular trick-taking game in Bangladesh. Using the `rlcard` library, this environment simulates the game, including phases like **bidding**, **trump selection**, and **trick-taking**. The goal of the project is to build a foundation for training advanced reinforcement learning agents while accurately modeling the Bangladeshi variant of the game.

## 🛠️ Setup Instructions

### 1. Virtual Environment:
This project uses a virtual environment named `myvenv`.

To activate it on **Linux**:
```bash
source myvenv/bin/activate
```

### 2. Install Dependencies:
Make sure `rlcard` is installed in the virtual environment:
```bash
pip install rlcard
```

### 3. Running the Game:
To run the game, execute the following:
```bash
python -u test_game.py
```
The output will be logged in `game_log.txt`, capturing the gameplay with a random agent.

## 📁 Project Structure

```
rlcard_custom/                 # Core folder containing the game implementation files (development-focused)
  env/__init__.py              # Register the TwentyNineEnv to RLCard Environment
  env/twenty_nine.py           # Custom environment for Twenty-Nine, registers the game with rlcard, and maps game states/actions to the RL framework.
  games/twenty_nine/game.py    # Main game logic, state management, and step function
  games/twenty_nine/player.py  # Player class (hand and trick management)
  games/twenty_nine/dealer.py  # Dealer class (card distribution)
  games/twenty_nine/judger.py  # Scoring and trick-winning logic
  games/twenty_nine/card.py    # Card representation and deck creation
  agents/random_agent.py       # Random agent for gameplay simulation
test_game.py                   # Runner script to initialize and execute the game environment
game_log.txt                   # Log file capturing game progress (bidding, tricks, scores)
twenty_nine_full_implementation_one_file.py  # A full implementation for reference (not part of active rlcard environment)
```

## 🚀 Development Workflow

### Branching Strategy:
- For new features, create a branch named after the feature (e.g., `feature-trump-reveal`).
- After implementation, merge into the **development** branch.
- Once tested, merge **development** into **main**.

> **Important**: Do not edit the `main` branch directly to maintain stability.

## ⚙️ Current Progress

### Completed Features:
- **Working rlcard environment** for Twenty-Nine, with core mechanics implemented in `rlcard_custom/`.
- **Core gameplay mechanics**:
  - 4-card deal to each of 4 players.
  - **Bidding phase** allowing bids from 16 to 28 with suit selection (e.g., '20C'). Ends after 4 actions, with the highest bidder setting the trump.
  - **Trick-taking phase**: 8 tricks per round with suit-following rules and trump precedence.
- **Random agent** (`CustomRandomAgent`) that selects random legal actions for all players.
- **Bug fixes**:
  - Ensured bidding ends correctly after 4 actions.
  - Limited rounds to 8 tricks using a `trick_count` variable.
  - Handled empty hands by returning `'pass'` in `get_legal_actions`, preventing agent crashes.
  - Fixed early termination issues, ensuring rounds complete before scoring.
- **Scoring system**: 
  - Teams earn +1 if they meet/exceed their bid, otherwise -1.
  - Game ends when a team's score reaches ±6.
- **Logging**: Detailed logs in `game_log.txt` to track bids, tricks, and scores.
  
### Next Steps:
- Integrating **advanced RL agents** (e.g., Q-learning, DQN) using the `rlcard` framework.
- Adding advanced **Bangladeshi variant** features like **double**, **redouble**, and **marriage**.

## 🧑‍💻 Game Flow and Phases

### 1. Initialization:
- Four players are created.
- A fresh deck of **32 cards** (7, 8, 9, T, J, Q, K, A across 4 suits) is used.
- Each player is dealt 4 cards initially.

### 2. Bidding Phase:
- Players bid to set the **trump suit** and target score (16-28).
- Legal actions: `'pass'` or a bid (e.g., `'20C'` for 20 points with Clubs as trump).
- Bidding ends after 4 bids. The highest bidder sets the trump and target, then 4 more cards are dealt to each player.

### 3. Trick-Taking Phase:
- Players play one card per trick, following the **lead suit** if possible, or any card (including trump).
- Each trick (4 cards) is judged, and the winner leads the next trick.
- The round consists of **8 tricks**, after which scores are calculated.

### 4. Scoring and Game End:
- The bidding team (e.g., Players 0+2 or 1+3) earns +1 if they meet/exceed their bid. Points are awarded as follows:
  - J = 3, 9 = 2, A = 1, T = 1

## 📂 File Responsibilities

### `rlcard_custom/games/twenty_nine/game.py`
- **Core game logic**: Manages state (hands, tricks, trump, etc.), processes actions via `step()`, tracks `trick_count`, and determines game end via `is_over()`.

### `rlcard_custom/games/twenty_nine/player.py`
- Defines **TwentyNinePlayer**: Manages hand (cards held), tricks (won tricks), and player methods (e.g., `add_card`, `play_card`, `get_points`).

### `rlcard_custom/games/twenty_nine/dealer.py`
- Defines **TwentyNineDealer**: Responsible for shuffling and dealing cards (4 initially, 4 after bidding).

### `rlcard_custom/games/twenty_nine/judger.py`
- Contains **TwentyNineJudger**: Handles **trick judging** (highest trump or lead suit) and **round scoring**.

### `rlcard_custom/games/twenty_nine/card.py`
- Defines **TwentyNineCard**: Represents cards with suit and rank, and provides deck generation.

### `rlcard_custom/agents/random_agent.py`
- Implements **CustomRandomAgent**: Selects random legal actions for gameplay simulation.

### `test_game.py`
- Runner script to set up the **rlcard environment**, register agents, and run the game.
- Outputs results to both the console and `game_log.txt`.

## 🎮 How the Agent Plays

The **CustomRandomAgent** simulates all four players by performing the following:

### 1. **Bidding**:
- Receives legal actions (e.g., `['pass', '16S', ..., '28D']`).
- Randomly picks one (e.g., `'20C'`), which is logged as: 
  - `"Player 0 takes action: 20C"`

### 2. **Trick-Taking**:
- Receives legal actions based on the lead suit (e.g., `['KH', '7H']`).
- If hand is empty or 8 tricks are completed, the agent picks `'pass'`.
- Otherwise, it randomly selects a card (e.g., `'9H'`), logged as:
  - `"Player 0 played: 9H"`

### 3. **Execution**:
- The game progresses via `env.run()`, calling `eval_step()` for each player's turn.
- The random choices simulate full games but lack strategic play, making it ideal for testing.

## 🧩 Current State
The game completes 8 tricks per round, calculates scores, and logs all actions and results in game_log.txt. While the current agent is random, future improvements may include integrating more intelligent RL agents, such as Q-learning.

This structure sets a solid foundation for implementing **advanced features** like **double**, **redouble**, and **marriage**, all specific to the **Bangladeshi variant** of Twenty-Nine.

---
