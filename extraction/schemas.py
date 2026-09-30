"""
extraction/schemas.py
Pydantic models for structured LLM output from resume extraction.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class WorkExperience(BaseModel):
    """Single work experience entry."""
    role: str = Field(description="Job title / role (e.g., 'Assistant Professor', 'Software Engineer')")
    organization: str = Field(description="Organization / company / institution name")
    duration: str = Field(description="Duration in that role (e.g., '2019-2022', '3 years')")
    responsibilities: Optional[str] = Field(default=None, description="Brief summary of responsibilities")


class Education(BaseModel):
    """Single education entry."""
    degree: str = Field(description="Degree name (e.g., 'Ph.D.', 'M.Tech.', 'B.E.')")
    specialization: str = Field(description="Branch / specialization / major")
    institution: str = Field(description="University or college name")
    year_of_completion: Optional[str] = Field(default=None, description="Year of passing / completion")
    percentage_or_cgpa: Optional[str] = Field(default=None, description="Marks percentage or CGPA (e.g., '75%', '8.5 CGPA')")
    classification: Optional[str] = Field(
        default=None,
        description="Grade classification (e.g., 'First Class', 'Distinction', 'Second Class')"
    )


class Publication(BaseModel):
    """Single research publication entry."""
    title: Optional[str] = Field(default=None, description="Title of the paper")
    journal_or_conference: Optional[str] = Field(default=None, description="Journal or conference name")
    index: Optional[str] = Field(
        default=None,
        description="Indexing (e.g., 'SCI', 'SCIE', 'Scopus', 'UGC-Care', 'ABDC', 'Conference')"
    )
    year: Optional[str] = Field(default=None, description="Year of publication")


class ResumeDetails(BaseModel):
    """
    Comprehensive structured Key-Value representation of a candidate's resume.
    Designed for AICTE faculty eligibility evaluation.
    """

    # ── Personal Info ──
    full_name: str = Field(description="Full name of the candidate")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")

    # ── Education ──
    education: List[Education] = Field(description="All educational qualifications, from highest to lowest")
    highest_degree: str = Field(
        description="Highest degree held (e.g., 'Ph.D.', 'M.Tech.', 'M.Pharm.')"
    )
    phd_completed: bool = Field(description="Whether Ph.D. has been completed (True/False)")
    phd_discipline: Optional[str] = Field(default=None, description="Ph.D. discipline if completed")
    phd_year: Optional[str] = Field(default=None, description="Year Ph.D. was awarded")
    first_class_at_bachelor: Optional[bool] = Field(
        default=None, description="Whether First Class (60%+) was achieved at Bachelor's level"
    )
    first_class_at_master: Optional[bool] = Field(
        default=None, description="Whether First Class (60%+) was achieved at Master's level"
    )

    # ── Experience ──
    total_experience_years: Optional[str] = Field(
        default="0",
        description="Total years of experience across all roles (e.g., '8 years', '10+ years')"
    )
    teaching_experience_years: Optional[str] = Field(
        default="0",
        description="Teaching-specific experience in years (e.g., '5 years')"
    )
    industry_experience_years: Optional[str] = Field(
        default="0",
        description="Industry / corporate experience in years (e.g., '3 years', 'None')"
    )
    research_experience_years: Optional[str] = Field(
        default="0",
        description="Research-specific experience in years (e.g., '2 years', 'None')"
    )
    post_phd_experience_years: Optional[str] = Field(
        default=None, description="Years of experience after Ph.D. completion (if applicable)"
    )
    work_history: List[WorkExperience] = Field(
        description="Detailed list of all work positions held"
    )

    # ── Publications ──
    total_publications_count: int = Field(
        description="Total number of research publications (journal + conference)"
    )
    sci_scie_scopus_publications_count: int = Field(
        description="Number of publications in SCI / SCIE / Scopus indexed journals"
    )
    publications: List[Publication] = Field(
        default_factory=list,
        description="List of individual publication entries"
    )
    books_or_book_chapters_count: int = Field(
        default=0,
        description="Number of books or book chapters published"
    )

    # ── Qualifications & Tests ──
    net_cleared: Optional[bool] = Field(
        default=None, description="Whether UGC-NET / SLET / SET has been cleared"
    )
    certifications: List[str] = Field(
        default_factory=list,
        description="List of professional certifications or achievements"
    )
    professional_registrations: List[str] = Field(
        default_factory=list,
        description="Professional body registrations (e.g., 'COA', 'IEEE Member')"
    )

    # ── Skills & Domain ──
    core_discipline: str = Field(
        description="Primary academic discipline (e.g., 'Computer Science and Engineering', 'Pharmacy')"
    )
    technical_skills: List[str] = Field(
        default_factory=list, description="Technical skills and tools"
    )

    # ── Administrative Experience ──
    administrative_experience_years: str = Field(
        default="0",
        description="Years in administrative or leadership roles (e.g., HOD, Principal)"
    )

    # ── Catch-all ──
    other_details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any other relevant Key-Value details from the resume not captured above"
    )
