"""
Predictive modeling module for magic squares analysis.

This module provides functionality to build and evaluate machine learning models
for predicting geometric properties of magic squares based on their structural features.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any

def prepare_features(geometric_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare feature matrix X and target variables y from geometric properties dataframe.
    
    Parameters:
    -----------
    geometric_df : pd.DataFrame
        DataFrame containing geometric properties of magic squares
        
    Returns:
    --------
    Tuple[pd.DataFrame, pd.DataFrame]
        X: Feature matrix
        y: Target variables
    """
    # Features to use as predictors
    feature_cols = [
        'vertex_count', 'face_point_count', 'interior_point_count',
        'hull_volume', 'surface_area', 'angular_uniformity'
    ]
    
    # Target variables to predict
    target_cols = [
        'eigenvalue_ratio_1', 'eigenvalue_ratio_2',
        'manifold_dimension', 'emd_mean'
    ]
    
    X = geometric_df[feature_cols].copy()
    y = geometric_df[target_cols].copy()
    
    return X, y

def build_predictive_models(geometric_df: pd.DataFrame, 
                          target_properties: List[str] = None) -> Dict[str, Any]:
    """
    Build and evaluate predictive models for geometric properties.
    
    Parameters:
    -----------
    geometric_df : pd.DataFrame
        DataFrame containing geometric properties of magic squares
    target_properties : List[str], optional
        List of target properties to predict. If None, uses all available targets.
        
    Returns:
    --------
    Dict[str, Any]
        Dictionary containing trained models and their performance metrics
    """
    X, y = prepare_features(geometric_df)
    
    if target_properties is not None:
        y = y[target_properties]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'gradient_boosting': GradientBoostingRegressor(random_state=42),
        'lasso': LassoCV(cv=5, random_state=42)
    }
    
    results = {
        'models': {},
        'feature_importance': {},
        'predictions': {},
        'metrics': {}
    }
    
    for target in y.columns:
        target_results = {}
        
        for model_name, model in models.items():
            # Train model
            model.fit(X_train_scaled, y_train[target])
            
            # Make predictions
            y_pred = model.predict(X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(y_test[target], y_pred)
            r2 = r2_score(y_test[target], y_pred)
            cv_scores = cross_val_score(model, X_train_scaled, y_train[target], cv=5)
            
            target_results[model_name] = {
                'model': model,
                'mse': mse,
                'r2': r2,
                'cv_scores': cv_scores,
                'predictions': y_pred
            }
            
            # Store feature importance for tree-based models
            if model_name in ['random_forest', 'gradient_boosting']:
                target_results[model_name]['feature_importance'] = pd.Series(
                    model.feature_importances_,
                    index=X.columns
                )
        
        results['models'][target] = target_results
    
    return results

def evaluate_model_performance(results: Dict[str, Any], 
                             save_dir: str = None) -> Dict[str, float]:
    """
    Evaluate and visualize model performance.
    
    Parameters:
    -----------
    results : Dict[str, Any]
        Dictionary containing model results from build_predictive_models
    save_dir : str, optional
        Directory to save visualization plots
        
    Returns:
    --------
    Dict[str, float]
        Dictionary containing aggregated performance metrics
    """
    performance_summary = {}
    
    for target in results['models'].keys():
        plt.figure(figsize=(12, 6))
        
        # Plot feature importance for random forest
        if 'random_forest' in results['models'][target]:
            feature_importance = results['models'][target]['random_forest']['feature_importance']
            feature_importance.sort_values().plot(kind='barh')
            plt.title(f'Feature Importance for {target}')
            plt.xlabel('Importance')
            
            if save_dir:
                plt.savefig(f'{save_dir}/feature_importance_{target}.png')
            plt.close()
        
        # Aggregate metrics
        target_metrics = {
            'mean_r2': np.mean([
                results['models'][target][model]['r2']
                for model in results['models'][target].keys()
            ]),
            'mean_cv_score': np.mean([
                results['models'][target][model]['cv_scores'].mean()
                for model in results['models'][target].keys()
            ])
        }
        
        performance_summary[target] = target_metrics
    
    return performance_summary

def plot_prediction_comparison(results: Dict[str, Any], 
                             geometric_df: pd.DataFrame,
                             save_dir: str = None) -> None:
    """
    Plot actual vs predicted values for each target variable.
    
    Parameters:
    -----------
    results : Dict[str, Any]
        Dictionary containing model results
    geometric_df : pd.DataFrame
        Original geometric properties dataframe
    save_dir : str, optional
        Directory to save plots
    """
    for target in results['models'].keys():
        plt.figure(figsize=(10, 10))
        
        # Get predictions from random forest (could use any model)
        model_results = results['models'][target]['random_forest']
        predictions = model_results['predictions']
        actual = geometric_df[target].iloc[model_results['test_indices']]
        
        plt.scatter(actual, predictions, alpha=0.5)
        plt.plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'r--')
        
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title(f'Actual vs Predicted: {target}')
        
        if save_dir:
            plt.savefig(f'{save_dir}/prediction_comparison_{target}.png')
        plt.close() 