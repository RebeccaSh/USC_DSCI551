import streamlit as st
import utils
import college_profile

ss = st.session_state


def college_selected():
    id = ss.cid
    utils.set_state("college", None if id == 0 else ss.lookup.loc[id].to_dict())
    utils.set_state(
        "city", None if id == 0 else utils.get_city_data(ss.college["city_id"])
    )


def format_func(options):
    return st.session_state.lookup.loc[options, "institution"]


def setup():

    # header setup
    b, _, h, _ = st.columns((1, 1, 10, 1))
    b.button("🔙", on_click=utils.show_home)
    h.markdown(utils.get_header("Explore Colleges"), unsafe_allow_html=True)

    ss = st.session_state
    data = ss.data
    with st.expander("Filter Colleges:", True):

        st.write("Institution:")
        c1, c2, c3, c4 = st.columns((1, 1, 2, 2))
        c1.checkbox("Public", True, key="public")
        c2.checkbox("Private", True, key="private")
        c3.checkbox("Offers Graduate Programs", False, key="graduate")
        c4.checkbox("Offers Distant Programs", False, key="distant")
        utils.render_hr("50%")

        # Application Requirements
        st.write("Application Requirements:")
        r1, r2, r3 = st.columns(3)
        r1.multiselect(
            "Recommendations:", data["recommendations"].unique(), [], key="recom"
        )
        r2.multiselect(
            "Admission Test Scores:",
            data["admission_test_scores"].unique(),
            [],
            key="tests",
        )
        r3.multiselect("TOEFL:", data["TOEFL"].unique(), [], key="toefl")

        utils.render_hr("50%")
        t1, t2, t3 = st.columns(3)
        t1.radio("Standardized Test Type:", ("SAT", "ACT"), 0, key="test")
        sat_rw_min = data[data["SAT_reading_writing_lower"] > 0][
            "SAT_reading_writing_lower"
        ].min()
        t2.number_input(
            "SAT Reading Writing:",
            sat_rw_min,
            800,
            sat_rw_min,
            10,
            key="sat_rw",
            disabled=ss.test == "ACT",
        )
        sat_m_min = data[data["SAT_math_lower"] > 0]["SAT_math_lower"].min()
        t3.number_input(
            "SAT Math:",
            sat_m_min,
            800,
            sat_m_min,
            10,
            key="sat_m",
            disabled=ss.test == "ACT",
        )

        t1, t2, t3 = st.columns(3)
        act_e_min = data[data["ACT_english_lower"] > 0]["ACT_english_lower"].min()
        t1.number_input(
            "ACT English:",
            act_e_min,
            36,
            act_e_min,
            1,
            key="act_e",
            disabled=ss.test == "SAT",
        )
        act_m_min = data[data["ACT_math_lower"] > 0]["ACT_math_lower"].min()
        t2.number_input(
            "ACT Math:",
            act_m_min,
            36,
            act_m_min,
            1,
            key="act_m",
            disabled=ss.test == "SAT",
        )
        act_c_min = data[data["ACT_composite_lower"] > 0]["ACT_composite_lower"].min()
        t3.number_input(
            "ACT Composite:",
            act_c_min,
            36,
            act_c_min,
            1,
            key="act_c",
            disabled=ss.test == "SAT",
        )

        utils.render_hr("50%")

        s1, s2 = st.columns(2)
        s1.slider(
            "Tuition:",
            0,
            int(data["out_of_state_total"].max()),
            int(data["out_of_state_total"].max()),
            5000,
            format="$%f",
            key="tuition",
        )

        s2.multiselect(
            "Study Location (States):", sorted(data["state"].unique()), [], key="states"
        )

        utils.render_hr("50%")
        _, b = st.columns((3, 1))
        b.button("Clear Filters", on_click=utils.reset_filters)
        utils.render_hr()
        search()
        st.subheader(f"{ss.search_result.shape[0]} Colleges Found:")
        """
        # st.markdown(
        #     f"</span><h5 style='padding:0;'>{ss.search_result.shape[0]} Colleges Found:</h5>",
        #     unsafe_allow_html=True,
        # )
        # df = pd.DataFrame(
        #     list(map(lambda x: eval(x), ss.search_result['location'])),
        #     columns=["lat", "lon"],
        # )
        # st.map(df)
        # st.write(pd.DataFrame(list(map(lambda x: eval(x), ss.search_result['location']))))
        """
        st.write(
            ss.search_result[
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
            ].sort_values("rank")
        )

    utils.render_hr()
    st.markdown(utils.get_header("College Profile"), unsafe_allow_html=True)
    st.write("")
    st.selectbox(
        "Select College to View its Profile:",
        key="cid",
        options=list(ss.lookup.sort_values("rank").index),
        format_func=format_func,
        on_change=college_selected,
    )

    if ss.college:
        college_profile.display(ss.college, ss.city)


def search():
    ss = st.session_state
    data = ss.data.copy()
    if ss["public"] != ss["private"]:
        data = data[data["private"] == ss["private"]]
    if ss["recom"]:
        data = data[data["recommendations"].isin(ss["recom"])]
    if ss["tests"]:
        data = data[data["admission_test_scores"].isin(ss["tests"])]
    if ss["toefl"]:
        data = data[data["TOEFL"].isin(ss["toefl"])]
    data = data[data["out_of_state_total"] <= ss["tuition"]]
    if ss["distant"]:
        data = data[data["distance_education_offered"]]
    if ss["graduate"]:
        data = data[data["graduate_offering"]]
    if ss["states"]:
        data = data[data["state"].isin(ss["states"])]

    if ss.test == "SAT":
        data = data[
            (data["SAT_reading_writing_lower"] >= ss["sat_rw"])
            | (data["SAT_reading_writing_lower"] == 0)
        ]
        data = data[
            (data["SAT_math_lower"] >= ss["sat_m"]) | (data["SAT_math_lower"] == 0)
        ]
    else:
        data = data[
            (data["ACT_english_lower"] >= ss["act_e"])
            | (data["ACT_english_lower"] == 0)
        ]
        data = data[
            (data["ACT_math_lower"] >= ss["act_m"]) | (data["ACT_math_lower"] == 0)
        ]
        data = data[
            (data["ACT_composite_lower"] >= ss["act_c"])
            | (data["ACT_composite_lower"] == 0)
        ]

    ss.search_result = data
    ss.lookup = ss.lookup.iloc[0:1].append(data)
