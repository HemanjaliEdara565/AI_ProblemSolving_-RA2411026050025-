import streamlit as st
from collections import deque
import time

st.set_page_config(page_title="Drone Delivery Path Finder", page_icon="🚁", layout="wide")

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2ff, #f8fafc);
}
.title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #1e3a8a;
    text-align: center;
    margin-bottom: 0.3rem;
}
.subtitle {
    text-align: center;
    font-size: 1rem;
    color: #475569;
    margin-bottom: 1.5rem;
}
.section-box {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
.metric-box {
    background: #f8fafc;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #e2e8f0;
}
.grid-cell {
    text-align: center;
    font-weight: bold;
    padding: 12px 0px;
    border-radius: 10px;
    margin: 2px;
    border: 1px solid #cbd5e1;
}
.small-note {
    color: #64748b;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)

ROWS = 6
COLS = 6

# -----------------------------
# Helper Functions
# -----------------------------
def get_neighbors(node):
    r, c = node
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            neighbors.append((nr, nc))

    return neighbors

def bfs(start, goal, obstacles):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in get_neighbors(node):
            if neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None

def dfs(start, goal, obstacles):
    stack = [[start]]
    visited = set([start])

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in get_neighbors(node):
            if neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)

    return None

def parse_obstacles(text, start, goal):
    obstacles = set()
    lines = text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            r, c = map(int, line.split(","))
            if 0 <= r < ROWS and 0 <= c < COLS and (r, c) != start and (r, c) != goal:
                obstacles.add((r, c))
        except:
            pass

    return obstacles

def get_cell_style(node, start, goal, obstacles, path):
    if node == start:
        return "S", "#86efac"
    elif node == goal:
        return "G", "#fde68a"
    elif node in obstacles:
        return "X", "#fca5a5"
    elif path and node in path:
        return "*", "#93c5fd"
    else:
        return ".", "#ffffff"

# -----------------------------
# App Title
# -----------------------------
st.markdown('<div class="title">🚁 Drone Delivery Path Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find an optimal or valid route from source to destination using BFS or DFS</div>', unsafe_allow_html=True)

# -----------------------------
# Fixed Start and Goal
# -----------------------------
start = (0, 0)
goal = (5, 5)

default_obstacles = "1,1\n1,2\n2,2\n3,4"

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([1, 1.4])

with left:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Input Configuration")

    algorithm = st.selectbox("Choose Algorithm", ["BFS", "DFS"])

    obstacle_text = st.text_area(
        "Enter obstacles (row,col) one per line",
        value=default_obstacles,
        height=180
    )

    st.markdown('<p class="small-note">Example: 1,1 means row 1 and column 1 is blocked.</p>', unsafe_allow_html=True)

    run = st.button("Find Path", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Project Information")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-box"><b>Start</b><br>(0, 0)</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-box"><b>Goal</b><br>(5, 5)</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><b>Grid</b><br>{ROWS} x {COLS}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Processing
# -----------------------------
path = None
exec_time = None
obstacles = parse_obstacles(obstacle_text, start, goal)

if run:
    t1 = time.time()

    if algorithm == "BFS":
        path = bfs(start, goal, obstacles)
    else:
        path = dfs(start, goal, obstacles)

    t2 = time.time()
    exec_time = round((t2 - t1) * 1000, 2)

# -----------------------------
# Results
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Grid Visualization")

for r in range(ROWS):
    cols = st.columns(COLS)
    for c in range(COLS):
        node = (r, c)
        symbol, color = get_cell_style(node, start, goal, obstacles, path)
        cols[c].markdown(
            f"<div class='grid-cell' style='background-color:{color};'>{symbol}</div>",
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Output Section
# -----------------------------
if run:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Output")

    if path:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.success(f"Algorithm Used: {algorithm}")
        with c2:
            st.info(f"Execution Time: {exec_time} ms")
        with c3:
            st.warning(f"Path Length: {len(path)}")

        st.write("### Path Coordinates")
        st.code(str(path))

        st.write("### Path Explanation")
        st.write(
            f"The drone starts at {start}, avoids the blocked cells, and reaches the goal {goal} "
            f"using the {algorithm} algorithm. The discovered route is shown in the grid using `*` symbols."
        )
    else:
        st.error("No valid path found. Please change the obstacle positions.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Legend and Theory
# -----------------------------
l1, l2 = st.columns(2)

with l1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Legend")
    st.write("**S** → Start Point")
    st.write("**G** → Goal Point")
    st.write("**X** → Obstacle")
    st.write("**\\*** → Final Path")
    st.write("**.** → Empty Cell")
    st.markdown('</div>', unsafe_allow_html=True)

with l2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Algorithms Used")
    st.write("**BFS (Breadth First Search):** Finds the shortest path in an unweighted grid.")
    st.write("**DFS (Depth First Search):** Explores deeply first and finds a valid path, but not always the shortest.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Project Features")
st.write("- Clean interactive user interface")
st.write("- BFS and DFS based path finding")
st.write("- Obstacle-based route planning")
st.write("- Execution time measurement")
st.write("- Path length and path coordinate display")
st.write("- Grid visualization for easy understanding")
st.markdown('</div>', unsafe_allow_html=True)