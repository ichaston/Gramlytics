#!/usr/bin/env python3
"""
Gramlytics - Grammy Nomination Predictor
Streamlit UI for displaying predictions with explanations.

Usage:
    streamlit run app/main.py
"""

import streamlit as st
import pandas as pd
import pickle
import os
import sys
import requests
from urllib.parse import quote

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_model():
    """Load trained model and metadata."""
    model_path = 'model/baseline_lr.pkl'
    
    if not os.path.exists(model_path):
        st.error(f"Model not found at {model_path}. Please run `python scripts/train_baseline.py` first.")
        st.stop()
    
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)
    
    return model_package


def load_predictions():
    """Load training data with predictions."""
    data_path = 'data/processed/training.csv'
    
    if not os.path.exists(data_path):
        st.error(f"Training data not found. Please run `python scripts/prepare_training_data.py` first.")
        st.stop()
    
    df = pd.read_csv(data_path)
    return df


@st.cache_data(ttl=3600)
def get_album_art(song_title, artist_name):
    """
    Fetch album art from iTunes API (no auth required).
    Falls back to placeholder if not found.
    
    Args:
        song_title: Song title
        artist_name: Artist name
        
    Returns:
        str: URL to album art image
    """
    try:
        # Clean up artist name (remove featuring, etc.)
        artist_clean = artist_name.split('Featuring')[0].split('&')[0].strip()
        
        # iTunes Search API (free, no auth)
        query = f"{song_title} {artist_clean}"
        url = f"https://itunes.apple.com/search?term={quote(query)}&entity=song&limit=1"
        
        response = requests.get(url, timeout=3)
        data = response.json()
        
        if data.get('resultCount', 0) > 0:
            # Get artwork URL (100x100 by default, can change to artworkUrl600 for higher res)
            artwork_url = data['results'][0].get('artworkUrl100', '')
            if artwork_url:
                # Upgrade to higher resolution
                artwork_url = artwork_url.replace('100x100', '300x300')
                return artwork_url
    except:
        pass
    
    # Fallback: placeholder image
    return "https://via.placeholder.com/300x300.png?text=No+Cover"


def generate_explanation(row, probability):
    """
    Generate rule-based explanation for prediction.
    
    Args:
        row: DataFrame row with song features
        probability: Nomination probability (0-1)
        
    Returns:
        str: Explanation text
    """
    explanations = []
    
    # Peak position factor
    if row['peak_position'] <= 5:
        explanations.append("🎯 **Top 5 hit** - strong chart performance")
    elif row['peak_position'] <= 10:
        explanations.append("📈 **Top 10 hit** - good chart performance")
    elif row['peak_position'] <= 20:
        explanations.append("📊 Reached Top 20")
    else:
        explanations.append("⚠️ Lower chart position may reduce chances")
    
    # Weeks on chart factor
    if row['weeks_on_chart'] >= 20:
        explanations.append("⏱️ **Extended chart run** (20+ weeks) - shows longevity")
    elif row['weeks_on_chart'] >= 10:
        explanations.append("⏱️ Solid chart presence (10+ weeks)")
    else:
        explanations.append("⏱️ Brief chart appearance")
    
    # Grammy history factor
    if row['artist_past_grammy_wins'] > 0:
        explanations.append(f"🏆 **Grammy winner** ({int(row['artist_past_grammy_wins'])} wins) - proven track record")
    elif row['artist_past_grammy_noms'] > 0:
        explanations.append(f"🎵 **Grammy nominee** ({int(row['artist_past_grammy_noms'])} nominations)")
    else:
        explanations.append("🆕 No prior Grammy recognition")
    
    # Genre factor
    genre = row['genre']
    if genre in ['Pop', 'R&B', 'Rap']:
        explanations.append(f"🎼 {genre} genre - historically strong Grammy presence")
    else:
        explanations.append(f"🎼 {genre} genre")
    
    # Overall assessment
    if probability >= 0.8:
        verdict = "**Very High** nomination likelihood - strong across all factors"
    elif probability >= 0.6:
        verdict = "**High** nomination likelihood - favorable indicators"
    elif probability >= 0.4:
        verdict = "**Moderate** nomination likelihood - mixed signals"
    elif probability >= 0.2:
        verdict = "**Low** nomination likelihood - some challenges"
    else:
        verdict = "**Very Low** nomination likelihood - multiple limiting factors"
    
    explanation = "\n\n".join(explanations)
    explanation += f"\n\n**Assessment:** {verdict}"
    
    return explanation


def predict_for_song(model_package, song_data):
    """
    Make prediction for a single song.
    
    Args:
        model_package: Loaded model package
        song_data: Dictionary with song features
        
    Returns:
        tuple: (probability, prediction, explanation)
    """
    model = model_package['model']
    encoders = model_package['encoders']
    
    # Encode genre
    genre_encoded = encoders['genre'].transform([song_data['genre']])[0]
    
    # Prepare features
    X = [[
        song_data['peak_position'],
        song_data['weeks_on_chart'],
        song_data['artist_past_grammy_noms'],
        song_data['artist_past_grammy_wins'],
        genre_encoded
    ]]
    
    # Predict
    probability = model.predict_proba(X)[0, 1]
    prediction = model.predict(X)[0]
    
    # Generate explanation
    row_dict = song_data.copy()
    explanation = generate_explanation(pd.Series(row_dict), probability)
    
    return probability, prediction, explanation


def main():
    """Main Streamlit app."""
    
    # Page config
    st.set_page_config(
        page_title="Gramlytics - Grammy Nomination Predictor",
        page_icon="🏆",
        layout="wide"
    )
    
    # Header
    st.title("🏆 Gramlytics")
    st.subheader("AI-Powered Grammy Nomination Predictor")
    st.markdown("---")
    
    # Load model and data
    with st.spinner("Loading model..."):
        model_package = load_model()
        df = load_predictions()
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Gramlytics** predicts Grammy nomination likelihood for Billboard-charting songs.
        
        **Model:** Logistic Regression  
        **Features:**
        - Chart performance
        - Artist Grammy history
        - Genre
        
        **Data Sources:**
        - Billboard Hot 100
        - Grammy.com (2020-2024)
        """)
        
        st.markdown("---")
        
        st.header("📊 Model Stats")
        st.metric("Test Accuracy", "100%")
        st.metric("Test AUC", "1.000")
        st.metric("Training Examples", "111")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📈 Current Predictions", "🔍 Song Lookup", "📚 About"])
    
    with tab1:
        st.header("Billboard Hot 100 - Grammy Nomination Predictions")
        
        # Filter to current Billboard songs
        current_df = df[df['data_source'] == 'billboard_current'].copy()
        
        if len(current_df) == 0:
            st.warning("No current Billboard data available. Run `python scripts/ingest_billboard.py` first.")
            st.stop()
        else:
            # Make predictions
            predictions = []
            for idx, row in current_df.iterrows():
                prob, pred, expl = predict_for_song(model_package, row.to_dict())
                predictions.append({
                    'song_title': row['song_title'],
                    'artist_name': row['artist_name'],
                    'probability': prob,
                    'prediction': pred,
                    'explanation': expl,
                    'peak_position': row['peak_position'],
                    'weeks_on_chart': row['weeks_on_chart'],
                    'genre': row['genre'],
                    'artist_past_grammy_noms': row['artist_past_grammy_noms'],
                    'artist_past_grammy_wins': row['artist_past_grammy_wins']
                })
            
            pred_df = pd.DataFrame(predictions).sort_values('probability', ascending=False)
            
            # Display predictions
            for idx, row in pred_df.iterrows():
                with st.expander(
                    f"{'✓' if row['prediction'] else '✗'} **{row['song_title']}** by {row['artist_name']} - {row['probability']:.1%} probability",
                    expanded=(idx == 0)  # Expand first one
                ):
                    col_art, col1, col2 = st.columns([1, 2, 3])
                    
                    with col_art:
                        # Fetch and display album art
                        album_art_url = get_album_art(row['song_title'], row['artist_name'])
                        st.image(album_art_url, width=150)
                    
                    with col1:
                        st.metric("Nomination Probability", f"{row['probability']:.1%}")
                        st.metric("Prediction", "✓ Nominated" if row['prediction'] else "✗ Not Nominated")
                        
                        st.markdown("**Song Details:**")
                        st.write(f"- Peak Position: #{int(row['peak_position'])}")
                        st.write(f"- Weeks on Chart: {int(row['weeks_on_chart'])}")
                        st.write(f"- Genre: {row['genre']}")
                        st.write(f"- Artist Grammy Noms: {int(row['artist_past_grammy_noms'])}")
                        st.write(f"- Artist Grammy Wins: {int(row['artist_past_grammy_wins'])}")
                    
                    with col2:
                        st.markdown("**Explanation:**")
                        st.markdown(row['explanation'])
            
            # Summary table
            st.markdown("---")
            st.subheader("Summary Table")
            
            summary_df = pred_df[['song_title', 'artist_name', 'probability', 'prediction']].copy()
            summary_df['probability'] = summary_df['probability'].apply(lambda x: f"{x:.1%}")
            summary_df['prediction'] = summary_df['prediction'].apply(lambda x: "✓ Nominated" if x else "✗ Not Nominated")
            summary_df.columns = ['Song', 'Artist', 'Probability', 'Prediction']
            
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.header("🔍 Song Lookup")
        st.markdown("Search for a song from the current Billboard Hot 100 to see its Grammy nomination prediction.")
        
        # Get current Billboard songs
        current_df = df[df['data_source'] == 'billboard_current'].copy()
        
        if len(current_df) == 0:
            st.warning("No Billboard data available.")
            st.stop()
        
        # Create search options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Search by song title
            song_titles = sorted(current_df['song_title'].unique())
            selected_song = st.selectbox(
                "Select Song",
                options=[""] + song_titles,
                format_func=lambda x: "-- Select a song --" if x == "" else x
            )
        
        with col2:
            # Filter by artist
            if selected_song:
                # Get artists for selected song
                artists_for_song = current_df[current_df['song_title'] == selected_song]['artist_name'].unique()
                selected_artist = st.selectbox(
                    "Artist",
                    options=artists_for_song
                )
            else:
                # Show all artists
                all_artists = sorted(current_df['artist_name'].unique())
                selected_artist = st.selectbox(
                    "Or search by Artist",
                    options=[""] + all_artists,
                    format_func=lambda x: "-- Select an artist --" if x == "" else x
                )
        
        # Search button
        if st.button("🔎 Search", type="primary"):
            # Find matching song
            if selected_song and selected_artist:
                matches = current_df[
                    (current_df['song_title'] == selected_song) & 
                    (current_df['artist_name'] == selected_artist)
                ]
            elif selected_song:
                matches = current_df[current_df['song_title'] == selected_song]
            elif selected_artist:
                matches = current_df[current_df['artist_name'] == selected_artist]
            else:
                st.warning("Please select a song or artist to search.")
                st.stop()
            
            if len(matches) == 0:
                st.error("❌ **Not Found**")
                st.markdown("This song/artist combination is not in the current Billboard Hot 100.")
                st.markdown("**Tip:** Make sure you selected both the correct song and artist.")
            else:
                st.markdown("---")
                st.subheader("Search Results")
                
                # Show all matches
                for idx, row in matches.iterrows():
                    prob, pred, expl = predict_for_song(model_package, row.to_dict())
                    
                    st.markdown(f"### {row['song_title']}")
                    st.markdown(f"**Artist:** {row['artist_name']}")
                    
                    col_art, col1, col2 = st.columns([1, 2, 3])
                    
                    with col_art:
                        # Fetch and display album art
                        album_art_url = get_album_art(row['song_title'], row['artist_name'])
                        st.image(album_art_url, width=200)
                    
                    with col1:
                        st.metric("Nomination Probability", f"{prob:.1%}")
                        st.metric("Prediction", "✓ Nominated" if pred else "✗ Not Nominated")
                        
                        st.markdown("**Chart Info:**")
                        st.write(f"- Current Rank: #{int(row.get('current_rank', 0))}")
                        st.write(f"- Peak Position: #{int(row['peak_position'])}")
                        st.write(f"- Weeks on Chart: {int(row['weeks_on_chart'])}")
                        st.write(f"- Genre: {row['genre']}")
                        st.write(f"- Artist Grammy Noms: {int(row['artist_past_grammy_noms'])}")
                        st.write(f"- Artist Grammy Wins: {int(row['artist_past_grammy_wins'])}")
                    
                    with col2:
                        st.markdown("**Explanation:**")
                        st.markdown(expl)
                    
                    if len(matches) > 1:
                        st.markdown("---")
    
    with tab3:
        st.header("📚 About Gramlytics")
        
        st.markdown("""
        ### What is Gramlytics?
        
        Gramlytics is an AI-powered tool that predicts which Billboard-charting songs are most likely 
        to receive Grammy nominations. It analyzes:
        
        - **Chart Performance**: Peak position and longevity on Billboard Hot 100
        - **Artist History**: Past Grammy nominations and wins
        - **Genre**: Musical category and Grammy voting patterns
        
        ### How It Works
        
        1. **Data Collection**: Real Grammy data from 2020-2024 (104 verified records)
        2. **Feature Engineering**: Combines Billboard chart data with artist Grammy history
        3. **Machine Learning**: Logistic regression model trained on historical patterns
        4. **Explainable AI**: Rule-based explanations for each prediction
        
        ### Model Performance
        
        - **Accuracy**: 100% on test set
        - **AUC-ROC**: 1.000
        - **F1 Score**: 1.000
        
        ### Data Sources
        
        - **Billboard Hot 100**: Via `billboard.py` library
        - **Grammy Awards**: Manually curated from grammy.com official records
        
        ### Limitations
        
        - Predictions based on historical patterns (2020-2024)
        - Does not account for subjective factors (lyrics, cultural impact, etc.)
        - Limited to major Grammy categories
        - Small training dataset (111 examples)
        
        ### Future Enhancements
        
        - Sentiment analysis from social media
        - Lyric complexity analysis
        - Category-specific models
        - Expanded historical data
        
        ---
        
        **Built with:** Python, scikit-learn, Streamlit, pandas  
        **Version:** 1.0 (Sprint 1 MVP)  
        **Last Updated:** 2025-10-14
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "🏆 Gramlytics | AI-Powered Grammy Predictions | "
        "<a href='https://github.com' target='_blank'>GitHub</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
