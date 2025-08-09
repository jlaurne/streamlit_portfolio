import streamlit as st
import pandas as pd
import datetime
from datetime import date
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Zodiac Academy Book Club",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .main-header {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #4A0E4E, #81007F, #FF6B9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .book-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #FF6B9D;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(255, 107, 157, 0.3);
    }
    
    .safe-zone {
        background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #00ff88;
    }
    
    .spoiler-zone {
        background: linear-gradient(135deg, #8b0000 0%, #dc143c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff4444;
    }
    
    .theory-box {
        background: linear-gradient(135deg, #2d1b69 0%, #11998e 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ffd700;
    }
    
    .character-card {
        background: linear-gradient(135deg, #4A0E4E 0%, #81007F 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #FF6B9D 0%, #4A0E4E 100%);
        height: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing discussions
if 'discussions' not in st.session_state:
    st.session_state.discussions = {
        'book1_safe': [],
        'book1_spoilers': [],
        'character_thoughts': [],
        'theories': [],
        'emotional_damage': []
    }

if 'reading_progress' not in st.session_state:
    st.session_state.reading_progress = {
        'Ketchup': {'current_book': '5.5/5.6', 'progress_percent': 85, 'last_update': '2025-08-08'},
        'Snick': {'current_book': 8, 'progress_percent': 100, 'last_update': '2024-12-15'}
    }

# Sidebar
st.sidebar.title("⭐ Zodiac Academy Book Club")
st.sidebar.markdown("---")

# Reading Progress
st.sidebar.markdown("### 📚 Reading Progress")
Ketchup_progress = st.session_state.reading_progress['Ketchup']
your_progress = st.session_state.reading_progress['Snick']

st.sidebar.markdown(f"**Ketchup:** Reading Novellas 5.5/5.6 ({Ketchup_progress['progress_percent']}%)")
st.sidebar.markdown(f"**Snick:** Completed Series ✨")

# Navigation
page = st.sidebar.selectbox(
    "Navigate to:",
    ["📖 Reading Dashboard", "💭 Books 1-5 Discussion", "🎉 Short Stories", "⚡ Character Deep Dive", 
     "🔮 What's Coming Next", "💔 We Need to Talk About Book 4", "📝 Add Thoughts"]
)

st.sidebar.markdown("---")
st.sidebar.info("🚨 Spoiler Protection Active! Only discussions for completed books are shown.")

# Books data
books = [
    {"num": 1, "title": "The Awakening", "status_Ketchup": "Complete", "status_you": "Complete"},
    {"num": 2, "title": "Ruthless Fae", "status_Ketchup": "Complete", "status_you": "Complete"},
    {"num": 3, "title": "The Reckoning", "status_Ketchup": "Complete", "status_you": "Complete"},
    {"num": 4, "title": "Shadow Princess", "status_Ketchup": "Complete", "status_you": "Complete"},
    {"num": 5, "title": "Cursed Fates", "status_Ketchup": "Complete", "status_you": "Complete"},
    {"num": "5.5", "title": "The Big A.S.S. Party", "status_Ketchup": "Reading", "status_you": "Complete"},
    {"num": "5.6", "title": "Seth on the Moon", "status_Ketchup": "Reading", "status_you": "Complete"},
    {"num": 6, "title": "Fated Throne", "status_Ketchup": "Not Started", "status_you": "Complete"},
    {"num": 7, "title": "Heartless Sky", "status_Ketchup": "Not Started", "status_you": "Complete"},
    {"num": 8, "title": "Sorrow and Starlight", "status_Ketchup": "Not Started", "status_you": "Complete"}
]

# Main content
if page == "📖 Reading Dashboard":
    st.markdown('<div class="main-header">Zodiac Academy Book Club</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #FF6B9D; margin-bottom: 2rem;">Your Private Discussion Space 💫</div>', unsafe_allow_html=True)
    
    # Progress Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="book-card">', unsafe_allow_html=True)
        st.markdown("### 📚 Series Progress")
        
        # Create progress visualization
        progress_data = pd.DataFrame(books)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Ketchup',
            x=[f"Book {b['num']}" for b in books],
            y=[1 if b['status_Ketchup'] == 'Complete' else 0.5 if b['status_Ketchup'] == 'Reading' else 0 for b in books],
            marker_color='#FF6B9D'
        ))
        fig.add_trace(go.Bar(
            name='You',
            x=[f"Book {b['num']}" for b in books],
            y=[1 if b['status_you'] == 'Complete' else 0 for b in books],
            marker_color='#4A0E4E'
        ))
        
        fig.update_layout(
            title="Reading Progress Comparison",
            yaxis_title="Completion Status",
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="book-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Current Status")
        st.markdown("**Ketchup is reading:** The Big A.S.S. Party & Seth on the Moon")
        st.markdown("**Current focus:** Post-Book 5 short stories and character moments")
        st.markdown("**Safe to discuss:** EVERYTHING through Book 5!")
        st.markdown("**⚠️ AVOID:** Book 6+ spoilers (Fated Throne and beyond)")
        
        st.markdown("### 📅 Reading Pace")
        st.metric("Books completed", "5", "+1 since last check")
        st.metric("Emotional damage sustained", "High", "Book 4 broke us all")
        st.metric("Ready for Book 6?", "Almost!", "Novellas first")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Book Status Cards
    st.markdown("### 📖 Book by Book Status")
    cols = st.columns(4)
    for i, book in enumerate(books[:4]):
        with cols[i % 4]:
            if book['status_Ketchup'] == 'Reading':
                card_class = 'theory-box'
                status_emoji = '📖'
            elif book['status_Ketchup'] == 'Complete':
                card_class = 'safe-zone'
                status_emoji = '✅'
            else:
                card_class = 'spoiler-zone'
                status_emoji = '🔒'
            
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            st.markdown(f"### {status_emoji} Book {book['num']}")
            st.markdown(f"**{book['title']}**")
            st.markdown(f"Ketchup: {book['status_Ketchup']}")
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "💭 Books 1-5 Discussion":
    st.markdown('<div class="main-header">Books 1-5 Discussion Zone</div>', unsafe_allow_html=True)
    st.markdown("*Everything through Cursed Fates is fair game!*")
    
    st.markdown('<div class="safe-zone">', unsafe_allow_html=True)
    st.markdown("### ✅ SAFE TO DISCUSS: Books 1-5 Complete!")
    st.markdown("Ketchup has been through the emotional gauntlet - discuss away!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Discussion categories for Books 1-5
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Book 1-2 Feels", "Book 3 Chaos", "Book 4 PAIN", "Book 5 Recovery", "Overall Arc"])
    
    with tab1:
        st.markdown("### 🌟 Books 1-2: The Foundation")
        st.markdown("**Discussion Topics:**")
        st.markdown("- The Awakening introductions vs how you feel about everyone now")
        st.markdown("- Ruthless Fae development - when did you start shipping the pairs?")
        st.markdown("- Order revelations and power development")
        st.markdown("- Early Heir dynamics vs later character growth")
        
        book12_thought = st.text_area("Your thoughts on the early books now that you've seen the full character development:")
        if st.button("Add Book 1-2 Thoughts"):
            st.success("Thoughts saved!")
    
    with tab2:
        st.markdown("### ⚡ Book 3: The Reckoning")
        st.markdown("**Major Discussion Points:**")
        st.markdown("- The Reckoning power reveals")
        st.markdown("- Relationship developments heating up")
        st.markdown("- Academy politics and Lionel's increasing threat")
        st.markdown("- Setup for the devastation to come...")
        
    with tab3:
        st.markdown("### 💔 Book 4: Shadow Princess")
        st.markdown("**WE NEED TO TALK ABOUT THIS:**")
        
        st.error("⚠️ MAJOR EMOTIONAL DAMAGE ZONE ⚠️")
        
        if st.button("🔓 UNLOCK BOOK 4 TRAUMA DISCUSSION"):
            st.markdown("### The Big Topics:")
            st.markdown("- **THAT ending** - how are we still breathing?")
            st.markdown("- Character sacrifices and impossible choices")
            st.markdown("- The moment everything changed")
            st.markdown("- How did you cope? (Asking for both of us)")
            
            st.text_area("Book 4 feelings dump (all the tears welcome):")
    
    with tab4:
        st.markdown("### 🌅 Book 5: Cursed Fates")
        st.markdown("**Recovery and New Challenges:**")
        st.markdown("- Picking up the pieces after Book 4")
        st.markdown("- New dynamics and power shifts")
        st.markdown("- Hope vs despair balance")
        st.markdown("- Setting up for the final act")
    
    with tab5:
        st.markdown("### 📚 Overall Character & Plot Arc")
        st.markdown("**Big Picture Discussions:**")
        
        character_focus = st.selectbox("Pick a character to deep dive:", 
                                     ["Tory", "Darcy", "Darius", "Caleb", "Max", "Seth", "Orion", "Lionel"])
        
        st.markdown(f"#### {character_focus} Evolution (Books 1-5)")
        st.text_area(f"Your thoughts on {character_focus}'s journey so far:")

elif page == "🎉 Short Stories":
    st.markdown('<div class="main-header">Short Stories Deep Dive</div>', unsafe_allow_html=True)
    st.markdown("*Currently Reading: The Big A.S.S. Party & Seth on the Moon*")
    
    st.markdown('<div class="theory-box">', unsafe_allow_html=True)
    st.markdown("### 📖 CURRENTLY READING ZONE")
    st.markdown("Perfect time to discuss the short stories as she reads them!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎉 The Big A.S.S. Party (5.5)")
        st.markdown("**Discussion Points:**")
        st.markdown("- Post-Book 5 celebrations and moments")
        st.markdown("- Character interactions and relationships")
        st.markdown("- Light-hearted content after Book 5's intensity")
        st.markdown("- Setup moments for what's coming")
        
        party_thoughts = st.text_area("Your thoughts on The Big A.S.S. Party:")
        
    with col2:
        st.markdown("### 🌙 Seth on the Moon (5.6)")
        st.markdown("**Discussion Points:**")
        st.markdown("- Seth's perspective and character development")
        st.markdown("- His unique storyline and experiences")
        st.markdown("- Character depth and backstory")
        st.markdown("- How it fits into the larger narrative")
        
        seth_thoughts = st.text_area("Your thoughts on Seth's story:")
    
    st.markdown("### 💭 Short Story Impact")
    st.markdown("How do these shorter pieces add to the overall series? What new insights do they give?")
    
    comparison_thoughts = st.text_area("How do these short stories enhance the main series for you?")
    
    if st.button("Save Short Story Thoughts"):
        st.success("Short story discussions saved!")

elif page == "⚡ Character Deep Dive":
    st.markdown('<div class="main-header">Character Analysis</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="spoiler-zone">', unsafe_allow_html=True)
    st.markdown("### 🚨 SPOILER WARNING")
    st.markdown("This section contains character analysis across the full series. Only view after Ketchup finishes more books!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Character evolution tracking (for when she's further along)
    characters = {
        "Tory": {"growth": 95, "romance": 100, "power": 90},
        "Darcy": {"growth": 92, "romance": 85, "power": 88},
        "Darius": {"growth": 98, "romance": 100, "power": 95},
        "Caleb": {"growth": 85, "romance": 80, "power": 85},
        "Max": {"growth": 88, "romance": 75, "power": 90},
        "Seth": {"growth": 90, "romance": 70, "power": 85}
    }
    
    if st.button("🔓 UNLOCK CHARACTER ANALYSIS (Spoiler Alert!)"):
        st.warning("Remember: Ketchup is only on Book 1! Don't accidentally spoil anything!")
        
        for char, stats in characters.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f'<div class="character-card"><h3>{char}</h3></div>', unsafe_allow_html=True)
            with col2:
                st.progress(stats['growth']/100, text=f"Character Growth: {stats['growth']}%")
                st.progress(stats['romance']/100, text=f"Romance Development: {stats['romance']}%")
                st.progress(stats['power']/100, text=f"Power Evolution: {stats['power']}%")

elif page == "🔮 What's Coming Next":
    st.markdown('<div class="main-header">What\'s Coming Next</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="spoiler-zone">', unsafe_allow_html=True)
    st.markdown("### 🚨 SPOILER WARNING: Books 6-8")
    st.markdown("This section contains info about Fated Throne, Heartless Sky, and Sorrow and Starlight!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔓 UNLOCK FUTURE BOOKS DISCUSSION (Major Spoilers!)"):
        st.error("⚠️ MAJOR SPOILERS FOR BOOKS 6-8 AHEAD!")
        
        tab1, tab2, tab3 = st.tabs(["Book 6 Prep", "Book 7 Warning", "Series Finale"])
        
        with tab1:
            st.markdown("### 📚 Fated Throne Preparation")
            st.markdown("What to expect without major spoilers:")
            st.markdown("- Stakes get MUCH higher")
            st.markdown("- Political intrigue intensifies")
            st.markdown("- Character development continues")
            st.markdown("- Prepare for emotional investment")
        
        with tab2:
            st.markdown("### ⚠️ Heartless Sky Warning")
            st.markdown("**EMOTIONAL PREPARATION REQUIRED:**")
            st.markdown("- Have tissues ready")
            st.markdown("- Clear your schedule")
            st.markdown("- Prepare for book hangover")
            st.markdown("- Maybe warn Ketchup you'll be unavailable")
        
        with tab3:
            st.markdown("### 🌟 Series Finale")
            st.markdown("Sorrow and Starlight - the epic conclusion")
            st.markdown("No spoilers, but prepare for:")
            st.markdown("- All the emotions")
            st.markdown("- Satisfying conclusions")
            st.markdown("- Epic finale moments")

elif page == "💔 We Need to Talk About Book 4":
    st.markdown('<div class="main-header">Emotional Damage Report</div>', unsafe_allow_html=True)
    st.markdown("*For when Caroline Peckham and Susanne Valenti destroy your soul*")
    
    st.markdown('<div class="spoiler-zone">', unsafe_allow_html=True)
    st.markdown("### ⚠️ EXTREME SPOILER ZONE")
    st.markdown("This is where we cry about THAT scene, THOSE deaths, and ALL the pain.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Emotional damage tracker
    damage_levels = {
        "Book 1": 20,
        "Book 2": 45,
        "Book 3": 60,
        "Book 4": 85,
        "Book 5": 95,
        "Book 6": 100,
        "Book 7": 150,  # Off the charts
        "Book 8": 200   # Recovery mode
    }
    
    fig = px.bar(x=list(damage_levels.keys()), y=list(damage_levels.values()),
                 title="Emotional Damage by Book",
                 color=list(damage_levels.values()),
                 color_continuous_scale="Reds")
    fig.update_layout(yaxis_title="Emotional Damage Level (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔓 UNLOCK CRYING SESSION"):
        st.error("WARNING: Major spoilers ahead!")
        st.markdown("### Most Devastating Moments:")
        st.markdown("- 📚 Book 4: *You know what happens* 💔")
        st.markdown("- 📚 Book 6: The throne room scene 😭")
        st.markdown("- 📚 Book 7: EVERYTHING. JUST EVERYTHING.")

elif page == "📝 Add Thoughts":
    st.markdown('<div class="main-header">Add Your Thoughts</div>', unsafe_allow_html=True)
    
    # Quick thought logger
    thought_category = st.selectbox("What kind of thought?", 
                                   ["Book 1 Safe", "Character Development", "Plot Theory", 
                                    "Emotional Reaction", "Favorite Quote", "Question for Ketchup"])
    
    thought_content = st.text_area("Your thought:", height=150)
    spoiler_level = st.selectbox("Spoiler Level:", ["Safe (Book 1)", "Minor Spoilers", "Major Spoilers", "Series Ending"])
    
    if st.button("Save Thought"):
        # Save to appropriate category
        new_thought = {
            'content': thought_content,
            'category': thought_category,
            'spoiler_level': spoiler_level,
            'date': str(date.today())
        }
        
        if spoiler_level == "Safe (Book 1)":
            st.session_state.discussions['book1_safe'].append(new_thought)
        else:
            st.session_state.discussions['character_thoughts'].append(new_thought)
        
        st.success("Thought saved! It will appear in the appropriate section.")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #FF6B9D;">Built for book besties who need spoiler-free discussion space ⭐✨</div>', unsafe_allow_html=True)