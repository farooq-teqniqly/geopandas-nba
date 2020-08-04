import matplotlib.pyplot as plt
import geopandas as gp
import os

if __name__ == "__main__":
    data_root = os.path.join(os.getcwd(), "data")
    shape_files_root = os.path.join(data_root, "shp")
    shape_file_collection = "cb_2018_us_state_500k"

    geo_df = gp.read_file(
        os.path.join(
            shape_files_root, shape_file_collection, f"{shape_file_collection}.shp"
        )
    )
    geo_df = geo_df.to_crs(epsg=3857)

    _, ax = plt.subplots(1, figsize=(60, 20))
    geo_df.plot(ax=ax)
    plt.show()
