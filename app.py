import matplotlib.pyplot as plt
import geopandas as gp
import os
import pandas as pd
import requests
from geopandas import GeoDataFrame
from matplotlib.axes import Axes
from pandas import DataFrame

import dataservice
import fips


def _init_matplotlib() -> Axes:
    _, axes = plt.subplots(1, figsize=(24, 12))
    axes.axis("off")
    return axes


def _init_geo_dataframe(shape_file_path: str) -> GeoDataFrame:
    geo_df = gp.read_file(os.path.join(shape_file_path))
    geo_df = geo_df.astype({"STATEFP": int})
    geo_df = geo_df.to_crs(epsg=3395)
    geo_df["COORDS"] = geo_df["geometry"].apply(
        lambda x: x.representative_point().coords[:]
    )
    geo_df["COORDS"] = [coords[0] for coords in geo_df["COORDS"]]
    geo_df = geo_df[geo_df.NAME.isin([code[1] for code in fips.fips_codes])]

    return geo_df


def _get_player_dataframe(data_service) -> DataFrame:
    state_data = data_service.get_data(
        "https://www.basketball-reference.com/friv/high_schools.fcgi", requests
    )

    player_df = pd.DataFrame.from_records(state_data, columns=["STATE", "PLAYER_COUNT"])
    fips_df = pd.DataFrame.from_records(fips.fips_codes, columns=["STATEFP", "STATE"])

    player_df = pd.merge(player_df, fips_df, on=["STATE"])
    return player_df


def plot_all_states(df: DataFrame, **plot_config):
    df.plot(**plot_config)


def plot_quantiles(df: DataFrame, **plot_config):
    df.plot(**plot_config, scheme="quantiles")


def plot_some_states(df: DataFrame, **plot_config):
    df = df[(df.PLAYER_COUNT > 10)]
    df.plot(**plot_config)


def plot_with_labels(df: DataFrame, **plot_config):
    df = df[(df.PLAYER_COUNT > 10)]
    df.plot(**plot_config)

    for idx, row in df.iterrows():
        if row.PLAYER_COUNT >= 100:
            label = f"{row.STATE} ({row.PLAYER_COUNT})"
            plt.text(
                row.COORDS[0], row.COORDS[1], s=label, horizontalalignment="center"
            )


def main(option: int):
    data_root = os.path.join(os.getcwd(), "data")

    shape_file_path = os.path.join(
        os.path.join(data_root, "shp"),
        "cb_2018_us_state_500k",
        "cb_2018_us_state_500k.shp",
    )

    axes = _init_matplotlib()

    plot_config = dict(
        column="PLAYER_COUNT", ax=axes, legend=True, cmap="Oranges", edgecolor="0.8"
    )

    geo_df = _init_geo_dataframe(shape_file_path)
    geo_df = pd.merge(geo_df, _get_player_dataframe(dataservice), on=["STATEFP"])

    if option == 1:
        plot_all_states(geo_df, **plot_config)
    elif option == 2:
        plot_quantiles(geo_df, **plot_config)
    elif option == 3:
        plot_some_states(geo_df, **plot_config)
    elif option == 4:
        plot_with_labels(geo_df, **plot_config)
    else:
        raise ValueError("Invalid option.")

    plt.show()


if __name__ == "__main__":
    choice = 0

    while choice not in range(1, 5):
        print("Welcome! Choose a demo to run: ")
        print("1: Basic chloropeth map.")
        print("2: Chloropeth with quantiles.")
        print("3: Chloropeth with some states removed.")
        print("4: Chloropeth with labels.")

        choice = int(input())

    main(choice)
