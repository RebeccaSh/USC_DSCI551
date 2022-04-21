import requests
import pandas as pd
import sys


def get_data(city_id, data_type):
    return requests.get(
        "https://www.numbeo.com/api/"
        + data_type
        + "?api_key=vs1miugk8sz73g&city_id="
        + str(city_id)
    ).json()


# Fetching cost of living data
def get_city_prices(city_id):
    data = get_data(city_id, "city_prices")
    df = pd.DataFrame.from_dict(data["prices"])
    prices = None
    if "item_name" in df.columns:
        df["category"] = df["item_name"].str.split(",").str[-1].str.strip()
        df["item"] = df["item_name"].str.split(",").str[:-1].str.join(",").str.strip()
        df = df[["category", "item", "average_price"]]
        df = df[
            df["category"].isin(
                [
                    "Restaurants",
                    "Transportation",
                    "Utilities (Monthly)",
                    "Rent Per Month",
                ]
            )
        ]

        prices = {"city": data["name"]}
        prices.update(
            df.set_index("category")
            .groupby(level=0)
            .apply(lambda x: x.to_dict("records"))
            .to_dict()
        )
    return prices


def get_index(index, indices):
    return round(indices[index], 2) if index in indices else None


# Fetching general indices
def get_indices(city_id):
    indices = get_data(city_id, "indices")
    return {
        "life_quality": get_index("quality_of_life_index", indices),
        "safety": get_index("safety_index", indices),
        "health": get_index("health_care_index", indices),
        "traffic": get_index("traffic_index", indices),
    }


# Fetching transportation means
def get_transportation_means(city_id):
    data = get_data(city_id, "city_traffic")
    return (
        dict(
            filter(
                lambda i: i[1] > 0,
                {
                    k: round(v)
                    for k, v in dict(
                        data["primary_means_percentage_map"].items()
                    ).items()
                }.items(),
            )
        )
        if "primary_means_percentage_map" in data.keys()
        else None
    )


# def filter_data(data):
#     data["Rent Per Month"] = list(
#         filter(lambda i: "1 bedroom" in i["item"], data["Rent Per Month"])
#     )
#     data["Rent Per Month"] = dict(
#         map(
#             lambda i: (i["item"].split(")")[1], round(i["average_price"] / 10) * 10),
#             data["Rent Per Month"],
#         )
#     )
#     data["Transportation"] = list(
#         filter(
#             lambda i: any(
#                 substring in i["item"]
#                 for substring in ["One-way", "Gasoline", "Monthly Pass"]
#             ),
#             data["Transportation"],
#         )
#     )
#     data["Transportation"] = dict(
#         map(lambda i: (i["item"], round(i["average_price"], 2)), data["Transportation"])
#     )
#     data["Utilities (Monthly)"] = list(
#         filter(
#             lambda i: any(
#                 substring in i["item"] for substring in ["Basic", "Internet"]
#             ),
#             data["Utilities (Monthly)"],
#         )
#     )
#     data["Utilities (Monthly)"] = dict(
#         map(
#             lambda i: (i["item"], round(i["average_price"])),
#             data["Utilities (Monthly)"],
#         )
#     )
#     data["Restaurants"] = list(
#         filter(
#             lambda i: any(
#                 substring in i["item"]
#                 for substring in ["Inexpensive Restaurant", "Mid-range Restaurant"]
#             ),
#             data["Restaurants"],
#         )
#     )
#     data["Restaurants"] = dict(
#         map(lambda i: (i["item"], round(i["average_price"], 2)), data["Restaurants"])
#     )

#     return data


def get_value(obj, category, item, dec):
    price = 0
    if category in obj.keys():
        lst = list(filter(lambda i: i["item"] == item, obj[category]))
        price = lst[0]["average_price"] if lst else 0
    return price


def get_idx_lvl(idx):
    lvls = {
        (-1, 0): "",
        (0, 20): "(Very Low)",
        (20, 40): "(Low)",
        (40, 60): "(Moderate)",
        (60, 80): "(High)",
        (80, 100): "(Very High)",
    }

    return (
        lvls[list(filter(lambda k: k[0] < round(idx, 2) <= k[1], lvls.keys()))[0]]
        if idx
        else None
    )


# Fetching relevant city data
def fetch(city_id):
    traffic = get_transportation_means(city_id)
    indices = get_indices(city_id)
    prices = None
    try:
        prices = get_city_prices(city_id)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

    city = (
        {
            "id": city_id,
            "name": prices["city"] if "city" in prices.keys() else None,
            "safety_index": indices["safety"],
            "health_index": indices["health"],
            "1b_rent_oc": get_value(
                prices, "Rent Per Month", "Apartment (1 bedroom) Outside of Centre", 0
            ),
            "1b_rent_cc": get_value(
                prices, "Rent Per Month", "Apartment (1 bedroom) in City Centre", 0
            ),
            "basic_utils_85m2": get_value(
                prices,
                "Utilities (Monthly)",
                "Basic (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment",
                2,
            ),
            "internet_60mbps": get_value(
                prices,
                "Utilities (Monthly)",
                "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)",
                0,
            ),
            "trans_means": traffic,
            "gas_liter": get_value(prices, "Transportation", "Gasoline (1 liter)", 3),
            "monthly_pass_local_trans": get_value(
                prices, "Transportation", "Monthly Pass (Regular Price)", 3
            ),
            "one_way_local_trans": get_value(
                prices, "Transportation", "One-way Ticket (Local Transport)", 2
            ),
            "meal_for_two_midrange_rest": get_value(
                prices,
                "Restaurants",
                "Meal for 2 People, Mid-range Restaurant, Three-course",
                0,
            ),
            "meal_inex_rest": get_value(
                prices, "Restaurants", "Meal, Inexpensive Restaurant", 0
            ),
            "safety_lvl": get_idx_lvl(indices["safety"]),
            "health_lvl": get_idx_lvl(indices["health"]),
        }
        if prices
        else None
    )
    return city