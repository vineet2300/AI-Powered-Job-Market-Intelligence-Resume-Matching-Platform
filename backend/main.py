from fastapi import FastAPI

from backend.routes.jobs import router as jobs_router

from backend.routes.resumes import router as resumes_router

from backend.routes.matching import router as matching_router

from backend.routes.target_role import router as target_role_router

from backend.routes.analytics import router as analytics_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Job Market Intelligence API",
    description="Backend API for Job Market Intelligence and Resume Matching",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Job Market Intelligence API is running"
    }



app.include_router(jobs_router, prefix="/api")
app.include_router(resumes_router, prefix="/api")
app.include_router(matching_router, prefix="/api")
app.include_router(target_role_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")