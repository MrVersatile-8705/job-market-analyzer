#!/usr/bin/env python3
"""
Advanced Analytics Dashboard Generator
Creates comprehensive visualizations and insights from job market data
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

class JobMarketAnalyticsDashboard:
    """Advanced analytics dashboard for job market data."""
    
    def __init__(self, data_file):
        """Initialize dashboard with job data."""
        self.data_file = Path(data_file)
        self.output_dir = Path("data/analytics/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and prepare data
        self.raw_data = self.load_data()
        self.df = self.prepare_dataframe()
        
        print(f"📊 Dashboard initialized with {len(self.df)} jobs")
    
    def load_data(self):
        """Load job data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def prepare_dataframe(self):
        """Convert job data to pandas DataFrame for analysis."""
        if not self.raw_data:
            return pd.DataFrame()
        
        jobs = self.raw_data.get('jobs', [])
        df_data = []
        
        for job in jobs:
            # Basic job info
            row = {
                'title': job.get('title', ''),
                'company': job.get('company', ''),
                'location': job.get('location', ''),
                'scenario': job.get('scenario', ''),
                'remote_option': job.get('remote_option', False),
                'job_type': job.get('job_type', ''),
                'experience_level': job.get('experience_level', ''),
                'salary': job.get('salary', ''),
                'scraped_at': job.get('scraped_at', ''),
                'has_ai_analysis': 'ai_analysis' in job and 'error' not in job.get('ai_analysis', {})
            }
            
            # AI Analysis data
            if row['has_ai_analysis']:
                ai_data = job['ai_analysis']
                
                # OpenAI insights
                openai = ai_data.get('openai_insights', {})
                row.update({
                    'ai_industry': openai.get('industry', ''),
                    'ai_career_level': openai.get('career_level', ''),
                    'ai_remote_friendly': openai.get('remote_friendly', False),
                    'ai_experience_level': openai.get('experience_level', ''),
                    'skills_count': len(openai.get('skills_required', []))
                })
                
                # Skills (flatten for analysis)
                skills = openai.get('skills_required', [])
                claude_skills = ai_data.get('claude_requirements', {}).get('must_have_skills', [])
                all_skills = list(set(skills + claude_skills))
                
                for i, skill in enumerate(all_skills[:10]):  # Top 10 skills per job
                    row[f'skill_{i+1}'] = skill
                
                # Claude compensation
                claude_comp = ai_data.get('claude_compensation', {})
                row.update({
                    'ai_salary_range': claude_comp.get('salary_range', ''),
                    'compensation_score': claude_comp.get('compensation_score', 0),
                    'benefits_count': len(claude_comp.get('benefits_mentioned', []))
                })
            
            df_data.append(row)
        
        return pd.DataFrame(df_data)
    
    def create_comprehensive_dashboard(self):
        """Create comprehensive analytics dashboard."""
        print("🎨 Creating comprehensive dashboard...")
        
        # Set up styling
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create multiple chart types
        self.create_overview_charts()
        self.create_skills_analysis()
        self.create_geographic_analysis()
        self.create_company_insights()
        self.create_industry_trends()
        self.create_compensation_analysis()
        self.create_interactive_dashboard()
        
        print("✅ Dashboard creation complete!")
        print(f"📁 Charts saved to: {self.output_dir}")
    
    def create_overview_charts(self):
        """Create overview and summary charts."""
        print("📊 Creating overview charts...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Job Market Analysis Overview', fontsize=16, fontweight='bold')
        
        # 1. Jobs by Scenario
        scenario_counts = self.df['scenario'].value_counts()
        axes[0, 0].pie(scenario_counts.values, labels=scenario_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Jobs Distribution by Scenario')
        
        # 2. Remote vs On-site
        remote_counts = self.df['remote_option'].value_counts()
        axes[0, 1].bar(['On-site', 'Remote'], [remote_counts.get(False, 0), remote_counts.get(True, 0)])
        axes[0, 1].set_title('Remote vs On-site Positions')
        axes[0, 1].set_ylabel('Number of Jobs')
        
        # 3. AI Analysis Coverage
        ai_coverage = self.df['has_ai_analysis'].value_counts()
        axes[1, 0].pie(ai_coverage.values, labels=['With AI Analysis', 'Without AI Analysis'], autopct='%1.1f%%')
        axes[1, 0].set_title('AI Analysis Coverage')
        
        # 4. Experience Levels
        exp_levels = self.df['ai_experience_level'].value_counts().head(10)
        if not exp_levels.empty:
            axes[1, 1].barh(range(len(exp_levels)), exp_levels.values)
            axes[1, 1].set_yticks(range(len(exp_levels)))
            axes[1, 1].set_yticklabels(exp_levels.index)
            axes[1, 1].set_title('Required Experience Levels')
            axes[1, 1].set_xlabel('Number of Jobs')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'overview_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_skills_analysis(self):
        """Create detailed skills market analysis."""
        print("🛠️ Creating skills analysis...")
        
        # Extract all skills
        all_skills = []
        for _, row in self.df.iterrows():
            for i in range(1, 11):
                skill = row.get(f'skill_{i}')
                if pd.notna(skill) and skill:
                    all_skills.append(skill)
        
        if not all_skills:
            print("⚠️ No skills data found")
            return
        
        skill_counts = Counter(all_skills)
        top_skills = dict(skill_counts.most_common(20))
        
        # Create skills charts
        fig, axes = plt.subplots(2, 1, figsize=(14, 12))
        fig.suptitle('Skills Market Analysis', fontsize=16, fontweight='bold')
        
        # Top skills bar chart
        skills_df = pd.DataFrame(list(top_skills.items()), columns=['Skill', 'Count'])
        sns.barplot(data=skills_df, x='Count', y='Skill', ax=axes[0])
        axes[0].set_title('Top 20 Most Demanded Skills')
        axes[0].set_xlabel('Number of Job Postings')
        
        # Skills frequency heatmap (grouped by categories)
        tech_skills = [skill for skill in top_skills.keys() if any(tech in skill.lower() for tech in ['python', 'sql', 'excel', 'tableau', 'power', 'r ', 'java', 'spark', 'aws'])]
        soft_skills = [skill for skill in top_skills.keys() if any(soft in skill.lower() for soft in ['communication', 'teamwork', 'leadership', 'problem', 'analytical'])]
        
        # Create skill category analysis
        categories = {
            'Technical': len([s for s in all_skills if s in tech_skills]),
            'Soft Skills': len([s for s in all_skills if s in soft_skills]),
            'Other': len([s for s in all_skills if s not in tech_skills and s not in soft_skills])
        }
        
        axes[1].pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        axes[1].set_title('Skills Distribution by Category')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'skills_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Save detailed skills data
        skills_report = {
            'total_skills_mentions': len(all_skills),
            'unique_skills': len(skill_counts),
            'top_20_skills': dict(skill_counts.most_common(20)),
            'skill_categories': categories
        }
        
        with open(self.output_dir / 'skills_report.json', 'w') as f:
            json.dump(skills_report, f, indent=2)
    
    def create_geographic_analysis(self):
        """Create geographic and location-based analysis."""
        print("📍 Creating geographic analysis...")
        
        location_counts = self.df['location'].value_counts().head(15)
        
        if location_counts.empty:
            print("⚠️ No location data found")
            return
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle('Geographic Job Market Analysis', fontsize=16, fontweight='bold')
        
        # Top locations bar chart
        axes[0].barh(range(len(location_counts)), location_counts.values)
        axes[0].set_yticks(range(len(location_counts)))
        axes[0].set_yticklabels(location_counts.index)
        axes[0].set_title('Top 15 Job Markets by Location')
        axes[0].set_xlabel('Number of Jobs')
        
        # Remote vs location analysis
        remote_by_location = self.df.groupby('location')['remote_option'].agg(['count', 'sum']).reset_index()
        remote_by_location['remote_percentage'] = (remote_by_location['sum'] / remote_by_location['count']) * 100
        top_locations_remote = remote_by_location.nlargest(10, 'count')
        
        axes[1].scatter(top_locations_remote['count'], top_locations_remote['remote_percentage'], 
                       s=100, alpha=0.7)
        axes[1].set_xlabel('Total Jobs in Location')
        axes[1].set_ylabel('Remote Work Percentage')
        axes[1].set_title('Remote Work Availability by Job Market Size')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'geographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_company_insights(self):
        """Create company hiring insights."""
        print("🏢 Creating company analysis...")
        
        company_counts = self.df['company'].value_counts().head(20)
        
        if company_counts.empty:
            print("⚠️ No company data found")
            return
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(company_counts)), company_counts.values)
        plt.yticks(range(len(company_counts)), company_counts.index)
        plt.title('Top 20 Hiring Companies', fontsize=14, fontweight='bold')
        plt.xlabel('Number of Job Postings')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'company_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Company diversity analysis
        total_jobs = len(self.df)
        total_companies = self.df['company'].nunique()
        avg_jobs_per_company = total_jobs / total_companies if total_companies > 0 else 0
        
        company_stats = {
            'total_companies': total_companies,
            'total_jobs': total_jobs,
            'average_jobs_per_company': round(avg_jobs_per_company, 2),
            'top_20_companies': dict(company_counts.head(20)),
            'hiring_concentration': round((company_counts.head(5).sum() / total_jobs) * 100, 1)
        }
        
        with open(self.output_dir / 'company_stats.json', 'w') as f:
            json.dump(company_stats, f, indent=2)
    
    def create_industry_trends(self):
        """Create industry analysis and trends."""
        print("🏭 Creating industry analysis...")
        
        if 'ai_industry' not in self.df.columns or self.df['ai_industry'].isna().all():
            print("⚠️ No industry data found")
            return
        
        industry_counts = self.df['ai_industry'].value_counts().head(10)
        
        plt.figure(figsize=(12, 8))
        plt.pie(industry_counts.values, labels=industry_counts.index, autopct='%1.1f%%')
        plt.title('Job Distribution by Industry', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'industry_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_compensation_analysis(self):
        """Create compensation and salary analysis."""
        print("💰 Creating compensation analysis...")
        
        # Filter jobs with compensation data
        comp_data = self.df[self.df['compensation_score'] > 0]
        
        if comp_data.empty:
            print("⚠️ No compensation data found")
            return
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle('Compensation Analysis', fontsize=16, fontweight='bold')
        
        # Compensation scores distribution
        axes[0].hist(comp_data['compensation_score'], bins=20, alpha=0.7, edgecolor='black')
        axes[0].set_title('Distribution of Compensation Scores')
        axes[0].set_xlabel('Compensation Score')
        axes[0].set_ylabel('Number of Jobs')
        
        # Benefits analysis
        benefits_data = comp_data[comp_data['benefits_count'] > 0]
        if not benefits_data.empty:
            axes[1].scatter(benefits_data['compensation_score'], benefits_data['benefits_count'], alpha=0.6)
            axes[1].set_title('Compensation Score vs. Benefits Mentioned')
            axes[1].set_xlabel('Compensation Score')
            axes[1].set_ylabel('Number of Benefits Mentioned')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'compensation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_interactive_dashboard(self):
        """Create interactive Plotly dashboard."""
        print("🌐 Creating interactive dashboard...")
        
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Jobs by Scenario', 'Skills Distribution', 'Geographic Distribution', 'Company Analysis'),
                specs=[[{"type": "pie"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Jobs by scenario (pie chart)
            scenario_counts = self.df['scenario'].value_counts()
            fig.add_trace(
                go.Pie(labels=scenario_counts.index, values=scenario_counts.values, name="Scenarios"),
                row=1, col=1
            )
            
            # Top skills (bar chart)
            all_skills = []
            for _, row in self.df.iterrows():
                for i in range(1, 11):
                    skill = row.get(f'skill_{i}')
                    if pd.notna(skill) and skill:
                        all_skills.append(skill)
            
            if all_skills:
                skill_counts = Counter(all_skills)
                top_skills = dict(skill_counts.most_common(10))
                fig.add_trace(
                    go.Bar(x=list(top_skills.values()), y=list(top_skills.keys()), 
                           orientation='h', name="Skills"),
                    row=1, col=2
                )
            
            # Top locations
            location_counts = self.df['location'].value_counts().head(10)
            if not location_counts.empty:
                fig.add_trace(
                    go.Bar(x=location_counts.values, y=location_counts.index, 
                           orientation='h', name="Locations"),
                    row=2, col=1
                )
            
            # Top companies
            company_counts = self.df['company'].value_counts().head(10)
            if not company_counts.empty:
                fig.add_trace(
                    go.Bar(x=company_counts.values, y=company_counts.index, 
                           orientation='h', name="Companies"),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title_text="Interactive Job Market Analysis Dashboard",
                title_x=0.5,
                height=800,
                showlegend=False
            )
            
            # Save interactive dashboard
            dashboard_file = self.output_dir / 'interactive_dashboard.html'
            pyo.plot(fig, filename=str(dashboard_file), auto_open=False)
            print(f"✅ Interactive dashboard saved: {dashboard_file}")
            
        except Exception as e:
            print(f"⚠️ Interactive dashboard creation failed: {e}")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        print("📋 Generating summary report...")
        
        total_jobs = len(self.df)
        ai_analyzed = self.df['has_ai_analysis'].sum()
        unique_companies = self.df['company'].nunique()
        unique_locations = self.df['location'].nunique()
        remote_jobs = self.df['remote_option'].sum()
        
        # Skills analysis
        all_skills = []
        for _, row in self.df.iterrows():
            for i in range(1, 11):
                skill = row.get(f'skill_{i}')
                if pd.notna(skill) and skill:
                    all_skills.append(skill)
        
        unique_skills = len(set(all_skills))
        
        summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "dataset_overview": {
                "total_jobs_analyzed": total_jobs,
                "ai_analysis_coverage": round((ai_analyzed / total_jobs) * 100, 1) if total_jobs > 0 else 0,
                "unique_companies": unique_companies,
                "unique_locations": unique_locations,
                "unique_skills_identified": unique_skills,
                "remote_work_percentage": round((remote_jobs / total_jobs) * 100, 1) if total_jobs > 0 else 0
            },
            "top_insights": {
                "most_demanded_skills": dict(Counter(all_skills).most_common(10)),
                "top_hiring_companies": dict(self.df['company'].value_counts().head(10)),
                "hottest_job_markets": dict(self.df['location'].value_counts().head(10)),
                "dominant_scenarios": dict(self.df['scenario'].value_counts())
            },
            "market_trends": {
                "remote_work_adoption": f"{round((remote_jobs / total_jobs) * 100, 1)}% of positions offer remote work",
                "hiring_diversity": f"Jobs distributed across {unique_companies} companies",
                "geographic_spread": f"Opportunities available in {unique_locations} different locations",
                "skill_diversity": f"{unique_skills} unique skills identified across all positions"
            }
        }
        
        # Save summary report
        summary_file = self.output_dir / 'analysis_summary_report.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Summary report saved: {summary_file}")
        
        # Display key insights
        print("\n🎯 KEY MARKET INSIGHTS")
        print("=" * 40)
        print(f"📊 Total Jobs Analyzed: {total_jobs}")
        print(f"🤖 AI Analysis Coverage: {summary['dataset_overview']['ai_analysis_coverage']}%")
        print(f"🏠 Remote Work Opportunities: {summary['dataset_overview']['remote_work_percentage']}%")
        print(f"🏢 Companies Hiring: {unique_companies}")
        print(f"📍 Geographic Markets: {unique_locations}")
        print(f"🛠️ Unique Skills: {unique_skills}")
        
        if all_skills:
            top_skills = Counter(all_skills).most_common(5)
            print(f"\n🔥 Top 5 Most Demanded Skills:")
            for i, (skill, count) in enumerate(top_skills, 1):
                print(f"  {i}. {skill}: {count} mentions")
        
        return summary

def main():
    """Main function to create analytics dashboard."""
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
    
    # Create dashboard
    dashboard = JobMarketAnalyticsDashboard(data_file)
    dashboard.create_comprehensive_dashboard()
    dashboard.generate_summary_report()
    
    print("\n🎉 Analytics dashboard generation complete!")
    print(f"📊 Charts and reports saved to: {dashboard.output_dir}")

if __name__ == "__main__":
    main()
