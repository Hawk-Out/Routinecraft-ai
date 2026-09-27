import pandas as pd
import streamlit as st

from src.auth import (
    auth_is_configured,
    require_authorized_user,
    user_is_logged_in,
)
from src.solver import (
    generate_schedules,
    load_course_sections,
)
from src.validators import (
    find_missing_prerequisites,
    load_prerequisite_map,
    max_credits_for_cgpa,
    validate_credit_request,
)
from views.landing import (
    apply_styles,
    render_dashboard,
    render_landing,
)


COURSES_FILE = "data/courses.csv"
SECTIONS_FILE = "data/sections.csv"


st.set_page_config(
    page_title="RoutineCraft AI",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)


apply_styles()


# The landing page's "Open the planner" links arrive as ?login=1.
login_requested = st.query_params.get("login") == "1"


# Logged-out users can only view the public landing page.
if not user_is_logged_in():
    if login_requested and auth_is_configured():
        st.login("google")
        st.stop()

    render_landing(show_auth_warning=login_requested)
    st.stop()


if login_requested:
    del st.query_params["login"]


# Verify Google authentication and the permitted UIU email domain.
current_user = require_authorized_user()


# Protected application navigation.
with st.sidebar:
    st.title("RoutineCraft AI")
    st.caption(current_user["email"])

    selected_page = st.radio(
        "Navigation",
        options=[
            "Dashboard",
            "Routine Generator",
        ],
        key="main_navigation",
    )

    st.divider()

    if st.button(
        "Log out",
        use_container_width=True,
        key="sidebar_logout",
    ):
        st.logout()

    st.divider()
    st.header("About")

    st.write(
        "RoutineCraft AI uses CSP backtracking to generate "
        "valid, conflict-free course routines."
    )

    st.caption("Developed by Adit, Efty, and Siyam")


# Avoid loading routine-generator data while viewing the dashboard.
if selected_page == "Dashboard":
    render_dashboard(current_user)
    st.stop()


# Load academic data only for authenticated and authorized users.
course_data = pd.read_csv(COURSES_FILE)

course_codes = course_data["course_code"].tolist()

course_name_map = dict(
    zip(
        course_data["course_code"],
        course_data["course_name"],
    )
)

course_credit_map = dict(
    zip(
        course_data["course_code"],
        course_data["credits"],
    )
)

prerequisite_map = load_prerequisite_map()

prerequisite_options = sorted(
    {
        prerequisite
        for requirements in prerequisite_map.values()
        for prerequisite in requirements
    }
)


st.title("📅 Routine Generator")
st.subheader("Create a conflict-free course routine")

st.write(
    "Enter your academic information, select courses, and "
    "generate suitable routine combinations."
)

st.info(
    "RoutineCraft validates your CGPA credit limit, selected "
    "credits, prerequisites, class times, and examination times."
)

st.markdown("---")
st.header("Student Information")


user_name = current_user.get("name", "UIU Student")

default_student_name = (
    ""
    if user_name == "UIU Student"
    else user_name
)


with st.form("student_information_form"):
    name = st.text_input(
        "Student Name",
        value=default_student_name,
        placeholder="Enter your full name",
    )

    col1, col2 = st.columns(2)

    with col1:
        cgpa = st.number_input(
            "Current CGPA",
            min_value=0.00,
            max_value=4.00,
            value=3.00,
            step=0.01,
        )

    with col2:
        requested_credits = st.number_input(
            "Requested Credits",
            min_value=1,
            max_value=16,
            value=9,
            step=1,
        )

    selected_courses = st.multiselect(
        "Select Courses",
        options=course_codes,
        format_func=lambda code: (
            f"{code} — {course_name_map[code]}"
        ),
    )

    completed_courses = st.multiselect(
        "Completed Prerequisite Courses",
        options=prerequisite_options,
    )

    preference = st.selectbox(
        "Routine Preference",
        options=[
            "No preference",
            "Morning classes",
            "Fewer class days",
        ],
    )

    submitted = st.form_submit_button(
        "Generate Routine",
        type="primary",
        use_container_width=True,
    )


if submitted:
    if not name.strip():
        st.error("Please enter the student name.")

    elif not selected_courses:
        st.error("Please select at least one course.")

    elif not validate_credit_request(
        cgpa,
        requested_credits,
    ):
        maximum_credits = max_credits_for_cgpa(cgpa)

        st.error(
            f"Your CGPA allows a maximum of "
            f"{maximum_credits} credits."
        )

    else:
        selected_credit_total = sum(
            course_credit_map[course]
            for course in selected_courses
        )

        if selected_credit_total != requested_credits:
            st.error(
                f"Your selected courses contain "
                f"{selected_credit_total} credits, but you "
                f"requested {requested_credits} credits."
            )

        else:
            missing_prerequisites = find_missing_prerequisites(
                selected_courses=selected_courses,
                completed_courses=completed_courses,
                prerequisite_map=prerequisite_map,
            )

            if missing_prerequisites:
                missing_message = "; ".join(
                    f"{course}: {', '.join(requirements)}"
                    for course, requirements
                    in missing_prerequisites.items()
                )

                st.error(
                    "Missing prerequisites — "
                    f"{missing_message}"
                )

            else:
                all_course_sections = load_course_sections(
                    SECTIONS_FILE
                )

                selected_course_sections = {
                    course: all_course_sections.get(
                        course,
                        [],
                    )
                    for course in selected_courses
                }

                schedules = generate_schedules(
                    selected_course_sections,
                    max_solutions=3,
                )

                if not schedules:
                    st.error(
                        "No conflict-free routine was found."
                    )

                else:
                    maximum_credits = max_credits_for_cgpa(
                        cgpa
                    )

                    st.success(
                        f"{len(schedules)} conflict-free "
                        f"routine option(s) found."
                    )

                    summary_col1, summary_col2 = st.columns(2)

                    with summary_col1:
                        st.write(f"**Student:** {name}")
                        st.write(f"**CGPA:** {cgpa:.2f}")
                        st.write(
                            f"**Selected credits:** "
                            f"{selected_credit_total}"
                        )

                    with summary_col2:
                        st.write(
                            f"**Maximum allowed credits:** "
                            f"{maximum_credits}"
                        )
                        st.write(
                            f"**Preference:** {preference}"
                        )
                        st.write(
                            f"**Courses:** "
                            f"{', '.join(selected_courses)}"
                        )

                    st.info(
                        "These routines satisfy the current "
                        "academic and scheduling constraints."
                    )

                    for index, schedule in enumerate(
                        schedules,
                        start=1,
                    ):
                        st.subheader(
                            f"Routine Option {index}"
                        )

                        routine_rows = []

                        for course, section in schedule.items():
                            class_days = section["class_days"]

                            if isinstance(class_days, list):
                                class_days = ", ".join(
                                    class_days
                                )

                            routine_rows.append(
                                {
                                    "Course": course,
                                    "Course Name": (
                                        course_name_map[course]
                                    ),
                                    "Section": (
                                        section["section_id"]
                                    ),
                                    "Class Days": class_days,
                                    "Class Time": (
                                        f"{section['class_start']}–"
                                        f"{section['class_end']}"
                                    ),
                                    "Exam Date": (
                                        section["exam_date"]
                                    ),
                                    "Exam Time": (
                                        f"{section['exam_start']}–"
                                        f"{section['exam_end']}"
                                    ),
                                }
                            )

                        st.dataframe(
                            pd.DataFrame(routine_rows),
                            use_container_width=True,
                            hide_index=True,
                        )
