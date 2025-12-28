import streamlit as st
from PIL import Image
import utils

# --- Page Configuration ---
st.set_page_config(
    page_title="Little Vintage Photobooth",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def reset_session():
    st.session_state.captures = []
    st.session_state.temp_image = None
    st.session_state.step = 1
    st.session_state.uploader_key += 1

def get_live_filter_css(filter_name, mirror):
    """Generate CSS for live camera preview with filters and mirroring"""
    transform = "scaleX(-1)" if mirror else "scaleX(1)"
    filters = ""
    
    if filter_name == "Sepia":
        filters = "sepia(0.8) contrast(1.1)"
    elif filter_name == "Black & White":
        filters = "grayscale(1) contrast(1.2)"
    elif filter_name == "Dramatic Noir":
        filters = "grayscale(1) contrast(1.5) brightness(0.9)"
    elif filter_name == "Warm Retro":
        filters = "sepia(0.4) saturate(1.4) contrast(1.05)"
    elif filter_name == "Cool Cinema":
        filters = "contrast(1.1) saturate(0.8) hue-rotate(190deg) sepia(0.3)"
    elif filter_name == "Vintage Rose":
        filters = "contrast(1.1) saturate(1.1) sepia(0.3) hue-rotate(315deg)"
    elif filter_name == "1970s Grain":
        filters = "sepia(0.4) saturate(1.4) contrast(1.1)" 
    elif filter_name == "Soft Glow":
        filters = "brightness(1.1) blur(0.5px) contrast(1.1)"
    else:
        filters = "none"

    return f"""
    <style>
    return f"""
    <style>
        /* Camera Container Sizing - Enforce Square Aspect Ratio on Container */
        div[data-testid="stCameraInput"] {{
            width: 100% !important;
            max-width: 500px !important;
            aspect-ratio: 1 / 1 !important; /* Force square shape on container */
            margin: 0 auto !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 4px solid #333 !important;
            position: relative !important;
            background-color: black !important;
        }}
        
        /* Video - Fill the Square Container */
        div[data-testid="stCameraInput"] video {{
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important; /* Crop to fill square */
            object-position: center center !important; /* Match Python crop */
            transform: {transform} !important;
            filter: {filters} !important;
            -webkit-filter: {filters} !important;
            display: block !important;
        }}
        
        /* Ensure Sidebar Toggle is Visible (Backup to style.css) */
        header[data-testid="stHeader"] {{
            visibility: visible !important;
            background: transparent !important;
            z-index: 99999 !important;
        }}
        header[data-testid="stHeader"] > div:first-child {{
            visibility: visible !important;
        }}
        
        /* Camera Button */
        div[data-testid="stCameraInput"] button {{
            position: absolute !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            z-index: 10 !important;
            color: #ffffff !important;
            background-color: #D4AF37 !important; 
            border: none !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            border-radius: 0 !important; 
            padding: 10px !important;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            div[data-testid="stCameraInput"] {{
                max-width: 90vw !important;
            }}
        }}
        
        @media (max-height: 800px) {{
            div[data-testid="stCameraInput"] {{
                max-height: 60vh !important;
                 max-width: 60vh !important; /* Keep square */
            }}
        }}
    </style>
    """

# --- Session State Init ---
if 'captures' not in st.session_state:
    st.session_state.captures = []
if 'temp_image' not in st.session_state:
    st.session_state.temp_image = None
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

# --- Load Styles ---
load_css("style.css")

# --- Sidebar ---
with st.sidebar:
    st.image("assets/logo.png", use_container_width=True)
    st.markdown("### 🛠️ Booth Settings")
    
    strip_length = st.radio("Photos per Strip:", (3, 4), horizontal=True)
    mirror_mode = st.toggle("Mirror Camera", value=True)
    
    st.markdown("### 🎨 Aesthetics")
    filter_option = st.selectbox(
        "Film Stock:",
        ("Original", "Sepia", "Black & White", "Dramatic Noir", "Warm Retro", "Cool Cinema", "Vintage Rose", "1970s Grain", "Soft Glow"),
        index=4
    )
    
    st.markdown("### ✍️ Customization")
    frame_style = st.selectbox("Frame Style:", ("Cream", "Black", "Film Noir", "Gold", "Rose", "Neon", "Custom"))
    
    custom_border_color = None
    if frame_style == "Custom":
        custom_border_color = st.color_picker("Border Color", "#FCFAF6")

    st.markdown("### 🔤 Typography")
    font_style = st.selectbox(
        "Font Style:", 
        ("Modern Sans", "Classic Serif", "Retro Typewriter", "Elegant Script", "Bold Display", "Minimal"),
        index=0
    )

    # --- Sticker Feature ---
    st.markdown("### ✨ Decoration")
    sticker_pack = st.selectbox("Sticker Pack:", ["None", "Classic ❤️", "Vintage 🎞️", "Party 🎉", "Nature 🌸", "Love 💌", "Spooky 👻"])
    custom_sticker = st.text_input("Custom Emojis:", placeholder="🐶,🎉,💕 (comma-separated)")
    sticker_density = st.slider("Decor Intensity:", 1, 10, 3)

    st.markdown("### 📝 Strip Footer")
    footer_text = st.text_input("Footer Text:", value="Little Vintage Photobooth")
    
    col_c1, col_c2 = st.columns([1, 3])
    with col_c1:
        text_color = st.color_picker("Text Color", "#303030")
    with col_c2:
        include_date = st.checkbox("Include Date", value=False)
        
    st.markdown("---")
    if st.button("🔄 Reset / New Session", type="primary", use_container_width=True):
        reset_session()
        st.rerun()

# --- Inject Live Filter CSS ---
st.markdown(get_live_filter_css(filter_option, mirror_mode), unsafe_allow_html=True)

# --- Main Layout ---
spacer_l, center_col, spacer_r = st.columns([1, 2, 1])

with center_col:
    st.markdown('<h1 class="main-title">Vintage Photobooth</h1>', unsafe_allow_html=True)
    
    needed_photos = strip_length
    current_count = len(st.session_state.captures)
    
    if current_count < needed_photos:
        # --- CAPTURE PHASE ---
        st.markdown(f"""
            <div class="booth-status">
                Pose {current_count + 1} / {needed_photos}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="booth-container">', unsafe_allow_html=True)
        
        # Check if we have a pending image to review
        if st.session_state.temp_image:
             # --- REVIEW STEP (WYSIWYG) ---
             review_img = utils.process_image(st.session_state.temp_image, filter_option, flip=mirror_mode)
             st.image(review_img, caption="Does this look good?", use_container_width=True)
             
             col_rev1, col_rev2 = st.columns(2)
             with col_rev1:
                 if st.button("❌ Retake", use_container_width=True):
                     st.session_state.temp_image = None
                     st.session_state.uploader_key += 1
                     st.rerun()
             with col_rev2:
                 if st.button("✅ Keep It", type="primary", use_container_width=True):
                     st.session_state.captures.append(st.session_state.temp_image)
                     st.session_state.temp_image = None
                     st.session_state.uploader_key += 1
                     st.rerun()
        else:
            # --- CAMERA INPUT ---
            tab1, tab2 = st.tabs(["📷 Camera", "📤 Upload"])
            
            with tab1:
                camera_key = f"cam_{current_count}_{st.session_state.uploader_key}"
                photo = st.camera_input("Pose!", key=camera_key, label_visibility="collapsed")
                
                if photo:
                    st.session_state.temp_image = Image.open(photo)
                    st.rerun()
                    
            with tab2:
                upload_key = f"uploader_{st.session_state.uploader_key}"
                uploaded = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'], key=upload_key, label_visibility="collapsed")
                
                if uploaded:
                    try:
                        img = Image.open(uploaded)
                        st.session_state.temp_image = img
                        st.rerun()
                    except Exception as e:
                        st.error("Error loading image. Try another one.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # --- RESULT PHASE ---
        st.markdown(f"""
            <div class="booth-status" style="background-color: #2C2C2C; color: #D4AF37;">
                Strip Ready
            </div>
        """, unsafe_allow_html=True)
        
        # Process Captures
        processed_captures = []
        for img in st.session_state.captures:
            processed_captures.append(utils.process_image(img, filter_option, flip=mirror_mode))
            
        final_strip = utils.create_strip(
            processed_captures, 
            footer_text=footer_text, 
            frame_style=frame_style,
            text_color=text_color,
            include_date=include_date,
            custom_border_color=custom_border_color,
            sticker_pack=sticker_pack,
            custom_stickers=custom_sticker,
            sticker_density=sticker_density,
            font_style=font_style
        )
        
        st.image(final_strip, caption=f"{filter_option} • {frame_style} • {sticker_pack}", use_container_width=True)
        
        # Controls
        c1, c2 = st.columns(2)
        with c1:
            strip_bytes = utils.convert_to_bytes(final_strip)
            st.download_button(
                label="⬇️ Download Strip",
                data=strip_bytes,
                file_name="photobooth_strip.png",
                mime="image/png",
                use_container_width=True
            )
        with c2:
             if st.button("✨ New Session", use_container_width=True):
                reset_session()
                st.rerun()
