import streamlit as st

import numpy as np
import yaml
from typing import Tuple


@st.cache_data
def generate_logo(
    app_name: str,
    size: Tuple[int, int] = (256, 256),
) -> np.ndarray:
    """Generate a circular logo with the first letter of the app name.

    Parameters
    ----------
    size : Tuple[int, int]
        Width and height of the output image in pixels
    app_name : str
        Name of the app to generate logo for

    Returns
    -------
    np.ndarray
        RGBA image array with transparent background
    """
    from PIL import Image, ImageDraw, ImageFont

    # Create a blank image with transparent background
    logo = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    logo[:, :, 3] = 0  # Set alpha channel to fully transparent

    # Create PIL Image
    image = Image.fromarray(logo)
    draw = ImageDraw.Draw(image)

    # Use Streamlit's blue color scheme
    fill_color = (28, 131, 255, int(255 * 0.1))  # RGB values from the badge background
    text_color = (0, 84, 163, 255)  # RGB values from the badge text

    # Draw circle
    circle_bbox = [2, 2, size[0] - 2, size[1] - 2]  # Leave 2px border
    draw.ellipse(circle_bbox, fill=fill_color)  # Add alpha=255

    # Add first letter
    first_letter = app_name[0].upper()
    font_size = int(min(size) * 0.6)
    font = ImageFont.load_default().font_variant(size=font_size)

    # Center the letter
    text_bbox = draw.textbbox((0, 0), first_letter, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (size[0] - text_w) // 2
    text_y = (size[1] - text_h) // 2 - text_h // 3  # Shift up by 1/4 of text height

    draw.text((text_x, text_y), first_letter, fill=text_color, font=font)

    return np.array(image)


def read_app_name() -> str:
    """Read the app name from the snowflake.yml file."""
    with open("snowflake.yml", "r") as f:
        config = yaml.safe_load(f)
        return list(config["entities"].keys())[0]


APP_NAME = read_app_name().title()
APP_LOGO = generate_logo(app_name=APP_NAME)
