# app.py - Professional Movie Recommender with Animations & Modern UI
import streamlit as st
import requests
import time
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CineMate Pro - AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ADVANCED CUSTOM CSS
# =========================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Container */
    .main-container {
        padding: 2rem;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, rgba(102,126,234,0.95) 0%, rgba(118,75,162,0.95) 100%);
        border-radius: 30px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #ffd89b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 2rem;
    }
    
    /* Movie Card - Glassmorphism */
    .movie-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 15px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .movie-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        border-color: rgba(102,126,234,0.8);
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .movie-card:hover::before {
        left: 100%;
    }
    
    .movie-poster {
        width: 100%;
        border-radius: 15px;
        height: 300px;
        object-fit: cover;
        transition: transform 0.3s;
    }
    
    .movie-title {
        font-size: 1rem;
        font-weight: 600;
        color: white;
        margin: 12px 0 5px 0;
        text-align: center;
        font-family: 'Poppins', sans-serif;
    }
    
    .movie-year {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.7);
        text-align: center;
    }
    
    .rating-badge {
        position: absolute;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #FFD700, #FFA500);
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        color: #000;
        z-index: 1;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.95) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Custom Button */
    .custom-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
        margin: 5px 0;
    }
    
    .custom-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0 1.5rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Stats Card */
    .stats-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 10px 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #FFD700;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Loading Animation */
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    /* Select Box */
    .stSelectbox > div {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Search Box */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        padding: 10px 20px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.3);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# API CONFIGURATION
# =========================
API_URL = "https://movie-recommendation-system-9l20.onrender.com" or "http://localhost:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
# Session State
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'recent_searches' not in st.session_state:
    st.session_state.recent_searches = []

# =========================
# API FUNCTIONS
# =========================
@st.cache_data(ttl=300)
def get_home_feed(category="popular", limit=24):
    try:
        response = requests.get(f"{API_URL}/home", params={"category": category, "limit": limit}, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

@st.cache_data(ttl=60)
def search_tmdb(query):
    if not query:
        return []
    try:
        response = requests.get(f"{API_URL}/tmdb/search", params={"query": query}, timeout=10)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except:
        return []

@st.cache_data(ttl=300)
def get_movie_details(tmdb_id):
    try:
        response = requests.get(f"{API_URL}/movie/id/{tmdb_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@st.cache_data(ttl=300)
def get_search_bundle(query):
    if not query:
        return None
    try:
        response = requests.get(f"{API_URL}/movie/search", params={"query": query}, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# =========================
# PROFESSIONAL UI COMPONENTS
# =========================
def display_movie_card(movie, key, show_rating=True):
    if not movie:
        return
    
    poster = movie.get("poster_url")
    if not poster:
        poster = "https://via.placeholder.com/300x450?text=No+Poster"
    
    title = movie.get("title", "Unknown")[:35]
    rating = movie.get("vote_average", 0)
    movie_id = movie.get("tmdb_id", 0)
    year = movie.get("release_date", "")[:4] if movie.get("release_date") else ""
    
    st.markdown(f"""
    <div class="movie-card">
        {f'<div class="rating-badge">⭐ {rating:.1f}</div>' if show_rating and rating > 0 else ''}
        <img src="{poster}" class="movie-poster" style="height: 280px;">
        <div class="movie-title">{title}</div>
        <div class="movie-year">{year}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 Details", key=f"det_{key}", use_container_width=True):
            st.session_state.selected_movie = movie_id
            st.session_state.view = 'movie'
            st.rerun()
    with col2:
        is_fav = movie_id in st.session_state.favorites
        btn_text = "❤️ Saved" if is_fav else "🤍 Save"
        if st.button(btn_text, key=f"fav_{key}", use_container_width=True):
            if is_fav:
                st.session_state.favorites.remove(movie_id)
                st.toast("Removed from favorites", icon="💔")
            else:
                st.session_state.favorites.append(movie_id)
                st.toast("Added to favorites", icon="❤️")
            time.sleep(0.3)
            st.rerun()

def display_hero_section():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🎬 CineMate Pro</div>
        <div class="hero-subtitle">
            Experience AI-Powered Movie Recommendations Like Never Before
        </div>
        <p style="color: rgba(255,255,255,0.8);">
            Discover movies tailored to your taste using advanced TF-IDF algorithms
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: white;">🎬 CineMate</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">AI Movie Recommender</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        nav_options = {
            "🏠 Home": "home",
            "❤️ Favorites": "favorites",
            "🔍 Search": "search"
        }
        
        for label, view in nav_options.items():
            if st.button(label, use_container_width=True, key=f"nav_{view}"):
                st.session_state.view = view
                st.rerun()
        
        st.markdown("---")
        
        # Stats
        st.markdown("### 📊 Your Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.favorites)}</div>
                <div style="color: white;">Favorites</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">{len(st.session_state.recent_searches)}</div>
                <div style="color: white;">Searches</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About CineMate"):
            st.markdown("""
            **Features:**
            - 🎯 TF-IDF Based Recommendations
            - 🎭 Genre Similarity Matching
            - 🔍 Real-time TMDB Integration
            - ❤️ Personalized Favorites
            - 🎨 Modern Glassmorphism UI
            
            **Tech Stack:**
            - FastAPI Backend
            - Streamlit Frontend
            - TMDB API
            - Machine Learning
            """)
        
        st.markdown("---")
        st.caption("Made with ❤️ | Version 3.0")

def display_home():
    display_hero_section()
    
    # Category Selection with Icons
    st.markdown('<p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">🎯 Explore Categories</p>', unsafe_allow_html=True)
    
    categories = {
        "popular": "🔥 Popular",
        "top_rated": "⭐ Top Rated", 
        "upcoming": "📅 Upcoming",
        "now_playing": "🎬 Now Playing",
        "trending": "📈 Trending"
    }
    
    cols = st.columns(5)
    selected_category = "popular"
    for idx, (cat_value, cat_label) in enumerate(categories.items()):
        with cols[idx]:
            if st.button(cat_label, key=f"cat_{cat_value}", use_container_width=True):
                selected_category = cat_value
                st.rerun()
    
    st.markdown(f'<div class="section-header">{categories[selected_category]} Movies</div>', unsafe_allow_html=True)
    
    with st.spinner("Loading amazing movies for you..."):
        movies = get_home_feed(category=selected_category, limit=20)
        
        if movies:
            # Responsive grid
            cols_per_row = 4
            for i in range(0, len(movies), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(movies):
                        with cols[j]:
                            display_movie_card(movies[i+j], f"home_{i+j}")
        else:
            st.error("Unable to load movies. Please check your connection.")

def display_favorites():
    st.markdown('<div class="section-header">❤️ Your Favorites Collection</div>', unsafe_allow_html=True)
    
    if not st.session_state.favorites:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h3 style="color: rgba(255,255,255,0.7);">No favorites yet</h3>
            <p style="color: rgba(255,255,255,0.5);">Start exploring and save movies you love!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎬 Start Exploring", use_container_width=True):
            st.session_state.view = 'home'
            st.rerun()
        return
    
    with st.spinner("Loading your favorites..."):
        fav_movies = []
        for movie_id in st.session_state.favorites:
            movie = get_movie_details(movie_id)
            if movie:
                fav_movies.append(movie)
        
        if fav_movies:
            st.markdown(f"### You have {len(fav_movies)} favorite movies")
            cols = st.columns(3)
            for idx, movie in enumerate(fav_movies):
                with cols[idx % 3]:
                    display_movie_card(movie, f"fav_{idx}")
        else:
            st.warning("Could not load favorite movies")

def display_search():
    st.markdown('<div class="section-header">🔍 Discover Movies</div>', unsafe_allow_html=True)
    
    # Search input with placeholder
    query = st.text_input(
        "",
        placeholder="Search by movie title... (e.g., Inception, The Dark Knight, Interstellar)",
        label_visibility="collapsed"
    )
    
    if query:
        # Add to recent searches
        if query not in st.session_state.recent_searches:
            st.session_state.recent_searches.insert(0, query)
            st.session_state.recent_searches = st.session_state.recent_searches[:5]
        
        with st.spinner(f"Searching for '{query}'..."):
            results = search_tmdb(query)
            
            if results:
                st.markdown(f'### Found {len(results)} results for "{query}"')
                
                # Display results
                cols = st.columns(3)
                for idx, movie in enumerate(results[:15]):
                    with cols[idx % 3]:
                        movie_card = {
                            "tmdb_id": movie.get("id"),
                            "title": movie.get("title"),
                            "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None,
                            "release_date": movie.get("release_date"),
                            "vote_average": movie.get("vote_average")
                        }
                        display_movie_card(movie_card, f"search_{idx}")
            else:
                st.warning(f"No results found for '{query}'. Try a different title.")
    
    # Recent searches
    if st.session_state.recent_searches:
        st.markdown("### 🔄 Recent Searches")
        recent_cols = st.columns(min(5, len(st.session_state.recent_searches)))
        for idx, search_term in enumerate(st.session_state.recent_searches[:5]):
            with recent_cols[idx]:
                if st.button(search_term, key=f"recent_{idx}"):
                    st.rerun()

def display_movie_details():
    if not st.session_state.selected_movie:
        st.warning("No movie selected")
        st.session_state.view = 'home'
        st.rerun()
    
    # Back button
    if st.button("← Back to Home", use_container_width=False):
        st.session_state.view = 'home'
        st.rerun()
    
    with st.spinner("Loading movie details..."):
        movie = get_movie_details(st.session_state.selected_movie)
        
        if not movie:
            st.error("Movie not found")
            return
        
        # Hero section for movie
        col1, col2 = st.columns([1, 2])
        
        with col1:
            poster = movie.get("poster_url")
            if poster:
                st.image(poster, use_column_width=True)
            else:
                st.image("https://via.placeholder.com/300x450?text=No+Poster", use_column_width=True)
        
        with col2:
            st.markdown(f"<h1 style='font-size: 3rem;'>{movie.get('title', 'Unknown')}</h1>", unsafe_allow_html=True)
            
            # Movie stats with icons
            info_cols = st.columns(4)
            with info_cols[0]:
                year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
                st.metric("📅 Year", year)
            with info_cols[1]:
                rating = movie.get("vote_average", 0)
                st.metric("⭐ Rating", f"{rating:.1f}/10")
            with info_cols[2]:
                genres = [g.get("name", "") for g in movie.get("genres", [])]
                st.metric("🎭 Genres", genres[0] if genres else "N/A")
            with info_cols[3]:
                st.metric("❤️ Favorites", "Yes" if st.session_state.selected_movie in st.session_state.favorites else "No")
            
            st.markdown("---")
            st.markdown("### 📖 Synopsis")
            st.markdown(movie.get("overview", "No overview available"))
            
            # Action buttons
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("❤️ Add to Favorites", use_container_width=True):
                    if st.session_state.selected_movie not in st.session_state.favorites:
                        st.session_state.favorites.append(st.session_state.selected_movie)
                        st.success("Added to favorites!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
            with col_b:
                st.button("🔗 Share", use_container_width=True)
            with col_c:
                st.button("🎬 Trailer", use_container_width=True)
        
        # Recommendations section
        st.markdown("---")
        st.markdown('<div class="section-header">🎯 Intelligent Recommendations</div>', unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 1rem;'>Powered by AI and TMDB's vast database</p>", unsafe_allow_html=True)
        
        with st.spinner("Analyzing and finding similar movies..."):
            bundle = get_search_bundle(movie.get("title"))
            
            if bundle:
                tab1, tab2 = st.tabs(["🎯 AI Content-Based", "🎭 Genre Similarity"])
                
                with tab1:
                    st.markdown("### Based on Movie Content & Metadata")
                    st.caption("Using TF-IDF algorithm to find semantically similar movies")
                    
                    tfidf_recs = bundle.get("tfidf_recommendations", [])
                    if tfidf_recs:
                        rec_movies = [rec.get("tmdb") for rec in tfidf_recs if rec.get("tmdb")]
                        if rec_movies:
                            cols = st.columns(4)
                            for idx, rec_movie in enumerate(rec_movies[:8]):
                                with cols[idx % 4]:
                                    display_movie_card(rec_movie, f"rec_{idx}")
                        else:
                            st.info("✨ Recommendations ready but posters loading...")
                    else:
                        st.info("🎬 No content-based recommendations available for this movie")
                
                with tab2:
                    st.markdown("### Movies You May Like Based on Genre")
                    st.caption("Discovering popular movies from similar genres")
                    
                    genre_recs = bundle.get("genre_recommendations", [])
                    if genre_recs:
                        cols = st.columns(4)
                        for idx, rec_movie in enumerate(genre_recs[:8]):
                            with cols[idx % 4]:
                                display_movie_card(rec_movie, f"genre_{idx}")
                    else:
                        st.info("🎭 No genre-based recommendations found")
            else:
                st.warning("Unable to fetch recommendations. Please try again.")

# =========================
# MAIN APP
# =========================
def main():
    display_sidebar()
    
    # Main content area
    if st.session_state.view == 'home':
        display_home()
    elif st.session_state.view == 'favorites':
        display_favorites()
    elif st.session_state.view == 'search':
        display_search()
    elif st.session_state.view == 'movie':
        display_movie_details()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">
            🎬 Powered by TMDB API | 🤖 AI Recommendations using TF-IDF | 💡 Made with Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()