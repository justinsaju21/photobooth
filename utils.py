from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import numpy as np
import io
import random
import os
import platform

# --- FONT HELPERS ---
def load_font(size=40, font_type="regular", style="Modern Sans"):
    """
    Robust font loading with expanded style support using local assets.
    """
    candidates = []
    
    family = style.lower().strip()
    
    # Map style names to bundled Google Fonts
    if family == "classic serif":
        # System fallbacks for Serif as assets are missing
        candidates.extend(["times.ttf", "Times New Roman.ttf", "georgia.ttf", "Georgia.ttf", "LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
        candidates.append("assets/Lato-Regular.ttf") # Clean fallback
        
    elif family == "retro typewriter":
        candidates.append("assets/CourierPrime-Regular.ttf") # Primary (Exists)
        candidates.extend(["cour.ttf", "Courier New.ttf", "LiberationMono-Regular.ttf"])
        
    elif family == "elegant script":
        candidates.append("assets/GreatVibes-Regular.ttf") # Primary (Exists)
        candidates.extend(["brushsci.ttf", "Brush Script MT.ttf", "LiberationSerif-Italic.ttf"])
        
    elif family == "bold display":
        # System fallbacks for Bold as assets are missing
        candidates.extend(["impact.ttf", "Impact.ttf", "ariblk.ttf", "Arial Bold.ttf", "Verdana Bold.ttf", "LiberationSans-Bold.ttf"])
        candidates.append("assets/Lato-Regular.ttf") # Clean fallback
        
    elif family == "minimal":
        candidates.append("assets/Lato-Regular.ttf") # Primary (Exists - fits Minimal style well)
        candidates.extend(["arial.ttf", "Arial.ttf", "segoeui.ttf", "Calibri.ttf", "LiberationSans-Regular.ttf"])
        
    elif family == "gothic":
        candidates.append("assets/UnifrakturMaguntia-Book.ttf") # Primary (Exists)
        candidates.extend(["oldenglish.ttf", "OldEnglish.ttf", "LiberationSerif-Bold.ttf"])
        
    elif family == "playful":
       candidates.append("assets/PatrickHand-Regular.ttf") # Primary (Exists)
       candidates.extend(["comic.ttf", "Comic Sans MS.ttf", "Chalkboard.ttf", "LiberationSans-Regular.ttf"])

    else:  # "Modern Sans" (default)
        candidates.append("assets/Lato-Regular.ttf")
        candidates.extend(["arial.ttf", "Arial.ttf", "Helvetica.ttf"])

    # Absolute last resort - provide a sensible fallback list
    candidates.extend(["arial.ttf", "Arial.ttf", "georgia.ttf", "times.ttf", "cour.ttf", "segoeui.ttf"])
    
    # Load first available font
    for font_path in candidates:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            continue
    
    return ImageFont.load_default()

def load_emoji_font(size=60):
    """
    Load font capable of rendering emojis, targeting Streamlit Cloud (Linux) specifically.
    """
    emoji_candidates = [
        # Streamlit Cloud / Debian / Ubuntu paths
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
        "/usr/share/fonts/noto/NotoColorEmoji.ttf",
        "NotoColorEmoji.ttf",    
        "AppleColorEmoji.ttf",   
        "seguiemj.ttf",          
        "Symbola.ttf",
        # Fallback to standard fonts that might have some symbols
        "DejaVuSans.ttf",
        "FreeSans.ttf",
        "assets/Lato-Regular.ttf"
    ]
    
    for font_name in emoji_candidates:
        try:
            # Need to specify layout engine for some emoji fonts
            return ImageFont.truetype(font_name, size) 
        except (OSError, IOError):
            continue
            
    return ImageFont.load_default()

# --- FILTER FUNCTIONS ---
# --- FILTER FUNCTIONS ---
# --- PROFESSIONAL FILM STOCK FILTERS ---

def apply_kodak_portra(image):
    # Warm, soft, natural. Rich skin tones.
    gray = ImageOps.grayscale(image)
    # Shadows: Deep Brown, Highlights: Warm Cream
    portra = ImageOps.colorize(gray, "#2D1C10", "#FFF6E5")
    img = Image.blend(image, portra, 0.4)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.05)
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(1.1)

def apply_fuji_velvia(image):
    # High saturation, vivid greens/blues, deep blacks.
    img = image.copy()
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.6)
    # Cool the shadows slightly
    gray = ImageOps.grayscale(image)
    cyan = ImageOps.colorize(gray, "#001A1A", "#FFFFFF")
    return Image.blend(img, cyan, 0.1)

def apply_polaroid_600(image):
    # Faded, warm, slightly blurry, aesthetic.
    gray = ImageOps.grayscale(image)
    # Shadow: Muted Blueish, Highlights: Warm Rose
    polaroid = ImageOps.colorize(gray, "#1A1A2E", "#FFFDF5")
    img = Image.blend(image, polaroid, 0.5)
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.85)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1.1)

def apply_ilford_hp5(image):
    # Classic Grainy B&W
    try:
        img = ImageOps.grayscale(image)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        img = img.convert("RGB")
        
        # Try to add grain, but abort if numpy fails
        try:
            noise = np.random.randint(0, 30, (img.size[1], img.size[0], 3), dtype='uint8')
            noise_img = Image.fromarray(noise).convert("RGB")
            return Image.blend(img, noise_img, 0.1)
        except Exception:
            return img
            
    except Exception:
        return image.convert("RGB")

def apply_cine_teal(image):
    # Teal/Orange Hollywood look
    gray = ImageOps.grayscale(image)
    # Shadows: Deep Teal, Highlights: Hot Orange
    teal_orange = ImageOps.colorize(gray, "#002B36", "#FF8C00")
    img = Image.blend(image, teal_orange, 0.3)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(1.3)

def apply_lomography(image):
    # Yellowish color shift, high contrast
    gray = ImageOps.grayscale(image)
    lomo = ImageOps.colorize(gray, "#2D2D00", "#FFFFD0")
    img = Image.blend(image, lomo, 0.4)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(1.8)

def apply_kodachrome(image):
    # Saturated reds, contrasty vintage magazine look
    img = image.copy()
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    # Red boost
    r, g, b = img.split()
    r = r.point(lambda i: i * 1.1)
    return Image.merge("RGB", (r, g, b))

def apply_dramatic_noir(image):
    # Gritty, deep shadows
    img = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.2)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(0.7).convert("RGB")
# --- FILTER MAPPING ---
FILTER_MAP = {
    "Kodak Portra 400": apply_kodak_portra,
    "Fuji Velvia": apply_fuji_velvia,
    "Polaroid 600": apply_polaroid_600,
    "Ilford HP5 (B&W)": apply_ilford_hp5,
    "Cine-Teal & Orange": apply_cine_teal,
    "Lomography": apply_lomography,
    "Kodachrome": apply_kodachrome,
    "Dramatic Noir": apply_dramatic_noir,
    "Original": lambda x: x
}

def process_image(image, filter_name, flip=False):
    """Process image with cropping, resizing, flipping, and filters"""
    # 1. Normalize to RGB immediately to prevent mode conflicts
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 2. Square Crop
    if image.width != image.height:
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
    
    # 3. Resize
    image = image.resize((600, 600), Image.Resampling.LANCZOS)
    
    # 4. Mirror
    if flip:
        image = ImageOps.mirror(image)

    # 5. Apply Filter using Direct Mapping
    # Default to Original if key missing or partial match failure
    filter_func = FILTER_MAP.get(filter_name)
    
    # Fallback for "Contains" matching if exact key fails (Legacy support)
    if not filter_func:
        name = str(filter_name).lower()
        if "portra" in name: filter_func = apply_kodak_portra
        elif "velvia" in name: filter_func = apply_fuji_velvia
        elif "polaroid" in name: filter_func = apply_polaroid_600
        elif "hp5" in name or "b&w" in name: filter_func = apply_ilford_hp5
        elif "teal" in name: filter_func = apply_cine_teal
        elif "lomo" in name: filter_func = apply_lomography
        elif "kodachrome" in name: filter_func = apply_kodachrome
        elif "noir" in name: filter_func = apply_dramatic_noir
        else: filter_func = lambda x: x

    try:
        return filter_func(image)
    except Exception as e:
        print(f"Filter Error: {e}")
        return image

# --- STICKER ASSETS ---
def draw_pattern(draw, strip_width, strip_height, pattern_type, density):
    """Draw geometric patterns on the strip borders (No Emojis)"""
    if pattern_type == "None":
        return

    num_shapes = int(density * 5) + 10
    
    # Define color palette based on vintage vibe
    colors = ["#D4AF37", "#8B5E3C", "#A52A2A", "#2C3E50", "#E67E22", "#27AE60"]
    
    for _ in range(num_shapes):
        x = random.randint(0, strip_width)
        y = random.randint(0, strip_height)
        
        # Bias towards edges (keep center clear for photos)
        if random.random() > 0.2:
             if random.choice([True, False]):
                x = random.randint(0, 60)
             else:
                x = random.randint(strip_width - 60, strip_width)
        else:
             # Randomly re-roll if it lands in the middle photo area
             if 100 < x < strip_width - 100:
                 continue

        color = random.choice(colors)
        size = random.randint(5, 15)
        
        if pattern_type == "Polka Dots":
            draw.ellipse([x, y, x+size, y+size], fill=color)
            
        elif pattern_type == "Confetti":
            # Random rectangles and triangles
            if random.choice([True, False]):
                draw.rectangle([x, y, x+size, y+size], fill=color)
            else:
                draw.polygon([(x, y), (x+size, y+size), (x-size, y+size)], fill=color)
                
        elif pattern_type == "Stars":
            # Simple Cross/Star shape
            draw.line((x - size, y, x + size, y), fill=color, width=2)
            draw.line((x, y - size, x, y + size), fill=color, width=2)
            
        elif pattern_type == "Minimal Lines":
            # Horizontal dashes near edges
            if x < 100 or x > strip_width - 100:
                draw.line((x, y, x+20, y), fill="#333", width=3)

def create_strip(images, footer_text="Photobooth", frame_style="Cream", text_color="#333", 
                 include_date=False, custom_border_color=None, pattern_type="None", 
                 sticker_density=5, font_style="Modern Sans"):
    """Create the final photo strip with all customizations"""
    photo_w, photo_h = 600, 600
    padding = 50
    header_h = 100
    footer_h = 150
    
    num_photos = len(images)
    strip_w = photo_w + (padding * 2)
    strip_h = header_h + (num_photos * (photo_h + padding)) + footer_h
    
    # Frame color selection
    bg_color = "#F5F1E8"
    if frame_style == "Black":
        bg_color = "#111111"
    elif frame_style == "Film Noir":
        bg_color = "#000000"
    elif frame_style == "Gold":
        bg_color = "#D4AF37"
    elif frame_style == "Rose":
        bg_color = "#FFD1DC"
    elif frame_style == "Neon":
        bg_color = "#1F51FF"
    elif frame_style == "Custom" and custom_border_color:
        bg_color = custom_border_color
        
    strip = Image.new("RGB", (strip_w, strip_h), color=bg_color)
    draw = ImageDraw.Draw(strip)
    
    y_offset = header_h
    
    # Auto-adjust text color for dark frames
    if frame_style in ["Black", "Film Noir"]:
        text_color = "#FFFFFF" if text_color == "#333" else text_color
    
    # Paste photos
    for img in images:
        img = img.resize((photo_w, photo_h))
        if frame_style == "Film Noir":
            img_border = ImageOps.expand(img, border=5, fill="white")
            img_border = img_border.resize((photo_w, photo_h))
            strip.paste(img_border, (padding, y_offset))
        else:
            strip.paste(img, (padding, y_offset))
        y_offset += photo_h + padding

    # Draw Patterns (Replaces Stickers)
    if pattern_type != "None":
        draw_pattern(draw, strip_w, strip_h, pattern_type, sticker_density)

    # Add text with selected font style
    font_title = load_font(60, "title", style=font_style)
    # Ensure footer uses the same decorative style, but regular weight
    font_footer = load_font(40, "regular", style=font_style)
    
    draw.text((strip_w/2, 50), "PHOTOBOOTH", fill=text_color, font=font_title, anchor="mm")
    
    footer_y = strip_h - 100
    draw.text((strip_w/2, footer_y), footer_text, fill=text_color, font=font_footer, anchor="mm")
    
    if include_date:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        # Ensure date also uses the selected style
        draw.text((strip_w/2, footer_y + 50), date_str, fill=text_color, 
                 font=load_font(25, "regular", style=font_style), anchor="mm")
        
    return strip 

def convert_to_bytes(image):
    """Convert PIL image to bytes for download"""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im
