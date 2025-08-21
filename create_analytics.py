#!/usr/bin/env python3
"""
Analytics Dashboard Generator
Creates visual insights from our job market data
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter
import sys

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def create_analytics_dashboard():
    """Create visual analytics from test results."""
    
    print("📊 Job Market Analytics Dashboard")
    print("=" * 40)
    
    # Load the most recent test results
    results_dir = Path("data/results")
    if not results_dir.exists():
        print("❌ No results found. Run focused_test.py first!")
        return
    
    # Find the most recent results file
    result_files = list(results_dir.glob("focused_test_*.json"))
    if not result_files:
        print("❌ No focused test results found!")
        return
    
    latest_file = max(result_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 Loading data from: {latest_file.name}")
    
    # Load and analyze data
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    if not results:
        print("❌ No job data found in results!")
        return
    
    print(f"✅ Loaded {len(results)} jobs for analysis")
    
    # Create analytics
    create_skills_analysis(results)
    create_company_analysis(results)
    create_salary_analysis(results)
    create_location_analysis(results)
    
    print("\n🎉 Analytics dashboard generated!")
    print("📁 Charts saved in data/analytics/")

def create_skills_analysis(results):
    """Analyze skills distribution."""
    
    print("\n🛠️ Skills Analysis")
    print("-" * 20)
    
    all_skills = []
    for job in results:
        if 'ai_analysis' in job and 'skills_identified' in job['ai_analysis']:
            all_skills.extend(job['ai_analysis']['skills_identified'])
    
    if not all_skills:
        print("No skills data available")
        return
    
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(10)
    
    print("Top Skills in Demand:")
    for i, (skill, count) in enumerate(top_skills, 1):
        print(f"  {i:2d}. {skill}: {count} mentions")
    
    # Create visualization
    try:
        skills, counts = zip(*top_skills)
        
        plt.figure(figsize=(12, 6))
        plt.bar(skills, counts, color='skyblue', edgecolor='navy', alpha=0.7)
        plt.title('Top 10 Skills in Data Jobs', fontsize=16, fontweight='bold')
        plt.xlabel('Skills', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save chart
        Path("data/analytics").mkdir(parents=True, exist_ok=True)
        plt.savefig("data/analytics/skills_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("📊 Skills chart saved: data/analytics/skills_analysis.png")
        
    except Exception as e:
        print(f"❌ Chart generation failed: {e}")

def create_company_analysis(results):
    """Analyze company distribution."""
    
    print("\n🏢 Company Analysis")
    print("-" * 20)
    
    companies = [job['company'] for job in results if job.get('company')]
    company_counts = Counter(companies)
    
    print("Companies Hiring:")
    for company, count in company_counts.items():
        print(f"  • {company}: {count} positions")

def create_salary_analysis(results):
    """Analyze salary information."""
    
    print("\n💰 Salary Analysis")
    print("-" * 20)
    
    salaries = []
    for job in results:
        if job.get('salary'):
            salaries.append(job['salary'])
        elif 'ai_analysis' in job and 'salary_estimate' in job['ai_analysis']:
            ai_salary = job['ai_analysis']['salary_estimate']
            if ai_salary:
                salaries.append(ai_salary)
    
    if salaries:
        print("Salary Information Found:")
        for i, salary in enumerate(salaries, 1):
            print(f"  {i}. {salary}")
    else:
        print("No salary data available")

def create_location_analysis(results):
    """Analyze location distribution."""
    
    print("\n📍 Location Analysis")
    print("-" * 20)
    
    locations = [job['location'] for job in results if job.get('location')]
    location_counts = Counter(locations)
    
    remote_jobs = sum(1 for job in results if job.get('remote_option'))
    total_jobs = len(results)
    remote_percentage = (remote_jobs / total_jobs) * 100 if total_jobs > 0 else 0
    
    print(f"🏠 Remote Work: {remote_jobs}/{total_jobs} jobs ({remote_percentage:.1f}%)")
    print("\nTop Locations:")
    for location, count in location_counts.most_common(5):
        print(f"  • {location}: {count} jobs")

if __name__ == "__main__":
    try:
        create_analytics_dashboard()
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("💡 Install with: pip install pandas matplotlib seaborn")
    except Exception as e:
        print(f"❌ Error: {e}")
