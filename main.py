
import numpy as np
import streamlit as st
import requests
import pandas as pd
import numpy as np
import csv
import pandas as pd
from matplotlib import pyplot as plt


# testdata = pd.read_csv("/Users/rebeccashen/PycharmProjects/dsci551/venv/sortedTop200_copy.csv")
# check = pd.read_csv("/Users/rebeccashen/PycharmProjects/dsci551/venv/checktest.csv")
testdata = pd.read_csv("https://raw.githubusercontent.com/RebeccaSh/USC_DSCI551/main/sortedTop200_copy.csv")
check = pd.read_csv("https://raw.githubusercontent.com/RebeccaSh/USC_DSCI551/main/checktest.csv")


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.header('College project demo' )

# df = pd.DataFrame(
#      np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#      columns=['lat', 'lon'])
#
# st.map(df)

local_css("https://raw.githubusercontent.com/RebeccaSh/USC_DSCI551/main/style.css")

# selected = st.text_input("", "Search...")
# button_clicked = st.button("OK")
#


# Declare a form and call methods directly on the returned object
form = st.form(key='my_form')
form.text_input(label='Enter college name',placeholder="Search...")
submit_button = form.form_submit_button(label='ok')

act_score = [  str(i) for i in range(10,37)]
form_act = st.form(key='act_form')
form_act.selectbox(
     'Your act Score:',(act_score))
form_act.text_input(label='Enter GPA',placeholder="gpa")
submit_button = form_act.form_submit_button(label='sumbit')



st.markdown('<p class="text-small">top 200 college</p>', unsafe_allow_html=True)
option = st.selectbox(
     '',('Ranking', 'Univerity Name', 'City'))
st.write('Sorted By:', option)
st.table(testdata[["rank_display","Institution Name", "UnitID","cityData_Fetcch"]])


#centered
# st.markdown(
#     """<a style='display: block; text-align: center;' href="https://www.example.com/">example.com</a>
#     """,
#     unsafe_allow_html=True,
# )

# st.write(check['College'][0])


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    # text = link.split('=')[1]
    # link = check['Link']
    text = check['College'][0]
    return f'<a target="_blank" href="{link}">{text}</a>'

# link is the column with hyperlinks
check['Link'] = check['Link'].apply(make_clickable)
st.write(check['Link'][0], unsafe_allow_html=True)

# check = check.to_html(escape=False)
# st.write(check, unsafe_allow_html=True)



def get_data(city_id, data_type):
    return requests.get(
        "https://www.numbeo.com/api/"
        + data_type
        + "?api_key=vs1miugk8sz73g&city_id="
        + str(city_id)
    ).json()


# Fetching cost of living data
def get_city_prices(city_id):
    json_data = get_data(city_id, "city_prices")
    df = pd.DataFrame.from_dict(json_data["prices"])
    df["category"] = df["item_name"].str.split(",").str[-1].str.strip()
    df["item"] = df["item_name"].str.split(",").str[:-1].str.join(",").str.strip()
    df = df[["category", "item", "highest_price", "lowest_price", "average_price"]]
    df = df[
        df["category"].isin(
            [
                "Restaurants",
                "Markets",
                "Transportation",
                "Utilities (Monthly)",
                "Rent Per Month",
            ]
        )
    ]

    return {
        "city": json_data["name"],
        "cost of living": df.set_index("category")
        .groupby(level=0)
        .apply(lambda x: x.to_dict("records"))
        .to_dict(),
    }


# Fetching healthcare and safety indices
def get_indices(city_id):
    indices = get_data(city_id, "indices")

    lvls = {
        (0, 20): "Very Low",
        (20, 40): "Low",
        (40, 60): "Moderate",
        (60, 80): "High",
        (80, 100): "Very High",
    }

    safety_idx = round(indices["safety_index"], 2)
    safety_lvl = lvls[list(filter(lambda k: k[0] < safety_idx <= k[1], lvls.keys()))[0]]

    hc_idx = round(indices["health_care_index"], 2)
    hc_lvl = lvls[list(filter(lambda k: k[0] < hc_idx <= k[1], lvls.keys()))[0]]

    return {
        "safety": {"index": safety_idx, "level": safety_lvl},
        "healthcare": {"index": hc_idx, "level": hc_lvl},
    }


# Fetching main transportation means
def get_traffic_data(city_id):
    traffic = get_data(city_id, "city_traffic")
    means = dict(
        filter(lambda i: i[1] > 0, traffic["primary_means_percentage_map"].items())
    )
    return means


# Fetching relevant city data
def get_city_data(city_id):
    traffic = get_traffic_data(city_id)
    indices = get_indices(city_id)
    prices = get_city_prices(city_id)
    city_data = {"transportation_means": traffic, "indices": indices}
    city_data.update(prices)
    return city_data

st.write('primary_means_percentage_map')
st.write(get_traffic_data(3442))

trafficdata = get_traffic_data(3442)

# st.write(key for key,x in trafficdata.items())
labels = [key for key,x in trafficdata.items()]
sizes = [x for key,x in trafficdata.items()]
annotation = [allinfo for allinfo in trafficdata.items()]
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0,0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode,
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

ax1.legend( labels,
          title="City Traffic info",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))


ax1.set_title("Matplotlib bakery: A pie")

st.pyplot(fig1)
