from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import numpy as np
import io
import random
import os
import platform

# --- FONT HELPERS ---
def load_font(size=40, font_type="regular", style="Modern"):
    """
    Robust font loading with Style support.
    """
    candidates = []
    
    # style: "Modern" (Sans), "Classic" (Serif), "Retro" (Mono/Typewriter)
    
    if style == "Classic":
        if font_type == "title":
            candidates.append("assets/PlayfairDisplay-Bold.ttf")
        candidates.extend(["times.ttf", "LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
        
    elif style == "Retro":
        candidates.extend(["courier.ttf", "Courier New.ttf", "LiberationMono-Regular.ttf", "DejaVuSansMono.ttf"])
        
    else: # Modern (Default)
        if font_type == "title":
            candidates.append("assets/PlayfairDisplay-Bold.ttf") # Keep fancy title for Modern? Or stick to Sans?
            # actually, modern usually implies Sans title too. But the user liked the "Vintage" vibe.
            # Let's keep Playfair for Title only if it's explicitly requested or maybe just use Lato/Sans for modern to be distinct.
            # Let's make Modern purely Sans for contrast.
            pass 
        candidates.append("assets/Lato-Regular.ttf")
        candidates.extend(["arial.ttf", "LiberationSans-Regular.ttf", "DejaVuSans.ttf"])

    # Fallback to Lato if everything else fails (except for Retro where we really want Mono)
    if style != "Retro":
        candidates.append("assets/Lato-Regular.ttf")

    for font_name in candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
            
    return ImageFont.load_default()

def load_emoji_font(size=60):
    """
    Attempts to load a font capable of rendering emojis.
    Fallback to bundled Lato for text, which solves "Boxes" for text stickers.
    """
    emoji_candidates = [
        "seguiemj.ttf",          # Windows 10+
        "NotoColorEmoji.ttf",    # Linux / Cloud
        "AppleColorEmoji.ttf",   # Mac
        "Symbola.ttf",
        "assets/Lato-Regular.ttf" # Fallback to bundled font (renders text symbols at least)
    ]
    
    for font_name in emoji_candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            continue
            
    return ImageFont.load_default()

# --- FILTER FUNCTIONS ---
def apply_sepia(image):
    gray = ImageOps.grayscale(image)
    sepia = ImageOps.colorize(gray, "#704214", "#C0C080")
    return sepia

def apply_bw(image):
    return ImageOps.grayscale(image)

def apply_warm_retro(image):
    enhancer = ImageEnhance.Color(image)
    img = enhancer.enhance(1.2)
    layer = Image.new("RGB", img.size, (255, 200, 100))
    img = Image.blend(img, layer, 0.2)
    return img

def apply_grain(image):
    img = apply_sepia(image)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(0.8)

def apply_soft_glow(image):
    blur = image.filter(ImageFilter.GaussianBlur(radius=5))
    return Image.blend(image, blur, 0.5)

def apply_cool_cinema(image):
    enhancer = ImageEnhance.Color(image)
    img = enhancer.enhance(0.6)  
    layer = Image.new("RGB", img.size, (0, 50, 80)) 
    return Image.blend(img, layer, 0.2)

def apply_vintage_rose(image):
    layer = Image.new("RGB", image.size, (255, 192, 203))
    img = Image.blend(image, layer, 0.25)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.1)

def apply_dramatic(image):
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    return enhancer.enhance(1.6) 

def process_image(image, filter_name, flip=False):
    if image.width != image.height:
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
    
    image = image.resize((600, 600))
    
    if flip:
        image = ImageOps.mirror(image)

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
STICKER_PACKS = {
    "None": [],
    "Classic ❤️": ["❤️", "✨", "📷", "🕶️", "💋"],
    "Vintage 🎞️": ["🎞️", "🎩", "🕰️", "📻", "🚲"],
    "Party 🎉": ["🎉", "😎", "🍕", "🎈", "🦄"],
    "Nature 🌸": ["🌸", "🌿", "🦋", "🍄", "☀️"],
    "Love 💌": ["🧸", "💝", "💍", "🥰", "💏"],
    "Spooky 👻": ["👻", "💀", "🕸️", "🎃", "🕯️"]
}

def draw_stickers(draw, strip_width, strip_height, sticker_list, density):
    if not sticker_list:
        return

    font = load_emoji_font(size=60)
    num_stickers = int(density * 1.5) + 3 
    
    for _ in range(num_stickers):
        symbol = random.choice(sticker_list)
        x_pos = random.randint(0, strip_width - 60)
        y_pos = random.randint(0, strip_height - 60)
        
        if random.random() > 0.3: 
            if random.choice([True, False]):
                x_pos = random.randint(0, 40) 
            else:
                x_pos = random.randint(strip_width - 80, strip_width - 20) 
                
        try:
            draw.text((x_pos, y_pos), symbol, font=font, fill="#404040", embedded_color=True)
        except TypeError:
            draw.text((x_pos, y_pos), symbol, font=font, fill="#404040")


def create_strip(images, footer_text="Photobooth", frame_style="Cream", text_color="#333", include_date=False, custom_border_color=None, sticker_pack="None", custom_stickers="", sticker_density=5, font_style="Modern"):
    photo_w, photo_h = 600, 600
    padding = 50
    header_h = 100
    footer_h = 150
    
    num_photos = len(images)
    strip_w = photo_w + (padding * 2)
    strip_h = header_h + (num_photos * (photo_h + padding)) + footer_h
    
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
    
    if frame_style in ["Black", "Film Noir"]:
        text_color = "#FFFFFF" if text_color == "#333" else text_color
    
    for img in images:
        img = img.resize((photo_w, photo_h))
        if frame_style == "Film Noir":
            img_border = ImageOps.expand(img, border=5, fill="white")
            img_border = img_border.resize((photo_w, photo_h))
            strip.paste(img_border, (padding, y_offset))
        else:
            strip.paste(img, (padding, y_offset))
        y_offset += photo_h + padding

    # Stickers
    active_stickers = []
    if sticker_pack in STICKER_PACKS:
        active_stickers.extend(STICKER_PACKS[sticker_pack])
    
    if custom_stickers:
        if "," in custom_stickers:
            active_stickers.extend([s.strip() for s in custom_stickers.split(",")])
        else:
            active_stickers.append(custom_stickers)
            
    if active_stickers:
        draw_stickers(draw, strip_w, strip_h, active_stickers, sticker_density)

    # Text using Styled Fonts
    # Select title font based on chosen style
    font_title = load_font(60, "title", style=font_style)
    font_footer = load_font(40, "regular", style=font_style)
    
    draw.text((strip_w/2, 50), "PHOTOBOOTH", fill=text_color, font=font_title, anchor="mm")
    
    footer_y = strip_h - 100
    draw.text((strip_w/2, footer_y), footer_text, fill=text_color, font=font_footer, anchor="mm")
    
    if include_date:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        draw.text((strip_w/2, footer_y + 50), date_str, fill=text_color, font=load_font(25, "regular", style=font_style), anchor="mm")
        
    return strip 

def convert_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im
