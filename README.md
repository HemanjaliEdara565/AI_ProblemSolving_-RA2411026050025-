## DRONE DELIVERY PATH FINDER USING BFS AND DFS

📌 Problem Description
This project simulates a drone navigation system that finds a path from a starting point (S) to a goal point (G) in a 2D grid environment. The drone must avoid obstacles while reaching the destination.
The environment is represented as a 6 × 6 grid, where:
S → Start position
G → Goal position
X → Obstacles (blocked cells)
* → Path found by the algorithm
The objective is to compute a valid or optimal path using Artificial Intelligence search techniques.

🧠 Algorithms Used
1. Breadth First Search (BFS)
Explores the grid level by level
Guarantees the shortest path in an unweighted grid
Uses a queue data structure
2. Depth First Search (DFS)
Explores the grid depth-wise
Finds a valid path, but not always the shortest
Uses a stack (or recursion)

⚙️ Execution Steps
Install required library:
pip install streamlit

Navigate to project folder:
cd drone_path_finder
Run the application:
streamlit run app.py

## Open browser:
http://localhost:8501

## Steps in UI:
Select algorithm (BFS / DFS)
Enter obstacles (example: 1,4, 3,2)
Click Find Path
View grid and results


# ❌⭕ Interactive Game AI - Tic-Tac-Toe System

## 📌 Problem Description
This project implements an intelligent **Tic-Tac-Toe game** where a human player competes against an AI opponent in a **3 × 3 grid** environment. The user plays as **X**, and the AI plays as **O**.

The objective of the project is to build a computer opponent that always makes the **best possible move** for every user input. The AI analyzes the board state and decides its move using Artificial Intelligence search techniques.

The game board contains:
- **X** → Human player  
- **O** → AI player  
- Empty cells where moves can be placed  

The goal is to either:
- get **three symbols in a row**, column, or diagonal
- or prevent the opponent from winning

---

## 🧠 Algorithms Used

### 1. Minimax Algorithm
- Evaluates all possible future game states
- Chooses the **best move** for the AI
- Ensures the AI plays optimally

### 2. Alpha-Beta Pruning
- Optimizes the Minimax algorithm
- Reduces unnecessary search branches
- Improves execution speed without changing correctness

---

## ⚙️ Execution Steps

1. Install required library:
   ```bash
   pip install streamlit

##  open browser:
  http://localhost:8501/
## Steps in UI:
Click any empty cell to place X
AI will automatically place O
Continue playing until win, lose, or draw
