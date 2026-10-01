SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "react",
    "node.js",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "power bi",
    "tableau",
    "excel"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills