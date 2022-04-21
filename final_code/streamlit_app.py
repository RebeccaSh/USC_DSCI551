import streamlit as st
import config
import utils
import data_summary
import find_colleges
import colleges_explorer

config.setup()

ss = st.session_state

# home page
if ss.show_home:
    with st.container():
        # title
        st.markdown(
            "<h1 style='text-align:center;'>College Admission Advisor</h1>",
            unsafe_allow_html=True,
        )
        # welcome message
        st.write(
            """
            Hello prospective student 👋 
            This data application is designed to help you explore colleges and their neighborhoods across the United States.
            It also provides you with a college recommendations tool based on your preferences and academic standing.
            """
        )

        # app features icons, desc, navs
        lm, feat1, mm, feat2, m, feat3, rm = st.columns((1, 4, 1, 4, 1, 4, 1))

        feat1.markdown(ss.summary_img, unsafe_allow_html=True)
        feat1.button("About the Data", on_click=utils.show_summary)
        feat1.write("Learn more about the data sources used in this application.")
        feat1.markdown(utils.get_hr(), unsafe_allow_html=True)

        feat2.markdown(ss.recom_img, unsafe_allow_html=True)
        feat2.button("Find Colleges", on_click=utils.show_recommender)
        feat2.write("Find colleges that are compatable with your academic standing.")
        feat2.markdown(utils.get_hr(), unsafe_allow_html=True)

        feat3.markdown(ss.explore_img, unsafe_allow_html=True)
        feat3.button("Explore Colleges", on_click=utils.show_explore)
        feat3.write("Search and filter colleges based on various attributes and view their profile.")
        feat3.markdown(utils.get_hr(), unsafe_allow_html=True)

# data summary page
if ss.show_summary:
    with st.container():
        data_summary.setup()

# recommender page
if ss.show_recommender:
    with st.container():
        find_colleges.setup()

# college explorer page
if ss.show_explore:
    with st.container():
        colleges_explorer.setup()