import streamlit as st
from PIL import Image
import os

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Blood Glucose Control Team",
        page_icon="🖼️",
        layout="centered"
    )

    # Streamlit allows to do markdown, which is awesome!

    st.title("Blood Glucose Control with WAT.ai and Gluroo Imaginations Inc")
    st.header("Background ")  # use green colour for 'AI'
    st.write("Diabetes requires a unique way of living. For most, to successfully manage the disease and avoid its long-term adverse effects, you must have detailed fitness and nutrition tracking, not unlike professional athletes or bodybuilders, but with the added complication of knowing how and when to administer insulin. Some can get away without detailed monitoring if they are highly habitual. For most, that’s an undesirable restriction, but where a Person with Diabetes (PWD) falls on that scale is a trade-off that depends on the individual. ")  # use green colour for 'AI'

    # Path to the specific image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "assets", "glucose_logo.png")

    try:
        image = Image.open(image_path)
        st.image(image)

    except FileNotFoundError:
        st.error("Image not found")
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("Blood Glucose Control with WAT.ai")


main()