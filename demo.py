#!/usr/bin/env python3
"""
Demo Script for AI Cover Letter Generator
"""

import requests
import json

def demo_cover_letter_generation():
    """Demo the cover letter generation with different scenarios"""
    
    print("🎭 AI Cover Letter Generator Demo")
    print("=" * 50)
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Software Engineer Position",
            "job_posting": {
                "job_posting_text": """
                Senior Software Engineer - Python/FastAPI
                
                We are seeking a talented Senior Software Engineer to join our team. 
                The ideal candidate will have:
                - 3+ years of experience with Python
                - Experience with FastAPI or similar web frameworks
                - Knowledge of React and modern frontend technologies
                - Understanding of machine learning concepts
                - Experience with Docker and cloud platforms
                - Strong problem-solving skills
                
                Responsibilities:
                - Develop and maintain web applications
                - Collaborate with cross-functional teams
                - Implement best practices and code reviews
                - Mentor junior developers
                """
            },
            "cv_data": {
                "cv_text": """
                John Doe
                Software Developer
                
                Experience:
                - 4 years as Python Developer at TechCorp
                - Built REST APIs using FastAPI and Django
                - Developed frontend applications with React
                - Basic knowledge of machine learning algorithms
                - Experience with Docker and AWS
                - Led a team of 3 junior developers
                
                Skills:
                - Python, JavaScript, TypeScript
                - FastAPI, Django, React
                - PostgreSQL, MongoDB
                - Docker, AWS, Git
                - Basic ML (scikit-learn, TensorFlow)
                """
            },
            "tone": "formal"
        },
        {
            "name": "Data Scientist Position",
            "job_posting": {
                "job_posting_text": """
                Data Scientist - Machine Learning Focus
                
                Join our data science team to build innovative ML solutions.
                Requirements:
                - Advanced degree in Computer Science or related field
                - 2+ years of experience in machine learning
                - Proficiency in Python and ML libraries (scikit-learn, TensorFlow)
                - Experience with data analysis and visualization
                - Knowledge of SQL and big data technologies
                - Strong statistical background
                
                What you'll do:
                - Develop and deploy ML models
                - Analyze large datasets
                - Create data visualizations
                - Collaborate with product teams
                """
            },
            "cv_data": {
                "cv_text": """
                Jane Smith
                Data Analyst
                
                Education:
                - MSc in Computer Science, Stanford University
                - BSc in Mathematics, MIT
                
                Experience:
                - 2 years as Data Analyst at DataCorp
                - Built predictive models using scikit-learn
                - Created data visualizations with Tableau and Python
                - Worked with SQL databases and pandas
                - Published 3 papers on ML applications
                
                Skills:
                - Python, R, SQL
                - scikit-learn, TensorFlow, PyTorch
                - pandas, numpy, matplotlib
                - Tableau, PowerBI
                - Statistical analysis and hypothesis testing
                """
            },
            "tone": "friendly"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://localhost:8001/api/generate-cover-letter",
                headers={"Content-Type": "application/json"},
                data=json.dumps({
                    "job_posting": scenario["job_posting"],
                    "cv_data": scenario["cv_data"],
                    "tone": scenario["tone"]
                })
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"🎯 Position: {data['analysis']['position_title']}")
                print(f"🏢 Company: {data['analysis']['company_name']}")
                print(f"📊 Skills Extracted: {', '.join(data['analysis']['extracted_skills'])}")
                print(f"✅ Skill Matches: {len([s for s in data['skill_matches'] if s['matched']])}/{len(data['skill_matches'])}")
                print(f"💡 Recommendations: {len(data['recommendations'])}")
                print(f"📝 Tone Used: {data['tone_used']}")
                
                # Show top skill matches
                print("\n🎯 Top Skill Matches:")
                for match in data['skill_matches'][:3]:
                    status = "✅" if match['matched'] else "❌"
                    confidence = f"{match['confidence']*100:.0f}%"
                    print(f"   {status} {match['skill']} ({confidence})")
                
                # Show recommendations
                print("\n💡 Recommendations:")
                for rec in data['recommendations'][:2]:
                    print(f"   • {rec}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50)

def main():
    """Run the demo"""
    print("🚀 Starting AI Cover Letter Generator Demo")
    print("Make sure both backend (port 8001) and frontend (port 3000) are running!")
    print()
    
    try:
        demo_cover_letter_generation()
        print("\n🎉 Demo completed successfully!")
        print("\n🌐 You can also test the web interface at: http://localhost:3000")
        print("📊 API documentation at: http://localhost:8001/docs")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
