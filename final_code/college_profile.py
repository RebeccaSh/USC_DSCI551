import streamlit as st
import pandas as pd
import utils
import matplotlib.pyplot as plt
import json


def display(college, city):

    st.header(college["institution"])
    # About Section
    with st.expander(f"About {college['institution']}", True):
        st.markdown(
            f"""
                {college['institution']} is a <b>{'private' if college['private'] else 'public'}</b> school in <b>{college['city']}, {college['state']}</b>.
                It is ranked at <b>#{college['rank']}</b>{'+' if college['rank']==150 else ''} nationally and offers {college['institution_level'].lower()} of <b>undergraduate
                {'and ' + 'graduate' if 'graduate_offering' in college.keys() else ''} programs</b>.
            """,
            unsafe_allow_html=True,
        )

    # Rates Section
    with st.expander("👨‍🎓️Acceptance and Enrollment Rate", True):
        desc, rates = st.columns((2, 1))
        desc.markdown(
            f""" 
            <b>Acceptance rate</b> is the percentage of applicants who are admitted. Last year, 
            {college['institution']} recieved <b>{'{:,}'.format(int(college['total_applicants']))}</b> applications, 
            <b>{'{:,}'.format(int(college['total_admissions']))}</b> of which were accepted. </br></br>
            <b>Yield rate</b> is the rate at which accepted students decide to attend, and out of
            <b>{'{:,}'.format(int(college['total_admissions']))}</b> applicants, <b>{'{:,}'.format(int(college['total_enrolled']))}</b>
            have decided to enroll to {college['institution']}.""",
            unsafe_allow_html=True,
        )
        rates.metric(label="Acceptance Rate", value=f"{college['acceptance_rate']}%")
        rates.metric(label="Yield Rate", value=f"{college['yield']}%")

    # Test Scores Section
    with st.expander("📝Test Scores Range", True):
        df = pd.DataFrame(
            [
                [
                    "ACT (English)",
                    college["ACT_english_lower"],
                    college["ACT_english_upper"],
                ],
                ["ACT (Math)", college["ACT_math_lower"], college["ACT_math_upper"]],
                [
                    "ACT (Composite)",
                    college["ACT_composite_lower"],
                    college["ACT_composite_upper"],
                ],
                [
                    "SAT (Reading and Writing)",
                    college["SAT_reading_writing_lower"],
                    college["SAT_reading_writing_upper"],
                ],
                ["SAT (Math)", college["SAT_math_lower"], college["SAT_math_upper"]],
            ],
            columns=["Test", "25th Percentile", "75th Percentile"],
        )
        st.table(df)

    # Application Section
    with st.expander("✉️ Application", True):
        reqs, app, fees = st.columns((3, 2, 2))
        # Requirements
        reqs.markdown("<h5>Application Requirements:</h5>", unsafe_allow_html=True)
        reqs.markdown(f"- TOEFL: <h6>{college['TOEFL']}</h6>", unsafe_allow_html=True)
        reqs.markdown(
            f"- Admission Tests: <h6>{college['admission_test_scores']}</h6>",
            unsafe_allow_html=True,
        )
        reqs.markdown(
            f"- Recommendations: <h6>{college['recommendations']}</h6>",
            unsafe_allow_html=True,
        )
        reqs.write("")
        # Tuition
        app.markdown("<h5>Tution and Fees:</h5>", unsafe_allow_html=True)
        app.metric("In State", f"${'{:,}'.format(int(college['in_state_total']))}")
        app.metric(
            "Out of State", f"${'{:,}'.format(int(college['out_of_state_total']))}"
        )
        # App Fees
        fees.markdown("<h5>Application Fee:</h5>", unsafe_allow_html=True)
        fees.metric(
            "Undergraduate",
            f"${'{:,}'.format(int(college['undergraduate_application_fee']))}",
        )
        fees.metric(
            "Graduate", f"${'{:,}'.format(int(college['graduate_application_fee']))}"
        )

        fees.markdown(
            f"""<button class='st_button' ><a class='anchor' href='https://{college['website']}'>Apply Now 👈</a></button>""",
            unsafe_allow_html=True,
        )

    # Location Section
    if city:
        with st.expander(f"📍 About {city['name']}", True):
            if isinstance(city["name"], str):
                # Indices
                i1, i2 = st.columns(2)
                i1.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Safety Index <span style=''>{city['safety_lvl'] if isinstance(city['safety_lvl'], str) else ''}</span></p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['safety_index']==0 else city['safety_index']}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                i2.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Healthcare Index <span style=''>{city['health_lvl'] if isinstance(city['health_lvl'], str) else ''}</span></p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['health_index']==0 else city['health_index']}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                utils.render_hr("50%")
                # Rent
                r1, r2 = st.columns(2)
                r1.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Rent (1 Bedroom in City Centre)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['1b_rent_cc']==0 else '$'+'{:,}'.format(round(city['1b_rent_cc']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                r2.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Rent (1 Bedroom Out of Centre)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['1b_rent_oc']==0 else '$'+'{:,}'.format(round(city['1b_rent_oc']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                utils.render_hr("50%")
                # Utilities
                u1, u2 = st.columns(2)
                u1.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Basic Utilities (85m<sup>2</sup> Apartment)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['basic_utils_85m2']==0 else '$'+'{:,}'.format(round(city['basic_utils_85m2']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                u2.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>Internet (60Mbps or More)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['internet_60mbps']==0 else '$'+'{:,}'.format(round(city['internet_60mbps']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                utils.render_hr("50%")
                # Food
                m1, m2 = st.columns(2)
                m1.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>A Meal for One (Inexpensive Restaurant)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['meal_inex_rest']==0 else '$'+'{:,}'.format(round(city['meal_inex_rest']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                m2.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <p style='margin:0;'>A Meal for Two (Mid-range Restaurant)</p>
                        <p style='margin:0;font-size:2rem;'>{'N/A' if city['meal_for_two_midrange_rest']==0 else '$'+'{:,}'.format(round(city['meal_for_two_midrange_rest']))}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )
                utils.render_hr("50%")
                # transportation
                t1, t2 = st.columns(2)
                t1.markdown(
                    f"""
                    <div>
                        <p style='margin-bottom:5px;font-size:1.2rem;'> Transportation: </p>
                        <p style='margin:0;'>Gasoline (Per Liter): <b>{'N/A' if city['gas_liter']==0 else '$'+str(round(city['gas_liter'], 2))}</b></p>
                        <p style='margin:0;'>One-Way Ticket (Local Transport): <b>{'N/A' if city['one_way_local_trans']==0 else '$'+str(round(city['one_way_local_trans'], 2))}</b></p>
                        <p style='margin:0 0 10px 0;'>Monthly Pass (Local Transport): <b>{'N/A' if city['monthly_pass_local_trans']==0 else '$'+str(city['monthly_pass_local_trans'])}</b></p>
                    </div>""",
                    unsafe_allow_html=True,
                )

                if isinstance(city["trans_means"], str) or city["trans_means"]:
                    means = json.loads(city["trans_means"].replace("'", '"')) if isinstance(city["trans_means"], str) else city["trans_means"]
                    data, labels = list(means.values()), list(means.keys())
                    fig, ax = plt.subplots(
                        figsize=(6, 3), subplot_kw=dict(aspect="equal")
                    )
                    fig.patch.set_alpha(0)
                    wedges, t, a = ax.pie(data, autopct="%1.0f%%")
                    ax.legend(
                        wedges,
                        labels,
                        loc="center left",
                        bbox_to_anchor=(1, 0, 0.5, 1)
                    )

                    t2.write("Main Transportation Means")
                    t2.pyplot(fig)
                utils.render_hr("50%")
                loc = pd.DataFrame(
                    [list(eval(college["location"]))], columns=["lat", "lon"]
                )
                st.map(loc)
            else:
                st.write("City Data is not Available.")

    st.markdown(
        f"<a style='text-decoration:none;float:right;font-size:1.5em' href='#home'>🔝</a>",
        unsafe_allow_html=True,
    )


def display_application_section(
    toefl, test_scores, recomm, instate, outstate, under_fee, grad_fee, url
):
    with st.expander("✉️ Application", True):
        reqs, app, fees = st.columns((3, 2, 2))
        # Requirements
        reqs.markdown("<h5>Application Requirements:</h5>", unsafe_allow_html=True)
        reqs.markdown(f"- TOEFL: <h6>{toefl}</h6>", unsafe_allow_html=True)
        reqs.markdown(
            f"- Admission Tests: <h6>{test_scores}</h6>",
            unsafe_allow_html=True,
        )
        reqs.markdown(
            f"- Recommendations: <h6>{recomm}</h6>",
            unsafe_allow_html=True,
        )
        reqs.write("")
        # Tuition
        app.markdown("<h5>Tution and Fees:</h5>", unsafe_allow_html=True)
        app.metric("In State", f"${'{:,}'.format(int(instate))}")
        app.metric("Out of State", f"${'{:,}'.format(int(outstate))}")
        # App Fees
        fees.markdown("<h5>Application Fee:</h5>", unsafe_allow_html=True)
        fees.metric(
            "Undergraduate",
            f"${'{:,}'.format(int(under_fee))}",
        )
        fees.metric("Graduate", f"${'{:,}'.format(int(grad_fee))}")

        fees.markdown(
            f"""<button class='st_button' ><a class='anchor' href='https://{url}'>Apply Now 👈</a></button>""",
            unsafe_allow_html=True,
        )
