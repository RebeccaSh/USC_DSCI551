import streamlit as st
import utils
import ml_model.college_ml as cml
import college_profile
import statistics as stat

ss = st.session_state


def run_ML():
    ss["ML_btn"] = True


def college_selected():
    id = ss.ops
    utils.set_state("rec_college", None if id == 0 else ss.lookup.loc[id].to_dict())
    utils.set_state(
        "city", None if id == 0 else utils.get_city_data(ss.rec_college["city_id"])
    )


def format_func(options):
    return ss.lookup.loc[options, "institution"]


def formatted_result(data):
    i = 1
    content = """
        <div class="table-wrapper">
            <table class="fl-table">
                <thead>
                <tr>
                    <th></th>
                    <th>Institution</th>
                    <th>Rank</th>
                    <th>Type</th>
                    <th>City</th>
                    <th>State</th>
                    <th>Acceptance Rate</th>
                    <th>Recommendations</th>
                    <th>Test Scores</th>
                    <th>TOEFL</th>
                </tr>
                </thead>
                <tbody>
    """
    data = data.sort_values(
        ["rank", "acceptance_rate", "institution"], ascending=[True, False, True]
    )
    for index, row in data.iloc[0:10].iterrows():
        content += f"<tr><td>{i}</td><td>{row['institution']}</td><td>{row['rank']}</td><td>{'Private' if row['private'] else 'Public'}</td><td>{row['city']}</td><td>{row['state']}</td><td>{row['acceptance_rate']}%</td><td>{row['recommendations']}</td><td>{row['admission_test_scores']}</td><td>{row['TOEFL']}</td></tr>"
        i += 1

    content += "<tbody></table></div>"
    return content


def setup():

    # header setup
    b, _, h, _ = st.columns((1, 1, 10, 1))
    b.button("🔙", on_click=utils.show_home)
    h.markdown(utils.get_header("Find Your College"), unsafe_allow_html=True)
    utils.render_hr()

    # user input
    l11, l12, l13 = st.columns((2, 2, 3))
    l11.radio("Standardized Test Type:", ("SAT", "ACT"), 0, key="test")
    l12.number_input("GPA (out of 4):", 0.0, 4.0, 3.0, 0.10, key="gpa")
    l13.multiselect(
        "Preferred Study Locations:",
        sorted(ss.data["state"].unique()),
        [],
        key="selected_states",
    )

    utils.render_hr("50%")

    t1, t2, t3, t4, t5 = st.columns(5)
    t1.number_input(
        "SAT Reading Writing:",
        0,
        800,
        500,
        10,
        key="sat_rw",
        disabled=ss.test == "ACT",
    )
    t2.number_input(
        "SAT Math:", 0, 800, 500, 10, key="sat_m", disabled=ss.test == "ACT"
    )
    t3.number_input(
        "ACT English:", 0, 36, 30, 1, key="act_e", disabled=ss.test == "SAT"
    )
    t4.number_input("ACT Math:", 0, 36, 30, 1, key="act_m", disabled=ss.test == "SAT")
    t5.number_input(
        "ACT Composite:", 0, 36, 30, 1, key="act_c", disabled=ss.test == "SAT"
    )

    utils.render_hr("50%")

    ml1, ml2 = st.columns(2)
    ml1, ml2, ml3, ml24 = st.columns(4)
    ml1.selectbox(
        "Research Experience:",
        ("None", "Fair", "Intermediate", "Advanced"),
        key="research",
    )
    ml2.selectbox(
        "Academic Awards:",
        ("No", "Yes"),
        key="awards",
    )
    ml3.selectbox(
        "Completed AP Courses:",
        ("None", "One", "Two", "Three", "Four or More"),
        key="ap",
    )
    ml24.selectbox(
        "Secured Scholarships:",
        ("No", "Yes, One", "Yes, Two", "Yes, Three or More"),
        key="scholar",
    )

    utils.render_hr("50%")

    _, b = st.columns((3, 1))
    b.button("Find College", on_click=run_ML)
    b.markdown(
        "<hr style='margin:0;border-bottom: 1px solid rgba(250, 250, 250, 0.2);'/>",
        unsafe_allow_html=True,
    )
    utils.render_hr()
    # on click
    if ss.ML_btn:
        with st.spinner("Working on it..."):
            scores = (
                ss.sat_rw + ss.sat_m
                if ss.test == "SAT"
                else stat.mean([ss.act_e, ss.act_m, ss.act_c])
            )
            awards = {"No": 0, "Yes": 1}
            research = {"None": 0, "Fair": 1, "Intermediate": 2, "Advanced": 3}
            scholar = {"No": 0, "Yes, One": 1, "Yes, Two": 2, "Yes, Three or More": 3}
            ap = {"None": 0, "One": 1, "Two": 1, "Three": 3, "Four or More": 4}

            resp = cml.main(
                {
                    "scores": scores,
                    "input_rate": [
                        ss.gpa,
                        awards.get(ss.awards),
                        research.get(ss.research),
                        scholar.get(ss.scholar),
                        ap.get(ss.ap),
                    ],
                    "k": 7,
                }
            )
            data = ss.data.loc[resp[2]]
            df = data[
                [
                    "institution",
                    "rank",
                    "private",
                    "city",
                    "state",
                    "acceptance_rate",
                    "recommendations",
                    "admission_test_scores",
                    "TOEFL",
                ]
            ].sort_values(["rank", "acceptance_rate", "institution"])
            if ss.selected_states:
                df = df[df["state"].isin(ss.selected_states)]
            utils.set_state("rec_result", df)

            utils.set_state("lookup", ss.lookup.iloc[0:1].append(data))
        ss["ML_btn"] = False
        ss["first_ml_run"] = True

    # display result data
    if ss.first_ml_run:
        st.subheader(f"Recommended Colleges (Top 10):")

        st.markdown(formatted_result(ss.rec_result), unsafe_allow_html=True)
        with st.expander("Full Recommendations List", False):
            st.write(ss.rec_result)

        utils.render_hr()
        st.markdown(utils.get_header("College Profile"), unsafe_allow_html=True)
        st.write("")
        st.selectbox(
            "Select College to View its Profile:",
            key="ops",
            options=list(ss.lookup.index),
            format_func=format_func,
            on_change=college_selected,
        )

        if ss.rec_college:
            college_profile.display(ss.rec_college, ss.city)
