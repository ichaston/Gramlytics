#!/usr/bin/env python3
"""
S1-01: Billboard Top 10 Ingestion Script
Pulls current Billboard Hot 100 Top 10 and normalizes to datamodel.md schema.

Usage:
    python scripts/ingest_billboard.py
    
Output:
    data/raw/billboard_top10_<date>.csv
"""

import billboard
import pandas as pd
from datetime import datetime
import os


def fetch_billboard_hot100():
    """
    Fetch current Billboard Hot 100 (all 100 songs).
    
    Returns:
        list: List of ChartEntry objects
    """
    print("Fetching Billboard Hot 100 chart...")
    chart = billboard.ChartData('hot-100')
    
    # Get all 100 entries
    hot100 = chart[:]
    
    print(f"✓ Fetched {len(hot100)} songs from Billboard Hot 100")
    print(f"  Chart date: {chart.date}")
    
    return hot100, chart.date


def normalize_to_schema(chart_entries):
    """
    Normalize Billboard data to datamodel.md schema.
    
    Args:
        chart_entries: List of billboard.ChartEntry objects
        
    Returns:
        pd.DataFrame: Normalized data with schema fields
    """
    records = []
    
    for entry in chart_entries:
        record = {
            'song_title': entry.title,
            'artist_name': entry.artist,
            'peak_position': entry.peakPos if entry.peakPos else entry.rank,
            'weeks_on_chart': entry.weeks if entry.weeks else 1,
            'genre': None,  # To be filled in S1-03 or manually
            'artist_past_grammy_noms': None,  # To be filled from Grammy data
            'artist_past_grammy_wins': None,  # To be filled from Grammy data
            'label_type': None,  # Optional for MVP
            'release_month': None,  # To be enriched later
            # Additional metadata for reference
            'current_rank': entry.rank,
            'last_week_rank': entry.lastPos if entry.lastPos else None,
            'chart_date': None,  # Will be set below
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    print(f"✓ Normalized {len(df)} records to schema")
    
    return df


def save_to_csv(df, chart_date):
    """
    Save DataFrame to data/raw/ with timestamped filename.
    
    Args:
        df: DataFrame to save
        chart_date: Chart date string (YYYY-MM-DD)
    """
    # Ensure data/raw exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Add chart date to all records
    df['chart_date'] = chart_date
    
    # Generate filename
    filename = f"data/raw/billboard_hot100_{chart_date}.csv"
    
    # Save
    df.to_csv(filename, index=False)
    
    print(f"✓ Saved to {filename}")
    print(f"\nPreview (Top 10):")
    print(df[['song_title', 'artist_name', 'current_rank', 'peak_position', 'weeks_on_chart']].head(10))
    
    return filename


def main():
    """Main execution function."""
    print("=" * 60)
    print("Billboard Hot 100 Ingestion")
    print("=" * 60)
    print()
    
    # Step 1: Fetch data
    hot100, chart_date = fetch_billboard_hot100()
    
    # Step 2: Normalize to schema
    df = normalize_to_schema(hot100)
    
    # Step 3: Save to CSV
    filename = save_to_csv(df, chart_date)
    
    print()
    print("=" * 60)
    print(f"✓ Complete: {len(df)} songs ingested")
    print(f"  Output: {filename}")
    print("=" * 60)
    
    return df


if __name__ == "__main__":
    main()
