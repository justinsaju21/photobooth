from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageFilter
import numpy as np
import io
import random
import os

def apply_sepia(image):
    gray = ImageOps.grayscale(image)
    sepia = ImageOps.colorize(gray, "#704214", "#C0C080")
    return sepia

def apply_bw(image):
    return ImageOps.grayscale(image)

def apply_warm_retro(image):
    # Warm shift
    enhancer = ImageEnhance.Color(image)
    img = enhancer.enhance(1.2)
    # Overlay yellow tint
    layer = Image.new("RGB", img.size, (255, 200, 100))
    img = Image.blend(img, layer, 0.2)
    return img

def apply_grain(image):
    # Sepia base
    img = apply_sepia(image)
    # Add noise (simulated)
    width, height = img.size
    noise = np.random.normal(0, 15, (height, width))
    # This is a simplified "fast" grain. 
    # For better grain, we'd overlay a texture, but let's stick to simple matrix ops isn't easy in PIL pure.
    # Instead, let's use a blend mode trick or simple enhancement.
    # Actually, let's just reduce quality/contrast to mimic old film.
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(0.8)

def apply_soft_glow(image):
    # Gaussian blur overlay
    blur = image.filter(ImageFilter.GaussianBlur(radius=5))
    return Image.blend(image, blur, 0.5)

def apply_cool_cinema(image):
    # Blue/Teal tint + Low Saturation
    enhancer = ImageEnhance.Color(image)
    img = enhancer.enhance(0.6)  # Desaturate
    layer = Image.new("RGB", img.size, (0, 50, 80)) # Dark Cyan
    return Image.blend(img, layer, 0.2)

def apply_vintage_rose(image):
    # Pink tint + Brightness
    layer = Image.new("RGB", image.size, (255, 192, 203))
    img = Image.blend(image, layer, 0.25)
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(1.1)

def apply_dramatic(image):
    # High Contrast B&W
    gray = ImageOps.grayscale(image)
    enhancer = ImageEnhance.Contrast(gray)
    return enhancer.enhance(1.6) # Very harsh contrast

def process_image(image, filter_name, flip=False):
    # Ensure image size (Example resizing for consistency)
    if image.width != image.height:
        # Crop to square center if not already
        size = min(image.size)
        left = (image.width - size) / 2
        top = (image.height - size) / 2
        right = (image.width + size) / 2
        bottom = (image.height + size) / 2
        image = image.crop((left, top, right, bottom))
    
    image = image.resize((600, 600))
    
    # 1. Flip (Mirror) - Applied manually here
    if flip:
        image = ImageOps.mirror(image)

    # 2. Filter
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
    """
    Randomly draws stickers on the strip, avoiding the central photo areas roughly.
    """
    if not sticker_list:
        return

    # Try to load Emoji font (Windows default)
    try:
        # Segoe UI Emoji is standard on Windows 10+
        font = ImageFont.truetype("seguiemj.ttf", size=60)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", size=60)
        except IOError:
            font = ImageFont.load_default()

    # Determine number of stickers based on density (1-10)
    num_stickers = int(density * 1.5) + 3 # approx 4 to 18 stickers
    
    for _ in range(num_stickers):
        symbol = random.choice(sticker_list)
        
        # Random Position
        # We want to favor the sides (margins)
        # Strip width ~700. Margins are roughly 0-50 and 650-700.
        # Also vertical gaps between photos.
        
        x_pos = random.randint(0, strip_width - 60)
        y_pos = random.randint(0, strip_height - 60)
        
        # Simple collision avoidance logic (very rough)
        # Photos are centered. Width 600. Strip width 700. 
        # So photos are from x=50 to x=650.
        # We prefer x < 50 or x > 600.
        
        # Let's force some to be on the sides
        if random.random() > 0.3: # 70% chance to force to side
            if random.choice([True, False]):
                x_pos = random.randint(0, 40) # Left edge
            else:
                x_pos = random.randint(strip_width - 80, strip_width - 20) # Right edge
                
        # Draw
        # Random rotation is hard with simple text draw, would need to make separate image.
        # For now, simple direct draw.
        
        # Color: Use a color that contrasts or matches the vintage vibe
        # Let's use a semi-transparent dark grey or raw color if supporting rgba
        # PIL draw.text with embedded color (emojis) works if supported, otherwise it renders mono.
        # On many systems PIL + standard font = B&W outline. 
        # Let's try to pass 'embedded_color=True' if PIL version supports it (recent versions do).
        
        try:
            draw.text((x_pos, y_pos), symbol, font=font, fill="#404040", embedded_color=True)
        except TypeError:
             # Fallback for older PIL
            draw.text((x_pos, y_pos), symbol, font=font, fill="#404040")


def create_strip(images, footer_text="Photobooth", frame_style="Cream", text_color="#333", include_date=False, custom_border_color=None, sticker_pack="None", custom_stickers="", sticker_density=5):
    # Base dimensions
    photo_w, photo_h = 600, 600
    padding = 50
    header_h = 100
    footer_h = 150
    
    num_photos = len(images)
    strip_w = photo_w + (padding * 2)
    strip_h = header_h + (num_photos * (photo_h + padding)) + footer_h
    
    # Background Color Logic
    bg_color = "#F5F1E8" # Default Cream
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
    
    # 1. Draw Photos
    y_offset = header_h
    
    # Film Noir / Black specific styling
    if frame_style in ["Black", "Film Noir"]:
        text_color = "#FFFFFF" if text_color == "#333" else text_color
    
    for img in images:
        # Resize if needed (already done in process, but safe to ensure)
        img = img.resize((photo_w, photo_h))
        
        # Add a thin border around image if style requires
        if frame_style == "Film Noir":
            # Perforations or simple white border
            img_border = ImageOps.expand(img, border=5, fill="white")
            img_border = img_border.resize((photo_w, photo_h))
            strip.paste(img_border, (padding, y_offset))
        else:
            strip.paste(img, (padding, y_offset))
            
        y_offset += photo_h + padding

    # 2. Draw Embellishments (Stickers)
    # Combine pack and custom
    active_stickers = []
    if sticker_pack in STICKER_PACKS:
        active_stickers.extend(STICKER_PACKS[sticker_pack])
    
    if custom_stickers:
        # Split by chars? or space? Emojis are chars.
        # Let's just treat the string as a sequence of chars if it's short, or a list if commas.
        # Simple approach: add the whole string as one sticker if it's short, else split
        if "," in custom_stickers:
            active_stickers.extend([s.strip() for s in custom_stickers.split(",")])
        else:
            # Add individual chars if they seem like emojis (naive), or just the string
            active_stickers.append(custom_stickers)
            
    if active_stickers:
        draw_stickers(draw, strip_w, strip_h, active_stickers, sticker_density)

    # 3. Text & Branding
    try:
        # Try to load a fancy font
        # Windows typical path or relative "assets/font.ttf". 
        # Making a proactive guess that fonts might not be here, falling back.
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_footer = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_title = ImageFont.load_default()
        font_footer = ImageFont.load_default()
        
    # Header Logo/Text
    draw.text((strip_w/2, 50), "PHOTOBOOTH", fill=text_color, font=font_title, anchor="mm")
    
    # Footer
    footer_y = strip_h - 100
    draw.text((strip_w/2, footer_y), footer_text, fill=text_color, font=font_footer, anchor="mm")
    
    if include_date:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
        draw.text((strip_w/2, footer_y + 50), date_str, fill=text_color, font=ImageFont.truetype("arial.ttf", 25) if font_footer else None, anchor="mm")
        
    return strip 

def convert_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im
