import { useEffect, useState } from "react";
import "./App.css";

function App() {
  /* ========================================= */
  /* STATES */
  /* ========================================= */

  const [scrollY, setScrollY] = useState(0);

  const [analytics, setAnalytics] = useState(null);
  const [jobs, setJobs] = useState([]);

  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRole, setSelectedRole] = useState("all");
  const [selectedLocation, setSelectedLocation] = useState("all");
  const [selectedSource, setSelectedSource] = useState("all");
  

  /* RESUME MATCH */
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeMatches, setResumeMatches] = useState(null);
  const [resumeLoading, setResumeLoading] = useState(false);
  const [resumeError, setResumeError] = useState("");

  /* TARGET ROLE */
  const [targetRole, setTargetRole] = useState("");
  const [targetResumeFile, setTargetResumeFile] = useState(null);
  const [targetRoleResult, setTargetRoleResult] = useState(null);
  const [targetRoleLoading, setTargetRoleLoading] = useState(false);
  const [targetRoleError, setTargetRoleError] = useState("");

  /* POST A JOB */
const [jobForm, setJobForm] = useState({
  title: "",
  company: "",
  location: "",
  description: "",
  skills: "",
  salary_min: "",
  salary_max: "",
  recruiter_email: "",
});

const [jobPosting, setJobPosting] = useState(false);
const [jobPostMessage, setJobPostMessage] = useState("");
const [jobPostError, setJobPostError] = useState("");
/* JOB DETAILS */
const [selectedJobDetails, setSelectedJobDetails] = useState(null);

  /* ========================================= */
  /* HERO SCROLL */
  /* ========================================= */

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  /* ========================================= */
  /* FETCH ANALYTICS */
  /* ========================================= */

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/analytics/overview"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch analytics");
        }

        const data = await response.json();
        setAnalytics(data);
      } catch (error) {
        console.error("Analytics error:", error);
      }
    };

    fetchAnalytics();
  }, []);

  /* ========================================= */
  /* FETCH JOBS */
  /* ========================================= */

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/jobs/"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch jobs");
        }

        const data = await response.json();
        setJobs(data);
      } catch (error) {
        console.error("Jobs error:", error);
      }
    };

    fetchJobs();
  }, []);

  /* ========================================= */
  /* HERO EFFECT */
  /* ========================================= */

  const heroOpacity = Math.max(0, 1 - scrollY / 400);
  const heroTranslate = Math.min(scrollY * 0.12, 50);

  /* ========================================= */
  /* JOB FILTERING */
  /* ========================================= */

  const filteredJobs = jobs.filter((job) => {
    const search = searchTerm.toLowerCase().trim();

    const title = (job.title || "").toLowerCase();
    const company = (job.company || "").toLowerCase();
    const location = (job.location || "").toLowerCase();
    const jobRole = (job.role_category || "").toLowerCase();
    const source = (job.source || "").toLowerCase();

    const matchesSearch =
      title.includes(search) ||
      company.includes(search) ||
      location.includes(search);

    const matchesRole =
      selectedRole === "all" ||
      jobRole === selectedRole.toLowerCase();

    const matchesLocation =
      selectedLocation === "all" ||
      location === selectedLocation.toLowerCase();

    const matchesSource =
      selectedSource === "all" ||
      source === selectedSource.toLowerCase();


    return matchesSearch && matchesRole && matchesLocation && matchesSource;
  });

  const displayedJobs = filteredJobs
    

  /* ========================================= */
  /* UNIQUE ROLES */
  /* ========================================= */

  const roles = [
    ...new Set(
      jobs
        .map((job) => job.role_category)
        .filter(Boolean)
    ),
  ].sort();
  const locations = [
    ...new Set(
      jobs
        .map((job) => job.location)
        .filter(Boolean)
    ),
  ].sort();
  const sources = [
    ...new Set(
      jobs
         .map((job) => job.source)
         .filter(Boolean)
    ),
  ].sort();

  /* ========================================= */
  /* DASHBOARD VALUES */
  /* ========================================= */

  const sourceCount =
    analytics?.jobs_by_source?.length ?? "—";

  const topSkill =
    analytics?.top_detected_skills?.[0]?.skill || "—";

  /* ========================================= */
  /* SCROLL */
  /* ========================================= */

  const scrollToSection = (sectionId) => {
    const section = document.getElementById(sectionId);

    if (section) {
      section.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  /* ========================================= */
  /* RESUME MATCH */
  /* ========================================= */

  const handleResumeMatch = async () => {
    if (!resumeFile) {
      setResumeError("Please select a PDF resume first.");
      return;
    }

    if (resumeFile.type !== "application/pdf") {
      setResumeError("Please upload a PDF file.");
      return;
    }

    setResumeLoading(true);
    setResumeError("");
    setResumeMatches(null);

    try {
      const formData = new FormData();
      formData.append("file", resumeFile);

      const response = await fetch(
        "http://127.0.0.1:8000/matching/best-jobs?limit=5",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Resume matching failed.");
      }

      const data = await response.json();
      setResumeMatches(data);
    } catch (error) {
      console.error("Resume matching error:", error);

      setResumeError(
        "Could not analyze the resume. Please make sure the backend is running and try again."
      );
    } finally {
      setResumeLoading(false);
    }
  };

  /* ========================================= */
  /* TARGET ROLE ANALYSIS */
  /* ========================================= */

  const handleTargetRoleAnalysis = async () => {
    if (!targetRole) {
      setTargetRoleError("Please select your target role.");
      return;
    }

    if (!targetResumeFile) {
      setTargetRoleError("Please select a PDF resume.");
      return;
    }

    if (targetResumeFile.type !== "application/pdf") {
      setTargetRoleError("Please upload a PDF file.");
      return;
    }

    setTargetRoleLoading(true);
    setTargetRoleError("");
    setTargetRoleResult(null);

    try {
      const formData = new FormData();

      formData.append("role", targetRole);
      formData.append("file", targetResumeFile);

      const response = await fetch(
        "http://127.0.0.1:8000/target-role/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Target role analysis failed.");
      }

      const data = await response.json();

      setTargetRoleResult(data);
    } catch (error) {
      console.error("Target role error:", error);

      setTargetRoleError(
        "Could not analyze the target role. Please make sure the backend is running and try again."
      );
    } finally {
      setTargetRoleLoading(false);
    }
  };

  /* ========================================= */
/* POST A JOB */
/* ========================================= */

const handlePostJob = async (event) => {
  event.preventDefault();

  setJobPostMessage("");
  setJobPostError("");

  if (
    !jobForm.title.trim() ||
    !jobForm.company.trim() ||
    !jobForm.description.trim() ||
    !jobForm.recruiter_email.trim()
  ) {
    setJobPostError(
      "Please enter job title, company and description."
    );
    return;
  }

  const salaryMin =
    jobForm.salary_min === ""
      ? 0
      : Number(jobForm.salary_min);

  const salaryMax =
    jobForm.salary_max === ""
      ? 0
      : Number(jobForm.salary_max);

  if (
    Number.isNaN(salaryMin) ||
    Number.isNaN(salaryMax) ||
    salaryMin < 0 ||
    salaryMax < 0
  ) {
    setJobPostError("Please enter valid salary values.");
    return;
  }

  if (
    salaryMin > 0 &&
    salaryMax > 0 &&
    salaryMax < salaryMin
  ) {
    setJobPostError(
      "Maximum salary cannot be less than minimum salary."
    );
    return;
  }

  setJobPosting(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/jobs/",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          title: jobForm.title.trim(),
          company: jobForm.company.trim(),
          location: jobForm.location.trim(),
          description: jobForm.description.trim(),
          skills: jobForm.skills.trim(),
          salary_min: salaryMin,
          salary_max: salaryMax,
          recruiter_email: jobForm.recruiter_email.trim(),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data?.detail || "Could not post the job."
      );
    }

    setJobPostMessage(
      `Job posted successfully. Job ID: ${data.job_id}`
    );

    setJobForm({
      title: "",
      company: "",
      location: "",
      description: "",
      skills: "",
      salary_min: "",
      salary_max: "",
      recruiter_email: "",
    });

    /* Refresh jobs */
    const jobsResponse = await fetch(
      "http://127.0.0.1:8000/jobs/"
    );

    if (jobsResponse.ok) {
      const jobsData = await jobsResponse.json();
      setJobs(jobsData);
    }

    /* Refresh analytics */
    const analyticsResponse = await fetch(
      "http://127.0.0.1:8000/analytics/overview"
    );

    if (analyticsResponse.ok) {
      const analyticsData = await analyticsResponse.json();
      setAnalytics(analyticsData);
    }
  } catch (error) {
    console.error("Post job error:", error);

    setJobPostError(
      error.message ||
        "Could not post the job. Please make sure the backend is running."
    );
  } finally {
    setJobPosting(false);
  }
};

  /* ========================================= */
  /* RETURN */
  /* ========================================= */

  return (
    <div className="app">

      {/* HERO */}

      <section className="hero">
        <div
          className="hero-content"
          style={{
            opacity: heroOpacity,
            transform: `translateY(-${heroTranslate}px)`,
          }}
        >
          <p className="hero-label">
            AI-POWERED CAREER PLATFORM
          </p>

          <h1>
            Job Market
            <br />
            Intelligence
          </h1>

          <p className="hero-description">
            Explore jobs, analyze the market
            and find roles that match your skills.
          </p>

          <nav className="hero-nav">
            <button onClick={() => scrollToSection("dashboard")}>
              Dashboard
            </button>

            <button onClick={() => scrollToSection("jobs")}>
              Jobs
            </button>

            <button onClick={() => scrollToSection("analytics")}>
              Analytics
            </button>

            <button onClick={() => scrollToSection("resume-match")}>
              Resume Match
            </button>

            <button onClick={() => scrollToSection("target-role")}>
              Target Role
            </button>

            <button onClick={() => scrollToSection("post-job")}>
              Post a Job
            </button>
          </nav>
        </div>

        <p
          className="scroll-text"
          style={{ opacity: heroOpacity }}
        >
          Scroll to explore
        </p>
      </section>

      {/* CURRENT MARKET */}

      <section className="market-summary">
        <p className="market-label">
          CURRENT JOB MARKET
        </p>

        <h2>
          <span>{analytics?.total_jobs ?? "—"}</span>{" "}
          jobs available
        </h2>

        <p className="market-description">
          Explore all available opportunities without
          uploading a resume. Upload your resume for
          personalized job recommendations, compatibility
          insights and skill-gap analysis.
        </p>

        <div className="market-actions">
          <button
            className="market-primary"
            onClick={() => scrollToSection("jobs")}
          >
            Browse Jobs
          </button>

          <button
            className="market-secondary"
            onClick={() => scrollToSection("resume-match")}
          >
            Upload Resume
          </button>
        </div>
      </section>

      {/* JOBS */}

      <section className="jobs-section" id="jobs">
        <div className="jobs-heading">
          <div>
            <p>OPPORTUNITIES</p>
            <h2>Explore current jobs.</h2>
          </div>

          <span>{filteredJobs.length} jobs</span>
        </div>

        <div className="job-controls">
          <input
            type="text"
            placeholder="Search by job, company or location"
            value={searchTerm}
            onChange={(event) => {
              setSearchTerm(event.target.value);
              
            }}
          />

          <select
            value={selectedRole}
            onChange={(event) => {
              setSelectedRole(event.target.value);
              
            }}
          >
            <option value="all">All roles</option>

            {roles.map((role) => (
              <option key={role} value={role}>
                {role}
              </option>
            ))}
          </select>
          <select
            value={selectedLocation}
            onChange={(event) => {
              setSelectedLocation(event.target.value);
              
            }}
          >
            <option value="all">All locations</option>

            {locations.map((location) => (
             <option key={location} value={location}>
               {location}
              </option>
            ))}
          </select>
          <select
            value={selectedSource}
            onChange={(event) => {
              setSelectedSource(event.target.value);
              
            }}
        
          >
            <option value="all">All sources</option>

            {sources.map((source) => (
              <option key={source} value={source}>
                {source}
             </option>
           ))}
         </select>
         <button
           type="button"
           className="clear-job-filters"
           onClick={() => {
             setSearchTerm("");
             setSelectedRole("all");
             setSelectedLocation("all");
             setSelectedSource("all");
             
           }}
         >
           Clear Filters
         </button>

        </div>

        <div className="job-columns">
          <span>JOB / COMPANY</span>
          <span>ROLE</span>
          <span>SOURCE</span>
          <span>ACTION</span>
        </div>

        <div className="jobs-list">
          {displayedJobs.length > 0 ? (
            displayedJobs.map((job) => (
              <div className="job-row" key={job.id}>
                <div className="job-main">
                  <h3>{job.title}</h3>

                  <p>
                    {job.company}
                    {job.location && ` · ${job.location}`}
                  </p>
                </div>

                <div className="job-meta">
                  <span>
                    {job.role_category || "General"}
                  </span>

                  <span>
                    {job.source || "Recruiter"}
                  </span>

                  
                    <button
                    type="button"
                    onClick={() => setSelectedJobDetails(job)}
                    > 
                    View Details
                    </button>
                    
                </div>
              </div>
            ))
          ) : (
            <div className="no-jobs">
              No jobs found.
            </div>
          )}
        </div>

        
          
        
      </section>

      {/* DASHBOARD */}

      <section className="dashboard" id="dashboard">
        <div className="section-header">
          <p>OVERVIEW</p>
          <h2>Current job market</h2>
        </div>

        <div className="stats">
          <div className="stat">
            <span>Total Jobs</span>
            <h3>{analytics?.total_jobs ?? "—"}</h3>
            <p>Available opportunities</p>
          </div>

          <div className="stat">
            <span>Sources</span>
            <h3>{sourceCount}</h3>
            <p>Job data sources</p>
          </div>

          <div className="stat">
            <span>Top Skill</span>
            <h3>{topSkill}</h3>
            <p>Most detected skill</p>
          </div>

          <div className="stat">
            <span>Resume Matching</span>
            <h3>Smart</h3>
            <p>Skill-based compatibility</p>
          </div>
        </div>

        <div className="sections">
          <article>
            <span>01</span>
            <h3>Browse Jobs</h3>

            <p>
              Explore jobs collected from external job
              sources and recruiter postings.
            </p>

            <button onClick={() => scrollToSection("jobs")}>
              Explore Jobs
            </button>
          </article>

          <article>
            <span>02</span>
            <h3>Market Analytics</h3>

            <p>
              Understand current roles, skills,
              locations and available salary data.
            </p>

            <button onClick={() => scrollToSection("analytics")}>
              View Analytics
            </button>
          </article>

          <article>
            <span>03</span>
            <h3>Resume Match</h3>

            <p>
              Compare your resume with available jobs
              and discover matching and missing skills.
            </p>

            <button onClick={() => scrollToSection("resume-match")}>
              Match Resume
            </button>
          </article>
        </div>
      </section>

      {/* ANALYTICS */}

      <section className="analytics-section" id="analytics">
        <div className="analytics-header">
          <div>
            <p className="analytics-label">
              MARKET ANALYTICS
            </p>

            <h2>
              Understand the current
              <br />
              job market.
            </h2>
          </div>

          <p className="analytics-intro">
            Insights generated from{" "}
            <strong>{analytics?.total_jobs ?? "—"}</strong>{" "}
            current job listings.
          </p>
        </div>

        <div className="analytics-summary">
          <div>
            <span>JOBS ANALYZED</span>
            <strong>{analytics?.total_jobs ?? "—"}</strong>
          </div>

          <div>
            <span>JOB SOURCES</span>
            <strong>
              {analytics?.jobs_by_source?.length ?? "—"}
            </strong>
          </div>

          <div>
            <span>TOP ROLE</span>
            <strong>
              {analytics?.jobs_by_role?.find(
                (item) => item.role?.toLowerCase() !== "other"
              )?.role ?? "—"}
            </strong>
          </div>

          <div>
            <span>TOP DETECTED SKILL</span>
            <strong>
              {analytics?.top_detected_skills?.[0]?.skill ?? "—"}
            </strong>
          </div>
        </div>

        <div className="analytics-block">
          <div className="analytics-block-heading">
            <div>
              <span>01</span>
              <h3>Role distribution</h3>
            </div>

            <p>
              Current number of listings classified
              under each role.
            </p>
          </div>

          <div className="analytics-bars">
            {analytics?.jobs_by_role
              ?.slice(0, 10)
              .map((item) => {
                const maxJobs =
                  analytics?.jobs_by_role?.[0]?.jobs || 1;

                const width =
                  (item.jobs / maxJobs) * 100;

                return (
                  <div
                    className="analytics-bar-row"
                    key={item.role}
                  >
                    <div className="analytics-bar-info">
                      <span>{item.role}</span>
                      <strong>{item.jobs}</strong>
                    </div>

                    <div className="analytics-bar-track">
                      <div
                        className="analytics-bar-fill"
                        style={{ width: `${width}%` }}
                      />
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        <div className="analytics-grid">
          <div className="analytics-panel">
            <div className="analytics-panel-title">
              <span>02</span>
              <h3>Top detected skills</h3>
            </div>

            <div className="skill-list">
              {analytics?.top_detected_skills
                ?.slice(0, 8)
                .map((skill, index) => (
                  <div
                    className="skill-row"
                    key={skill.skill}
                  >
                    <span className="skill-number">
                      {String(index + 1).padStart(2, "0")}
                    </span>

                    <strong>{skill.skill}</strong>

                    <span>
                      {skill.jobs_detected} jobs
                    </span>

                    <span>
                      {skill.percentage_of_analyzed_jobs}%
                    </span>
                  </div>
                ))}
            </div>

            <p className="analytics-note">
              Percentages show where the skill was
              detected in analyzed job descriptions.
            </p>
          </div>

          <div className="analytics-panel">
            <div className="analytics-panel-title">
              <span>03</span>
              <h3>Job sources</h3>
            </div>

            <div className="source-list">
              {analytics?.jobs_by_source?.map((source) => {
                const percentage =
                  analytics?.total_jobs
                    ? (
                        (source.jobs /
                          analytics.total_jobs) *
                        100
                      ).toFixed(1)
                    : 0;

                return (
                  <div
                    className="source-row"
                    key={source.source}
                  >
                    <div>
                      <strong>{source.source}</strong>
                      <span>{source.jobs} jobs</span>
                    </div>

                    <strong>{percentage}%</strong>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="analytics-block">
          <div className="analytics-block-heading">
            <div>
              <span>04</span>
              <h3>Top locations</h3>
            </div>

            <p>
              Locations with the highest number of
              current listings.
            </p>
          </div>

          <div className="location-grid">
            {analytics?.top_locations
              ?.slice(0, 8)
              .map((location, index) => (
                <div
                  className="location-item"
                  key={`${location.location}-${index}`}
                >
                  <span>
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <div>
                    <strong>{location.location}</strong>
                    <p>{location.jobs} jobs</p>
                  </div>
                </div>
              ))}
          </div>
        </div>

        <div className="salary-section">
          <div>
            <p className="analytics-label">
              SALARY INSIGHTS
            </p>

            <h3>Available salary data.</h3>

            <p>
              Based only on{" "}
              <strong>
                {analytics?.salary_insights?.jobs_with_salary ??
                  "—"}
              </strong>{" "}
              listings that currently include salary
              information.
            </p>
          </div>

          <div className="salary-values">
            <div>
              <span>AVERAGE MINIMUM</span>

              <strong>
                ₹
                {analytics?.salary_insights?.average_min_salary
                  ? Math.round(
                      analytics.salary_insights
                        .average_min_salary
                    ).toLocaleString("en-IN")
                  : "—"}
              </strong>
            </div>

            <div>
              <span>AVERAGE MAXIMUM</span>

              <strong>
                ₹
                {analytics?.salary_insights?.average_max_salary
                  ? Math.round(
                      analytics.salary_insights
                        .average_max_salary
                    ).toLocaleString("en-IN")
                  : "—"}
              </strong>
            </div>
          </div>
        </div>

        <div className="analytics-disclaimer">
          <strong>About this data</strong>

          <p>
            Role distribution represents current listing
            counts, not time-based hiring trends. Skill
            insights are based on skills detected in
            available job descriptions.
          </p>
        </div>
      </section>

      {/* ===================================== */}
      {/* RESUME MATCH */}
      {/* ===================================== */}

      <section
        className="resume-match-section"
        id="resume-match"
      >
        <div className="resume-match-header">
          <div>
            <p className="resume-match-label">
              RESUME MATCH
            </p>

            <h2>
              Find jobs that
              <br />
              match your skills.
            </h2>
          </div>

          <p>
            Upload your resume and compare your detected
            skills with current job listings.
          </p>
        </div>

        <div className="resume-upload-area">
          <div className="resume-upload-info">
            <span>01</span>
            <h3>Upload your resume</h3>

            <p>
              PDF format only. Your resume will be
              analyzed to identify skills and compare
              them with available jobs.
            </p>
          </div>

          <div className="resume-upload-control">
            <label
              className="resume-file-label"
              htmlFor="resume-file"
            >
              <span>
                {resumeFile
                  ? resumeFile.name
                  : "Choose PDF resume"}
              </span>

              <strong>Browse</strong>
            </label>

            <input
              id="resume-file"
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const file = event.target.files[0];

                setResumeFile(file || null);
                setResumeError("");
                setResumeMatches(null);
              }}
            />

            <button
              className="resume-match-button"
              onClick={handleResumeMatch}
              disabled={resumeLoading}
            >
              {resumeLoading
                ? "Analyzing Resume..."
                : "Find Matching Jobs"}
            </button>

            {resumeError && (
              <p className="resume-error">
                {resumeError}
              </p>
            )}
          </div>
        </div>

        {resumeLoading && (
          <div className="resume-loading">
            <span />

            <p>
              Comparing your skills with available jobs...
            </p>
          </div>
        )}

        {resumeMatches && !resumeLoading && (
          <div className="resume-results">
            <div className="resume-results-header">
              <div>
                <p className="resume-match-label">
                  MATCH RESULTS
                </p>

                <h3>
                  Best matches for your resume.
                </h3>
              </div>

              <div className="resume-result-stats">
                <div>
                  <span>JOBS ANALYZED</span>
                  <strong>
                    {resumeMatches.jobs_analyzed}
                  </strong>
                </div>

                <div>
                  <span>
                    JOBS WITH DETECTED SKILLS
                  </span>

                  <strong>
                    {
                      resumeMatches
                        .jobs_with_detected_skills
                    }
                  </strong>
                </div>
              </div>
            </div>

            <div className="resume-match-list">
              {resumeMatches.top_matches?.map(
                (job, index) => (
                  <article
                    className="resume-match-card"
                    key={job.job_id}
                  >
                    <div className="match-score">
                      <span>
                        {String(index + 1).padStart(2, "0")}
                      </span>

                      <strong>
                        {job.match_percentage}%
                      </strong>

                      <p>compatibility</p>
                    </div>

                    <div className="match-job-details">
                      <div className="match-job-heading">
                        <div>
                          <h3>{job.title}</h3>

                          <p>
                            {job.company}
                            {job.location &&
                              ` · ${job.location}`}
                          </p>
                        </div>

                        <span className="match-role">
                          {job.role_category || "General"}
                        </span>
                      </div>

                      <div className="match-metrics">
                        <div>
                          <span>SKILL MATCH</span>

                          <strong>
                            {job.skill_match_percentage ??
                              "—"}
                            %
                          </strong>
                        </div>

                        <div>
                          <span>SKILLS MATCHED</span>

                          <strong>
                            {job.matched_skill_count ??
                              job.matched_skills?.length ??
                              0}
                            {" / "}
                            {job.detected_job_skill_count ??
                              job.job_skills?.length ??
                              0}
                          </strong>
                        </div>

                        <div>
                          <span>
                            EVIDENCE CONFIDENCE
                          </span>

                          <strong>
                            {job.evidence_confidence ??
                              "—"}
                            %
                          </strong>
                        </div>
                      </div>

                      <p className="why-match">
                        {job.why_match}
                      </p>

                      {job.evidence_confidence < 60 && (
                        <div className="evidence-warning">
                          <strong>
                            Limited evidence
                          </strong>

                          <p>
                            Only{" "}
                            {job.detected_job_skill_count ??
                              job.job_skills?.length ??
                              0}{" "}
                            recognizable job skills were
                            detected. The compatibility
                            score is therefore shown with
                            lower confidence.
                          </p>
                        </div>
                      )}

                      <div className="match-skills-grid">
                        <div>
                          <span className="skill-section-label">
                            MATCHED SKILLS
                          </span>

                          <div className="skill-tags">
                            {job.matched_skills?.length >
                            0 ? (
                              job.matched_skills.map(
                                (skill) => (
                                  <span
                                    className="skill-tag matched"
                                    key={skill}
                                  >
                                    {skill}
                                  </span>
                                )
                              )
                            ) : (
                              <span className="no-skill">
                                No detected matches
                              </span>
                            )}
                          </div>
                        </div>

                        <div>
                          <span className="skill-section-label">
                            MISSING SKILLS
                          </span>

                          <div className="skill-tags">
                            {job.missing_skills?.length >
                            0 ? (
                              job.missing_skills.map(
                                (skill) => (
                                  <span
                                    className="skill-tag missing"
                                    key={skill}
                                  >
                                    {skill}
                                  </span>
                                )
                              )
                            ) : (
                              <span className="no-skill">
                                No missing detected skills
                              </span>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className="match-card-footer">
                        <span>
                          Source:{" "}
                          {job.source || "Recruiter"}
                        </span>

                        {job.source_url && (
                          <a
                            href={job.source_url}
                            target="_blank"
                            rel="noreferrer"
                          >
                            View Job
                          </a>
                        )}
                      </div>
                    </div>
                  </article>
                )
              )}
            </div>

            <div className="match-disclaimer">
              <strong>About compatibility</strong>

              <p>
                The compatibility percentage compares
                skills detected in your resume with
                skills detected in each job description
                and adjusts the result based on the
                amount of recognizable skill evidence.
                It does not represent your probability
                of being hired.
              </p>
            </div>
          </div>
        )}
      </section>

      {/* ===================================== */}
      {/* TARGET ROLE - NEW WORKING SECTION */}
      {/* ===================================== */}

      <section
        className="target-role-section"
        id="target-role"
      >
        <div className="target-role-header">
          <div>
            <p className="target-label">
              TARGET ROLE ANALYSIS
            </p>

            <h2>
              Know what your target
              <br />
              role requires.
            </h2>
          </div>

          <p>
            Choose the role you want to pursue and
            compare your resume with skills detected
            across current job listings.
          </p>
        </div>

        {/* INPUT AREA */}

        <div className="target-input-area">
          <div className="target-input-info">
            <span>01</span>

            <h3>
              Choose your target role
            </h3>

            <p>
              Select a role and upload your resume.
              We will compare your detected skills
              with current listings for that role.
            </p>
          </div>

          <div className="target-controls">
            <label className="target-control-label">
              TARGET ROLE
            </label>

            <select
              className="target-role-select"
              value={targetRole}
              onChange={(event) => {
                setTargetRole(event.target.value);
                setTargetRoleError("");
                setTargetRoleResult(null);
              }}
            >
              <option value="">
                Select target role
              </option>

              {roles
                .filter(
                  (role) =>
                    role.toLowerCase() !== "other"
                )
                .map((role) => (
                  <option
                    key={role}
                    value={role}
                  >
                    {role}
                  </option>
                ))}
            </select>

            <label className="target-control-label">
              RESUME
            </label>

            <label
              className="target-file-label"
              htmlFor="target-resume-file"
            >
              <span>
                {targetResumeFile
                  ? targetResumeFile.name
                  : "Choose PDF resume"}
              </span>

              <strong>Browse</strong>
            </label>

            <input
              id="target-resume-file"
              className="target-file-input"
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const file = event.target.files[0];

                setTargetResumeFile(file || null);
                setTargetRoleError("");
                setTargetRoleResult(null);
              }}
            />

            <button
              className="target-analyze-button"
              onClick={handleTargetRoleAnalysis}
              disabled={targetRoleLoading}
            >
              {targetRoleLoading
                ? "Analyzing Target Role..."
                : "Analyze Target Role"}
            </button>

            {targetRoleError && (
              <p className="target-error">
                {targetRoleError}
              </p>
            )}
          </div>
        </div>

        {/* LOADING */}

        {targetRoleLoading && (
          <div className="target-loading">
            <span />

            <p>
              Comparing your resume with current{" "}
              {targetRole} listings...
            </p>
          </div>
        )}

        {/* RESULTS */}

        {targetRoleResult &&
          !targetRoleLoading && (
            <div className="target-results">

              {/* RESULT HEADER */}

              <div className="target-results-header">
                <div>
                  <p className="target-label">
                    ANALYSIS RESULT
                  </p>

                  <h3>
                    {targetRoleResult.target_role}
                  </h3>
                </div>

                <div className="target-summary">
                  <div>
                    <span>
                      CURRENT FIT
                    </span>

                    <strong>
                      {
                        targetRoleResult
                          .current_fit_percentage
                      }
                      %
                    </strong>
                  </div>

                  <div>
                    <span>
                      JOBS ANALYZED
                    </span>

                    <strong>
                      {
                        targetRoleResult
                          .jobs_analyzed
                      }
                    </strong>
                  </div>
                </div>
              </div>

              {/* MATCHED / MISSING */}

              <div className="target-skill-comparison">
                <div>
                  <span className="target-section-label">
                    MATCHED SKILLS
                  </span>

                  <h3>
                    Skills you already have
                  </h3>

                  <div className="skill-tags">
                    {targetRoleResult
                      .matched_skills?.length > 0 ? (
                      targetRoleResult
                        .matched_skills
                        .map((skill) => (
                          <span
                            className="skill-tag matched"
                            key={skill}
                          >
                            {skill}
                          </span>
                        ))
                    ) : (
                      <span className="no-skill">
                        No matching skills detected
                      </span>
                    )}
                  </div>
                </div>

                <div>
                  <span className="target-section-label">
                    SKILLS TO DEVELOP
                  </span>

                  <h3>
                    Skills currently missing
                  </h3>

                  <div className="skill-tags">
                    {targetRoleResult
                      .missing_skills?.length > 0 ? (
                      targetRoleResult
                        .missing_skills
                        .map((skill) => (
                          <span
                            className="skill-tag missing"
                            key={skill}
                          >
                            {skill}
                          </span>
                        ))
                    ) : (
                      <span className="no-skill">
                        No missing detected skills
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* MARKET SKILLS */}

              <div className="target-market-skills">
                <div className="target-market-heading">
                  <div>
                    <span>02</span>

                    <h3>
                      Important market skills
                    </h3>
                  </div>

                  <p>
                    Skills detected across current{" "}
                    {
                      targetRoleResult
                        .target_role
                    }{" "}
                    listings.
                  </p>
                </div>

                <div className="target-market-list">
                  {targetRoleResult
                    .important_market_skills
                    ?.map(
                      (
                        skill,
                        index
                      ) => (
                        <div
                          className="target-market-row"
                          key={skill.skill}
                        >
                          <span className="target-market-number">
                            {String(
                              index + 1
                            ).padStart(
                              2,
                              "0"
                            )}
                          </span>

                          <div className="target-market-name">
                            <strong>
                              {skill.skill}
                            </strong>

                            <p>
                              Detected in{" "}
                              {
                                skill.percentage_of_jobs
                              }
                              % of analyzed
                              listings
                            </p>
                          </div>

                          <strong className="target-market-count">
                            {skill.job_count}{" "}
                            {skill.job_count === 1
                              ? "job"
                              : "jobs"}
                          </strong>
                        </div>
                      )
                    )}
                </div>
              </div>

              {/* RECOMMENDATION */}

              <div className="target-recommendation">
                <span>
                  RECOMMENDATION
                </span>

                <p>
                  {
                    targetRoleResult
                      .recommendation
                  }
                </p>
              </div>

              {/* DISCLAIMER */}

              <div className="target-disclaimer">
                <strong>
                  About current fit
                </strong>

                <p>
                  Current fit compares skills
                  detected in your resume with
                  skills observed in the analyzed
                  listings for this role. Skill
                  percentages show how often a
                  skill was detected in those
                  listings. They do not represent
                  hiring probability or guarantee
                  that every employer requires
                  that skill.
                </p>
              </div>
            </div>
          )}
      </section>

      {/* ===================================== */}
{/* POST A JOB */}
{/* ===================================== */}

<section
  className="recruiter-section"
  id="post-job"
>
  <div className="job-post-header">
    <p>FOR RECRUITERS</p>

    <h2>Hiring? Post a job.</h2>

    <span>
      Add an opportunity directly to the platform.
      The job will appear with the other available listings.
    </span>
  </div>

  <form
    className="job-post-form"
    onSubmit={handlePostJob}
  >
    <div className="job-form-grid">

      <div className="job-form-field">
        <label>JOB TITLE *</label>

        <input
          type="text"
          placeholder="e.g. Junior Python Developer"
          value={jobForm.title}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              title: event.target.value,
            })
          }
        />
      </div>

      <div className="job-form-field">
        <label>COMPANY *</label>

        <input
          type="text"
          placeholder="e.g. Demo Tech"
          value={jobForm.company}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              company: event.target.value,
            })
          }
        />
      </div>

      <div className="job-form-field">
        <label>RECRUITER EMAIL *</label>
        <input
           type="email"
           placeholder="e.g. hr@company.com"
           value={jobForm.recruiter_email}
           onChange={(event) =>
              setJobForm({
                ...jobForm,
                recruiter_email: event.target.value,
              })
           }
           required
          />
      </div>

      <div className="job-form-field">
        <label>LOCATION</label>

        <input
          type="text"
          placeholder="e.g. Noida"
          value={jobForm.location}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              location: event.target.value,
            })
          }
        />
      </div>

      <div className="job-form-field">
        <label>SKILLS</label>

        <input
          type="text"
          placeholder="e.g. Python, FastAPI, PostgreSQL, Git"
          value={jobForm.skills}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              skills: event.target.value,
            })
          }
        />
      </div>

      <div className="job-form-field">
        <label>MINIMUM SALARY</label>

        <input
          type="number"
          min="0"
          placeholder="e.g. 400000"
          value={jobForm.salary_min}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              salary_min: event.target.value,
            })
          }
        />
      </div>

      <div className="job-form-field">
        <label>MAXIMUM SALARY</label>

        <input
          type="number"
          min="0"
          placeholder="e.g. 700000"
          value={jobForm.salary_max}
          onChange={(event) =>
            setJobForm({
              ...jobForm,
              salary_max: event.target.value,
            })
          }
        />
      </div>

    </div>

    <div className="job-form-field job-description-field">
      <label>JOB DESCRIPTION *</label>

      <textarea
        rows="6"
        placeholder="Describe the role, responsibilities and required skills..."
        value={jobForm.description}
        onChange={(event) =>
          setJobForm({
            ...jobForm,
            description: event.target.value,
          })
        }
      />
    </div>

    <div className="job-post-bottom">

      <div className="job-post-status">
        {jobPostMessage && (
          <p className="job-post-success">
            {jobPostMessage}
          </p>
        )}

        {jobPostError && (
          <p className="job-post-error">
            {jobPostError}
          </p>
        )}
      </div>

      <button
        type="submit"
        className="job-post-button"
        disabled={jobPosting}
      >
        {jobPosting ? "Posting Job..." : "Post Job"}
      </button>

    </div>
  </form>
</section>

{/* ===================================== */}
{/* JOB DETAILS MODAL */}
{/* ===================================== */}

{selectedJobDetails && (
  <div
    className="job-modal-overlay"
    onClick={() => setSelectedJobDetails(null)}
  >
    <div
      className="job-modal"
      onClick={(event) => event.stopPropagation()}
    >
      <div className="job-modal-top">
        <div>
          <p className="job-modal-label">JOB DETAILS</p>

          <h2>{selectedJobDetails.title}</h2>

          <span>
            {selectedJobDetails.company}

            {selectedJobDetails.location &&
              ` · ${selectedJobDetails.location}`}
          </span>
        </div>

        <button
          type="button"
          className="job-modal-close"
          onClick={() => setSelectedJobDetails(null)}
        >
          Close
        </button>
      </div>

      <div className="job-modal-info">
        <div>
          <span>ROLE</span>
          <strong>
            {selectedJobDetails.role_category || "General"}
          </strong>
        </div>

        <div>
          <span>SOURCE</span>
          <strong>
            {selectedJobDetails.source || "Recruiter"}
          </strong>
        </div>

        <div>
          <span>LOCATION</span>
          <strong>
            {selectedJobDetails.location || "Not specified"}
          </strong>
        </div>
      </div>

      {selectedJobDetails.skills && (
        <div className="job-modal-section">
          <span className="job-modal-section-label">
            SKILLS
          </span>

          <p>{selectedJobDetails.skills}</p>
        </div>
      )}

      <div className="job-modal-section">
        <span className="job-modal-section-label">
          SALARY
        </span>

        <p>
          {selectedJobDetails.salary_min ||
          selectedJobDetails.salary_max ? (
            <>
              {selectedJobDetails.salary_min > 0
                ? `₹${Number(
                    selectedJobDetails.salary_min
                  ).toLocaleString("en-IN")}`
                : "Not specified"}

              {" – "}

              {selectedJobDetails.salary_max > 0
                ? `₹${Number(
                    selectedJobDetails.salary_max
                  ).toLocaleString("en-IN")}`
                : "Not specified"}
            </>
          ) : (
            "Not specified"
          )}
        </p>
      </div>

      <div className="job-modal-section">
        <span className="job-modal-section-label">
          JOB DESCRIPTION
        </span>

        <p>
          {selectedJobDetails.description ||
            "No description available."}
        </p>
      </div>
      {/* APPLY VIA EMAIL - ONLY FOR RECRUITER JOBS */}
      {selectedJobDetails.source === "recruiter" &&
       selectedJobDetails.recruiter_email && (
         <div className="job-modal-section">
           <span className="job-modal-section-label">
             APPLY FOR THIS JOB
           </span>

           <p>
             Recruiter Email:{" "}
             <strong>
               {selectedJobDetails.recruiter_email}
             </strong>
           </p>

           <a
             className="job-apply-email"
             href={`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(
               selectedJobDetails.recruiter_email
             )}&su=${encodeURIComponent(
              `Application for ${selectedJobDetails.title} - ${selectedJobDetails.company}`
            )}`}
            target="_blank"
            rel="noreferrer"
            >
             Apply via Email
            </a>
          </div>
        )}

       {/* APPLY ON SOURCE - FOR EXTERNAL JOBS */}
       {selectedJobDetails.source !== "recruiter" &&
         selectedJobDetails.source_url && (
           <div className="job-modal-section">
             <span className="job-modal-section-label">
               APPLY FOR THIS JOB
              </span>

              <p>
               Continue to the original job source to view the listing
               and application details.
              </p>

              <a
               className="job-apply-email"
               href={selectedJobDetails.source_url}
               target="_blank"
               rel="noreferrer"
              >
               Apply on Source
              </a>
              
              </div>
              
              )}
              </div>
              </div>
              )}
              <button
                type="button"
                className="back-to-top"
                onClick={() =>
                 window.scrollTo({
                   top: 0,
                   behavior: "smooth",
                 })
                }
                aria-label="Back to top"
              >
               ↑
              </button>
        

      {/* FOOTER */}

      <footer>
        <p>Job Market Intelligence</p>

        <span>
          Data-driven job discovery
          and resume matching.
        </span>
      </footer>
    </div>
  );
}

export default App;