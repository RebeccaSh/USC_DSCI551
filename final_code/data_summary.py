import streamlit as st
import utils
import altair as alt


def setup():
    colleges = st.session_state.data
    cities = st.session_state.cities

    ipeds = "https://nces.ed.gov/ipeds/"
    numbeo = "https://www.numbeo.com/cost-of-living/"

    # header setup
    b, _, h, _ = st.columns((1, 1, 10, 1))
    b.button("🔙", on_click=utils.show_home)
    h.markdown(utils.get_header("About the Data"), unsafe_allow_html=True)

    # college admission data
    st.subheader("College Admission Data")
    st.write(
        f"""
        College admission data is coming from [IPEDS]({ipeds}), the Integrated Postsecondary Education Data System.
        IPEDS provides basic data needed to describe — and analyze trends in — postsecondary education in the United States.
        Such data includes institutions characteristics, numbers of students enrolled, admission requirements, test scores and more.
        """
    )

    st.markdown(
        f"""
        The data used in this application is of the year 2020. There is a total of <b>{colleges.shape[0]}</b> institutions from <b>{colleges['state'].nunique()}</b> states,
        <b>{colleges[~colleges['private']]['institution'].nunique()}</b> of which are public institutions. Here are some additional facts about the dataset:
        """,
        unsafe_allow_html=True,
    )

    utils.render_hr("50%")

    t1, t2 = st.columns(2)
    t1.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Average Tuition (Public)</h5>
            <p style='margin:0;font-size:2rem;'>${'{:,}'.format(round(colleges[(colleges['in_state_tuition']>0)&(~colleges['private'])]['in_state_tuition'].mean()))}<sub> In State</sub></p>
            <p style='margin:0 0 1rem 0;font-size:2rem;'>${'{:,}'.format(round(colleges[(colleges['out_of_state_tuition']>0) & (~colleges['private'])]['out_of_state_tuition'].mean()))}<sub> Out of State</sub></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    t2.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Average Tuition (Private)</h5>
            <p style='margin:0;font-size:2rem;'>${'{:,}'.format(round(colleges[(colleges['in_state_tuition']>0)& (colleges['private'])]['in_state_tuition'].mean()))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    utils.render_hr("50%")
    a1, a2 = st.columns(2)

    a1.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Acceptance Rate</h5>
            <p style='margin:0;font-size:2rem;'>{'{:,}'.format(round(colleges[~colleges['private']]['total_admissions'].sum()/colleges[~colleges['private']]['total_applicants'].sum()*100))}% <sub> (Public)</sub></p>
            <p style='margin:0 0 1rem 0;font-size:2rem;'>{'{:,}'.format(round(colleges[colleges['private']]['total_admissions'].sum()/colleges[colleges['private']]['total_applicants'].sum()*100))}% <sub> (Private)</sub></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    a2.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Enrollment Rate:</h5>
            <p style='margin:0;font-size:2rem;'>{'{:,}'.format(round(colleges[~colleges['private']]['total_enrolled'].sum()/colleges[~colleges['private']]['total_admissions'].sum()*100))}% <sub> (Public)</sub></p>
            <p style='margin:0 0 1rem 0;font-size:2rem;'>{'{:,}'.format(round(colleges[colleges['private']]['total_enrolled'].sum()/colleges[colleges['private']]['total_admissions'].sum()*100))}% <sub> (Private)</sub></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Colleges per State
    utils.render_hr("50%")
    st.markdown("<h5 style='text-align:center'>Colleges per State</h5>", unsafe_allow_html=True)
    source = colleges
    source["College Type"] = list(
        map(lambda i: "Private" if i else "Public", source["private"])
    )
    ac = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            x=alt.X("state", axis=alt.Axis(title="States", labelAngle=315)),
            y=alt.Y("count(institution)", axis=alt.Axis(title="No. of Colleges")),
            color="College Type",
            tooltip=["state"],
        )
    )

    st.altair_chart(ac, use_container_width=True)
    # Raw Data
    with st.expander("College Admission Raw Data", False):
        st.write(colleges)
        st.download_button(
            label="Download data as CSV",
            data=colleges.to_csv().encode("utf-8"),
            file_name="college_admission_data.csv",
            mime="text/csv",
        )

    utils.render_hr()

    # college admission data
    st.subheader("Cities Data")
    st.write(
        f"""
        [Numbeo]({numbeo}) is a crowd-sourced global database of quality-of-life 
        information including housing indicators, perceived crime rates, and quality of healthcare, among many other statistics.
        """
    )

    st.markdown(
        f"""
        The cities dataset used in this application includes <b>{cities['id'].nunique()}</b> cities 
        and consists of general city information, such as: rent, transportaion, cost-of-living and safety and healthcare indices. 
        Here are some facts about the dataset:
        """,
        unsafe_allow_html=True,
    )
    utils.render_hr("50%")

    # National Indices
    i1, i2 = st.columns(2)
    i1.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Safety Index:<span style='font-size:1rem;font-weight: normal;'>(Moderate)</span></h5>
            <p style='margin:0 0 1rem 0;font-size:2rem;'>{round(cities[cities['safety_index']>0]['safety_index'].mean(),1)} <sub> (National Average)</sub></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    i2.markdown(
        f"""
        <div style='text-align:center'>
            <h5 style='padding:0;'>Healthcare Index:<span style='font-size:1rem;font-weight: normal;'>(High)</span></h5>
            <p style='margin:0 0 1rem 0;font-size:2rem;'>{round(cities[cities['health_index']>0]['health_index'].mean(),1)} <sub> (National Average)</sub></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    utils.render_hr("50%")

    st.markdown("<h5 style='padding:0;text-align:center'>Average 1 Bedroom Rent</h5>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>In City Centre vs Out of City Centre</p>", unsafe_allow_html=True)

    source = cities[(cities["1b_rent_cc"] > 0) & (cities["1b_rent_oc"] > 0)]
    source = (
        source.merge(colleges, left_on="id", right_on="city_id").reindex(
            columns=["id", "1b_rent_cc", "1b_rent_oc", "state", "city"]
        )
    ).drop_duplicates()

    ac = (
        alt.Chart(source)
        .mark_point()
        .encode(
            x=alt.X(
                "1b_rent_cc:Q",
                axis=alt.Axis(title="1 Bedroom Rent (City Centre)", labelAngle=315),
            ),
            y=alt.Y(
                "1b_rent_oc:Q",
                axis=alt.Axis(
                    title="1 Bedroom Rent (Out of City Centre)", labelAngle=0
                ),
            ),
            color="state:N",
            tooltip=["city", "state", "1b_rent_cc", "1b_rent_oc"],
        )
    )
    st.altair_chart(ac, use_container_width=True)

    with st.expander("Cities Raw Data", False):
        st.write(cities)
        st.download_button(
            label="Download data as CSV",
            data=cities.to_csv().encode("utf-8"),
            file_name="cities_data.csv",
            mime="text/csv",
        )

