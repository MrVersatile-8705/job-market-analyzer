#!/usr/bin/env python3
"""
Simple Analytics Dashboard for Job Market Data
Creates visualizations from existing focused test results
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from collections import Counter
import numpy as np

def create_simple_dashboard(data_file):
    """Create a simple analytics dashboard from job data."""
    
    print(f"📊 Creating analytics dashboard from: {data_file}")
    
    # Load data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract jobs data based on structure
    if 'results' in data:
        jobs = data['results']
        metadata = data.get('test_metadata', {})
    elif 'jobs' in data:
        jobs = data['jobs']
        metadata = data.get('metadata', {})
    elif 'analyses' in data:
        # Handle AI enhanced analysis format
        analyses = data['analyses']
        jobs = []
        for analysis in analyses:
            job = analysis.get('scraped_data', {})
            job['ai_analysis'] = analysis.get('ai_analysis', {})
            job['test_case'] = analysis.get('test_case', '')
            jobs.append(job)
        metadata = data.get('analysis_metadata', {})
    else:
        print("❌ No recognized data structure found")
        return
    
    print(f"✅ Loaded {len(jobs)} jobs for analysis")
    
    # Create output directory
    output_dir = Path("data/analytics/simple_charts")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Overview Statistics
    create_overview_stats(jobs, metadata, output_dir)
    
    # 2. Skills Analysis
    create_skills_analysis(jobs, output_dir)
    
    # 3. Company and Location Analysis
    create_company_location_analysis(jobs, output_dir)
    
    # 4. AI Analysis Quality
    create_ai_analysis_charts(jobs, output_dir)
    
    # 5. Generate Summary Report
    generate_summary_report(jobs, metadata, output_dir)
    
    print(f"🎉 Dashboard completed! Charts saved to: {output_dir}")

def create_overview_stats(jobs, metadata, output_dir):
    """Create overview statistics charts."""
    print("📊 Creating overview statistics...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Job Market Analysis Overview', fontsize=16, fontweight='bold')
    
    # 1. Jobs by Company
    companies = [job.get('company', 'Unknown') for job in jobs]
    company_counts = Counter(companies)
    
    if len(company_counts) > 1:
        axes[0, 0].pie(company_counts.values(), labels=company_counts.keys(), autopct='%1.1f%%')
        axes[0, 0].set_title('Jobs by Company')
    else:
        axes[0, 0].text(0.5, 0.5, f"All jobs from: {list(company_counts.keys())[0]}", 
                       ha='center', va='center', transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('Company Distribution')
    
    # 2. Remote vs On-site
    remote_counts = Counter([job.get('remote_option', False) for job in jobs])
    remote_labels = ['On-site', 'Remote']
    remote_values = [remote_counts.get(False, 0), remote_counts.get(True, 0)]
    
    axes[0, 1].bar(remote_labels, remote_values, color=['lightcoral', 'lightblue'])
    axes[0, 1].set_title('Remote vs On-site Positions')
    axes[0, 1].set_ylabel('Number of Jobs')
    
    # 3. AI Analysis Success Rate
    ai_success = sum(1 for job in jobs if job.get('ai_analysis') and 'error' not in job.get('ai_analysis', {}))
    ai_total = len(jobs)
    
    success_rate = (ai_success / ai_total) * 100 if ai_total > 0 else 0
    
    axes[1, 0].pie([ai_success, ai_total - ai_success], 
                   labels=[f'AI Analyzed ({ai_success})', f'No AI Analysis ({ai_total - ai_success})'], 
                   autopct='%1.1f%%',
                   colors=['lightgreen', 'lightgray'])
    axes[1, 0].set_title(f'AI Analysis Coverage: {success_rate:.1f}%')
    
    # 4. Data Quality Score
    quality_factors = {
        'Has Title': sum(1 for job in jobs if job.get('title')),
        'Has Company': sum(1 for job in jobs if job.get('company')),
        'Has Location': sum(1 for job in jobs if job.get('location')),
        'Has AI Analysis': ai_success
    }
    
    quality_percentages = [(count / len(jobs)) * 100 for count in quality_factors.values()]
    
    bars = axes[1, 1].bar(quality_factors.keys(), quality_percentages, color=['skyblue', 'orange', 'green', 'purple'])
    axes[1, 1].set_title('Data Quality Metrics')
    axes[1, 1].set_ylabel('Percentage (%)')
    axes[1, 1].set_ylim(0, 105)
    
    # Add percentage labels on bars
    for bar, pct in zip(bars, quality_percentages):
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                       f'{pct:.1f}%', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / 'overview_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_skills_analysis(jobs, output_dir):
    """Create skills market analysis."""
    print("🛠️ Creating skills analysis...")
    
    # Extract all skills
    all_skills = []
    for job in jobs:
        ai_analysis = job.get('ai_analysis', {})
        if 'skills_identified' in ai_analysis:
            all_skills.extend(ai_analysis['skills_identified'])
        elif 'openai_insights' in ai_analysis:
            skills = ai_analysis['openai_insights'].get('skills_required', [])
            all_skills.extend(skills)
    
    if not all_skills:
        print("⚠️ No skills data found")
        return
    
    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(15))
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    fig.suptitle('Skills Market Analysis', fontsize=16, fontweight='bold')
    
    # Top skills bar chart
    skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Count'])
    sns.barplot(data=skills_df, x='Count', y='Skill', ax=axes[0])
    axes[0].set_title(f'Top {len(top_skills)} Most Demanded Skills')
    axes[0].set_xlabel('Number of Job Mentions')
    
    # Skills frequency distribution
    skill_freq = list(skill_counts.values())
    axes[1].hist(skill_freq, bins=min(10, len(set(skill_freq))), alpha=0.7, edgecolor='black')
    axes[1].set_title('Skills Mention Frequency Distribution')
    axes[1].set_xlabel('Number of Mentions')
    axes[1].set_ylabel('Number of Skills')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'skills_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create skills report
    skills_report = {
        'total_skills_mentions': len(all_skills),
        'unique_skills': len(skill_counts),
        'top_skills': dict(skill_counts.most_common(10)),
        'skills_per_job_avg': round(len(all_skills) / len(jobs), 2)
    }
    
    with open(output_dir / 'skills_report.json', 'w') as f:
        json.dump(skills_report, f, indent=2)

def create_company_location_analysis(jobs, output_dir):
    """Create company and location analysis."""
    print("🏢 Creating company and location analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Company and Location Analysis', fontsize=16, fontweight='bold')
    
    # Company analysis
    companies = [job.get('company', 'Unknown') for job in jobs if job.get('company')]
    company_counts = Counter(companies)
    
    if company_counts:
        axes[0].barh(range(len(company_counts)), list(company_counts.values()))
        axes[0].set_yticks(range(len(company_counts)))
        axes[0].set_yticklabels(list(company_counts.keys()))
        axes[0].set_title('Jobs by Company')
        axes[0].set_xlabel('Number of Positions')
    
    # Location analysis
    locations = [job.get('location', 'Not Specified') for job in jobs]
    location_counts = Counter(locations)
    
    if len(location_counts) > 1:
        axes[1].pie(location_counts.values(), labels=location_counts.keys(), autopct='%1.1f%%')
        axes[1].set_title('Geographic Distribution')
    else:
        axes[1].text(0.5, 0.5, f"Location: {list(location_counts.keys())[0]}", 
                    ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('Location Distribution')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'company_location_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_ai_analysis_charts(jobs, output_dir):
    """Create AI analysis quality charts."""
    print("🤖 Creating AI analysis charts...")
    
    # Extract AI analysis data
    ai_jobs = [job for job in jobs if job.get('ai_analysis') and 'error' not in job.get('ai_analysis', {})]
    
    if not ai_jobs:
        print("⚠️ No AI analysis data found")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('AI Analysis Quality Metrics', fontsize=16, fontweight='bold')
    
    # Confidence scores
    confidence_scores = []
    for job in ai_jobs:
        conf = job['ai_analysis'].get('confidence_score', 0)
        if conf:
            confidence_scores.append(conf)
    
    if confidence_scores:
        axes[0, 0].hist(confidence_scores, bins=10, alpha=0.7, edgecolor='black')
        axes[0, 0].set_title('AI Confidence Score Distribution')
        axes[0, 0].set_xlabel('Confidence Score')
        axes[0, 0].set_ylabel('Number of Jobs')
    
    # Analysis quality
    quality_ratings = []
    for job in ai_jobs:
        quality = job['ai_analysis'].get('analysis_quality', '')
        if quality:
            quality_ratings.append(quality)
    
    if quality_ratings:
        quality_counts = Counter(quality_ratings)
        axes[0, 1].pie(quality_counts.values(), labels=quality_counts.keys(), autopct='%1.1f%%')
        axes[0, 1].set_title('AI Analysis Quality Ratings')
    
    # Skills identification success
    skills_success = sum(1 for job in ai_jobs if job['ai_analysis'].get('skills_identified', []))
    total_ai = len(ai_jobs)
    
    success_data = [skills_success, total_ai - skills_success]
    axes[1, 0].pie(success_data, labels=[f'Skills Found ({skills_success})', f'No Skills ({total_ai - skills_success})'], 
                   autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    axes[1, 0].set_title('Skills Identification Success Rate')
    
    # AI processing time (if available)
    axes[1, 1].text(0.5, 0.5, f'AI Analysis Success Rate:\n{(len(ai_jobs)/len(jobs)*100):.1f}%\n\n' +
                              f'Jobs Processed: {len(jobs)}\n' +
                              f'AI Analyzed: {len(ai_jobs)}', 
                   ha='center', va='center', transform=axes[1, 1].transAxes,
                   fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    axes[1, 1].set_title('AI Analysis Summary')
    axes[1, 1].set_xticks([])
    axes[1, 1].set_yticks([])
    
    plt.tight_layout()
    plt.savefig(output_dir / 'ai_analysis_quality.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_summary_report(jobs, metadata, output_dir):
    """Generate comprehensive summary report."""
    print("📋 Generating summary report...")
    
    # Extract comprehensive statistics
    total_jobs = len(jobs)
    ai_analyzed = sum(1 for job in jobs if job.get('ai_analysis') and 'error' not in job.get('ai_analysis', {}))
    
    # Skills analysis
    all_skills = []
    for job in jobs:
        ai_analysis = job.get('ai_analysis', {})
        if 'skills_identified' in ai_analysis:
            all_skills.extend(ai_analysis['skills_identified'])
        elif 'openai_insights' in ai_analysis:
            skills = ai_analysis['openai_insights'].get('skills_required', [])
            all_skills.extend(skills)
    
    unique_skills = len(set(all_skills))
    companies = list(set([job.get('company') for job in jobs if job.get('company')]))
    remote_jobs = sum(1 for job in jobs if job.get('remote_option'))
    
    # Create summary
    summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "source_data": "job_market_analysis_data",
        "dataset_overview": {
            "total_jobs_analyzed": total_jobs,
            "ai_analysis_coverage_percent": round((ai_analyzed / total_jobs) * 100, 1) if total_jobs > 0 else 0,
            "unique_companies": len(companies),
            "unique_skills_identified": unique_skills,
            "remote_work_percentage": round((remote_jobs / total_jobs) * 100, 1) if total_jobs > 0 else 0
        },
        "market_insights": {
            "most_demanded_skills": dict(Counter(all_skills).most_common(10)),
            "hiring_companies": companies,
            "remote_work_availability": f"{remote_jobs} out of {total_jobs} positions offer remote work"
        },
        "data_quality": {
            "ai_analysis_success_rate": round((ai_analyzed / total_jobs) * 100, 1),
            "average_skills_per_job": round(len(all_skills) / total_jobs, 2) if total_jobs > 0 else 0,
            "data_completeness_score": calculate_completeness_score(jobs)
        },
        "recommendations": generate_recommendations(jobs, all_skills)
    }
    
    # Save summary report
    summary_file = output_dir / 'analysis_summary_report.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Summary report saved: {summary_file}")
    
    # Display key insights
    print("\n🎯 KEY MARKET INSIGHTS")
    print("=" * 40)
    print(f"📊 Total Jobs Analyzed: {total_jobs}")
    print(f"🤖 AI Analysis Coverage: {summary['dataset_overview']['ai_analysis_coverage_percent']}%")
    print(f"🏠 Remote Work Opportunities: {summary['dataset_overview']['remote_work_percentage']}%")
    print(f"🏢 Companies Represented: {len(companies)}")
    print(f"🛠️ Unique Skills Identified: {unique_skills}")
    
    if all_skills:
        top_skills = Counter(all_skills).most_common(5)
        print(f"\n🔥 Top 5 Most Demanded Skills:")
        for i, (skill, count) in enumerate(top_skills, 1):
            print(f"  {i}. {skill}: {count} mentions")
    
    return summary

def calculate_completeness_score(jobs):
    """Calculate data completeness score."""
    if not jobs:
        return 0
    
    total_jobs = len(jobs)
    scores = []
    
    for job in jobs:
        job_score = 0
        # Basic data fields (40% weight)
        if job.get('title'): job_score += 10
        if job.get('company'): job_score += 10
        if job.get('location'): job_score += 10
        if job.get('description'): job_score += 10
        
        # AI analysis (40% weight)
        if job.get('ai_analysis') and 'error' not in job.get('ai_analysis', {}):
            job_score += 40
        
        # Additional fields (20% weight)
        if job.get('salary'): job_score += 5
        if job.get('remote_option') is not None: job_score += 5
        if job.get('url'): job_score += 5
        if job.get('scraped_at'): job_score += 5
        
        scores.append(job_score)
    
    return round(sum(scores) / len(scores), 1)

def generate_recommendations(jobs, all_skills):
    """Generate actionable recommendations."""
    recommendations = []
    
    # Skills recommendations
    if all_skills:
        top_skills = Counter(all_skills).most_common(3)
        recommendations.append(f"Focus on developing these high-demand skills: {', '.join([skill for skill, _ in top_skills])}")
    
    # Remote work insights
    remote_jobs = sum(1 for job in jobs if job.get('remote_option'))
    if remote_jobs > 0:
        recommendations.append(f"Remote work is available in {(remote_jobs/len(jobs)*100):.0f}% of positions analyzed")
    
    # Company diversity
    companies = [job.get('company') for job in jobs if job.get('company')]
    if len(set(companies)) > 1:
        recommendations.append("Diverse hiring landscape with opportunities across multiple companies")
    
    return recommendations

def main():
    """Main function to run simple dashboard."""
    import sys
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        # Find most recent results file
        results_dir = Path("data/results")
        if not results_dir.exists():
            print("❌ No results directory found. Run analysis first.")
            return
        
        json_files = list(results_dir.glob("*.json"))
        if not json_files:
            print("❌ No results files found. Run analysis first.")
            return
        
        # Use most recent file
        data_file = max(json_files, key=lambda f: f.stat().st_mtime)
        print(f"📁 Using most recent results file: {data_file}")
    
    create_simple_dashboard(data_file)

if __name__ == "__main__":
    main()
