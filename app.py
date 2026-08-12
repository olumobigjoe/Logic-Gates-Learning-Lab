import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Logic Gates Learning Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 100%);
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102a43 0%, #173f5f 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Hero */
    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #102a43, #1f6f8b);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(16, 42, 67, 0.18);
    }

    .hero h1 {
        margin-bottom: 0.5rem;
        font-size: 2.6rem;
    }

    .hero p {
        font-size: 1.1rem;
        opacity: 0.95;
    }

    /* Cards */
    .card {
        background: white;
        padding: 1.4rem;
        border-radius: 16px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.07);
        border-left: 5px solid #1f6f8b;
    }

    .gate-card {
        background: white;
        padding: 1.3rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
        border-top: 4px solid #1f6f8b;
    }

    .gate-symbol {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem;
    }

    /* Output indicators */
    .led-on {
        background: #d8f3dc;
        color: #1b7f3a;
        border: 3px solid #2e9d57;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        font-size: 3rem;
        font-weight: bold;
    }

    .led-off {
        background: #eeeeee;
        color: #555555;
        border: 3px solid #888888;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: auto;
        font-size: 3rem;
        font-weight: bold;
    }

    /* Result box */
    .result-box {
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }

    /* Section headings */
    .section-title {
        color: #102a43;
        border-bottom: 3px solid #1f6f8b;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Quiz answer */
    .correct-answer {
        background: #d8f3dc;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.4rem 0;
    }

    .wrong-answer {
        background: #ffe0e0;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.4rem 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #607080;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIC GATE DATA
# ============================================================

GATE_INFO = {
    "AND": {
        "expression": "Y = A · B",
        "symbol": "A ──┐\n    AND ── Y\nB ──┘",
        "description": "The output is 1 only when BOTH inputs are 1.",
        "application": "Safety systems where two conditions must be satisfied.",
    },
    "OR": {
        "expression": "Y = A + B",
        "symbol": "A ──┐\n    OR ── Y\nB ──┘",
        "description": "The output is 1 when AT LEAST ONE input is 1.",
        "application": "Alarm systems where any one of several sensors can trigger an alarm.",
    },
    "NOT": {
        "expression": "Y = ¬A",
        "symbol": "A ── NOT ── Y",
        "description": "The output is the opposite of the input.",
        "application": "Inverting a digital signal or creating complementary control signals.",
    },
    "NAND": {
        "expression": "Y = ¬(A · B)",
        "symbol": "A ──┐\n    NAND ── Y\nB ──┘",
        "description": "The output is 0 only when BOTH inputs are 1.",
        "application": "NAND gates can be combined to build many other digital circuits.",
    },
    "NOR": {
        "expression": "Y = ¬(A + B)",
        "symbol": "A ──┐\n    NOR ── Y\nB ──┘",
        "description": "The output is 1 only when BOTH inputs are 0.",
        "application": "Control circuits, memory circuits, and digital decision-making systems.",
    },
    "XOR": {
        "expression": "Y = A ⊕ B",
        "symbol": "A ──┐\n    XOR ── Y\nB ──┘",
        "description": "The output is 1 when the inputs are DIFFERENT.",
        "application": "Binary addition and error-detection circuits.",
    },
    "XNOR": {
        "expression": "Y = ¬(A ⊕ B)",
        "symbol": "A ──┐\n    XNOR ── Y\nB ──┘",
        "description": "The output is 1 when the inputs are the SAME.",
        "application": "Digital comparison circuits that check whether two bits match.",
    }
}


# ============================================================
# LOGIC FUNCTIONS
# ============================================================

def calculate_output(gate, a, b=None):
    """
    Calculate a gate output using actual Python boolean logic.

    a and b are converted to Boolean values before calculation.
    The function returns an integer: 0 or 1.
    """

    a = bool(a)

    if gate == "NOT":
        return int(not a)

    b = bool(b)

    if gate == "AND":
        return int(a and b)

    if gate == "OR":
        return int(a or b)

    if gate == "NAND":
        return int(not (a and b))

    if gate == "NOR":
        return int(not (a or b))

    if gate == "XOR":
        return int(a != b)

    if gate == "XNOR":
        return int(a == b)

    return 0


# ============================================================
# TRUTH TABLE GENERATOR
# ============================================================

def create_truth_table(gate):
    """Create a truth table dynamically using the gate logic."""

    rows = []

    if gate == "NOT":
        for a in [0, 1]:
            output = calculate_output(gate, a)
            rows.append({
                "A": a,
                "Output": output
            })

    else:
        for a in [0, 1]:
            for b in [0, 1]:
                output = calculate_output(gate, a, b)
                rows.append({
                    "A": a,
                    "B": b,
                    "Output": output
                })

    return pd.DataFrame(rows)


# ============================================================
# TRUTH TABLE WITH CURRENT ROW HIGHLIGHT
# ============================================================

def highlight_current_row(df, gate, a, b=None):
    """Highlight the row matching the simulator's current inputs."""

    def highlight(row):
        if gate == "NOT":
            match = row["A"] == a
        else:
            match = row["A"] == a and row["B"] == b

        if match:
            return ["background-color: #d8f3dc; font-weight: bold"] * len(row)

        return [""] * len(row)

    return df.style.apply(highlight, axis=1)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style="text-align:center;">⚡ Logic Gates Lab</h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 📚 Student Guide")

    st.markdown(
        """
        **How to use this app:**

        1. Start with the Introduction.
        2. Study each logic gate.
        3. Examine the truth tables.
        4. Try the Interactive Simulator.
        5. Test yourself with the Quiz.

        💡 **Tip:** Try predicting the output before changing the simulator inputs.
        """
    )

    st.markdown("---")

    page = st.radio(
        "🧭 Navigate",
        [
            "🏠 Introduction",
            "🔌 Types of Logic Gates",
            "🌍 Uses & Applications",
            "🎛️ Interactive Simulator",
            "📝 Quiz"
        ]
    )

    st.markdown("---")

    st.caption(
        "Designed for undergraduate students learning digital electronics for the first time."
    )


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>⚡ Logic Gates Learning Lab</h1>
        <p>
        An interactive beginner-friendly introduction to the building blocks
        of digital electronics.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 1. INTRODUCTION
# ============================================================

if page == "🏠 Introduction":

    st.markdown(
        '<h2 class="section-title">🏠 Introduction to Logic Gates</h2>',
        unsafe_allow_html=True
    )

    st.info(
        "Welcome! This section introduces the basic idea of logic gates "
        "before you start experimenting with them."
    )

    st.markdown(
        """
        <div class="card">
        <h3>💡 What is a Logic Gate?</h3>

        <p>
        A <b>logic gate</b> is a small digital circuit that makes a decision
        based on one or more inputs.
        </p>

        <p>
        Think of it as a tiny electronic decision-maker. It receives information,
        processes it according to a rule, and produces an output.
        </p>

        <p>
        For example, an AND gate asks:
        <b>"Are both conditions true?"</b>
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">
            <h3>🔢 Binary: 0 and 1</h3>

            <p>
            Digital electronics normally represents information using two
            states:
            </p>

            <ul>
                <li><b>0</b> = LOW / OFF / False</li>
                <li><b>1</b> = HIGH / ON / True</li>
            </ul>

            <p>
            These two values form the foundation of binary digital systems.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">
            <h3>💡 Simple Analogy: Light Switches</h3>

            <p>
            Imagine two light switches.
            </p>

            <p>
            An <b>AND gate</b> behaves like a lamp that turns on only when
            <b>both switches</b> are ON.
            </p>

            <p>
            An <b>OR gate</b> behaves like a lamp that turns on when
            <b>at least one switch</b> is ON.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="card">
        <h3>🖥️ Why Do Logic Gates Matter?</h3>

        <p>
        Logic gates are the basic building blocks of digital electronics.
        Millions or billions of gates can work together inside modern
        electronic devices.
        </p>

        <ul>
            <li>💻 Computers</li>
            <li>🧠 CPUs and processors</li>
            <li>💾 Memory systems</li>
            <li>📱 Smartphones</li>
            <li>🧮 Calculators</li>
            <li>🚦 Control systems</li>
            <li>🤖 Digital and robotic systems</li>
        </ul>

        <p>
        Understanding logic gates is therefore an important first step toward
        understanding how digital computers and electronic control systems work.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "Key idea: A logic gate takes binary inputs and produces a binary output according to a specific rule."
    )


# ============================================================
# 2. TYPES OF LOGIC GATES
# ============================================================

elif page == "🔌 Types of Logic Gates":

    st.markdown(
        '<h2 class="section-title">🔌 The 7 Basic Logic Gates</h2>',
        unsafe_allow_html=True
    )

    st.caption(
        "Study the expression, simple symbol representation, truth table, and behavior of each gate."
    )

    selected_gate = st.selectbox(
        "Choose a gate to study:",
        list(GATE_INFO.keys())
    )

    info = GATE_INFO[selected_gate]

    st.markdown(
        f"""
        <div class="gate-card">

        <h2>{selected_gate} Gate</h2>

        <div class="gate-symbol">
        <pre>{info["symbol"]}</pre>
        </div>

        <h4>Boolean Expression</h4>

        <p style="font-size:1.3rem;">
        <b>{info["expression"]}</b>
        </p>

        <h4>In simple English</h4>

        <p>{info["description"]}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📊 Truth Table")

    truth_table = create_truth_table(selected_gate)

    st.table(truth_table)

    st.success(
        f"Remember: {selected_gate} — {info['description']}"
    )

    st.markdown("---")

    st.subheader("📚 Quick Reference: All 7 Gates")

    for gate_name, gate_info in GATE_INFO.items():

        with st.expander(f"⚡ {gate_name} Gate"):

            col1, col2 = st.columns([1, 2])

            with col1:
                st.code(gate_info["symbol"])

            with col2:
                st.markdown(
                    f"**Boolean expression:** `{gate_info['expression']}`"
                )
                st.write(gate_info["description"])


# ============================================================
# 3. USES AND APPLICATIONS
# ============================================================

elif page == "🌍 Uses & Applications":

    st.markdown(
        '<h2 class="section-title">🌍 Uses and Areas of Application</h2>',
        unsafe_allow_html=True
    )

    st.info(
        "Logic gates are not just classroom concepts. They are used inside many of the digital systems we interact with every day."
    )

    applications = [
        (
            "💻 Computers and CPUs",
            "Logic gates combine to perform calculations, comparisons, and decisions inside processors.",
            "AND, OR, NOT, XOR"
        ),
        (
            "🧮 Calculators",
            "Digital arithmetic circuits use logic gates to perform addition, subtraction, and other operations.",
            "AND, XOR, NOT"
        ),
        (
            "🚦 Traffic Light Controllers",
            "Logic circuits can decide when lights should change based on timing and sensor conditions.",
            "AND, OR, NOT"
        ),
        (
            "🚨 Alarm Systems",
            "Several sensors can be combined so that an alarm activates when specific conditions occur.",
            "AND, OR, NOT"
        ),
        (
            "➕ Arithmetic Circuits",
            "XOR and AND gates are important components of binary addition circuits.",
            "XOR, AND"
        ),
        (
            "💾 Memory Devices",
            "Logic gates can be connected to create circuits capable of storing digital states.",
            "NAND, NOR"
        ),
        (
            "📱 Smartphones",
            "Processors and digital control circuits inside smartphones contain huge numbers of logic gates.",
            "All basic gates"
        ),
        (
            "🤖 Control Systems",
            "Industrial machines and robots use digital logic to make decisions based on sensors.",
            "AND, OR, NOT, NAND, NOR"
        ),
    ]

    for title, description, gates in applications:

        with st.expander(title):

            st.write(description)

            st.markdown(
                f"**Useful gates:** `{gates}`"
            )

    st.markdown("---")

    st.subheader("🔍 Gate-to-Application Map")

    application_data = pd.DataFrame(
        {
            "Gate": [
                "AND",
                "OR",
                "NOT",
                "NAND",
                "NOR",
                "XOR",
                "XNOR"
            ],
            "Example Application": [
                "Safety/interlock systems",
                "Alarm systems",
                "Signal inversion",
                "Universal digital circuits",
                "Control and memory circuits",
                "Binary addition",
                "Digital comparison"
            ]
        }
    )

    st.dataframe(
        application_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 4. INTERACTIVE SIMULATOR
# ============================================================

elif page == "🎛️ Interactive Simulator":

    st.markdown(
        '<h2 class="section-title">🎛️ Interactive Logic Gate Simulator</h2>',
        unsafe_allow_html=True
    )

    st.info(
        "Change the inputs and watch the output change immediately. "
        "The output is calculated using Python Boolean logic."
    )

    gate = st.selectbox(
        "🔌 Select a logic gate:",
        list(GATE_INFO.keys()),
        key="simulator_gate"
    )

    st.markdown(
        f"""
        <div class="card">
        <h3>{gate} Gate</h3>
        <p>{GATE_INFO[gate]["description"]}</p>
        <p><b>Boolean expression:</b> {GATE_INFO[gate]["expression"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # INPUT CONTROLS
    # --------------------------------------------------------

    st.subheader("🎚️ Inputs")

    if gate == "NOT":

        a = st.radio(
            "Input A",
            [0, 1],
            horizontal=True,
            key="not_input_a"
        )

        b = None

    else:

        col1, col2 = st.columns(2)

        with col1:

            a = st.radio(
                "Input A",
                [0, 1],
                horizontal=True,
                key="input_a"
            )

        with col2:

            b = st.radio(
                "Input B",
                [0, 1],
                horizontal=True,
                key="input_b"
            )

    # Calculate output
    output = calculate_output(gate, a, b)

    st.markdown("---")

    # --------------------------------------------------------
    # DISPLAY CIRCUIT INPUTS
    # --------------------------------------------------------

    if gate == "NOT":

        st.markdown(
            f"""
            <div class="result-box">
                <h3>Input A</h3>
                <h1>{a}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                <div class="result-box">
                    <h3>Input A</h3>
                    <h1>{a}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="result-box">
                    <h3>Input B</h3>
                    <h1>{b}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # OUTPUT LED
    # --------------------------------------------------------

    st.subheader("💡 Output")

    if output == 1:

        st.markdown(
            """
            <div class="led-on">
                1
            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("🟢 OUTPUT = 1 — HIGH / ON / TRUE")

    else:

        st.markdown(
            """
            <div class="led-off">
                0
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("🔴 OUTPUT = 0 — LOW / OFF / FALSE")

    # --------------------------------------------------------
    # CURRENT TRUTH TABLE ROW
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("📊 Current Truth Table Row")

    table = create_truth_table(gate)

    highlighted = highlight_current_row(
        table,
        gate,
        a,
        b
    )

    st.dataframe(
        highlighted,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # SIMPLE CASCADING CIRCUIT
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🔗 Try a Two-Gate Combination")

    st.caption(
        "This example connects an AND gate to a NOT gate. "
        "The AND output becomes the input of the NOT gate."
    )

    combo_col1, combo_col2 = st.columns(2)

    with combo_col1:

        combo_a = st.radio(
            "Combination Input A",
            [0, 1],
            horizontal=True,
            key="combo_a"
        )

    with combo_col2:

        combo_b = st.radio(
            "Combination Input B",
            [0, 1],
            horizontal=True,
            key="combo_b"
        )

    and_output = calculate_output(
        "AND",
        combo_a,
        combo_b
    )

    final_output = calculate_output(
        "NOT",
        and_output
    )

    st.markdown(
        f"""
        <div class="card">
        <h3>AND → NOT Circuit</h3>

        <p style="font-size:1.2rem;">
        A = <b>{combo_a}</b>
        &nbsp;&nbsp; | &nbsp;&nbsp;
        B = <b>{combo_b}</b>
        </p>

        <p style="font-size:1.2rem;">
        AND output = <b>{and_output}</b>
        </p>

        <p style="font-size:1.2rem;">
        NOT receives {and_output} and produces:
        <b>{final_output}</b>
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "This demonstrates an important digital-electronics idea: "
        "gates can be connected together to create more complex circuits."
    )


# ============================================================
# 5. QUIZ
# ============================================================

elif page == "📝 Quiz":

    st.markdown(
        '<h2 class="section-title">📝 Logic Gates Quiz</h2>',
        unsafe_allow_html=True
    )

    st.info(
        "There are 5 questions. Each question has exactly three possible answers. "
        "Choose your answers and click Submit Quiz."
    )

    # --------------------------------------------------------
    # QUIZ DATA
    # --------------------------------------------------------

    questions = {
        1: {
            "question": "Which gate produces 1 only when BOTH inputs are 1?",
            "options": [
                "AND gate",
                "OR gate",
                "NOT gate"
            ],
            "answer": "AND gate"
        },

        2: {
            "question": "What does a NOT gate do?",
            "options": [
                "Adds two inputs",
                "Reverses the input",
                "Always produces 1"
            ],
            "answer": "Reverses the input"
        },

        3: {
            "question": "Which gate produces 1 when its two inputs are DIFFERENT?",
            "options": [
                "XOR gate",
                "XNOR gate",
                "NOR gate"
            ],
            "answer": "XOR gate"
        },

        4: {
            "question": "If A = 1 and B = 0, what is the output of an OR gate?",
            "options": [
                "0",
                "1",
                "It depends on the NOT gate"
            ],
            "answer": "1"
        },

        5: {
            "question": "Which type of gate is commonly used in binary addition?",
            "options": [
                "XOR gate",
                "NOR gate",
                "XNOR gate"
            ],
            "answer": "XOR gate"
        }
    }

    # Initialize session state
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    # --------------------------------------------------------
    # DISPLAY QUESTIONS
    # --------------------------------------------------------

    for number, data in questions.items():

        st.markdown(
            f"""
            <div class="card">
            <h3>Question {number}</h3>
            <p>{data["question"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.radio(
            f"Choose your answer for Question {number}:",
            data["options"],
            key=f"quiz_q_{number}"
        )

    # --------------------------------------------------------
    # SUBMIT QUIZ
    # --------------------------------------------------------

    if st.button(
        "🚀 Submit Quiz",
        type="primary",
        use_container_width=True
    ):

        correct = 0
        student_answers = {}

        for number, data in questions.items():

            selected = st.session_state.get(
                f"quiz_q_{number}"
            )

            student_answers[number] = selected

            if selected == data["answer"]:
                correct += 1

        score = int((correct / len(questions)) * 100)

        st.session_state.quiz_score = score
        st.session_state.quiz_answers = student_answers
        st.session_state.quiz_submitted = True

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score
        answers = st.session_state.quiz_answers

        st.markdown("---")

        st.subheader("🏆 Quiz Results")

        st.metric(
            "Your Score",
            f"{score}%"
        )

        st.progress(
            score / 100
        )

        if score > 80:

            st.success(
                "🎉 Excellent work! You have a strong understanding of the basic logic gates."
            )

            st.balloons()

        elif score >= 60:

            st.info(
                "👍 Good work! Review the truth tables and try the quiz again."
            )

        else:

            st.warning(
                "📚 Keep learning! Review the gate explanations and simulator before trying again."
            )

        st.markdown("---")

        st.subheader("📋 Question Review")

        for number, data in questions.items():

            selected = answers.get(number)

            if selected == data["answer"]:

                st.markdown(
                    f"""
                    <div class="correct-answer">
                    ✅ <b>Question {number}: Correct</b><br>
                    Your answer: {selected}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="wrong-answer">
                    ❌ <b>Question {number}: Incorrect</b><br>
                    Your answer: {selected}<br>
                    Correct answer: <b>{data["answer"]}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("---")

        if st.button("🔄 Try Quiz Again"):

            st.session_state.quiz_submitted = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ⚡ <b>Logic Gates Learning Lab</b><br>
        Learn • Experiment • Predict • Understand<br><br>
        A beginner-friendly digital electronics learning tool.
    </div>
    """,
    unsafe_allow_html=True
)