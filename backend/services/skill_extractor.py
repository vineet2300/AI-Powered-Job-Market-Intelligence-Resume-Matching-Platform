import re


# =========================================================
# SKILL ALIASES
# =========================================================
# Left side = standard skill name stored/displayed by system
# Right side = different ways the skill may appear in text

SKILL_ALIASES = {

    # =====================================================
    # PROGRAMMING LANGUAGES
    # =====================================================

    "python": [
        "python",
        "python3",
        "python 3"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "c": [
        "c language",
        "programming in c"
    ],

    "c#": [
        "c#",
        "c sharp"
    ],

    "javascript": [
        "javascript",
        "java script",
        "js"
    ],

    "typescript": [
        "typescript",
        "type script"
    ],

    "r": [
        "r programming",
        "r language"
    ],

    "php": [
        "php"
    ],

    "go": [
        "golang",
        "go language"
    ],

    "kotlin": [
        "kotlin"
    ],

    "swift": [
        "swift"
    ],


    # =====================================================
    # FRONTEND
    # =====================================================

    "html": [
        "html",
        "html5"
    ],

    "css": [
        "css",
        "css3"
    ],

    "react": [
        "react",
        "react.js",
        "reactjs",
        "react js"
    ],

    "angular": [
        "angular",
        "angular.js",
        "angularjs"
    ],

    "vue.js": [
        "vue",
        "vue.js",
        "vuejs",
        "vue js"
    ],

    "next.js": [
        "next.js",
        "nextjs",
        "next js"
    ],

    "bootstrap": [
        "bootstrap"
    ],

    "tailwind css": [
        "tailwind",
        "tailwind css",
        "tailwindcss"
    ],

    "redux": [
        "redux"
    ],

    "jquery": [
        "jquery"
    ],


    # =====================================================
    # BACKEND / FRAMEWORKS
    # =====================================================

    "node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "express.js": [
        "express.js",
        "expressjs",
        "express js",
        "express"
    ],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "django": [
        "django"
    ],

    "flask": [
        "flask"
    ],

    "spring": [
        "spring framework",
        "spring"
    ],

    "spring boot": [
        "spring boot",
        "springboot"
    ],

    ".net": [
        ".net",
        "dotnet",
        "dot net"
    ],

    "asp.net": [
        "asp.net",
        "asp net"
    ],


    # =====================================================
    # DATABASE
    # =====================================================

    "sql": [
        "sql"
    ],

    "mysql": [
        "mysql",
        "my sql"
    ],

    "postgresql": [
        "postgresql",
        "postgres",
        "postgre sql"
    ],

    "mongodb": [
        "mongodb",
        "mongo db"
    ],

    "oracle": [
        "oracle database",
        "oracle db",
        "oracle"
    ],

    "sqlite": [
        "sqlite"
    ],

    "redis": [
        "redis"
    ],

    "firebase": [
        "firebase"
    ],

    "microsoft sql server": [
        "sql server",
        "mssql",
        "microsoft sql server"
    ],


    # =====================================================
    # DATA ANALYSIS / DATA SCIENCE
    # =====================================================

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "matplotlib": [
        "matplotlib"
    ],

    "seaborn": [
        "seaborn"
    ],

    "scipy": [
        "scipy"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "jupyter": [
        "jupyter",
        "jupyter notebook"
    ],

    "data analysis": [
        "data analysis",
        "data analytics",
        "data analyst"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "statistics": [
        "statistics",
        "statistical analysis"
    ],

    "data cleaning": [
        "data cleaning",
        "data cleansing"
    ],

    "etl": [
        "etl",
        "extract transform load"
    ],

    "data mining": [
        "data mining"
    ],


    # =====================================================
    # MACHINE LEARNING / AI
    # =====================================================

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "computer vision": [
        "computer vision"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch",
        "py torch"
    ],

    "keras": [
        "keras"
    ],

    "opencv": [
        "opencv",
        "open cv"
    ],

    "generative ai": [
        "generative ai",
        "gen ai",
        "genai"
    ],

    "large language models": [
        "large language model",
        "large language models",
        "llm",
        "llms"
    ],

    "prompt engineering": [
        "prompt engineering"
    ],


    # =====================================================
    # CLOUD
    # =====================================================

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "google cloud": [
        "google cloud",
        "google cloud platform",
        "gcp"
    ],

    "ec2": [
        "amazon ec2",
        "aws ec2",
        "ec2"
    ],

    "s3": [
        "amazon s3",
        "aws s3"
    ],

    "lambda": [
        "aws lambda",
        "lambda"
    ],


    # =====================================================
    # DEVOPS
    # =====================================================

    "docker": [
        "docker"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "jenkins": [
        "jenkins"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "gitlab": [
        "gitlab"
    ],

    "github actions": [
        "github actions"
    ],

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous deployment"
    ],

    "terraform": [
        "terraform"
    ],

    "ansible": [
        "ansible"
    ],

    "linux": [
        "linux"
    ],

    "bash": [
        "bash",
        "shell scripting"
    ],


    # =====================================================
    # APIs / ARCHITECTURE
    # =====================================================

    "rest api": [
        "rest api",
        "restful api",
        "restful services",
        "rest services"
    ],

    "graphql": [
        "graphql",
        "graph ql"
    ],

    "microservices": [
        "microservices",
        "micro services",
        "microservice architecture"
    ],

    "api development": [
        "api development",
        "api integration"
    ],

    "web services": [
        "web services"
    ],

    "json": [
        "json"
    ],

    "xml": [
        "xml"
    ],


    # =====================================================
    # BIG DATA
    # =====================================================

    "hadoop": [
        "hadoop"
    ],

    "spark": [
        "apache spark",
        "pyspark",
        "spark"
    ],

    "kafka": [
        "apache kafka",
        "kafka"
    ],

    "hive": [
        "apache hive",
        "hive"
    ],

    "databricks": [
        "databricks"
    ],

    "snowflake": [
        "snowflake"
    ],

    "airflow": [
        "apache airflow",
        "airflow"
    ],


    # =====================================================
    # BUSINESS INTELLIGENCE
    # =====================================================

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": [
        "tableau"
    ],

    "excel": [
        "microsoft excel",
        "ms excel",
        "excel"
    ],

    "advanced excel": [
        "advanced excel"
    ],


    # =====================================================
    # CYBER SECURITY
    # =====================================================

    "cyber security": [
        "cyber security",
        "cybersecurity",
        "information security"
    ],

    "network security": [
        "network security"
    ],

    "penetration testing": [
        "penetration testing",
        "pen testing",
        "pentesting"
    ],

    "vulnerability assessment": [
        "vulnerability assessment"
    ],

    "siem": [
        "siem"
    ],

    "splunk": [
        "splunk"
    ],

    "firewall": [
        "firewall",
        "firewalls"
    ],

    "owasp": [
        "owasp"
    ],


    # =====================================================
    # SOFTWARE ENGINEERING
    # =====================================================

    "oop": [
        "object oriented programming",
        "object-oriented programming",
        "oop",
        "oops"
    ],

    "data structures": [
        "data structures",
        "data structure",
        "dsa"
    ],

    "algorithms": [
        "algorithms",
        "algorithm design"
    ],

    "system design": [
        "system design"
    ],

    "design patterns": [
        "design patterns",
        "design pattern"
    ],

    "software development": [
        "software development"
    ],

    "software engineering": [
        "software engineering"
    ],

    "debugging": [
        "debugging"
    ],

    "unit testing": [
        "unit testing",
        "unit tests"
    ],

    "integration testing": [
        "integration testing"
    ],


    # =====================================================
    # DEVELOPMENT METHODS
    # =====================================================

    "agile": [
        "agile"
    ],

    "scrum": [
        "scrum"
    ],

    "jira": [
        "jira"
    ],

    "sdlc": [
        "sdlc",
        "software development life cycle"
    ],


    # =====================================================
    # TOOLS
    # =====================================================

    "postman": [
        "postman"
    ],

    "visual studio code": [
        "visual studio code",
        "vs code",
        "vscode"
    ],

    "intellij idea": [
        "intellij",
        "intellij idea"
    ],

    "eclipse": [
        "eclipse ide",
        "eclipse"
    ]
}


# =========================================================
# HELPER FUNCTION
# =========================================================

def contains_skill(text, alias):
    """
    Check whether a skill alias exists as a complete
    term instead of accidentally matching inside
    another word.
    """

    pattern = (
        r"(?<![a-zA-Z0-9])"
        + re.escape(alias.lower())
        + r"(?![a-zA-Z0-9])"
    )

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE
    ) is not None


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = set()

    for standard_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_skill(text, alias):

                found_skills.add(
                    standard_skill
                )

                # Once one alias matches,
                # no need to check remaining aliases
                break


    # -----------------------------------------------------
    # REMOVE REDUNDANT / OVERLAPPING SKILLS
    # -----------------------------------------------------

    # Spring Boot already implies Spring
    if "spring boot" in found_skills:
        found_skills.discard("spring")

    # Advanced Excel already implies Excel
    if "advanced excel" in found_skills:
        found_skills.discard("excel")


    return sorted(found_skills)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_text = """
    Python Developer with experience in Python,
    FastAPI, PostgreSQL, REST APIs, Docker,
    Kubernetes, AWS, GitHub Actions and CI/CD.

    Worked with Pandas, NumPy, Machine Learning,
    Power BI and React.js.

    Familiar with Java, Spring Boot,
    Microservices and SQL.
    """

    skills = extract_skills(
        sample_text
    )

    print("\nExtracted skills:")

    for skill in skills:
        print("-", skill)

    print(
        "\nTotal skills detected:",
        len(skills)
    )