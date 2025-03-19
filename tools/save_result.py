import requests
from metagpt.tools.tool_registry import register_tool
import pandas as pd
from datetime import datetime

@register_tool()
def save_csv(dataframe: pd.DataFrame, title: str) -> str:
    """
    Save the given DataFrame to a CSV file. This is important to ensure that the data is saved and can be accessed later.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        title (str): The title to use for the saved CSV file.
    Returns:
        str: The path to the saved CSV file.
    """
    record_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


    data_dir = f"data/output/csv/analysis_data_{record_time}_{title}.csv"

    dataframe.to_csv(data_dir, index=False)
    print(f"Data saved to {data_dir}")

    return data_dir

@register_tool()
def save_plot_image(plt, title: str) -> str:
    """
    Save the given plot to an image file. This is important to ensure that the plot is saved and can be accessed later.

    Args:
        plt: The plot to save.
        title (str): The title to use for the saved image file.
    Returns:
        str: The path to the saved image file.
    """
    record_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    image_dir = f"data/output/images/plot_{record_time}_{title}.png"

    plt.savefig(image_dir)
    print(f"Image saved to {image_dir}")

    return image_dir