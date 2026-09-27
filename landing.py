from pathlib import Path

import streamlit as st


LANDING_FILE = Path(__file__).with_name("landing.html")


def apply_styles() -> None:
    """Apply the shared RoutineCraft visual style."""

    st.markdown(
        """
        <style>
        :root {
            --rc-ground: #eef2f0;
            --rc-panel: #ffffff;
            --rc-ink: #0f1b2d;
            --rc-soft: #4a5a6b;
            --rc-rule: #cbd5d2;
            --rc-grid: #dde5e2;
            --rc-mark: #d4ee3a;
            --rc-ok: #1f7a4d;
            --rc-danger: #d9383f;
            --rc-mono: "JetBrains Mono", "Cascadia Mono", Consolas, monospace;
            --rc-display: "Bricolage Grotesque", "Arial Narrow", sans-serif;
            --rc-body: "Schibsted Grotesk", "Segoe UI", sans-serif;
        }

        @import url("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Schibsted+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap");

        .stApp {
            background: var(--rc-ground);
            color: var(--rc-ink);
            font-family: var(--rc-body);
        }

        .block-container {
            max-width: 1160px;
            padding: 0 1.25rem 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .rc-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1.05rem 0;
            border-bottom: 1px solid var(--rc-rule);
        }

        .rc-brand {
            color: var(--rc-ink);
            font: 800 1.35rem/1 var(--rc-display);
            letter-spacing: -.03em;
        }

        .rc-brand span,
        .rc-highlight {
            background: var(--rc-mark);
            color: var(--rc-ink);
            padding: .05em .16em;
        }

        .rc-nav-label {
            color: var(--rc-soft);
            font: 500 .7rem/1 var(--rc-mono);
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .rc-hero {
            padding: 4.5rem 0 2.8rem;
        }

        .rc-eyebrow,
        .rc-section-label {
            color: var(--rc-soft);
            font: 500 .72rem/1.2 var(--rc-mono);
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .rc-hero h1 {
            max-width: 850px;
            margin: 1rem 0 0;
            color: var(--rc-ink);
            font: 800 clamp(2.8rem, 7vw, 5.65rem)/.96 var(--rc-display);
            letter-spacing: -.055em;
        }

        .rc-hero-copy {
            max-width: 650px;
            margin: 1.45rem 0 0;
            color: var(--rc-soft);
            font-size: 1.12rem;
            line-height: 1.65;
        }

        .rc-hero-copy strong {
            color: var(--rc-ink);
            font-weight: 600;
        }

        .rc-demo {
            display: grid;
            grid-template-columns: minmax(0, 1.65fr) minmax(260px, 1fr);
            gap: 1.1rem;
            margin-top: 2.8rem;
        }

        .rc-board,
        .rc-trace,
        .rc-step,
        .rc-auth-panel {
            background: var(--rc-panel);
            border: 1px solid var(--rc-rule);
        }

        .rc-board-head {
            display: flex;
            justify-content: space-between;
            gap: .75rem;
            padding: .8rem 1rem;
            border-bottom: 1px solid var(--rc-rule);
        }

        .rc-status {
            color: var(--rc-ok);
            font: 500 .68rem/1 var(--rc-mono);
            text-transform: uppercase;
            letter-spacing: .08em;
        }

        .rc-status::before {
            display: inline-block;
            width: .45rem;
            height: .45rem;
            margin-right: .4rem;
            border-radius: 50%;
            background: var(--rc-ok);
            content: "";
            box-shadow: 0 0 0 .25rem rgba(31, 122, 77, .12);
        }

        .rc-timetable {
            display: grid;
            grid-template-columns: 3.4rem 1fr;
            min-width: 500px;
            padding: .7rem 1rem 1rem;
        }

        .rc-days {
            display: grid;
            grid-column: 2;
            grid-template-columns: repeat(6, 1fr);
            padding: .45rem 0 .6rem;
        }

        .rc-days span,
        .rc-time,
        .rc-block {
            font-family: var(--rc-mono);
        }

        .rc-days span {
            color: var(--rc-soft);
            font-size: .65rem;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .rc-times {
            position: relative;
            height: 240px;
        }

        .rc-time {
            position: absolute;
            right: .55rem;
            color: var(--rc-soft);
            font-size: .62rem;
            transform: translateY(-50%);
        }

        .rc-grid {
            position: relative;
            height: 240px;
            border-top: 1px solid var(--rc-grid);
            border-left: 1px solid var(--rc-grid);
            background:
                repeating-linear-gradient(to right, transparent 0, transparent calc(16.666% - 1px), var(--rc-grid) calc(16.666% - 1px), var(--rc-grid) 16.666%),
                repeating-linear-gradient(to bottom, transparent 0, transparent calc(25% - 1px), var(--rc-grid) calc(25% - 1px), var(--rc-grid) 25%);
        }

        .rc-block {
            position: absolute;
            padding: .4rem .5rem;
            overflow: hidden;
            border: 2px solid var(--rc-ink);
            background: var(--rc-mark);
            color: var(--rc-ink);
            font-size: .64rem;
            line-height: 1.3;
        }

        .rc-block b {
            display: block;
            font-size: .72rem;
            font-weight: 500;
        }

        .rc-block.try {
            border-style: dashed;
            background: var(--rc-panel);
        }

        .rc-block.clash {
            z-index: 2;
            border-color: var(--rc-danger);
            background: repeating-linear-gradient(135deg, rgba(217, 56, 63, .14) 0 6px, transparent 6px 12px), var(--rc-panel);
            color: var(--rc-danger);
        }

        .rc-caption {
            margin: .6rem 1rem .9rem;
            color: var(--rc-soft);
            font: .65rem/1.5 var(--rc-mono);
        }

        .rc-trace-title {
            padding: .8rem 1rem;
            border-bottom: 1px solid var(--rc-rule);
            color: var(--rc-soft);
            font: 500 .7rem/1 var(--rc-mono);
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .rc-trace ol {
            margin: 0;
            padding: .45rem 0;
            list-style: none;
        }

        .rc-trace li {
            display: grid;
            grid-template-columns: 3.4rem 1fr;
            gap: .55rem;
            padding: .72rem 1rem;
            color: var(--rc-soft);
            font-size: .86rem;
            line-height: 1.4;
        }

        .rc-trace li.active {
            border-left: 4px solid var(--rc-ink);
            padding-left: .75rem;
            background: var(--rc-ground);
            color: var(--rc-ink);
        }

        .rc-pill {
            align-self: start;
            border: 1px solid currentColor;
            padding: .22rem .25rem;
            color: var(--rc-ok);
            font: 500 .58rem/1 var(--rc-mono);
            text-align: center;
        }

        .rc-pill.no {
            color: var(--rc-danger);
        }

        .rc-auth-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.1rem;
            margin-top: 1.1rem;
        }

        .rc-auth-panel {
            padding: 1.3rem 1.4rem;
        }

        .rc-auth-panel h3,
        .rc-step h3 {
            margin: .45rem 0 .4rem;
            color: var(--rc-ink);
            font: 600 1.25rem/1.15 var(--rc-display);
        }

        .rc-auth-panel p,
        .rc-step p {
            margin: 0;
            color: var(--rc-soft);
            font-size: .9rem;
            line-height: 1.55;
        }

        .rc-section {
            padding: 3.8rem 0 1rem;
            border-top: 1px solid var(--rc-rule);
        }

        .rc-section h2 {
            max-width: 620px;
            margin: .75rem 0 1.5rem;
            color: var(--rc-ink);
            font: 800 clamp(2rem, 4vw, 3.4rem)/1 var(--rc-display);
            letter-spacing: -.04em;
        }

        .rc-steps {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.1rem;
        }

        .rc-step {
            min-height: 170px;
            padding: 1.25rem;
            transition: transform .2s ease, box-shadow .2s ease;
        }

        .rc-step:hover {
            transform: translateY(-4px);
            box-shadow: 6px 6px 0 var(--rc-mark);
        }

        .rc-step-number {
            color: var(--rc-soft);
            font: 500 .68rem/1 var(--rc-mono);
            letter-spacing: .12em;
        }

        .rc-footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--rc-rule);
            color: var(--rc-soft);
            font: .7rem/1.5 var(--rc-mono);
            text-align: center;
        }

        div[data-testid="stButton"] > button {
            min-height: 2.8rem;
            border: 2px solid var(--rc-ink);
            border-radius: 0;
            background: var(--rc-ink);
            color: var(--rc-ground);
            font-weight: 600;
            box-shadow: none;
        }

        div[data-testid="stButton"] > button:hover {
            border-color: var(--rc-ink);
            background: var(--rc-ink);
            color: var(--rc-ground);
            box-shadow: 4px 4px 0 var(--rc-mark);
            transform: translate(-2px, -2px);
        }

        @media (max-width: 800px) {
            .rc-demo,
            .rc-auth-wrap {
                grid-template-columns: 1fr;
            }

            .rc-steps {
                grid-template-columns: 1fr;
            }

            .rc-hero {
                padding-top: 3.2rem;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            .rc-step,
            div[data-testid="stButton"] > button {
                transition: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_landing(show_auth_warning: bool = False) -> None:
    """Render the public page shown before authentication.

    The page itself lives in views/landing.html. Its "Open the planner"
    links point to ?login=1, which app.py turns into a Google sign-in.
    """

    page = LANDING_FILE.read_text(encoding="utf-8")

    if show_auth_warning:
        page = page.replace(
            "<!--NOTICE-->",
            '<div class="notice"><div class="wrap">'
            "Google login is not configured yet. "
            "The project administrator must add local secrets."
            "</div></div>",
        )

    st.html(page, unsafe_allow_javascript=True)


def render_dashboard(user: dict) -> None:
    """Render the protected student dashboard."""

    st.title(f"Welcome, {user['name']}")
    st.caption(user["email"])

    st.write(
        "Your account is authorized. Continue to the routine "
        "generator from the sidebar."
    )

    first, second, third = st.columns(3)

    first.metric(
        "Routine options",
        "Up to 3",
        help="The solver can return up to three valid combinations.",
    )

    second.metric(
        "Academic checks",
        "CGPA + Prerequisite",
    )

    third.metric(
        "Conflict checks",
        "Class + Exam",
    )

    st.subheader("How RoutineCraft works")

    st.markdown(
        "1. Open **Routine Generator** from the sidebar.\n"
        "2. Enter your academic information.\n"
        "3. Select courses and completed prerequisites.\n"
        "4. Generate and compare valid routines."
    )

    st.info(
        "RoutineCraft provides recommendations only. "
        "It does not register courses or access UCAM."
    )
