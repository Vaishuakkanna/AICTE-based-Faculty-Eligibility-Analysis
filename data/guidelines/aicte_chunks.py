"""
data/guidelines/aicte_chunks.py
Pre-defined MEANINGFUL chunks — one chunk per (role x discipline).
Keywords are NOT hardcoded here. KeyBERT generates them at ingestion time.

Chunk boundary rule:
  One logical unit of eligibility = one chunk.
  e.g.  "Engineering & Technology — Associate Professor" = 1 chunk
        "Computer Science / IT / MCA — Professor"        = 1 chunk
        "CAS: Stage 1 → Stage 2"                         = 1 chunk
"""

AICTE_CHUNKS = [

    # =========================================================
    # DEGREE LEVEL — ENGINEERING & TECHNOLOGY
    # =========================================================
    {
        "id": "eng_asst_prof",
        "discipline": "Engineering and Technology",
        "position": "Assistant Professor",
        "institution_type": "degree",
        "content": (
            "ASSISTANT PROFESSOR — Engineering and Technology (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class (60% or above) in Bachelor's degree AND First Class in Master's degree "
            "in the relevant branch of Engineering or Technology.\n"
            "2. OR: First Class Master's degree in the relevant discipline alone is acceptable.\n"
            "3. PhD is desirable but NOT mandatory for initial appointment.\n"
            "4. Candidates with PhD in the relevant subject may be exempted from the First Class "
            "requirement at Bachelor's or Master's level.\n"
            "5. Candidates without PhD must clear NET (National Eligibility Test) or equivalent.\n"
            "6. NET exemption: PhD awarded through a regular UGC 2009 compliant program exempts from NET.\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 0,
            "min_publications": 0,
            "pay_level": "Level 10",
        },
    },
    {
        "id": "eng_assoc_prof",
        "discipline": "Engineering and Technology",
        "position": "Associate Professor",
        "institution_type": "degree",
        "content": (
            "ASSOCIATE PROFESSOR — Engineering and Technology (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in the relevant discipline — MANDATORY.\n"
            "2. First Class (60% or above) at Bachelor's and Master's degree levels in the relevant branch.\n"
            "3. Minimum 8 years of experience in teaching or research or industry, "
            "of which at least 2 years must be POST-PhD.\n"
            "4. At least 2 research publications in SCI or SCIE or Scopus indexed journals.\n"
            "Pay Band: Level 13A — Rs. 1,31,400 to 2,04,700 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 8,
            "min_post_phd_experience_years": 2,
            "min_publications": 2,
            "publication_index": "SCI/SCIE/Scopus",
            "pay_level": "Level 13A",
        },
    },
    {
        "id": "eng_professor",
        "discipline": "Engineering and Technology",
        "position": "Professor",
        "institution_type": "degree",
        "content": (
            "PROFESSOR — Engineering and Technology (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in the relevant discipline — MANDATORY.\n"
            "2. First Class (60% or above) at Bachelor's and Master's degree levels in the relevant branch.\n"
            "3. Minimum 10 years of experience in teaching or research or industry.\n"
            "4. At least 6 research publications in SCI or SCIE or Scopus indexed journals.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 10,
            "min_publications": 6,
            "publication_index": "SCI/SCIE/Scopus",
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # DEGREE LEVEL — COMPUTER SCIENCE / IT / MCA
    # =========================================================
    {
        "id": "cs_asst_prof",
        "discipline": "Computer Science / IT / MCA",
        "position": "Assistant Professor",
        "institution_type": "degree",
        "content": (
            "ASSISTANT PROFESSOR — Computer Science / Information Technology / MCA (Degree Level, AICTE 2019 + Amendment 2022)\n"
            "Minimum Qualifications:\n"
            "1. First Class Master's degree in Computer Applications (MCA) or Computer Science or Information Technology.\n"
            "2. OR: First Class B.E./B.Tech. in Computer Engineering or CSE or IT "
            "AND First Class M.E./M.Tech. in relevant discipline.\n"
            "3. PhD in MCA or Computer Science is desirable but not mandatory.\n"
            "4. Candidates without PhD must clear NET or equivalent.\n"
            "5. Gazette Notification XIII (07.11.2022): MCA holders with PhD are now eligible "
            "for Associate Professor and Professor level appointments (not just Assistant Professor).\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 + Gazette XIII 2022",
            "phd_mandatory": False,
            "min_experience_years": 0,
            "min_publications": 0,
            "pay_level": "Level 10",
            "amendment_2022": True,
        },
    },
    {
        "id": "cs_assoc_prof",
        "discipline": "Computer Science / IT / MCA",
        "position": "Associate Professor",
        "institution_type": "degree",
        "content": (
            "ASSOCIATE PROFESSOR — Computer Science / IT / MCA (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Computer Science or IT or Computer Applications — MANDATORY.\n"
            "2. First Class (60% or above) at both Bachelor's and Master's levels.\n"
            "3. Minimum 8 years of teaching or research or industry experience.\n"
            "4. Minimum 2 publications in SCI or SCIE or Scopus indexed journals.\n"
            "Pay Band: Level 13A — Rs. 1,31,400 to 2,04,700 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 8,
            "min_publications": 2,
            "publication_index": "SCI/SCIE/Scopus",
            "pay_level": "Level 13A",
        },
    },
    {
        "id": "cs_professor",
        "discipline": "Computer Science / IT / MCA",
        "position": "Professor",
        "institution_type": "degree",
        "content": (
            "PROFESSOR — Computer Science / IT / MCA (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in relevant discipline (Computer Science or IT or MCA) — MANDATORY.\n"
            "2. Minimum 10 years of teaching or research or industry experience.\n"
            "3. At least 6 publications in SCI or SCIE or Scopus indexed journals.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 10,
            "min_publications": 6,
            "publication_index": "SCI/SCIE/Scopus",
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # DEGREE LEVEL — MANAGEMENT / MBA
    # =========================================================
    {
        "id": "mgmt_asst_prof",
        "discipline": "Management / MBA",
        "position": "Assistant Professor",
        "institution_type": "degree",
        "content": (
            "ASSISTANT PROFESSOR — Management / MBA (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class Master's Degree in Business Administration (MBA) or equivalent management qualification.\n"
            "2. OR: First Class CA or ICWA or CS combined with First Class MBA or equivalent.\n"
            "3. PhD in Management or Business Administration is desirable but not mandatory.\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 0,
            "min_publications": 0,
            "pay_level": "Level 10",
        },
    },
    {
        "id": "mgmt_assoc_prof",
        "discipline": "Management / MBA",
        "position": "Associate Professor",
        "institution_type": "degree",
        "content": (
            "ASSOCIATE PROFESSOR — Management / MBA (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Management or Business Administration or related discipline — MANDATORY.\n"
            "2. 8 years of experience in teaching or research or industry.\n"
            "3. At least 2 publications in SCI or SCIE or Scopus or ABDC or ABS or UGC-Care listed journals.\n"
            "Pay Band: Level 13A — Rs. 1,31,400 to 2,04,700 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 8,
            "min_publications": 2,
            "publication_index": "SCI/SCIE/Scopus/ABDC/ABS/UGC-Care",
            "pay_level": "Level 13A",
        },
    },
    {
        "id": "mgmt_professor",
        "discipline": "Management / MBA",
        "position": "Professor",
        "institution_type": "degree",
        "content": (
            "PROFESSOR — Management / MBA (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in relevant discipline (Management or Business Administration) — MANDATORY.\n"
            "2. 10 years of total teaching or research or industry experience.\n"
            "3. At least 6 publications in SCI or SCIE or Scopus or ABDC or ABS or UGC-Care listed journals.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 10,
            "min_publications": 6,
            "publication_index": "SCI/SCIE/Scopus/ABDC/ABS/UGC-Care",
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # DEGREE LEVEL — PHARMACY
    # =========================================================
    {
        "id": "pharma_asst_prof",
        "discipline": "Pharmacy",
        "position": "Assistant Professor",
        "institution_type": "degree",
        "content": (
            "ASSISTANT PROFESSOR — Pharmacy (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class (60% or above) Master's degree in Pharmacy (M.Pharm) in the relevant specialization.\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 0,
            "min_publications": 0,
            "pay_level": "Level 10",
        },
    },
    {
        "id": "pharma_assoc_prof",
        "discipline": "Pharmacy",
        "position": "Associate Professor",
        "institution_type": "degree",
        "content": (
            "ASSOCIATE PROFESSOR — Pharmacy (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Pharmacy (relevant specialization) — MANDATORY.\n"
            "2. 8 years of teaching or research or industry experience.\n"
            "3. Minimum 2 publications in indexed journals.\n"
            "Pay Band: Level 13A — Rs. 1,31,400 to 2,04,700 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 8,
            "min_publications": 2,
            "pay_level": "Level 13A",
        },
    },
    {
        "id": "pharma_professor",
        "discipline": "Pharmacy",
        "position": "Professor",
        "institution_type": "degree",
        "content": (
            "PROFESSOR — Pharmacy (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Pharmacy — MANDATORY.\n"
            "2. 10 years of teaching or research or industry experience.\n"
            "3. At least 6 publications in indexed journals.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": True,
            "min_experience_years": 10,
            "min_publications": 6,
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # DEGREE LEVEL — ARCHITECTURE
    # =========================================================
    {
        "id": "arch_asst_prof",
        "discipline": "Architecture",
        "position": "Assistant Professor",
        "institution_type": "degree",
        "content": (
            "ASSISTANT PROFESSOR — Architecture (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class Bachelor's degree in Architecture (B.Arch).\n"
            "2. Must be registered with the Council of Architecture (COA).\n"
            "3. Master's degree in Architecture or Planning or equivalent is preferred.\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "coa_registration_required": True,
            "min_experience_years": 0,
            "min_publications": 0,
            "pay_level": "Level 10",
        },
    },
    {
        "id": "arch_assoc_prof",
        "discipline": "Architecture",
        "position": "Associate Professor",
        "institution_type": "degree",
        "content": (
            "ASSOCIATE PROFESSOR — Architecture (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Architecture or Planning, OR\n"
            "2. Master's degree in Architecture PLUS 8 years of relevant teaching or research or industry experience.\n"
            "3. At least 2 publications or significant recognized design works.\n"
            "Pay Band: Level 13A — Rs. 1,31,400 to 2,04,700 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 8,
            "min_publications": 2,
            "pay_level": "Level 13A",
        },
    },
    {
        "id": "arch_professor",
        "discipline": "Architecture",
        "position": "Professor",
        "institution_type": "degree",
        "content": (
            "PROFESSOR — Architecture (Degree Level, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. PhD in Architecture or Planning, OR extensive professional accomplishment recognized nationally.\n"
            "2. 10 years of teaching or research or industry experience.\n"
            "3. Significant publications or contributions to the field of Architecture.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 10,
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # DIPLOMA LEVEL
    # =========================================================
    {
        "id": "diploma_lecturer",
        "discipline": "Engineering and Technology",
        "position": "Lecturer",
        "institution_type": "diploma",
        "content": (
            "LECTURER — Diploma Level Institutions (equivalent to Assistant Professor, AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class Bachelor's Degree in Engineering or Technology in the relevant discipline, OR\n"
            "2. First Class Diploma in the relevant discipline with at least 2 years of "
            "industry or teaching experience.\n"
            "Pay Band: Level 10 — Rs. 57,700 to 1,82,400 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE Diploma 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 0,
            "pay_level": "Level 10",
        },
    },
    {
        "id": "diploma_senior_lecturer_hod",
        "discipline": "Engineering and Technology",
        "position": "Senior Lecturer / Head of Department",
        "institution_type": "diploma",
        "content": (
            "SENIOR LECTURER / HEAD OF DEPARTMENT — Diploma Level Institutions (AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class Bachelor's Degree in Engineering or Technology.\n"
            "2. Minimum 5 years of teaching or industry experience.\n"
            "3. Master's degree in relevant discipline is preferred.\n"
            "Pay Band: Level 11 — Rs. 68,900 to 2,05,500 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE Diploma 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 5,
            "pay_level": "Level 11",
        },
    },
    {
        "id": "diploma_principal",
        "discipline": "Engineering and Technology",
        "position": "Principal",
        "institution_type": "diploma",
        "content": (
            "PRINCIPAL — Diploma Level Institutions (AICTE 2019 / 7th CPC)\n"
            "Minimum Qualifications:\n"
            "1. First Class Bachelor's Degree in Engineering or Technology.\n"
            "2. Minimum 15 years of experience including at least 5 years in administration.\n"
            "3. Master's degree in relevant discipline — REQUIRED.\n"
            "4. PhD is preferred.\n"
            "Pay Band: Level 14 — Rs. 1,44,200 to 2,18,200 as per 7th CPC."
        ),
        "metadata": {
            "regulation": "AICTE Diploma 2019 (7th CPC)",
            "phd_mandatory": False,
            "min_experience_years": 15,
            "min_admin_experience_years": 5,
            "pay_level": "Level 14",
        },
    },

    # =========================================================
    # CAREER ADVANCEMENT SCHEME (CAS)
    # =========================================================
    {
        "id": "cas_stage1_to_stage2",
        "discipline": "All",
        "position": "Assistant Professor (Stage 1 to Stage 2)",
        "institution_type": "degree",
        "content": (
            "CAREER ADVANCEMENT SCHEME (CAS) — Assistant Professor Stage 1 to Stage 2\n"
            "Source: AICTE Gazette Notifications V, VI (2012), VII (2016), XI, XII (2020)\n"
            "Criteria:\n"
            "1. Minimum 4 years of continuous service as Assistant Professor at Stage 1.\n"
            "2. Satisfactory performance in Annual Performance Index (API) scoring.\n"
            "3. All prescribed minimum API score requirements must be met."
        ),
        "metadata": {
            "regulation": "AICTE CAS 2012/2016/2020",
            "cas_transition": "Stage 1 to Stage 2",
            "min_service_years": 4,
            "api_required": True,
        },
    },
    {
        "id": "cas_stage2_to_stage3",
        "discipline": "All",
        "position": "Assistant Professor (Stage 2 to Stage 3)",
        "institution_type": "degree",
        "content": (
            "CAREER ADVANCEMENT SCHEME (CAS) — Assistant Professor Stage 2 to Stage 3\n"
            "Source: AICTE Gazette Notifications V, VI (2012), VII (2016), XI, XII (2020)\n"
            "Criteria:\n"
            "1. Minimum 3 additional years of service as Assistant Professor at Stage 2.\n"
            "2. Minimum prescribed API score requirements met.\n"
            "3. At least one published paper or significant academic contribution required."
        ),
        "metadata": {
            "regulation": "AICTE CAS 2012/2016/2020",
            "cas_transition": "Stage 2 to Stage 3",
            "min_service_years": 3,
            "api_required": True,
            "publication_required": True,
        },
    },
    {
        "id": "cas_stage3_to_assoc_prof",
        "discipline": "All",
        "position": "Assistant Professor Stage 3 to Associate Professor",
        "institution_type": "degree",
        "content": (
            "CAREER ADVANCEMENT SCHEME (CAS) — Assistant Professor Stage 3 to Associate Professor\n"
            "Source: AICTE Gazette Notifications V, VI (2012), VII (2016), XI, XII (2020)\n"
            "Criteria:\n"
            "1. Completion of PhD — MANDATORY for this CAS transition if not already completed.\n"
            "2. Minimum 3 years of service as Assistant Professor at Stage 3.\n"
            "3. Prescribed API score requirements must be satisfied.\n"
            "4. Interview or selection process by a duly constituted selection committee."
        ),
        "metadata": {
            "regulation": "AICTE CAS 2012/2016/2020",
            "cas_transition": "Stage 3 to Associate Professor",
            "min_service_years": 3,
            "phd_mandatory": True,
            "api_required": True,
            "interview_required": True,
        },
    },
    {
        "id": "cas_assoc_prof_to_professor",
        "discipline": "All",
        "position": "Associate Professor to Professor",
        "institution_type": "degree",
        "content": (
            "CAREER ADVANCEMENT SCHEME (CAS) — Associate Professor to Professor\n"
            "Source: AICTE Gazette Notifications V, VI (2012), VII (2016), XI, XII (2020)\n"
            "Criteria:\n"
            "1. Minimum 3 years of service as Associate Professor.\n"
            "2. Research publications as per AICTE prescribed norms must be met.\n"
            "3. Interview by a duly constituted selection committee."
        ),
        "metadata": {
            "regulation": "AICTE CAS 2012/2016/2020",
            "cas_transition": "Associate Professor to Professor",
            "min_service_years": 3,
            "publication_required": True,
            "interview_required": True,
        },
    },

    # =========================================================
    # NON-TEACHING STAFF
    # =========================================================
    {
        "id": "non_teaching_librarian",
        "discipline": "Library Science",
        "position": "Librarian",
        "institution_type": "degree and diploma",
        "content": (
            "LIBRARIAN — Non-Teaching Staff (AICTE 2019)\n"
            "Minimum Qualifications:\n"
            "1. First Class (60% or above) Master's in Library and Information Science (MLIS or M.Lib.I.Sc.).\n"
            "2. NET or SLET or SET qualification is desirable.\n"
            "3. Minimum 2 years of professional library experience required for Senior Librarian."
        ),
        "metadata": {
            "regulation": "AICTE 2019",
            "staff_type": "non-teaching",
            "min_experience_years": 2,
        },
    },
    {
        "id": "non_teaching_physical_edu",
        "discipline": "Physical Education",
        "position": "Physical Education Director",
        "institution_type": "degree and diploma",
        "content": (
            "PHYSICAL EDUCATION DIRECTOR — Non-Teaching Staff (AICTE 2019)\n"
            "Minimum Qualifications:\n"
            "1. First Class Master's degree in Physical Education (M.P.Ed.).\n"
            "2. NET or SLET or SET qualification is desirable.\n"
            "3. National or International representation in sports is an additional advantage."
        ),
        "metadata": {
            "regulation": "AICTE 2019",
            "staff_type": "non-teaching",
        },
    },
    {
        "id": "non_teaching_tpo",
        "discipline": "Management / Engineering",
        "position": "Training and Placement Officer",
        "institution_type": "degree and diploma",
        "content": (
            "TRAINING AND PLACEMENT OFFICER (TPO) — Non-Teaching Staff (AICTE 2019)\n"
            "Minimum Qualifications:\n"
            "1. First Class MBA or equivalent management qualification, OR\n"
            "2. First Class Engineering degree with relevant industry or placement experience.\n"
            "3. Experience in corporate relations and placement activities is mandatory."
        ),
        "metadata": {
            "regulation": "AICTE 2019",
            "staff_type": "non-teaching",
        },
    },

    # =========================================================
    # KEY CLARIFICATIONS — Split into 4 focused chunks
    # =========================================================
    {
        "id": "clarification_first_class_phd_net",
        "discipline": "All",
        "position": "General",
        "institution_type": "degree and diploma",
        "content": (
            "AICTE KEY CLARIFICATIONS — First Class Definition and PhD and NET Requirements\n"
            "First Class Definition: 60% or above marks (or equivalent CGPA or grade) at graduate "
            "and postgraduate levels. For SC or ST or OBC or PwD candidates, relaxation in minimum "
            "marks is applicable per Government of India reservation norms.\n"
            "PhD Requirement: PhD is MANDATORY for Associate Professor and Professor. "
            "For Assistant Professor without PhD, clearing NET or SLET or SET is required.\n"
            "NET Exemption: Candidates whose PhD was awarded through a regular program as per "
            "UGC 2009 regulations are EXEMPTED from NET or SLET for Assistant Professor appointments."
        ),
        "metadata": {
            "regulation": "AICTE 2019",
            "type": "clarification",
        },
    },
    {
        "id": "clarification_industry_experience",
        "discipline": "All",
        "position": "General",
        "institution_type": "degree and diploma",
        "content": (
            "AICTE KEY CLARIFICATION — Industry Experience Credit\n"
            "Each year of work experience in a reputed industry or R&D organization or Government "
            "organization at an appropriate level is counted as EQUIVALENT to one year of teaching "
            "experience for the purpose of direct recruitment to faculty positions.\n"
            "Relevant industry experience may be counted towards the teaching experience requirement "
            "at the discretion of the appointing institution, as per AICTE norms."
        ),
        "metadata": {
            "regulation": "AICTE 2019",
            "type": "clarification",
        },
    },
    {
        "id": "clarification_publications_api",
        "discipline": "All",
        "position": "General",
        "institution_type": "degree and diploma",
        "content": (
            "AICTE KEY CLARIFICATIONS — Publications Policy and API Scoring\n"
            "Publications:\n"
            "- Engineering disciplines: journals must be indexed in SCI or SCIE or Scopus.\n"
            "- Management: ABDC or ABS or UGC-Care listed journals also acceptable.\n"
            "- Books by reputed publishers and book chapters are counted separately from journals.\n"
            "- Conference papers may count for API scoring but do NOT substitute journal publications.\n"
            "API Scoring (CAS Regulations 2012 revised 2016):\n"
            "- Category I: Teaching, Learning and Evaluation Activities.\n"
            "- Category II: Co-curricular, Extracurricular and Professional Development.\n"
            "- Category III: Research and Academic Contributions (publications, patents, projects)."
        ),
        "metadata": {
            "regulation": "AICTE CAS 2012/2016",
            "type": "clarification",
        },
    },
    {
        "id": "clarification_mca_phd_2022",
        "discipline": "Computer Science / IT / MCA",
        "position": "General",
        "institution_type": "degree",
        "content": (
            "AICTE AMENDMENT 2022 — MCA with PhD Eligibility (Gazette Notification XIII, 07.11.2022)\n"
            "Prior to 2022: MCA holders with PhD were only considered eligible at Assistant Professor level.\n"
            "After Amendment XIII (November 2022): MCA holders who have completed PhD are now eligible "
            "for direct appointment as Associate Professor and Professor in Computer Science or "
            "Information Technology or related disciplines at AICTE-approved degree level institutions.\n"
            "This amendment significantly expanded career opportunities for MCA PhD holders."
        ),
        "metadata": {
            "regulation": "AICTE Gazette XIII 2022",
            "type": "amendment",
            "gazette_number": "XIII",
        },
    },

    # =========================================================
    # CORE ENGINEERING BRANCHES
    # =========================================================
    {
        "id": "core_branches_engineering",
        "discipline": "Engineering and Technology",
        "position": "General",
        "institution_type": "degree and diploma",
        "content": (
            "MAJOR AND CORE BRANCHES OF ENGINEERING AND TECHNOLOGY — AICTE Gazette Notification VIII (28.04.2017)\n"
            "AICTE has defined Major or Core Branches for determining relevant qualifications "
            "for teaching appointments. Faculty must hold degrees in branches relevant to the subject taught.\n"
            "Recognized Core Branches include:\n"
            "Civil Engineering, Mechanical Engineering, Electrical Engineering, "
            "Electronics and Communication Engineering, Computer Science and Engineering, "
            "Information Technology, Chemical Engineering, Metallurgical Engineering, "
            "Mining Engineering, Aerospace Engineering, Biomedical Engineering, Biotechnology, "
            "Environmental Engineering, Industrial Engineering.\n"
            "Branches deemed relevant or appropriate to a core branch are detailed in the 2017 Gazette."
        ),
        "metadata": {
            "regulation": "AICTE Gazette VIII 2017",
            "gazette_number": "VIII",
            "type": "branch classification",
        },
    },

    # =========================================================
    # PAY SCALES
    # =========================================================
    {
        "id": "pay_scales_degree",
        "discipline": "All",
        "position": "General",
        "institution_type": "degree",
        "content": (
            "PAY SCALES — Degree Level Institutions (AICTE 2019, 7th CPC)\n"
            "Assistant Professor Stage 1: Level 10 — Rs. 57,700 to 1,82,400\n"
            "Assistant Professor Stage 2: Level 11 — Rs. 68,900 to 2,05,500\n"
            "Assistant Professor Stage 3: Level 12 — Rs. 79,800 to 2,11,500\n"
            "Associate Professor: Level 13A — Rs. 1,31,400 to 2,04,700\n"
            "Professor: Level 14 — Rs. 1,44,200 to 2,18,200\n"
            "Senior Professor or HAG: Level 15 — Rs. 1,82,200 to 2,24,100"
        ),
        "metadata": {
            "regulation": "AICTE 2019 (7th CPC)",
            "type": "pay scales",
            "institution_type": "degree",
        },
    },
    {
        "id": "pay_scales_diploma",
        "discipline": "All",
        "position": "General",
        "institution_type": "diploma",
        "content": (
            "PAY SCALES — Diploma Level Institutions (AICTE 2019, 7th CPC)\n"
            "Lecturer: Level 10 — Rs. 57,700 to 1,82,400\n"
            "Senior Lecturer: Level 11 — Rs. 68,900 to 2,05,500\n"
            "Head of Department: Level 12 — Rs. 79,800 to 2,11,500\n"
            "Principal: Level 14 — Rs. 1,44,200 to 2,18,200"
        ),
        "metadata": {
            "regulation": "AICTE Diploma 2019 (7th CPC)",
            "type": "pay scales",
            "institution_type": "diploma",
        },
    },

    # =========================================================
    # CONFERENCE ATTENDANCE / TRAVEL GRANTS
    # =========================================================
    {
        "id": "faculty_travel_grant",
        "discipline": "All",
        "position": "Faculty",
        "institution_type": "degree and diploma",
        "content": (
            "PROFESSIONAL DEVELOPMENT SCHEME (TRAVEL GRANT) — For Faculty (AICTE)\n"
            "This scheme provides financial assistance to regular faculty members for presenting "
            "research papers at national and international conferences.\n"
            "Eligibility Criteria:\n"
            "1. Must be a full-time regular faculty member at an AICTE-approved institute.\n"
            "2. The institute must have been in existence for at least 5 years.\n"
            "3. Must have received a formal letter of acceptance for a paper presentation from the conference organizer.\n"
            "4. Frequency Constraint: The applicant must not have availed this grant during the previous 3 years.\n"
            "5. The scheme covers both events abroad and within India."
        ),
        "metadata": {
            "regulation": "AICTE Professional Development Scheme",
            "type": "travel grant",
            "institution_type": "degree and diploma",
        },
    },
    {
        "id": "fdp_atal_participant",
        "discipline": "All",
        "position": "Participant (Faculty/Scholar)",
        "institution_type": "degree and diploma",
        "content": (
            "FACULTY DEVELOPMENT PROGRAMMES (FDP) & ATAL ACADEMY — Participant Eligibility\n"
            "AICTE offers FDPs and STTPs (Short Term Training Programmes) to upgrade faculty skills.\n"
            "Participant Eligibility Criteria:\n"
            "1. Primarily open to faculty members, research scholars, and PG scholars from AICTE-approved institutions.\n"
            "2. Industry personnel may also be eligible for certain programs.\n"
            "3. Participants must maintain minimum attendance (often 80–90%) and clear assessments to receive certificates.\n"
            "Coordinator Eligibility (for organizing FDP): Must be full-time regular faculty with 10 years experience."
        ),
        "metadata": {
            "regulation": "AICTE ATAL / FDP Guidelines",
            "type": "training",
            "institution_type": "degree and diploma",
        },
    },
    {
        "id": "goc_organizing_conference",
        "discipline": "All",
        "position": "Coordinator / Organizer",
        "institution_type": "degree",
        "content": (
            "GRANT FOR ORGANIZING CONFERENCE (GOC) — Coordinator Eligibility (AICTE)\n"
            "Institutions seeking partial financial assistance to organize conferences must meet specific criteria:\n"
            "Coordinator Eligibility:\n"
            "1. Must be a full-time regular Professor or Associate Professor (or senior faculty) at the host institution.\n"
            "2. Must possess at least 10 years of teaching, research, or industry experience.\n"
            "3. Must have previously organized at least three conferences (for international level) or one conference (for national level).\n"
            "Institutional Eligibility: Must be an AICTE-approved institute with at least 8 years of existence."
        ),
        "metadata": {
            "regulation": "AICTE GOC Scheme",
            "type": "organizer grant",
            "institution_type": "degree",
        },
    },
]
