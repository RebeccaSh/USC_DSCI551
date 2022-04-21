import streamlit as st
import json
import pandas as pd
import numpy as np
import city_data


def set_state(state, value):
    st.session_state[state] = value


def get_json(filepath):
    with open(filepath) as json_data:
        return json.load(json_data)


def get_hr(w="100%"):
    return f"""<hr style="margin:auto;border-bottom: 1px solid rgba(49, 51, 63, 0.2);width:{w}" /> """


def render_hr(w="100%"):
    st.markdown(
        get_hr(w),
        unsafe_allow_html=True,
    )


from firebase_admin import firestore


def get_colleges_data():
    db = firestore.Client.from_service_account_json("./resources/firestore-key.json")
    try:

        colleges = list(db.collection("collegess").stream())

        colleges_dict = list(map(lambda x: x.to_dict(), colleges))
        df = pd.DataFrame(colleges_dict)
        if df.empty:
            df = pd.read_csv("./resources/colleges_data.csv")
    except:
        print("oopsy")
        df = pd.read_csv("./resources/colleges_data.csv")

    dummy_row = df.loc[1].copy()
    dummy_row["id"] = 0
    dummy_row["institution"] = "Select College..."
    dummy_row["rank"] = 0
    df.loc[-1] = dummy_row
    columns_by_type = df.columns.to_series().groupby(df.dtypes).groups
    for col in columns_by_type[np.dtype(object)]:
        df[col] = df[col].astype("string")
    return df.set_index("id").sort_index()


def show_home():
    set_state("show_explore", False)
    set_state("show_summary", False)
    set_state("show_recommender", False)
    set_state("show_home", True)


def show_explore():
    set_state("show_home", False)
    set_state("show_summary", False)
    set_state("show_recommender", False)
    set_state("show_explore", True)


def show_summary():
    set_state("show_home", False)
    set_state("show_explore", False)
    set_state("show_recommender", False)
    set_state("show_summary", True)


def show_recommender():
    set_state("show_home", False)
    set_state("show_summary", False)
    set_state("show_explore", False)
    set_state("ML_btn", False)
    set_state("show_recommender", True)
    set_state("rec_college", None)


import colleges_explorer


def reset_filters():
    data = st.session_state.data
    set_state("public", True)
    set_state("private", True)
    set_state("graduate", False)
    set_state("distant", False)

    set_state("recom", [])
    set_state("tests", [])
    set_state("toefl", [])

    set_state("states", [])
    set_state("urban", [])

    set_state("tuition", int(data["out_of_state_total"].max()))
    set_state("acc_rate", 0)
    set_state("grad_rate", 0)

    set_state(
        "sat_rw",
        data[data["SAT_reading_writing_lower"] > 0]["SAT_reading_writing_lower"].min(),
    )
    set_state("sat_m", data[data["SAT_math_lower"] > 0]["SAT_math_lower"].min())
    set_state("act_e", data[data["ACT_english_lower"] > 0]["ACT_english_lower"].min())
    set_state("act_m", data[data["ACT_math_lower"] > 0]["ACT_math_lower"].min())
    set_state(
        "act_c", data[data["ACT_composite_lower"] > 0]["ACT_composite_lower"].min()
    )


def get_header(text):
    return (
        "<h2 style='margin-top: -0.5rem;padding:0;text-align:center'>" + text + "</h2>"
    )


def get_city_data(id):
    city = city_data.fetch(id)
    if not city:
        try:
            city = st.session_state.cities[st.session_state.cities["id"] == id].to_dict(
                "records"
            )[0]
        except:
            city = None
    return city
