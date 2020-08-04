import matplotlib.pyplot as plt
import geopandas as gp
import os
import pandas as pd
import requests

import dataservice
import fips

if __name__ == "__main__":
    data_root = os.path.join(os.getcwd(), "data")
    shape_files_root = os.path.join(data_root, "shp")
    shape_file_collection = "cb_2018_us_state_500k"

    geo_df = gp.read_file(
        os.path.join(
            shape_files_root, shape_file_collection, f"{shape_file_collection}.shp"
        )
    )

    geo_df = geo_df.astype({"STATEFP": int})
    geo_df = geo_df.to_crs(epsg=3395)

    state_data = dataservice.get_data("https://www.basketball-reference.com/friv/high_schools.fcgi", requests)
    player_df = pd.DataFrame.from_records(state_data, columns=["STATE", "PLAYER_COUNT"])
    fips_df = pd.DataFrame.from_records(fips.fips_codes, columns=["STATEFP", "STATE"])

    player_df = pd.merge(player_df, fips_df, on=["STATE"])
    geo_df = pd.merge(geo_df, player_df, on=["STATEFP"])
    geo_df = geo_df[(geo_df.PLAYER_COUNT > 10)]

    geo_df['COORDS'] = geo_df['geometry'].apply(lambda x: x.representative_point().coords[:])
    geo_df['COORDS'] = [coords[0] for coords in geo_df['COORDS']]

    _, ax = plt.subplots(1, figsize=(24, 12))
    ax.axis("off")

    # The line below plots by quantiles (mapclassify).
    # https://github.com/pysal/mapclassify
    #geo_df.plot(column="PLAYER_COUNT", ax=ax, scheme="quantiles", legend=True, cmap="Oranges", edgecolor="0.8")

    # The lines below demonstrate the following:
    #   a. Filtering out states.
    #   b. Labeling states with data.
    geo_df.plot(column="PLAYER_COUNT", ax=ax, legend=True, cmap="Oranges", edgecolor="0.8")

    for idx, row in geo_df.iterrows():
        if row.PLAYER_COUNT >= 100:
            label = f'{row.STATE} ({row.PLAYER_COUNT})'
            plt.text(row.COORDS[0], row.COORDS[1], s=label, horizontalalignment='center')

    plt.show()
