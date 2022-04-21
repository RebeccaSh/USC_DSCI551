import streamlit as st
import utils
import base64
import pandas as pd


def setup():
    # page configs
    st.set_page_config(page_title="CAA", page_icon="📖", layout="wide")
    # styling
    st.markdown(
        """
        <style>
            div.row-widget.stRadio > div{flex-direction:row;}
            div.row-widget.stRadio > div > label{padding-right:10px;}
            .block-container{padding-top: 1.5rem;padding-bottom: 2.5rem;}
            footer {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            h3  a {text-decoration:None;color:white !important;}
            .metric-container {text-align:center;}
            tbody th {display:none;}
            .blank {display:none;}
            div[row-group="rowgroup"]: {display:none;}
            section[data-testid='stSidebar'] > div:first-child {padding: 2rem 1rem; width: 11rem;}
            section[data-testid='stSidebar']  button {width: 100% !important;}
            .row_heading.level0 {display:none; width:0px;}
                .row_heading.level0 > div {display:none; width:0px;}
                .table-top-right {left:0 !important;width:100% !important;}
                .table-bottom-right {left:0 !important;width:100% !important;}
                .blank {display:none;}
            .st_button {
                display: inline-flex;
                -webkit-box-align: center;
                align-items: center;
                -webkit-box-pack: center;
                justify-content: center;
                font-weight: 400;
                padding: 0;
                border-radius: 0.25rem;
                margin: 0px;
                line-height: 1.6;
                color: inherit;
                width:100% !important;
                user-select: none;
                background-color: rgb(43, 44, 54);
                border: 1px solid rgba(250, 250, 250, 0.2);
            }
            .st_button:hover {
                border-color: rgb(255, 75, 75);
                color: rgb(255, 75, 75);
            }
            .st_button:focus:not(:active) {
                border-color: rgb(255, 75, 75);
                color: rgb(255, 75, 75);
            }
            .st_button:active {
                color: rgb(255, 255, 255);
                border-color: rgb(255, 75, 75);
                background-color: rgb(255, 75, 75);
            }
            .st_button:focus {
                box-shadow: rgb(255 75 75 / 50%) 0px 0px 0px 0.2rem;
                outline: none;
            }
            .st_button > a {
                text-decoration:none !important;
                color:white !important;
                width:100% !important;
                padding: 0.25rem 0.75rem !important;
            }
            .st_button > a:hover {
                text-decoration:none !important;
            }

            .row-widget.stButton > button {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
            *{
                box-sizing: border-box;
                -webkit-box-sizing: border-box;
                -moz-box-sizing: border-box;
            }


            /* Table Styles */

            .table-wrapper{
                margin:0 0 15px 0;
                box-shadow: 0px 35px 50px rgba( 0, 0, 0, 0.2 );
                table-layout:fixed;
                overflow-y:auto;
            }

            .fl-table {
                font-size: 14px;
                font-weight: normal;
                border: none;
                border-collapse: collapse;
                width: 100%;
                max-width: 100%;
                white-space: nowrap;
                background-color: white;
            }

            .fl-table td, .fl-table th {
                text-align: center;
                padding: 8px;
            }

            .fl-table td {
                border-right: 1px solid #f8f8f8;
                font-size: 14px;
                color:black;
                white-space: pre-wrap;
            }

            .fl-table thead th {
                color: #ffffff;
                background: #227a61;
            }


            .fl-table thead th:nth-child(odd) {
                color: #ffffff;
                background: #182b3d;
            }

            .fl-table tr:nth-child(even) {
                background: #F8F8F8;
            }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # top of page hook
    st.markdown("<span id='home'></span>", unsafe_allow_html=True)

    # init state once
    if "setup" not in st.session_state:
        init_state()
        utils.set_state("setup", True)


def load_image(img):
    return "<img style='display: block; margin-left: auto; margin-right: auto; width: 80%; padding-bottom:1rem;' src='data:image/png;base64,{}' class='img-fluid'>".format(
        base64.b64encode(bytearray(open("resources/" + img, "rb").read())).decode()
    )


def init_state():
    # App Content
    utils.set_state("data", utils.get_colleges_data()[1:])
    utils.set_state("cities", pd.read_csv("./resources/cities_data.csv"))
    utils.set_state("lookup", utils.get_colleges_data())
    utils.set_state("search_result", [])
    utils.set_state("college", None)
    utils.set_state("city", None)
    utils.set_state("rec_college", None)
    utils.set_state("rec_result", None)
    utils.set_state("cid", 0)

    # App Nav Flags
    utils.set_state("show_home", True)
    utils.set_state("show_profile", False)
    utils.set_state("show_summary", False)
    utils.set_state("show_explore", False)
    utils.set_state("show_recommender", False)
    utils.set_state("ML_btn", False)
    utils.set_state("first_ml_run", False)

    # Loading App Imgs
    utils.set_state("summary_img", load_image("data.png"))
    utils.set_state("recom_img", load_image("search.png"))
    utils.set_state("explore_img", load_image("explore.png"))

    # init filters
    utils.reset_filters()
