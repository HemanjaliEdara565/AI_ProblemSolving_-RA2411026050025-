import streamlit as st
import math
import time

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="❌", layout="centered")

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.sub-title {
    text-align: center;
    color: gray;
    margin-bottom: 1rem;
}
.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 28px;
    font-weight: bold;
    border-radius: 12px;
}
.result-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #f2f2f2;
    font-weight: 600;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Game functions
# -----------------------------
def init_game():
    if "board" not in st.session_state:
        st.session_state.board = [" " for _ in range(9)]
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "current_turn" not in st.session_state:
        st.session_state.current_turn = "X"  # user
    if "scores" not in st.session_state:
        st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}

def check_winner(board):
    win_combinations = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for combo in win_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]

    if " " not in board:
        return "Draw"

    return None

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == " "]

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    result = check_winner(board)

    if result == "O":
        return 10 - depth
    elif result == "X":
        return depth - 10
    elif result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[move] = " "
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = "X"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[move] = " "
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None

    for i in available_moves(board):
        board[i] = "O"
        score = minimax(board, 0, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i

    return move

def ai_turn():
    if not st.session_state.game_over:
        move = best_move(st.session_state.board)
        if move is not None:
            time.sleep(0.4)
            st.session_state.board[move] = "O"
            result = check_winner(st.session_state.board)
            if result:
                st.session_state.game_over = True
                st.session_state.winner = result
                if result in ["X", "O"]:
                    st.session_state.scores[result] += 1
                else:
                    st.session_state.scores["Draw"] += 1
            else:
                st.session_state.current_turn = "X"

def player_move(index):
    if st.session_state.board[index] == " " and not st.session_state.game_over and st.session_state.current_turn == "X":
        st.session_state.board[index] = "X"
        result = check_winner(st.session_state.board)

        if result:
            st.session_state.game_over = True
            st.session_state.winner = result
            if result in ["X", "O"]:
                st.session_state.scores[result] += 1
            else:
                st.session_state.scores["Draw"] += 1
        else:
            st.session_state.current_turn = "O"
            ai_turn()

def reset_board():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = "X"

def reset_all():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.current_turn = "X"
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}

# -----------------------------
# UI
# -----------------------------
init_game()

st.markdown('<div class="main-title">Interactive Game AI - Tic-Tac-Toe</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">User (X) vs AI (O) using Minimax Algorithm</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Player (X)", st.session_state.scores["X"])
col2.metric("AI (O)", st.session_state.scores["O"])
col3.metric("Draws", st.session_state.scores["Draw"])

st.write("### Game Board")

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            st.button(
                st.session_state.board[idx],
                key=f"cell_{idx}",
                on_click=player_move,
                args=(idx,)
            )

st.write("")

if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.markdown('<div class="result-box">Game Over! It is a Draw.</div>', unsafe_allow_html=True)
    else:
        winner_text = "Player Wins!" if st.session_state.winner == "X" else "AI Wins!"
        st.markdown(f'<div class="result-box">{winner_text}</div>', unsafe_allow_html=True)
else:
    turn_text = "Your Turn" if st.session_state.current_turn == "X" else "AI Thinking..."
    st.info(turn_text)

c1, c2 = st.columns(2)
with c1:
    st.button("New Round", on_click=reset_board, use_container_width=True)
with c2:
    st.button("Reset Score", on_click=reset_all, use_container_width=True)

st.write("---")
st.write("### Algorithms Used")
st.write("- Minimax Algorithm")
st.write("- Alpha-Beta Pruning")
st.write("### Features")
st.write("- User vs AI gameplay")
st.write("- AI always chooses the best move")
st.write("- Score tracking")
st.write("- Interactive Streamlit web interface")