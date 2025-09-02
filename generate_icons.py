#!/usr/bin/env python3
"""
Generatore di icone per AUTENTICO v2.2
Crea l'icona dell'app e feature graphic per Google Play Console
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(size, filename):
    """Crea l'icona dell'app AUTENTICO"""
    
    # Colori del tema AUTENTICO
    bg_color = (139, 69, 19)  # Marrone principale
    accent_color = (245, 241, 232)  # Beige chiaro
    dark_color = (44, 24, 16)  # Marrone scuro
    
    # Crea l'immagine
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Bordo decorativo
    border_width = size // 20
    draw.rectangle([border_width, border_width, size - border_width, size - border_width], 
                  outline=accent_color, width=border_width//2)
    
    # Sfondo centrale
    center_margin = size // 6
    draw.rectangle([center_margin, center_margin, size - center_margin, size - center_margin], 
                  fill=accent_color)
    
    # Simbolo di sicurezza centrale (scudo)
    shield_size = size // 3
    shield_x = (size - shield_size) // 2
    shield_y = (size - shield_size) // 2 - size // 10
    
    # Disegna scudo
    shield_points = [
        (shield_x + shield_size//2, shield_y),  # Top center
        (shield_x + shield_size, shield_y + shield_size//3),  # Top right
        (shield_x + shield_size, shield_y + shield_size*2//3),  # Bottom right
        (shield_x + shield_size//2, shield_y + shield_size),  # Bottom center
        (shield_x, shield_y + shield_size*2//3),  # Bottom left
        (shield_x, shield_y + shield_size//3),  # Top left
    ]
    draw.polygon(shield_points, fill=bg_color, outline=dark_color, width=3)
    
    # Simbolo di crittografia (chiave)
    key_size = shield_size // 3
    key_x = shield_x + shield_size//2 - key_size//2
    key_y = shield_y + shield_size//2 - key_size//2
    
    # Corpo della chiave
    draw.rectangle([key_x, key_y, key_x + key_size//2, key_y + key_size//4], 
                  fill=accent_color)
    # Parte rotonda della chiave
    draw.ellipse([key_x - key_size//4, key_y - key_size//8, 
                 key_x + key_size//4, key_y + key_size//8], 
                fill=accent_color)
    # Denti della chiave
    draw.rectangle([key_x + key_size//2, key_y - key_size//16, 
                   key_x + key_size//2 + key_size//8, key_y + key_size//16], 
                  fill=accent_color)
    
    # Testo "A" stilizzato
    try:
        font_size = size // 4
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
    except:
        font = ImageFont.load_default()
    
    text = "A"
    text_y = shield_y + shield_size + size // 15
    
    # Calcola posizione centrata del testo
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    
    draw.text((text_x, text_y), text, fill=dark_color, font=font)
    
    # Salva l'icona
    img.save(filename, 'PNG', quality=95)
    print(f"Icona creata: {filename} ({size}x{size})")

def create_feature_graphic(width, height, filename):
    """Crea il feature graphic per Google Play"""
    
    # Colori del tema
    bg_gradient_start = (139, 69, 19)
    bg_gradient_end = (205, 133, 63)
    text_color = (245, 241, 232)
    accent_color = (255, 215, 0)  # Oro per accenti
    
    # Crea l'immagine
    img = Image.new('RGB', (width, height), bg_gradient_start)
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(bg_gradient_start[0] * (1 - ratio) + bg_gradient_end[0] * ratio)
        g = int(bg_gradient_start[1] * (1 - ratio) + bg_gradient_end[1] * ratio)  
        b = int(bg_gradient_start[2] * (1 - ratio) + bg_gradient_end[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Font setup
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 120)
        subtitle_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 60)
        desc_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Logo/Icona a sinistra
    icon_size = 200
    icon_x = 50
    icon_y = (height - icon_size) // 2
    
    # Disegna icona semplificata
    draw.ellipse([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size], 
                fill=text_color, outline=accent_color, width=8)
    
    # Simbolo scudo nell'icona
    shield_size = icon_size // 2
    shield_x = icon_x + (icon_size - shield_size) // 2
    shield_y = icon_y + (icon_size - shield_size) // 2
    
    shield_points = [
        (shield_x + shield_size//2, shield_y),
        (shield_x + shield_size, shield_y + shield_size//3),
        (shield_x + shield_size, shield_y + shield_size*2//3),
        (shield_x + shield_size//2, shield_y + shield_size),
        (shield_x, shield_y + shield_size*2//3),
        (shield_x, shield_y + shield_size//3),
    ]
    draw.polygon(shield_points, fill=bg_gradient_start, outline=accent_color, width=4)
    
    # Testi principali
    text_start_x = icon_x + icon_size + 80
    
    # Titolo principale
    title = "AUTENTICO v2.2"
    draw.text((text_start_x, 80), title, fill=text_color, font=title_font)
    
    # Sottotitolo
    subtitle = "Certificazione Digitale Sicura"
    draw.text((text_start_x, 220), subtitle, fill=accent_color, font=subtitle_font)
    
    # Descrizioni funzionalità
    features = [
        "🔐 Crittografia AES-256",
        "🔍 Autenticazione Biometrica", 
        "📋 Certificati Digitali",
        "🛡️ Sicurezza Militare"
    ]
    
    feature_y = 320
    for i, feature in enumerate(features):
        draw.text((text_start_x, feature_y + i * 60), feature, 
                 fill=text_color, font=desc_font)
    
    # Badge "Sicuro" in alto a destra
    badge_x = width - 300
    badge_y = 50
    badge_width = 250
    badge_height = 80
    
    draw.rectangle([badge_x, badge_y, badge_x + badge_width, badge_y + badge_height], 
                  fill=accent_color, outline=text_color, width=3)
    draw.text((badge_x + 30, badge_y + 20), "🛡️ SICURO", 
             fill=bg_gradient_start, font=subtitle_font)
    
    # Salva il feature graphic
    img.save(filename, 'PNG', quality=95)
    print(f"Feature graphic creato: {filename} ({width}x{height})")

def main():
    """Genera tutte le icone e graphics necessari"""
    
    # Percorsi
    icon_path = "/home/user/webapp/google_play_console_upload/app_icon"
    feature_path = "/home/user/webapp/google_play_console_upload/feature_graphic"
    
    # Crea icona dell'app (512x512 richiesta da Google Play)
    create_app_icon(512, f"{icon_path}/app_icon_512.png")
    
    # Crea anche versioni più piccole per riferimento
    create_app_icon(192, f"{icon_path}/app_icon_192.png")
    create_app_icon(144, f"{icon_path}/app_icon_144.png")
    create_app_icon(96, f"{icon_path}/app_icon_96.png")
    create_app_icon(72, f"{icon_path}/app_icon_72.png")
    create_app_icon(48, f"{icon_path}/app_icon_48.png")
    
    # Crea feature graphic (1024x500 richiesta da Google Play)
    create_feature_graphic(1024, 500, f"{feature_path}/feature_graphic_1024x500.png")
    
    print(f"\n✅ Tutte le icone e graphics sono stati generati!")
    print(f"📁 Icone: {icon_path}")
    print(f"📁 Feature Graphic: {feature_path}")

if __name__ == "__main__":
    main()