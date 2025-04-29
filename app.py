import streamlit as st
from PIL import Image

st.title("📸 Image Pixelization Demo (Custom Width & Height in cm)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # DPI input for cm↔px conversion
    dpi = st.number_input(
        "DPI (dots per inch)",
        min_value=10,
        max_value=1200,
        value=96,
        step=1,
        help="Convert between pixels and cm (1in = 2.54cm)."
    )

    # Pixel block size in cm (square)
    pixel_cm = st.number_input(
        "Pixel block size (cm)",
        min_value=0.1,
        max_value=20.0,
        value=1.0,
        step=0.1,
        help="Physical size of each square pixel block."
    )

    # Output dimensions in cm
    default_w = round(image.width * 2.54 / dpi, 1)
    default_h = round(image.height * 2.54 / dpi, 1)
    width_cm = st.number_input(
        "Output width (cm)",
        min_value=1.0,
        max_value=200.0,
        value=default_w,
        step=0.5,
        help="Physical width of the output image."
    )
    height_cm = st.number_input(
        "Output height (cm)",
        min_value=1.0,
        max_value=200.0,
        value=default_h,
        step=0.5,
        help="Physical height of the output image."
    )

    # Convert cm to px
    pixel_size = max(1, int(pixel_cm * dpi / 2.54))
    output_width = max(1, int(width_cm * dpi / 2.54))
    output_height = max(1, int(height_cm * dpi / 2.54))

    st.write(f"🔢 Pixel block: **{pixel_size}px** (≈{pixel_cm}cm)")
    st.write(f"🔢 Output dimensions: **{output_width}px** × **{output_height}px** (≈{width_cm}cm × {height_cm}cm)")

    # Pixelation: resize → downscale → upscale
    resized = image.resize((output_width, output_height), Image.NEAREST)
    small_w = max(1, output_width // pixel_size)
    small_h = max(1, output_height // pixel_size)
    pixelated = (
        resized
        .resize((small_w, small_h), Image.NEAREST)
        .resize((output_width, output_height), Image.NEAREST)
    )

    st.subheader("Pixelated Image")
    st.image(pixelated, use_container_width=True)


# # Instructions
# st.markdown("""
# ---
# **How to run this demo:**
# 1. Save this code as `app.py`.
# 2. Install dependencies: `pip install streamlit pillow`.
# 3. Run: `streamlit run app.py`.
# """)
