#!/usr/bin/env python3
"""
S1-04: Train Baseline Model
Trains logistic regression model to predict Grammy nominations.

Usage:
    python scripts/train_baseline.py
    
Output:
    model/baseline_lr.pkl
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, confusion_matrix
)
import warnings
warnings.filterwarnings('ignore')


def load_training_data():
    """Load processed training data."""
    filepath = 'data/processed/training.csv'
    
    if not os.path.exists(filepath):
        raise FileNotFoundError("Training data not found. Run scripts/prepare_training_data.py first.")
    
    print(f"Loading training data: {filepath}")
    df = pd.read_csv(filepath)
    print(f"  ✓ Loaded {len(df)} records")
    
    return df


def prepare_features(df):
    """
    Prepare features for model training.
    
    Args:
        df: Training DataFrame
        
    Returns:
        tuple: (X, y, feature_names, encoders)
    """
    print("\nPreparing features...")
    
    # Filter to labeled data only (for training)
    labeled_df = df[df['is_nominated'].notna()].copy()
    print(f"  Using {len(labeled_df)} labeled examples for training")
    
    # Feature columns
    feature_cols = [
        'peak_position',
        'weeks_on_chart',
        'artist_past_grammy_noms',
        'artist_past_grammy_wins',
        'genre'
    ]
    
    # Encode categorical features
    encoders = {}
    
    # Encode genre
    le_genre = LabelEncoder()
    labeled_df['genre_encoded'] = le_genre.fit_transform(labeled_df['genre'])
    encoders['genre'] = le_genre
    
    print(f"  Genre categories: {list(le_genre.classes_)}")
    
    # Select features
    X_cols = ['peak_position', 'weeks_on_chart', 'artist_past_grammy_noms', 
              'artist_past_grammy_wins', 'genre_encoded']
    
    X = labeled_df[X_cols].values
    y = labeled_df['is_nominated'].astype(int).values
    
    print(f"  Feature matrix shape: {X.shape}")
    print(f"  Target distribution: {np.bincount(y)} (0=not nominated, 1=nominated)")
    
    return X, y, X_cols, encoders, labeled_df


def train_model(X, y):
    """
    Train logistic regression model with train/test split.
    
    Args:
        X: Feature matrix
        y: Target labels
        
    Returns:
        tuple: (model, X_train, X_test, y_train, y_test)
    """
    print("\nTraining baseline logistic regression...")
    
    # Split data (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"  Train set: {len(X_train)} samples")
    print(f"  Test set: {len(X_test)} samples")
    
    # Train logistic regression
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        class_weight='balanced'  # Handle class imbalance
    )
    
    model.fit(X_train, y_train)
    
    print(f"  ✓ Model trained successfully")
    
    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_train, X_test, y_train, y_test, feature_names):
    """
    Evaluate model performance and print metrics.
    
    Args:
        model: Trained model
        X_train, X_test: Feature matrices
        y_train, y_test: Target labels
        feature_names: List of feature names
    """
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    y_train_proba = model.predict_proba(X_train)[:, 1]
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Training metrics
    print("\n📊 Training Set Performance:")
    print(f"  Accuracy:  {accuracy_score(y_train, y_train_pred):.3f}")
    print(f"  Precision: {precision_score(y_train, y_train_pred, zero_division=0):.3f}")
    print(f"  Recall:    {recall_score(y_train, y_train_pred, zero_division=0):.3f}")
    print(f"  F1 Score:  {f1_score(y_train, y_train_pred, zero_division=0):.3f}")
    print(f"  ROC AUC:   {roc_auc_score(y_train, y_train_proba):.3f}")
    
    # Test metrics
    print("\n📊 Test Set Performance:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_test_pred):.3f}")
    print(f"  Precision: {precision_score(y_test, y_test_pred, zero_division=0):.3f}")
    print(f"  Recall:    {recall_score(y_test, y_test_pred, zero_division=0):.3f}")
    print(f"  F1 Score:  {f1_score(y_test, y_test_pred, zero_division=0):.3f}")
    print(f"  ROC AUC:   {roc_auc_score(y_test, y_test_proba):.3f}")
    
    # Confusion matrix
    print("\n📈 Confusion Matrix (Test Set):")
    cm = confusion_matrix(y_test, y_test_pred)
    print(f"  True Negatives:  {cm[0, 0] if cm.shape[0] > 1 else 0}")
    print(f"  False Positives: {cm[0, 1] if cm.shape[0] > 1 and cm.shape[1] > 1 else 0}")
    print(f"  False Negatives: {cm[1, 0] if cm.shape[0] > 1 else 0}")
    print(f"  True Positives:  {cm[1, 1] if cm.shape[0] > 1 and cm.shape[1] > 1 else 0}")
    
    # Feature importance
    print("\n🔍 Feature Importance (Coefficients):")
    coefficients = model.coef_[0]
    for i, (feat, coef) in enumerate(zip(feature_names, coefficients)):
        print(f"  {feat:30s}: {coef:+.4f}")
    
    print("\n" + "=" * 60)


def save_model(model, encoders, feature_names):
    """
    Save trained model and metadata.
    
    Args:
        model: Trained model
        encoders: Dictionary of label encoders
        feature_names: List of feature names
    """
    os.makedirs('model', exist_ok=True)
    
    # Package model with metadata
    model_package = {
        'model': model,
        'encoders': encoders,
        'feature_names': feature_names,
        'version': '1.0',
        'trained_date': pd.Timestamp.now().isoformat()
    }
    
    filepath = 'model/baseline_lr.pkl'
    
    with open(filepath, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"\n✓ Model saved to {filepath}")
    
    return filepath


def predict_current_billboard(model, encoders, feature_names):
    """
    Make predictions on current Billboard Top 10.
    
    Args:
        model: Trained model
        encoders: Dictionary of label encoders
        feature_names: List of feature names
        
    Returns:
        pd.DataFrame: Predictions
    """
    print("\n" + "=" * 60)
    print("PREDICTIONS FOR CURRENT BILLBOARD TOP 10")
    print("=" * 60)
    
    # Load full dataset
    df = pd.read_csv('data/processed/training.csv')
    
    # Filter to unlabeled (current Billboard)
    current_df = df[df['is_nominated'].isna()].copy()
    
    if len(current_df) == 0:
        print("  No unlabeled data to predict")
        return None
    
    print(f"\n  Predicting for {len(current_df)} songs...")
    
    # Prepare features
    current_df['genre_encoded'] = encoders['genre'].transform(current_df['genre'])
    
    X_cols = ['peak_position', 'weeks_on_chart', 'artist_past_grammy_noms',
              'artist_past_grammy_wins', 'genre_encoded']
    
    X_current = current_df[X_cols].values
    
    # Predict
    predictions = model.predict(X_current)
    probabilities = model.predict_proba(X_current)[:, 1]
    
    # Add to dataframe
    current_df['nomination_probability'] = probabilities
    current_df['predicted_nominated'] = predictions
    
    # Sort by probability
    current_df = current_df.sort_values('nomination_probability', ascending=False)
    
    # Display
    print("\n  Results:")
    print(f"  {'Rank':<6} {'Song':<30} {'Artist':<25} {'Probability':<12} {'Prediction'}")
    print("  " + "-" * 85)
    
    for idx, row in current_df.iterrows():
        pred_str = "✓ Nominated" if row['predicted_nominated'] else "✗ Not nominated"
        print(f"  {int(row.get('current_rank', 0)):<6} {row['song_title'][:28]:<30} "
              f"{row['artist_name'][:23]:<25} {row['nomination_probability']:.1%}{'':>8} {pred_str}")
    
    return current_df


def main():
    """Main execution."""
    print("=" * 60)
    print("Train Baseline Model (S1-04)")
    print("=" * 60)
    print()
    
    # Load data
    df = load_training_data()
    
    # Prepare features
    X, y, feature_names, encoders, labeled_df = prepare_features(df)
    
    # Train model
    model, X_train, X_test, y_train, y_test = train_model(X, y)
    
    # Evaluate
    evaluate_model(model, X_train, X_test, y_train, y_test, feature_names)
    
    # Save
    model_path = save_model(model, encoders, feature_names)
    
    # Predict current Billboard
    predictions_df = predict_current_billboard(model, encoders, feature_names)
    
    print()
    print("=" * 60)
    print("✓ S1-04 Complete: Baseline model trained and saved")
    print(f"  Model: {model_path}")
    print("=" * 60)
    
    return model, predictions_df


if __name__ == "__main__":
    main()
