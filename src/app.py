"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# CV / Curriculum Vitae data
cv_data = {
    "personal": {
        "name": "Alex Djokic",
        "title": "Senior Software Engineer",
        "location": "Belgrade, Serbia",
        "email": "alex.djokic@example.com",
        "phone": "+381 60 123 4567",
        "linkedin": "linkedin.com/in/alexdjokic",
        "github": "github.com/adjokic2",
        "summary": (
            "Passionate software engineer with 8+ years of experience designing and "
            "building scalable backend services and modern web applications. "
            "Skilled at leading cross-functional teams, mentoring junior developers, "
            "and delivering high-quality software on time. Strong advocate for clean "
            "code, automated testing, and continuous improvement."
        )
    },
    "experience": [
        {
            "company": "TechNova Solutions",
            "role": "Senior Software Engineer",
            "period": "Jan 2021 – Present",
            "location": "Belgrade, Serbia (Hybrid)",
            "highlights": [
                "Architected a microservices platform handling 50M+ daily API requests using Python and FastAPI.",
                "Reduced average response latency by 40% through caching and query optimisation.",
                "Introduced CI/CD pipelines (GitHub Actions + Docker) that cut release cycle from 2 weeks to 2 days.",
                "Mentored a team of 4 junior engineers and conducted bi-weekly code reviews."
            ]
        },
        {
            "company": "DataStream d.o.o.",
            "role": "Backend Developer",
            "period": "Mar 2018 – Dec 2020",
            "location": "Novi Sad, Serbia",
            "highlights": [
                "Built RESTful APIs consumed by 3 client-facing mobile apps (React Native).",
                "Migrated legacy monolith to a service-oriented architecture, improving deployment flexibility.",
                "Implemented real-time data pipelines with Kafka and PostgreSQL."
            ]
        },
        {
            "company": "StartIT Hub",
            "role": "Junior Developer",
            "period": "Jun 2016 – Feb 2018",
            "location": "Belgrade, Serbia",
            "highlights": [
                "Developed features for an e-commerce platform (Django + Vue.js).",
                "Wrote unit and integration tests, raising code coverage from 32% to 78%.",
                "Collaborated in a 6-person agile team using Jira and GitLab."
            ]
        }
    ],
    "education": [
        {
            "institution": "University of Belgrade – School of Electrical Engineering",
            "degree": "M.Sc. in Computer Engineering",
            "period": "2014 – 2016",
            "details": "Thesis: 'Distributed Stream Processing with Apache Kafka'"
        },
        {
            "institution": "University of Novi Sad – Faculty of Technical Sciences",
            "degree": "B.Sc. in Software Engineering",
            "period": "2010 – 2014",
            "details": "Graduated with honours (GPA 9.2/10)"
        }
    ],
    "skills": {
        "Languages": ["Python", "JavaScript / TypeScript", "Go", "SQL"],
        "Frameworks & Libraries": ["FastAPI", "Django", "Node.js", "React", "Vue.js"],
        "Databases": ["PostgreSQL", "Redis", "MongoDB", "Elasticsearch"],
        "DevOps & Cloud": ["Docker", "Kubernetes", "GitHub Actions", "AWS (EC2, S3, RDS)", "Terraform"],
        "Practices": ["REST & GraphQL APIs", "Microservices", "TDD / BDD", "Agile / Scrum", "Code Review"]
    },
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect – Associate",
            "issuer": "Amazon Web Services",
            "year": "2022"
        },
        {
            "name": "Professional Scrum Master I (PSM I)",
            "issuer": "Scrum.org",
            "year": "2020"
        }
    ],
    "languages": [
        {"language": "Serbian", "level": "Native"},
        {"language": "English", "level": "Full Professional Proficiency (C1)"},
        {"language": "German", "level": "Intermediate (B1)"}
    ]
}

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.get("/cv")
def get_cv():
    """Return the curriculum vitae data"""
    return cv_data
