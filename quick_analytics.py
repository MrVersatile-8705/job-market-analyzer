#!/usr/bin/env python3
"""
Quick Analytics Script
Analyze job market data from the results files
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from collections import Counter
import numpy as np

def load_job_data(file_path):
    """Load job data from JSON results file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract jobs from results array
        jobs = data.get('results', [])
        metadata = data.get('test_metadata', {})
        
        print(f"📊 Loaded {len(jobs)} jobs from {file_path}")
        print(f"📅 Test timestamp: {metadata.get('timestamp', 'Unknown')}")
        print(f"🔍 Scrapers tested: {', '.join(metadata.get('scrapers_tested', []))}")
        
        return jobs, metadata
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return [], {}

def analyze_job_data(jobs):
    """Perform comprehensive analysis on job data."""
    if not jobs:
        print("❌ No job data to analyze")
        return
    
    print(f"\n🔬 COMPREHENSIVE JOB MARKET ANALYSIS")
    print("=" * 60)
    
    # Convert to DataFrame
    df = pd.DataFrame(jobs)
    
    # Basic statistics
    print(f"\n📈 BASIC STATISTICS:")
    print(f"   Total jobs: {len(jobs)}")
    print(f"   Unique companies: {df['company'].nunique()}")
    print(f"   Data sources: {', '.join(df['source'].unique())}")
    
    # Scenario analysis
    if 'scenario' in df.columns:
        print(f"\n📋 SCENARIO BREAKDOWN:")
        scenario_counts = df['scenario'].value_counts()
        for scenario, count in scenario_counts.items():
            print(f"   {scenario}: {count} jobs")
    
    # Company analysis
    print(f"\n🏢 TOP COMPANIES:")
    company_counts = df['company'].value_counts().head(10)
    for company, count in company_counts.items():
        print(f"   {company}: {count} jobs")
    
    # Location analysis
    print(f"\n🌍 LOCATION ANALYSIS:")
    # Handle empty locations
    locations = df['location'].fillna('Remote/Not Specified')
    location_counts = locations.value_counts().head(10)
    for location, count in location_counts.items():
        print(f"   {location}: {count} jobs")
    
    # Salary analysis
    print(f"\n💰 SALARY INFORMATION:")
    salary_count = df['salary'].notna().sum()
    print(f"   Jobs with salary info: {salary_count}/{len(jobs)} ({salary_count/len(jobs)*100:.1f}%)")
    
    # Remote work analysis
    print(f"\n🏠 REMOTE WORK OPTIONS:")
    if 'remote_option' in df.columns:
        remote_count = df['remote_option'].sum()
        print(f"   Remote-friendly jobs: {remote_count}/{len(jobs)} ({remote_count/len(jobs)*100:.1f}%)")
    
    # Title analysis
    print(f"\n📝 JOB TITLE ANALYSIS:")
    # Extract key words from titles
    all_titles = ' '.join(df['title'].fillna('').str.lower())
    title_words = all_titles.split()
    word_counts = Counter(title_words)
    
    print(f"   Most common title words:")
    for word, count in word_counts.most_common(10):
        if len(word) > 3:  # Skip short words
            print(f"     {word}: {count} times")
    
    # Description analysis
    print(f"\n📄 JOB DESCRIPTION INSIGHTS:")
    all_descriptions = ' '.join(df['description'].fillna('').str.lower())
    
    # Key skills to look for
    key_skills = ['python', 'sql', 'excel', 'tableau', 'power bi', 'r', 'analytics', 
                  'data', 'machine learning', 'statistics', 'visualization']
    
    skill_counts = {}
    for skill in key_skills:
        count = all_descriptions.count(skill)
        if count > 0:
            skill_counts[skill] = count
    
    print(f"   Top skills mentioned:")
    for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"     {skill}: {count} mentions")
    
    # AI Analysis if available
    if any('ai_analysis' in job for job in jobs):
        print(f"\n🤖 AI ANALYSIS INSIGHTS:")
        ai_jobs = [job for job in jobs if 'ai_analysis' in job]
        print(f"   Jobs with AI analysis: {len(ai_jobs)}")
        
        # Confidence scores
        confidence_scores = [job['ai_analysis'].get('confidence_score', 0) for job in ai_jobs]
        if confidence_scores:
            avg_confidence = np.mean(confidence_scores)
            print(f"   Average AI confidence: {avg_confidence:.2f}")
        
        # Analysis quality
        quality_counts = Counter([job['ai_analysis'].get('analysis_quality', 'unknown') for job in ai_jobs])
        print(f"   Analysis quality distribution:")
        for quality, count in quality_counts.items():
            print(f"     {quality}: {count} jobs")
    
    return df

def create_simple_visualizations(df, output_dir):
    """Create simple visualizations from the data."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plt.style.use('seaborn-v0_8')
    
    # 1. Jobs by scenario
    if 'scenario' in df.columns and len(df['scenario'].unique()) > 1:
        plt.figure(figsize=(10, 6))
        scenario_counts = df['scenario'].value_counts()
        plt.bar(range(len(scenario_counts)), scenario_counts.values)
        plt.title('Jobs by Scenario')
        plt.xlabel('Scenario')
        plt.ylabel('Number of Jobs')
        plt.xticks(range(len(scenario_counts)), scenario_counts.index, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_dir / 'jobs_by_scenario.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: jobs_by_scenario.png")
    
    # 2. Top companies
    plt.figure(figsize=(12, 6))
    company_counts = df['company'].value_counts().head(10)
    plt.bar(range(len(company_counts)), company_counts.values)
    plt.title('Top 10 Companies by Job Postings')
    plt.xlabel('Company')
    plt.ylabel('Number of Jobs')
    plt.xticks(range(len(company_counts)), company_counts.index, rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / 'top_companies.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✅ Saved: top_companies.png")
    
    # 3. Remote vs Non-remote
    if 'remote_option' in df.columns:
        plt.figure(figsize=(8, 6))
        remote_counts = df['remote_option'].value_counts()
        labels = ['Remote' if x else 'On-site' for x in remote_counts.index]
        plt.pie(remote_counts.values, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Remote vs On-site Job Distribution')
        plt.savefig(output_dir / 'remote_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✅ Saved: remote_distribution.png")

def main():
    """Main analysis function."""
    print("🚀 Starting Job Market Analytics")
    print("=" * 50)
    
    # Find results files
    results_dir = Path("data/results")
    json_files = list(results_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No results files found")
        return
    
    # Use the file with the most jobs
    best_file = None
    max_jobs = 0
    
    for file_path in json_files:
        jobs, metadata = load_job_data(file_path)
        job_count = metadata.get('total_jobs', len(jobs))
        if job_count > max_jobs:
            max_jobs = job_count
            best_file = file_path
    
    if best_file and max_jobs > 0:
        print(f"\n📁 Using file with most jobs: {best_file.name}")
        jobs, metadata = load_job_data(best_file)
        
        # Perform analysis
        df = analyze_job_data(jobs)
        
        if df is not None and len(df) > 0:
            # Create visualizations
            print(f"\n📊 Creating visualizations...")
            create_simple_visualizations(df, "data/analytics/charts")
            
            print(f"\n🎉 Analysis complete!")
            print(f"📊 Charts saved to: data/analytics/charts/")
        else:
            print("❌ No data available for visualization")
    else:
        print("❌ No files with job data found")

if __name__ == "__main__":
    main()
