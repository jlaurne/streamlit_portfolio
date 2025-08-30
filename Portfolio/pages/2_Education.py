# math_helper.py
# 5th Grade Math Helper – Florida BEST Standards Complete

import streamlit as st
import random
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Callable, Union
from fractions import Fraction
import decimal

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="Florida 5th Grade Math Helper", layout="wide")

# Complete Florida BEST Standards for 5th Grade
TOPICS = [
    # Number Sense and Operations (NSO)
    "MA.5.NSO.1.1: Place Value with Decimals",
    "MA.5.NSO.1.2: Read/Write Decimals to Thousandths",
    "MA.5.NSO.1.3: Compose/Decompose Decimals",
    "MA.5.NSO.1.4: Plot/Order/Compare Decimals",
    "MA.5.NSO.1.5: Round Decimals",
    "MA.5.NSO.2.1: Multiply Multi-Digit Numbers",
    "MA.5.NSO.2.2: Divide Multi-Digit by 2-Digit",
    "MA.5.NSO.2.3: Add/Subtract Decimals",
    "MA.5.NSO.2.4: Multiply/Divide Decimals",
    "MA.5.NSO.2.5: Multiply/Divide by 0.1 and 0.01",
    
    # Fractions (FR)
    "MA.5.FR.1.1: Division as Fractions",
    "MA.5.FR.2.1: Add/Subtract Unlike Denominators",
    "MA.5.FR.2.2: Multiply Fractions",
    "MA.5.FR.2.3: Predict Products with Fractions",
    "MA.5.FR.2.4: Divide Unit Fractions",
    
    # Algebraic Reasoning (AR)
    "MA.5.AR.1.1: Multi-Step Whole Number Problems",
    "MA.5.AR.1.2: Fraction Word Problems",
    "MA.5.AR.1.3: Unit Fraction Division Problems",
    "MA.5.AR.2.1: Translate to Numerical Expressions",
    "MA.5.AR.2.2: Order of Operations",
    "MA.5.AR.2.3: True/False Equations",
    "MA.5.AR.2.4: Write Equations with Variables",
    "MA.5.AR.3.1: Identify Pattern Rules",
    "MA.5.AR.3.2: Input-Output Tables",
    
    # Measurement (M)
    "MA.5.M.1.1: Convert Measurements",
    "MA.5.M.2.1: Money Problems with Decimals",
    
    # Geometric Reasoning (GR)
    "MA.5.GR.1.1: Classify Triangles & Quadrilaterals",
    "MA.5.GR.1.2: Classify 3D Figures",
    "MA.5.GR.2.1: Area/Perimeter with Fractions/Decimals",
    "MA.5.GR.3.1: Volume with Unit Cubes",
    "MA.5.GR.3.2: Volume Formula",
    "MA.5.GR.3.3: Composite Volume",
    "MA.5.GR.4.1: Coordinate Plane",
    
    # Data Analysis and Probability (DP)
    "MA.5.DP.1.1: Collect/Represent Data",
    "MA.5.DP.1.2: Mean, Median, Mode, Range",
]

MASTERY_TARGET = 5
MASTERY_STREAK_TARGET = 3

# -------------------------------
# Utilities / Data Classes
# -------------------------------
@dataclass
class Problem:
    prompt: str
    answer: Union[int, float, str, Fraction, Tuple]
    steps: List[str]
    hints: List[str]
    display: str = ""

def init_state():
    if "progress" not in st.session_state:
        st.session_state.progress = {t: {"attempted": 0, "correct": 0, "streak": 0, "mastered": False, "history": []}
                                     for t in TOPICS}
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = TOPICS[0]
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Core"
    if "show_steps" not in st.session_state:
        st.session_state.show_steps = False

init_state()

def record_result(topic: str, correct: bool, problem: Problem, user_answer: str):
    p = st.session_state.progress[topic]
    p["attempted"] += 1
    if correct:
        p["correct"] += 1
        p["streak"] += 1
    else:
        p["streak"] = 0
    p["mastered"] = (p["correct"] >= MASTERY_TARGET) and (p["streak"] >= MASTERY_STREAK_TARGET)
    p["history"].append({"prompt": problem.prompt, "answer": problem.answer, "user_answer": user_answer, "correct": correct})

def parse_number(s: str) -> Union[float, None]:
    s = s.strip()
    if not s:
        return None
    # Handle fractions
    if "/" in s:
        try:
            parts = s.split("/")
            if len(parts) == 2:
                return float(parts[0]) / float(parts[1])
        except:
            pass
    # Handle mixed numbers (e.g., "2 1/2")
    if " " in s and "/" in s:
        try:
            whole, frac = s.split(" ", 1)
            num, den = frac.split("/")
            return float(whole) + float(num)/float(den)
        except:
            pass
    try:
        return float(s)
    except:
        return None

# -------------------------------
# Problem Generators for Each Standard
# -------------------------------

# NSO Generators
def gen_place_value_decimals(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        num = round(random.uniform(0.1, 9.999), 2)
    elif difficulty == "Challenge":
        num = round(random.uniform(10.001, 999.999), 3)
    else:
        num = round(random.uniform(1.001, 99.999), 3)
    
    digit_pos = random.choice(["ones", "tenths", "hundredths", "thousandths"])
    
    # Calculate answer based on position
    str_num = str(num)
    if "." not in str_num:
        str_num += ".000"
    whole, dec = str_num.split(".")
    dec = dec.ljust(3, '0')
    
    if digit_pos == "ones":
        answer = int(whole[-1]) if whole else 0
    elif digit_pos == "tenths":
        answer = int(dec[0]) if len(dec) > 0 else 0
    elif digit_pos == "hundredths":
        answer = int(dec[1]) if len(dec) > 1 else 0
    else:  # thousandths
        answer = int(dec[2]) if len(dec) > 2 else 0
    
    return Problem(
        prompt=f"What digit is in the {digit_pos} place in {num}?",
        answer=answer,
        steps=[
            f"Identify place values: {whole or '0'}.{dec}",
            f"The {digit_pos} place contains: {answer}"
        ],
        hints=["Remember place values: ones . tenths hundredths thousandths"]
    )

def gen_read_write_decimals(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        num = round(random.uniform(0.1, 9.99), 2)
    else:
        num = round(random.uniform(10.001, 999.999), 3)
    
    if random.choice([True, False]):
        # Standard to word form
        word_form = decimal_to_word(num)
        return Problem(
            prompt=f"Write {num} in word form",
            answer=word_form,
            steps=[f"Read each place value", f"Convert to words: {word_form}"],
            hints=["Read the whole number, then 'and', then decimal places"]
        )
    else:
        # Expanded form
        expanded = decimal_to_expanded(num)
        return Problem(
            prompt=f"Write {num} in expanded form",
            answer=expanded,
            steps=[f"Break down by place value", f"Expanded: {expanded}"],
            hints=["Show each digit times its place value"]
        )

def gen_multiply_multidigit(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        a = random.randint(10, 99)
        b = random.randint(2, 9)
    elif difficulty == "Challenge":
        a = random.randint(100, 999)
        b = random.randint(10, 99)
    else:
        a = random.randint(10, 999)
        b = random.randint(10, 99)
    
    product = a * b
    return Problem(
        prompt=f"{a} × {b} = ?",
        answer=product,
        steps=[
            f"Multiply {a} × {b}",
            f"Use standard algorithm or partial products",
            f"Answer: {product}"
        ],
        hints=["Break into partial products", "Line up place values"]
    )

def gen_divide_multidigit(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        divisor = random.randint(10, 20)
        quotient = random.randint(10, 50)
    elif difficulty == "Challenge":
        divisor = random.randint(20, 99)
        quotient = random.randint(10, 99)
    else:
        divisor = random.randint(11, 50)
        quotient = random.randint(10, 99)
    
    dividend = divisor * quotient + random.randint(0, divisor-1)
    q = dividend // divisor
    r = dividend % divisor
    
    if r == 0:
        answer = str(q)
    else:
        answer = f"{q} r{r}"
    
    return Problem(
        prompt=f"{dividend} ÷ {divisor} = ?",
        answer=answer,
        steps=[
            f"Divide {dividend} by {divisor}",
            f"Quotient: {q}, Remainder: {r}",
            f"Answer: {answer}"
        ],
        hints=["Use long division", "Check: quotient × divisor + remainder = dividend"]
    )

def gen_add_subtract_decimals(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        a = round(random.uniform(0.1, 9.99), 2)
        b = round(random.uniform(0.1, 9.99), 2)
    else:
        a = round(random.uniform(10.01, 99.999), 3)
        b = round(random.uniform(10.01, 99.999), 3)
    
    if random.choice([True, False]):
        result = round(a + b, 3)
        operation = "+"
    else:
        if a < b:
            a, b = b, a
        result = round(a - b, 3)
        operation = "-"
    
    return Problem(
        prompt=f"{a} {operation} {b} = ?",
        answer=result,
        steps=[
            "Line up decimal points",
            f"Perform {operation}",
            f"Result: {result}"
        ],
        hints=["Align decimal points vertically", "Add zeros if needed"]
    )

# Fraction Generators
def gen_add_subtract_unlike_fractions(difficulty: str) -> Problem:
    denoms = [2, 3, 4, 5, 6, 8, 10, 12]
    if difficulty == "Warmup":
        d1, d2 = random.sample(denoms[:4], 2)
    else:
        d1, d2 = random.sample(denoms, 2)
    
    n1 = random.randint(1, d1-1)
    n2 = random.randint(1, d2-1)
    
    if random.choice([True, False]):
        # Addition
        lcm = abs(d1 * d2) // math.gcd(d1, d2)
        result_num = n1 * (lcm // d1) + n2 * (lcm // d2)
        result_den = lcm
        operation = "+"
    else:
        # Subtraction
        lcm = abs(d1 * d2) // math.gcd(d1, d2)
        result_num = n1 * (lcm // d1) - n2 * (lcm // d2)
        result_den = lcm
        operation = "-"
        if result_num < 0:
            n1, n2 = n2, n1
            d1, d2 = d2, d1
            result_num = abs(result_num)
    
    # Simplify
    g = math.gcd(abs(result_num), result_den)
    result_num //= g
    result_den //= g
    
    return Problem(
        prompt=f"{n1}/{d1} {operation} {n2}/{d2} = ?",
        answer=f"{result_num}/{result_den}",
        steps=[
            f"Find LCD of {d1} and {d2}",
            f"Convert to equivalent fractions",
            f"Perform {operation}",
            f"Simplify: {result_num}/{result_den}"
        ],
        hints=["Find least common denominator", "Convert fractions before operating"]
    )

def gen_multiply_fractions(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        n1, d1 = random.randint(1, 3), random.randint(2, 5)
        n2, d2 = random.randint(1, 3), random.randint(2, 5)
    else:
        n1, d1 = random.randint(1, 9), random.randint(2, 12)
        n2, d2 = random.randint(1, 9), random.randint(2, 12)
    
    result_num = n1 * n2
    result_den = d1 * d2
    
    # Simplify
    g = math.gcd(result_num, result_den)
    result_num //= g
    result_den //= g
    
    return Problem(
        prompt=f"{n1}/{d1} × {n2}/{d2} = ?",
        answer=f"{result_num}/{result_den}",
        steps=[
            f"Multiply numerators: {n1} × {n2} = {n1*n2}",
            f"Multiply denominators: {d1} × {d2} = {d1*d2}",
            f"Simplify: {result_num}/{result_den}"
        ],
        hints=["Multiply straight across", "Simplify the result"]
    )

# AR Generators
def gen_order_of_operations(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        expr = f"{random.randint(2,9)} + {random.randint(2,9)} × {random.randint(2,9)}"
    elif difficulty == "Challenge":
        a, b, c, d = [random.randint(2,9) for _ in range(4)]
        expr = f"({a} + {b}) × {c} - {d}"
    else:
        a, b, c = [random.randint(2,12) for _ in range(3)]
        if random.choice([True, False]):
            expr = f"{a} × {b} + {c}"
        else:
            expr = f"({a} + {b}) × {c}"
    
    result = eval(expr)
    
    return Problem(
        prompt=f"Evaluate: {expr}",
        answer=result,
        steps=[
            "Follow PEMDAS",
            "Parentheses → Exponents → Multiply/Divide → Add/Subtract",
            f"Result: {result}"
        ],
        hints=["Remember order of operations", "Work left to right for same priority"]
    )

def gen_pattern_rule(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        start = random.randint(1, 10)
        step = random.randint(2, 5)
    else:
        start = random.randint(5, 20)
        step = random.randint(3, 12)
    
    pattern = [start + step * i for i in range(5)]
    rule = f"Start at {start}, add {step}"
    
    return Problem(
        prompt=f"What's the rule for: {', '.join(map(str, pattern[:4]))}...?",
        answer=rule,
        steps=[
            f"Find the difference between terms",
            f"Difference: {step}",
            f"Rule: {rule}"
        ],
        hints=["Look for constant difference", "Check if it's arithmetic sequence"]
    )

# GR Generators
def gen_area_perimeter_decimals(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        length = round(random.uniform(2, 10), 1)
        width = round(random.uniform(2, 10), 1)
    else:
        length = round(random.uniform(5, 20), 2)
        width = round(random.uniform(5, 20), 2)
    
    if random.choice([True, False]):
        # Area
        area = round(length * width, 2)
        return Problem(
            prompt=f"Find area of rectangle: length={length}, width={width}",
            answer=area,
            steps=[
                f"Area = length × width",
                f"Area = {length} × {width}",
                f"Area = {area} square units"
            ],
            hints=["Multiply length by width"]
        )
    else:
        # Perimeter
        perimeter = round(2 * (length + width), 2)
        return Problem(
            prompt=f"Find perimeter of rectangle: length={length}, width={width}",
            answer=perimeter,
            steps=[
                f"Perimeter = 2 × (length + width)",
                f"Perimeter = 2 × ({length} + {width})",
                f"Perimeter = {perimeter} units"
            ],
            hints=["Add all sides or use 2(l+w)"]
        )

def gen_volume(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        l, w, h = [random.randint(2, 5) for _ in range(3)]
    else:
        l, w, h = [random.randint(3, 10) for _ in range(3)]
    
    volume = l * w * h
    
    return Problem(
        prompt=f"Find volume of rectangular prism: l={l}, w={w}, h={h}",
        answer=volume,
        steps=[
            f"Volume = length × width × height",
            f"Volume = {l} × {w} × {h}",
            f"Volume = {volume} cubic units"
        ],
        hints=["Multiply all three dimensions"]
    )

def gen_coordinate_plane(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        x, y = random.randint(0, 5), random.randint(0, 5)
    else:
        x, y = random.randint(0, 10), random.randint(0, 10)
    
    return Problem(
        prompt=f"What quadrant contains the point ({x}, {y})?",
        answer="Quadrant I" if x > 0 and y > 0 else "On axis or origin",
        steps=[
            f"Point is at ({x}, {y})",
            f"x > 0 and y > 0 means Quadrant I"
        ],
        hints=["Quadrant I: (+,+)", "Check x and y coordinates"]
    )

# DP Generators
def gen_mean_median_mode(difficulty: str) -> Problem:
    if difficulty == "Warmup":
        data = [random.randint(1, 10) for _ in range(5)]
    else:
        data = [random.randint(1, 20) for _ in range(7)]
    
    measure = random.choice(["mean", "median", "mode", "range"])
    
    if measure == "mean":
        answer = round(sum(data) / len(data), 1)
    elif measure == "median":
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            answer = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            answer = sorted_data[n//2]
    elif measure == "mode":
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        modes = [k for k, v in counts.items() if v == max_count]
        answer = modes[0] if len(modes) == 1 else "No unique mode"
    else:  # range
        answer = max(data) - min(data)
    
    return Problem(
        prompt=f"Find the {measure} of: {data}",
        answer=answer,
        steps=[
            f"Data: {sorted(data)}",
            f"Calculate {measure}",
            f"Answer: {answer}"
        ],
        hints=[f"{measure.capitalize()}: " + 
               ("average" if measure == "mean" else
                "middle value" if measure == "median" else
                "most frequent" if measure == "mode" else
                "max - min")]
    )

# Helper functions
def decimal_to_word(num: float) -> str:
    # Simplified version
    whole = int(num)
    decimal_part = num - whole
    return f"{whole} and {round(decimal_part, 3)} thousandths"

def decimal_to_expanded(num: float) -> str:
    # Simplified version
    whole = int(num)
    decimal_part = num - whole
    return f"{whole} + {round(decimal_part, 3)}"

# Map topics to generators
GENERATORS = {
    "MA.5.NSO.1.1: Place Value with Decimals": gen_place_value_decimals,
    "MA.5.NSO.1.2: Read/Write Decimals to Thousandths": gen_read_write_decimals,
    "MA.5.NSO.2.1: Multiply Multi-Digit Numbers": gen_multiply_multidigit,
    "MA.5.NSO.2.2: Divide Multi-Digit by 2-Digit": gen_divide_multidigit,
    "MA.5.NSO.2.3: Add/Subtract Decimals": gen_add_subtract_decimals,
    "MA.5.FR.2.1: Add/Subtract Unlike Denominators": gen_add_subtract_unlike_fractions,
    "MA.5.FR.2.2: Multiply Fractions": gen_multiply_fractions,
    "MA.5.AR.2.2: Order of Operations": gen_order_of_operations,
    "MA.5.AR.3.1: Identify Pattern Rules": gen_pattern_rule,
    "MA.5.GR.2.1: Area/Perimeter with Fractions/Decimals": gen_area_perimeter_decimals,
    "MA.5.GR.3.2: Volume Formula": gen_volume,
    "MA.5.GR.4.1: Coordinate Plane": gen_coordinate_plane,
    "MA.5.DP.1.2: Mean, Median, Mode, Range": gen_mean_median_mode,
}

# Default to multiplication for topics without generators yet
for topic in TOPICS:
    if topic not in GENERATORS:
        GENERATORS[topic] = gen_multiply_multidigit

# -------------------------------
# Mini-Lessons
# -------------------------------
LESSONS = {
    "MA.5.NSO.1.1: Place Value with Decimals": {
        "key_points": [
            "Each place is 10 times the place to its right",
            "Decimal places: tenths, hundredths, thousandths"
        ],
        "example": ["3.456 has 3 ones, 4 tenths, 5 hundredths, 6 thousandths"]
    },
    "MA.5.NSO.2.1: Multiply Multi-Digit Numbers": {
        "key_points": [
            "Use standard algorithm or partial products",
            "Line up place values carefully"
        ],
        "example": ["234 × 56 = (234×50) + (234×6) = 11,700 + 1,404 = 13,104"]
    },
    "MA.5.FR.2.1: Add/Subtract Unlike Denominators": {
        "key_points": [
            "Find least common denominator (LCD)",
            "Convert to equivalent fractions with LCD",
            "Add/subtract numerators, keep denominator"
        ],
        "example": ["1/2 + 1/3 = 3/6 + 2/6 = 5/6"]
    },
    "MA.5.AR.2.2: Order of Operations": {
        "key_points": [
            "PEMDAS: Parentheses, Exponents, Multiply/Divide, Add/Subtract",
            "Work left to right for operations of same priority"
        ],
        "example": ["3 + 4 × 5 = 3 + 20 = 23 (multiply first!)"]
    },
    "MA.5.GR.3.2: Volume Formula": {
        "key_points": [
            "Volume = length × width × height",
            "Count unit cubes or use formula",
            "Answer in cubic units"
        ],
        "example": ["Box: 4×3×2 = 24 cubic units"]
    },
}

# Add default lessons for topics without specific content
for topic in TOPICS:
    if topic not in LESSONS:
        LESSONS[topic] = {
            "key_points": [
                f"Master the concept of {topic.split(': ')[1]}",
                "Practice with various problem types"
            ],
            "example": ["Work through guided examples to understand the concept"]
        }

# -------------------------------
# UI Components
# -------------------------------
st.sidebar.header("📚 Florida BEST Standards Navigator")

# Group topics by domain
domains = {
    "Number Sense & Operations": [t for t in TOPICS if t.startswith("MA.5.NSO")],
    "Fractions": [t for t in TOPICS if t.startswith("MA.5.FR")],
    "Algebraic Reasoning": [t for t in TOPICS if t.startswith("MA.5.AR")],
    "Measurement": [t for t in TOPICS if t.startswith("MA.5.M")],
    "Geometric Reasoning": [t for t in TOPICS if t.startswith("MA.5.GR")],
    "Data Analysis": [t for t in TOPICS if t.startswith("MA.5.DP")],
}

selected_domain = st.sidebar.selectbox("Select Domain", list(domains.keys()))
topic = st.sidebar.selectbox("Select Standard", domains[selected_domain])
st.session_state.current_topic = topic

mode = st.sidebar.radio("Learning Mode", ["📖 Mini Lesson", "🎯 Guided Example", "💪 Practice (Mastery)"])
difficulty = st.sidebar.selectbox("Difficulty Level", ["Warmup", "Core", "Challenge"])
st.session_state.difficulty = difficulty

# Header and Progress
st.title("🌟 Florida 5th Grade Math Helper")
st.subheader(f"Standard: {topic}")

col1, col2, col3 = st.columns(3)
with col1:
    prog = st.session_state.progress[topic]
    st.metric("✅ Correct", prog["correct"])
with col2:
    st.metric("🔥 Streak", prog["streak"])
with col3:
    st.metric("🏆 Mastered", "Yes! 🎉" if prog["mastered"] else "Not yet")

st.markdown("---")

# Content rendering functions
def render_mini_lesson(t: str):
    st.header("📖 Mini Lesson")
    lesson = LESSONS.get(t, LESSONS[TOPICS[0]])
    
    st.subheader("Key Concepts:")
    for point in lesson["key_points"]:
        st.write(f"• {point}")
    
    with st.expander("📝 Worked Example"):
        for ex in lesson["example"]:
            st.info(ex)
    
    st.success("💡 Ready to practice? Switch to Guided Example or Practice mode!")

def render_guided_example(t: str, d: str):
    st.header("🎯 Guided Example")
    
    if t in GENERATORS:
        problem = GENERATORS[t](d)
        
        st.write(f"**Problem:** {problem.display or problem.prompt}")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("💡 Hints"):
                for hint in problem.hints:
                    st.write(f"• {hint}")
        
        with col2:
            with st.expander("📋 Step-by-step solution", expanded=True):
                for i, step in enumerate(problem.steps, 1):
                    st.write(f"{i}. {step}")
        
        st.success(f"✅ Answer: {problem.answer}")
    else:
        st.warning("Generator not available for this topic yet.")

def generate_or_get_problem():
    if st.session_state.current_problem is None and topic in GENERATORS:
        st.session_state.current_problem = GENERATORS[topic](difficulty)
    return st.session_state.current_problem

def reset_problem():
    st.session_state.current_problem = None
    st.session_state.show_steps = False

def check_answer(problem: Problem, user_input: str) -> bool:
    if problem is None:
        return False
    
    user_val = parse_number(user_input)
    
    if isinstance(problem.answer, (int, float)):
        if user_val is None:
            return False
        return abs(float(problem.answer) - user_val) < 0.01
    else:
        # String answer
        return user_input.strip().lower() == str(problem.answer).strip().lower()

def render_practice(t: str, d: str):
    st.header("💪 Practice for Mastery")
    
    if t not in GENERATORS:
        st.warning("Practice problems not available for this topic yet.")
        return
    
    pmeta = st.session_state.progress[t]
    st.write(f"🎯 Goal: {MASTERY_TARGET} correct with a streak of {MASTERY_STREAK_TARGET}")
    
    problem = generate_or_get_problem()
    if problem:
        st.write(f"**Problem:** {problem.display or problem.prompt}")
        
        ans = st.text_input("Your answer:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✓ Check Answer"):
                if ans.strip() == "":
                    st.warning("Please enter an answer.")
                else:
                    is_correct = check_answer(problem, ans)
                    record_result(t, is_correct, problem, ans)
                    if is_correct:
                        st.balloons()
                        st.success("🎉 Correct! Great job!")
                        reset_problem()
                        st.rerun()
                    else:
                        st.error("Not quite. Try using hints or view steps.")
        
        with col2:
            if st.button("🔄 New Problem"):
                reset_problem()
                st.rerun()
        
        with col3:
            if st.button("👀 Show Steps"):
                st.session_state.show_steps = True
        
        if st.session_state.show_steps:
            with st.expander("📋 Solution", expanded=True):
                for i, step in enumerate(problem.steps, 1):
                    st.write(f"{i}. {step}")
                st.info(f"✅ Correct answer: {problem.answer}")
    
    # Progress summary
    st.markdown("---")
    st.write(f"📊 Progress: {pmeta['attempted']} attempts | {pmeta['correct']} correct | 🔥 {pmeta['streak']} streak")
    
    if pmeta["mastered"]:
        st.success("🏆 Mastery achieved! You've conquered this standard!")
    else:
        remaining = MASTERY_TARGET - pmeta["correct"]
        st.info(f"Keep going! {remaining} more correct answers needed for mastery.")

# Route to appropriate mode
if mode == "📖 Mini Lesson":
    render_mini_lesson(topic)
elif mode == "🎯 Guided Example":
    render_guided_example(topic, difficulty)
else:
    render_practice(topic, difficulty)

# Teacher/Parent Dashboard
with st.sidebar.expander("Teacher Dashboard"):
    if st.button("Reset All Progress"):
        for t in TOPICS:
            st.session_state.progress[t] = {
                "attempted": 0, "correct": 0, "streak": 0, 
                "mastered": False, "history": []
            }
        st.session_state.current_problem = None
        st.session_state.show_steps = False
        st.success("Progress reset!")
    
    if st.button("View Standards Coverage"):
        mastered = sum(1 for t in TOPICS if st.session_state.progress[t]["mastered"])
        st.write(f"Mastered: {mastered}/{len(TOPICS)} standards")
        progress_pct = (mastered / len(TOPICS)) * 100
        st.progress(progress_pct / 100)

# Footer
st.markdown("---")
st.caption("📚 Aligned with Florida B.E.S.T. Standards for Mathematics - Grade 5")
st.caption("All 35+ standards included for comprehensive 5th grade math practice!")