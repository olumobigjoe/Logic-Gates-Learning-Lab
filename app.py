"""
Interactive Logic Gates Learning App
Built for undergraduate electronics students (first module: Logic Gates)
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Logic Gates 101",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {background-color: #0e1117;}
    .gate-card {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #374151;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }
    .app-card {
        background: #1a1f2b;
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .led-on {
        font-size: 3rem;
        color: #22c55e;
        text-align: center;
    }
    .led-off {
        font-size: 3rem;
        color: #ef4444;
        opacity: 0.5;
        text-align: center;
    }
    .big-symbol {
        font-family: monospace;
        font-size: 1.1rem;
        background: #0b0f17;
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        color: #93c5fd;
        white-space: pre;
    }
    h1, h2, h3 {
        color: #f9fafb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# GATE DATA (7 basic gates)
# ----------------------------------------------------------------------
GATES = {
    "AND": {
        "expr": "Y = A · B",
        "desc": "Output is HIGH (1) only when ALL inputs are HIGH.",
        "symbol": "  A ──┐\n       )D──── Y\n  B ──┘\n  (AND shape)",
        "apps": "Used in safety interlock systems (e.g., a machine only runs if door is closed AND power is on).",
        "inputs": 2,
        "logic": lambda a, b: int(a and b),
    },
    "OR": {
        "expr": "Y = A + B",
        "desc": "Output is HIGH (1) if AT LEAST ONE input is HIGH.",
        "symbol": "  A ──╮\n       )>──── Y\n  B ──╯\n  (OR curved shape)",
        "apps": "Used in alarm systems (alarm triggers if smoke sensor OR door sensor activates).",
        "inputs": 2,
        "logic": lambda a, b: int(a or b),
    },
    "NOT": {
        "expr": "Y = A'",
        "desc": "Output is the OPPOSITE (inverse) of the input.",
        "symbol": "  A ──▷o──── Y\n  (Triangle + bubble)",
        "apps": "Used to invert signals, e.g., turning an 'active LOW' sensor signal into 'active HIGH'.",
        "inputs": 1,
        "logic": lambda a, b=None: int(not a),
    },
    "NAND": {
        "expr": "Y = (A · B)'",
        "desc": "Output is LOW (0) only when ALL inputs are HIGH; otherwise HIGH. (AND + NOT)",
        "symbol": "  A ──┐\n       )Do──── Y\n  B ──┘\n  (AND shape + bubble)",
        "apps": "Universal gate — used to build ALL other gates; common in memory (SRAM) cells.",
        "inputs": 2,
        "logic": lambda a, b: int(not (a and b)),
    },
    "NOR": {
        "expr": "Y = (A + B)'",
        "desc": "Output is HIGH (1) only when ALL inputs are LOW; otherwise LOW. (OR + NOT)",
        "symbol": "  A ──╮\n       )>o──── Y\n  B ──╯\n  (OR shape + bubble)",
        "apps": "Universal gate — used in rocket guidance systems (Apollo Guidance Computer used only NOR gates).",
        "inputs": 2,
        "logic": lambda a, b: int(not (a or b)),
    },
    "XOR": {
        "expr": "Y = A ⊕ B",
        "desc": "Output is HIGH (1) only when inputs are DIFFERENT.",
        "symbol": "  A ──╮\n      ))>──── Y\n  B ──╯\n  (OR shape, double curve)",
        "apps": "Used in binary adders (half-adder sum bit) and simple parity/error-checking circuits.",
        "inputs": 2,
        "logic": lambda a, b: int(a != b),
    },
    "XNOR": {
        "expr": "Y = (A ⊕ B)'",
        "desc": "Output is HIGH (1) only when inputs are the SAME.",
        "symbol": "  A ──╮\n      ))>o──── Y\n  B ──╯\n  (XOR shape + bubble)",
        "apps": "Used in equality comparators — checking if two binary numbers/bits match.",
        "inputs": 2,
        "logic": lambda a, b: int(a == b),
    },
}

GATE_ORDER = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]


def truth_table(gate_name):
    g = GATES[gate_name]
    rows = []
    if g["inputs"] == 1:
        for a in [0, 1]:
            rows.append({"A": a, "Y": g["logic"](a)})
    else:
        for a in [0, 1]:
            for b in [0, 1]:
                rows.append({"A": a, "B": b, "Y": g["logic"](a, b)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------
# QUIZ DATA (5 questions, 3 options each)
# ----------------------------------------------------------------------
QUIZ = [
    {
        "q": "1. Which gate outputs HIGH only when ALL its inputs are HIGH?",
        "options": ["OR gate", "AND gate", "NOT gate"],
        "answer": "AND gate",
    },
    {
        "q": "2. What does the NOT gate do to its single input?",
        "options": ["Doubles it", "Inverts it", "Leaves it unchanged"],
        "answer": "Inverts it",
    },
    {
        "q": "3. Which gate is called a 'universal gate' because it can build all others?",
        "options": ["XOR gate", "NAND gate", "XNOR gate"],
        "answer": "NAND gate",
    },
    {
        "q": "4. An XOR gate outputs HIGH (1) when its two inputs are:",
        "options": ["The same", "Different", "Both zero"],
        "answer": "Different",
    },
    {
        "q": "5. Which of these is a real-world application of logic gates?",
        "options": ["Traffic light controllers", "Cooking pasta", "Painting a wall"],
        "answer": "Traffic light controllers",
    },
]

# ----------------------------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------------------------
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}

# ----------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
st.sidebar.title("🔌 Logic Gates 101")
st.sidebar.caption("Module 1 · Digital Electronics Fundamentals")
page = st.sidebar.radio(
    "Navigate",
    [
        "1️⃣ Introduction",
        "2️⃣ Types of Gates",
        "3️⃣ Uses & Applications",
        "4️⃣ Gate Simulator",
        "5️⃣ Quiz",
    ],
)
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 Tip: Work through the sections in order. Use the **Simulator** to "
    "build intuition before attempting the **Quiz**."
)

# ----------------------------------------------------------------------
# 1. INTRODUCTION
# ----------------------------------------------------------------------
if page.startswith("1"):
    st.title("🔌 Introduction to Logic Gates")
    st.markdown(
        """
        ### What is a Logic Gate?
        A **logic gate** is a tiny electronic building block that makes a decision based on
        **binary inputs** — signals that are either **0 (LOW / OFF)** or **1 (HIGH / ON)**.

        Think of a logic gate like a **light switch with rules**:
        - A simple switch turns a light ON or OFF based on *one* action.
        - A logic gate turns its output ON or OFF based on the **combination** of one or more inputs,
          following a fixed rule (its "logic").

        ### Why Do Logic Gates Matter?
        Logic gates are the **fundamental building blocks of all digital electronics** — including
        calculators, smartphones, and the CPU inside your laptop. By combining thousands (or billions!)
        of simple gates, engineers build circuits that can add numbers, store memory, and run entire computers.
        """
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="gate-card">
            <h4>🔢 Binary Basics</h4>
            <p><b>1 (HIGH)</b> = ON, True, usually 5V or 3.3V<br>
            <b>0 (LOW)</b> = OFF, False, usually 0V</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="gate-card">
            <h4>🚦 Everyday Analogy</h4>
            <p>An AND gate is like needing a <b>key AND a PIN</b> to open a safe —
            both conditions must be true before you get access.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.success("👉 Head to **'Types of Gates'** in the sidebar to explore all 7 gates.")

# ----------------------------------------------------------------------
# 2. TYPES OF GATES
# ----------------------------------------------------------------------
elif page.startswith("2"):
    st.title("2️⃣ Types of Logic Gates")
    st.caption("There are 7 basic logic gates every electronics student should know.")

    for name in GATE_ORDER:
        g = GATES[name]
        with st.expander(f"**{name} Gate** — {g['expr']}", expanded=False):
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(f'<div class="big-symbol">{g["symbol"]}</div>', unsafe_allow_html=True)
                st.markdown(f"**Boolean Expression:** `{g['expr']}`")
                st.write(g["desc"])
            with c2:
                st.markdown("**Truth Table**")
                st.dataframe(truth_table(name), use_container_width=True, hide_index=True)

# ----------------------------------------------------------------------
# 3. USES AND APPLICATIONS
# ----------------------------------------------------------------------
elif page.startswith("3"):
    st.title("3️⃣ Uses and Areas of Application")
    st.write(
        "Logic gates aren't just theory — they're at work inside devices you use every day. "
        "Expand each gate below to see a real-world application."
    )
    for name in GATE_ORDER:
        g = GATES[name]
        st.markdown(
            f"""
            <div class="app-card">
            <b>{name} Gate</b> — {g['apps']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🌍 Broader Application Areas")
    apps = [
        "🖩 **Calculators** — arithmetic circuits (adders/subtractors) built from XOR & AND gates",
        "🚦 **Traffic Light Controllers** — sequencing logic to switch lights safely",
        "🚨 **Alarm & Security Systems** — combining sensor inputs (motion, door, smoke)",
        "💾 **Computer Memory (RAM)** — NAND/NOR gates form the basis of memory cells",
        "🧠 **Microprocessors/CPUs** — billions of gates combined to execute instructions",
        "🔐 **Access Control Systems** — multi-condition unlocking (badge AND PIN)",
    ]
    for a in apps:
        st.markdown(f"- {a}")

# ----------------------------------------------------------------------
# 4. GATE SIMULATOR
# ----------------------------------------------------------------------
elif page.startswith("4"):
    st.title("4️⃣ Interactive Gate Simulator")
    st.caption("Choose a gate, toggle the inputs, and watch the output LED respond live.")

    sel = st.selectbox("Select a Logic Gate", GATE_ORDER)
    g = GATES[sel]

    st.markdown(f"**Boolean Expression:** `{g['expr']}`   |   {g['desc']}")

    col_inputs, col_output = st.columns([1, 1])

    with col_inputs:
        st.subheader("Inputs")
        a = st.toggle("Input A", value=False, key="input_a")
        a = int(a)
        if g["inputs"] == 2:
            b = st.toggle("Input B", value=False, key="input_b")
            b = int(b)
            output = g["logic"](a, b)
        else:
            b = None
            output = g["logic"](a)

    with col_output:
        st.subheader("Output")
        if output == 1:
            st.markdown('<div class="led-on">🟢</div>', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;color:#22c55e;'>Y = 1 (HIGH)</h3>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="led-off">🔴</div>', unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center;color:#ef4444;'>Y = 0 (LOW)</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Truth Table (current row highlighted)")
    tt = truth_table(sel)
    if g["inputs"] == 2:
        mask = (tt["A"] == a) & (tt["B"] == b)
    else:
        mask = tt["A"] == a

    def highlight_row(row):
        is_current = (row["A"] == a) and (g["inputs"] == 1 or row["B"] == b)
        return ["background-color: #16a34a; color: white" if is_current else "" for _ in row]

    st.dataframe(tt.style.apply(highlight_row, axis=1), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔗 Bonus: Cascaded Circuit — AND → NOT (i.e. a NAND gate built from parts)")
    st.caption("This shows how simple gates combine to build more complex logic.")
    cc1, cc2 = st.columns(2)
    with cc1:
        ca = st.toggle("Input A ", value=False, key="cascade_a")
        cb = st.toggle("Input B ", value=False, key="cascade_b")
    and_out = int(ca and cb)
    not_out = int(not and_out)
    with cc2:
        st.write(f"AND stage output: **{and_out}**")
        st.write(f"NOT stage output (final): **{not_out}**")
        st.markdown(
            '<div class="led-on">🟢</div>' if not_out == 1 else '<div class="led-off">🔴</div>',
            unsafe_allow_html=True,
        )
    st.info("Notice: this cascade behaves exactly like a single NAND gate!")

# ----------------------------------------------------------------------
# 5. QUIZ
# ----------------------------------------------------------------------
elif page.startswith("5"):
    st.title("5️⃣ Logic Gates Quiz")
    st.caption("5 questions · 3 options each · Scored out of 100%")

    with st.form("quiz_form"):
        for i, item in enumerate(QUIZ):
            st.markdown(f"**{item['q']}**")
            choice = st.radio(
                label=f"q{i}",
                options=item["options"],
                index=None,
                key=f"quiz_radio_{i}",
                label_visibility="collapsed",
            )
            st.session_state.quiz_answers[i] = choice
            st.markdown("")
        submitted = st.form_submit_button("✅ Submit Quiz")

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        answers = st.session_state.quiz_answers
        if any(v is None for v in answers.values()):
            st.warning("⚠️ Please answer all 5 questions before submitting.")
        else:
            correct_count = sum(
                1 for i, item in enumerate(QUIZ) if answers[i] == item["answer"]
            )
            score_pct = round((correct_count / len(QUIZ)) * 100)

            st.markdown("## 📊 Your Results")
            m1, m2 = st.columns(2)
            m1.metric("Score", f"{correct_count}/{len(QUIZ)}")
            m2.metric("Percentage", f"{score_pct}%")
            st.progress(score_pct / 100)

            if score_pct >= 80:
                st.success(f"🎉 Excellent work! You scored {score_pct}%.")
                st.balloons()
            elif score_pct >= 50:
                st.info(f"👍 Good effort! You scored {score_pct}%. Review the gates you missed below.")
            else:
                st.error(f"📚 You scored {score_pct}%. Revisit the 'Types of Gates' section and try again!")

            st.markdown("### Review")
            for i, item in enumerate(QUIZ):
                user_ans = answers[i]
                is_correct = user_ans == item["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"{icon} **{item['q']}**")
                st.write(f"Your answer: {user_ans}")
                if not is_correct:
                    st.write(f"Correct answer: **{item['answer']}**")
                st.markdown("---")

            if st.button("🔄 Retake Quiz"):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {i: None for i in range(len(QUIZ))}
                for i in range(len(QUIZ)):
                    st.session_state.pop(f"quiz_radio_{i}", None)
                st.rerun()
