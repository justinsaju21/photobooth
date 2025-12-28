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
    
    # Map style names to bundled Google Fonts
    if style == "Classic Serif":
        # System fallbacks for Serif as assets are missing
        candidates.extend(["Times New Roman.ttf", "Georgia.ttf", "LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
        candidates.append("assets/Lato-Regular.ttf") # Clean fallback
        
    elif style == "Retro Typewriter":
        candidates.append("assets/CourierPrime-Regular.ttf") # Primary (Exists)
        candidates.extend(["Courier New.ttf", "LiberationMono-Regular.ttf"])
        
    elif style == "Elegant Script":
        candidates.append("assets/GreatVibes-Regular.ttf") # Primary (Exists)
        candidates.extend(["Brush Script MT.ttf", "LiberationSerif-Italic.ttf"])
        
    elif style == "Bold Display":
        # System fallbacks for Bold as assets are missing
        candidates.extend(["Impact.ttf", "Arial Bold.ttf", "Verdana Bold.ttf", "LiberationSans-Bold.ttf"])
        candidates.append("assets/Lato-Regular.ttf") # Clean fallback
        
    elif style == "Minimal":
        candidates.append("assets/Lato-Regular.ttf") # Primary (Exists - fits Minimal style well)
        candidates.extend(["Calibri.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"])
        
    elif style == "Gothic":
        candidates.append("assets/UnifrakturMaguntia-Book.ttf") # Primary (Exists)
        candidates.extend(["OldEnglish.ttf", "LiberationSerif-Bold.ttf"])
        
    elif style == "Playful":
       candidates.append("assets/PatrickHand-Regular.ttf") # Primary (Exists)
       candidates.extend(["Comic Sans MS.ttf", "Chalkboard.ttf", "LiberationSans-Regular.ttf"])

    else:  # "Modern Sans" (default)
        if font_type == "title":
            candidates.append("assets/Lato-Regular.ttf")
        candidates.append("assets/Lato-Regular.ttf")
        candidates.extend(["Arial.ttf", "LiberationSans-Regular.ttf"])

    # Fallback System Paths (Linux/Windows)
    candidates.extend([
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "FreeSans.ttf"
    ])

    for font_name in candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except (OSError, IOError):
            continue
            
    # Absolute last resort
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
def apply_sepia(image):
    # Authentic Faded Sepia
    gray = ImageOps.grayscale(image)
    # Colorize: Deep brown shadows, warm paper highlights
    sepia = ImageOps.colorize(gray, "#2A1D0D", "#FDF6E3") 
    enhancer = ImageEnhance.Contrast(sepia)
    sepia = enhancer.enhance(0.9)
    enhancer = ImageEnhance.Brightness(sepia)
    return enhancer.enhance(1.05)

def apply_bw(image):
    # High Contrast Silver Gelatin look
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Brightness(gray)
    return enhancer.enhance(1.1)

def apply_warm_retro(image):
    # Warm, slightly overexposed cross-processed look
    gray = ImageOps.grayscale(image)
    warm = ImageOps.colorize(gray, "#2D1C02", "#FFF9E5")
    img = Image.blend(image, warm, 0.6)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.4)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.1)

def apply_grain(image):
    # Faded 70s Newsprint look
    gray = ImageOps.grayscale(image)
    faded = ImageOps.colorize(gray, "#201A15", "#E8D8C8")
    img = Image.blend(image, faded, 0.7)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.7)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.2)

def apply_soft_glow(image):
    # Dreamy, blooming highlights
    glow = image.filter(ImageFilter.GaussianBlur(3))
    img = Image.blend(image, glow, 0.3)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.15)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(0.9)

def apply_cool_cinema(image):
    # Cold Blue Cinema look
    gray = ImageOps.grayscale(image)
    cold = ImageOps.colorize(gray, "#000810", "#E0F0FF") 
    img = Image.blend(image, cold, 0.5)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.2)

def apply_vintage_rose(image):
    # Aesthetics Pink/Rose tint
    gray = ImageOps.grayscale(image)
    rose = ImageOps.colorize(gray, "#2D0A14", "#FFE5E5")
    img = Image.blend(image, rose, 0.4)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(0.9)

def apply_dramatic(image):
    # Gritty, High Contrast Noir
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    img = enhancer.enhance(1.8)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(0.8) 

def process_image(image, filter_name, flip=False):
    """Process image with cropping, resizing, flipping, and filters"""
    # Ensure square crop
    if image.width != image.height:
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
    
    image = image.resize((600, 600))
    
    # Apply mirror if requested
    if flip:
        image = ImageOps.mirror(image)

    # Apply filter
    if filter_name == "Sepia":
        return apply_sepia(image)
    elif filter_name == "Black & White":
        return apply_bw(image)
    elif filter_name == "Warm Retro":
        return apply_warm_retro(image)
    elif filter_name == "1970s Grain":
        return apply_grain(image)
    elif filter_name == "Soft Glow":
        return apply_soft_glow(image)
    elif filter_name == "Cool Cinema":
        return apply_cool_cinema(image)
    elif filter_name == "Vintage Rose":
        return apply_vintage_rose(image)
    elif filter_name == "Dramatic Noir":
        return apply_dramatic(image)
    
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
