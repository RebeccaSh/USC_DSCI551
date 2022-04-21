import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import joblib
import argparse


def main(args):
    # parsing input
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--scores", type=float)
    # parser.add_argument("--input-rate", type=float, nargs=5)  # --input-rate 1 2 3 4 5
    # parser.add_argument("--k", type=int, default=7)
    # args = parser.parse_args()
    
    # print(args)
    # return None
    df = pd.read_csv(r"resources/colleges_data.csv")

    # select useful columns and replace None to 0
    df = df[
        [
            "id",
            "SAT_reading_writing_upper",
            "ACT_english_upper",
            "SAT_reading_writing_lower",
            "ACT_english_lower",
            "SAT_math_upper",
            "ACT_math_upper",
            "SAT_math_lower",
            "ACT_math_lower",
            "acceptance_rate",
        ]
    ]
    for index, line in df.iterrows():
        if line["SAT_reading_writing_upper"] == 0:
            df.at[index, "SAT_reading_writing_upper"] = (
                line["ACT_english_upper"] / 36 * 800
            )

        if line["SAT_reading_writing_lower"] == 0:
            df.at[index, "SAT_reading_writing_lower"] = (
                line["ACT_english_lower"] / 36 * 800
            )

        if line["SAT_math_upper"] == 0:
            df.at[index, "SAT_math_upper"] = line["ACT_math_upper"] / 36 * 800

        if line["SAT_math_lower"] == 0:
            df.at[index, "SAT_math_lower"] = line["ACT_math_lower"] / 36 * 800

        if line["ACT_english_upper"] == 0:
            df.at[index, "ACT_english_upper"] = (
                line["SAT_reading_writing_upper"] / 800 * 36
            )

        if line["ACT_english_lower"] == 0:
            df.at[index, "ACT_english_lower"] = (
                line["SAT_reading_writing_lower"] / 800 * 36
            )

        if line["ACT_math_upper"] == 0:
            df.at[index, "ACT_math_upper"] = line["SAT_math_upper"] / 800 * 36

        if line["ACT_math_lower"] == 0:
            df.at[index, "ACT_math_lower"] = line["SAT_math_lower"] / 800 * 36
    # sat&act reading to percentage
    df = df.assign(
        reading_pc=(
            (df["SAT_reading_writing_upper"] + df["SAT_reading_writing_lower"])
            / 2
            / 800
            + (df["ACT_english_lower"] + df["ACT_english_upper"]) / 2 / 36
        )
        / 2
    )
    # sat&act math  to percentage
    df = df.assign(
        math_pc=(
            (df["SAT_math_upper"] + df["SAT_math_lower"]) / 2 / 800
            + (df["ACT_math_lower"] + df["ACT_math_upper"]) / 2 / 36
        )
        / 2
    )
    df = df.assign(pc=(df["reading_pc"] + df["math_pc"]) / 2)
    # percentage of scores, and its acceptance rate
    # total_pc = df[['reading_pc','math_pc','acceptance_rate']].values
    total_pc = df[["pc", "acceptance_rate"]].values

    # Machine Learning normalization
    X = np.array(total_pc)
    norm = MinMaxScaler().fit(X)
    X = norm.transform(X)
    # Machine Learning process
    kmeans = joblib.load("ml_model/mlmodel.pkl")
    # kmeans = KMeans(n_clusters=args.k, random_state=0).fit(X)

    # label = kmeans.labels_

    y_km = kmeans.fit_predict(X)  # clusters'labels of all insititution

    # Save the model
    # joblib.dump(kmeans,'mlmodel.pkl')

    # list of insitution name of clusters
    clusters = y_km.tolist()
    mycluster = [list() for _ in range(0, args["k"])]
    # index start from 1 (e.g., cluster1 == mycluster [1]) do not use mycluster [0]
    for i in range(0, len(clusters)):
        mycluster[clusters[i]].append(df.iloc[i]["id"])

    # process input SAT/ACT scores, convert to decimal/percentage format
    input_scores = 0  # default 0
    if args["scores"] in range(1, 37):
        input_scores = args["scores"] / 36
    elif args["scores"] in range(100, 1601):
        input_scores = args["scores"] / 1600
    else:
        input_scores = 0
    input_rate = args["input_rate"]
    # ML predict and output recommend insititution
    predict_result = kmeans.predict(
        [
            [
                input_scores,
                accept_rate(
                    input_rate[0],
                    input_rate[1],
                    input_rate[2],
                    input_rate[3],
                    input_rate[4],
                ),
            ]
        ]
    )
    # print("Cluster" + str(predict_result))
    # print(
    #     input_scores,
    #     accept_rate(
    #         input_rate[0], input_rate[1], input_rate[2], input_rate[3], input_rate[4]
    #     ),
    # )
    # print(mycluster[int(predict_result)])

    return (
        input_scores,
        accept_rate(
            input_rate[0], input_rate[1], input_rate[2], input_rate[3], input_rate[4]
        ),
        mycluster[int(predict_result)],
    )
    # ML Graph

    colors = [
        "lightgreen",
        "orange",
        "lightblue",
        "lightpink",
        "yellow",
        "green",
        "purple",
    ]
    for i in range(0, args["k"]):
        plt.scatter(
            X[y_km == i, 0],
            X[y_km == i, 1],
            s=50,
            c=colors[i % len(colors)],
            marker="v",
            edgecolor="black",
            label="cluster " + str(i),
        )

    # plot the centroids
    plt.scatter(
        kmeans.cluster_centers_[:, 0],
        kmeans.cluster_centers_[:, 1],
        s=250,
        marker="*",
        c="red",
        edgecolor="black",
        label="centroids",
    )

    plt.legend(scatterpoints=1)
    plt.grid()
    # uncomment the next line to show the graph
    # plt.show()


# acceptance rate calculation
def accept_rate(gpa, awards, leadership, scholarship, ap):
    gpa = min(4.0, max(0.0, gpa))
    df = pd.read_csv(r"resources/colleges_data.csv")
    school_arate = df.loc[:, ["acceptance_rate"]].fillna(0)
    rate = 20
    # pc:percentage
    # assume the full score of gpa=4,awards=1,leadership=3,scholarsp=3,ap=5)
    gpapc = gpa / 4 * rate

    if awards >= 1:
        awardspc = rate
    else:
        awardspc = 0
    if leadership >= 3:
        leadershippc = rate
    else:
        leadershippc = leadership / 3 * rate
    if scholarship >= 3:
        scholarshippc = rate
    else:
        scholarshippc = scholarship / 3 * rate
    if ap >= 5:
        appc = rate
    else:
        appc = ap / 5 * rate

    accp_rate = gpapc + awardspc + leadershippc + scholarshippc + appc
    accp_rate = 100 - accp_rate
    return accp_rate * 0.01


if __name__ == "__main__":
    main()
