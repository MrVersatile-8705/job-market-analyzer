from scipy.stats import pearsonr
import pandas as pd

def analyze_correlations(dataframe, target_column):
    """
    Analyzes correlations between different job requirements and the target column (e.g., salary).
    
    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing job data.
        target_column (str): The column name for the target variable (e.g., salary).
        
    Returns:
        pd.DataFrame: A DataFrame containing correlation coefficients and p-values.
    """
    correlations = {}
    
    for column in dataframe.columns:
        if column != target_column:
            corr, p_value = pearsonr(dataframe[column], dataframe[target_column])
            correlations[column] = {'correlation': corr, 'p_value': p_value}
    
    return pd.DataFrame(correlations).T

def significant_correlations(correlation_df, threshold=0.5):
    """
    Filters the correlation DataFrame to return only significant correlations above a given threshold.
    
    Parameters:
        correlation_df (pd.DataFrame): The DataFrame containing correlation coefficients and p-values.
        threshold (float): The threshold for filtering significant correlations.
        
    Returns:
        pd.DataFrame: A DataFrame containing only significant correlations.
    """
    return correlation_df[correlation_df['correlation'].abs() > threshold]