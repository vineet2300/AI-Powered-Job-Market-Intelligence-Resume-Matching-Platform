from backend.services.skill_extractor import extract_skills


# =========================================================
# EVIDENCE CONFIDENCE
# =========================================================

def calculate_evidence_confidence(detected_skill_count):
    """
    Measures how much skill evidence is available
    in the job description.

    This is NOT a hiring probability.

    More detected skills = more reliable comparison.
    """

    if detected_skill_count <= 0:
        return 0.0

    if detected_skill_count == 1:
        return 0.35

    if detected_skill_count == 2:
        return 0.50

    if detected_skill_count == 3:
        return 0.65

    if detected_skill_count == 4:
        return 0.80

    if detected_skill_count == 5:
        return 0.90

    return 1.0


# =========================================================
# MATCH RESUME WITH JOB
# =========================================================

def match_resume_with_job(
    resume_text,
    job_description,
    job_title=""
):

    # -----------------------------------------------------
    # EXTRACT SKILLS
    # -----------------------------------------------------

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    title_skills = set(
        extract_skills(job_title)
    )


    # -----------------------------------------------------
    # NO DETECTABLE JOB SKILLS
    # -----------------------------------------------------

    if not job_skills:

        return {
            "match_percentage": 0,
            "skill_match_percentage": 0,
            "evidence_confidence": 0,
            "matched_skill_count": 0,
            "detected_job_skill_count": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "why_match": (
                "Not enough recognizable skills "
                "were found in the job description "
                "to calculate a reliable "
                "compatibility score."
            )
        }


    # -----------------------------------------------------
    # MATCHED AND MISSING SKILLS
    # -----------------------------------------------------

    matched_skills = (
        resume_skills.intersection(
            job_skills
        )
    )

    missing_skills = (
        job_skills.difference(
            resume_skills
        )
    )

    matched_count = len(
        matched_skills
    )

    detected_count = len(
        job_skills
    )


    # -----------------------------------------------------
    # RAW SKILL MATCH
    # -----------------------------------------------------

    skill_match_percentage = (
        matched_count
        / detected_count
    ) * 100


    # -----------------------------------------------------
    # EVIDENCE CONFIDENCE
    # -----------------------------------------------------

    evidence_confidence = (
        calculate_evidence_confidence(
            detected_count
        )
    )


    # -----------------------------------------------------
    # EVIDENCE-AWARE SKILL SCORE
    # -----------------------------------------------------
    #
    # Example:
    #
    # 1/1 skills:
    # 100% raw match but low evidence.
    #
    # 5/5 skills:
    # 100% raw match with much stronger evidence.
    #
    # This prevents one detected skill from creating
    # an unrealistically high compatibility score.
    # -----------------------------------------------------

    evidence_adjusted_score = (
        skill_match_percentage
        * evidence_confidence
    )


    # -----------------------------------------------------
    # ROLE / TITLE RELEVANCE
    # -----------------------------------------------------

    role_score = None

    if title_skills:

        title_matches = (
            resume_skills.intersection(
                title_skills
            )
        )

        role_score = (
            len(title_matches)
            / len(title_skills)
        ) * 100


    # -----------------------------------------------------
    # FINAL COMPATIBILITY SCORE
    # -----------------------------------------------------
    #
    # 90% = skill/evidence score
    # 10% = title relevance
    #
    # Title has only a small influence so that it cannot
    # make a weak skill comparison look like a strong match.
    # -----------------------------------------------------

    if role_score is not None:

        final_score = (
            evidence_adjusted_score * 0.90
            +
            role_score * 0.10
        )

    else:

        final_score = (
            evidence_adjusted_score
        )


    final_score = round(
        min(
            max(
                final_score,
                0
            ),
            100
        ),
        2
    )


    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    if matched_count == 0:

        why_match = (
            f"No directly matching skills were "
            f"detected out of "
            f"{detected_count} recognizable "
            f"job skills."
        )

    else:

        why_match = (
            f"Your resume matches "
            f"{matched_count} of "
            f"{detected_count} detected "
            f"job skills."
        )


        # Missing skills
        if missing_skills:

            missing_count = len(
                missing_skills
            )

            if missing_count == 1:

                why_match += (
                    " 1 detected skill is "
                    "currently missing from "
                    "your resume."
                )

            else:

                why_match += (
                    f" {missing_count} detected "
                    f"skills are currently "
                    f"missing from your resume."
                )

        else:

            why_match += (
                " No missing skills were "
                "detected from the available "
                "job description."
            )


        # Low evidence warning
        if detected_count <= 2:

            why_match += (
                " However, only a small "
                "number of recognizable skills "
                "were available in the job "
                "description, so this match "
                "has lower evidence confidence."
            )


    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return {

        "match_percentage":
            final_score,

        "skill_match_percentage":
            round(
                skill_match_percentage,
                2
            ),

        "evidence_confidence":
            round(
                evidence_confidence * 100,
                2
            ),

        "matched_skill_count":
            matched_count,

        "detected_job_skill_count":
            detected_count,

        "matched_skills":
            sorted(
                matched_skills
            ),

        "missing_skills":
            sorted(
                missing_skills
            ),

        "resume_skills":
            sorted(
                resume_skills
            ),

        "job_skills":
            sorted(
                job_skills
            ),

        "why_match":
            why_match
    }


# =========================================================
# LOCAL TEST
# =========================================================

if __name__ == "__main__":

    resume = """
    Python developer with knowledge of
    SQL, Pandas, NumPy, HTML, CSS and Git.
    """

    job = """
    Looking for a Python developer with
    Python, SQL, Pandas, Power BI and Excel.
    """

    result = match_resume_with_job(
        resume,
        job,
        job_title="Python Developer"
    )


    print("\nCompatibility Score:")
    print(
        result["match_percentage"]
    )


    print("\nSkill Match:")
    print(
        result["skill_match_percentage"]
    )


    print("\nEvidence Confidence:")
    print(
        result["evidence_confidence"]
    )


    print("\nMatched Skill Count:")
    print(
        result["matched_skill_count"]
    )


    print("\nDetected Job Skill Count:")
    print(
        result["detected_job_skill_count"]
    )


    print("\nMatched Skills:")
    print(
        result["matched_skills"]
    )


    print("\nMissing Skills:")
    print(
        result["missing_skills"]
    )


    print("\nWhy Match:")
    print(
        result["why_match"]
    )