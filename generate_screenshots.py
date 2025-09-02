#!/usr/bin/env python3
"""
Generatore di screenshot per AUTENTICO v2.2
Crea screenshot mock per Google Play Console
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_mock_screenshot(width, height, title, description, filename, bg_color=(245, 241, 232)):
    """Crea uno screenshot mock dell'app AUTENTICO"""
    
    # Crea l'immagine base
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Prova a usare font di sistema
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
        desc_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 40)
        header_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
    except:
        # Fallback ai font di default
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
    
    # Header dell'app
    header_height = 150
    draw.rectangle([0, 0, width, header_height], fill=(139, 69, 19))
    
    # Logo placeholder
    logo_size = 100
    logo_x = 50
    logo_y = 25
    draw.rectangle([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size], 
                  fill=(245, 241, 232), outline=(44, 24, 16), width=3)
    draw.text((logo_x + 20, logo_y + 35), "🔒", fill=(139, 69, 19), font=desc_font)
    
    # Titolo app nell'header
    app_title = "AUTENTICO v2.2"
    draw.text((logo_x + logo_size + 30, logo_y + 20), app_title, 
             fill=(245, 241, 232), font=title_font)
    draw.text((logo_x + logo_size + 30, logo_y + 70), "Certificazione Digitale", 
             fill=(232, 207, 160), font=desc_font)
    
    # Contenuto principale
    content_y = header_height + 50
    
    # Titolo della schermata
    draw.text((50, content_y), title, fill=(44, 24, 16), font=title_font)
    
    # Descrizione
    desc_y = content_y + 100
    wrapped_desc = textwrap.wrap(description, width=30)
    for i, line in enumerate(wrapped_desc):
        draw.text((50, desc_y + i * 50), line, fill=(44, 24, 16), font=desc_font)
    
    # Elementi UI mock
    ui_y = desc_y + len(wrapped_desc) * 50 + 80
    
    # Bottone mock
    button_width = width - 100
    button_height = 80
    draw.rectangle([50, ui_y, 50 + button_width, ui_y + button_height], 
                  fill=(139, 69, 19), outline=(44, 24, 16), width=2)
    draw.text((width//2 - 100, ui_y + 25), "🔍 Impronta Digitale", 
             fill=(245, 241, 232), font=desc_font)
    
    # Campo input mock
    input_y = ui_y + 120
    draw.rectangle([50, input_y, 50 + button_width, input_y + 60], 
                  fill=(255, 255, 255), outline=(212, 184, 149), width=2)
    draw.text((60, input_y + 15), "inserisci@email.com", 
             fill=(150, 150, 150), font=desc_font)
    
    # Footer con sicurezza
    footer_y = height - 150
    draw.text((50, footer_y), "🔐 Crittografia AES-256", 
             fill=(139, 69, 19), font=desc_font)
    draw.text((50, footer_y + 50), "🛡️ Sicurezza di livello militare", 
             fill=(139, 69, 19), font=desc_font)
    draw.text((50, footer_y + 100), "📱 PWA Multi-piattaforma", 
             fill=(139, 69, 19), font=desc_font)
    
    # Salva l'immagine
    img.save(filename, 'PNG', quality=95)
    print(f"Screenshot creato: {filename}")

def main():
    """Genera tutti gli screenshot necessari"""
    
    base_path = "/home/user/webapp/google_play_console_upload/screenshots"
    
    # Screenshot per Phone (9:16 portrait)
    phone_screenshots = [
        {
            'title': 'Accesso Sicuro',
            'description': 'Login con autenticazione biometrica tramite impronta digitale o Face ID. Sicurezza massima per i tuoi dati personali.',
            'filename': f'{base_path}/phone/01_login_biometrico.png'
        },
        {
            'title': 'Registrazione',
            'description': 'Crea il tuo account sicuro inserendo i dati personali. Setup biometrico con WebAuthn per massima sicurezza.',
            'filename': f'{base_path}/phone/02_registrazione.png'
        },
        {
            'title': 'Dashboard',
            'description': 'Pannello di controllo principale. Accesso rapido a certificati digitali e cassaforte crittografata.',
            'filename': f'{base_path}/phone/03_dashboard.png'
        },
        {
            'title': 'Certificato Digitale', 
            'description': 'Genera certificati con timestamp GPS, firma digitale SHA-256 e protezione crittografica avanzata.',
            'filename': f'{base_path}/phone/04_certificato.png'
        },
        {
            'title': 'Cassaforte Digitale',
            'description': 'Archiviazione sicura con crittografia AES-256. I tuoi file sono protetti da algoritmi militari.',
            'filename': f'{base_path}/phone/05_cassaforte.png'
        }
    ]
    
    # Genera screenshot per phone
    for screenshot in phone_screenshots:
        create_mock_screenshot(1080, 1920, screenshot['title'], 
                             screenshot['description'], screenshot['filename'])
    
    # Screenshot per Tablet 7" (4:3 aspect ratio)
    tablet_7_screenshots = [
        {
            'title': 'AUTENTICO su Tablet',
            'description': 'Esperienza ottimizzata per tablet con interfaccia adattiva e controlli touch-friendly per certificazione digitale.',
            'filename': f'{base_path}/tablet_7_inch/01_tablet_7_overview.png'
        },
        {
            'title': 'Certificazione Avanzata',
            'description': 'Schermo più ampio per una migliore visualizzazione dei certificati digitali e gestione documenti sicuri.',
            'filename': f'{base_path}/tablet_7_inch/02_tablet_7_certificati.png'
        }
    ]
    
    for screenshot in tablet_7_screenshots:
        create_mock_screenshot(1200, 1920, screenshot['title'], 
                             screenshot['description'], screenshot['filename'])
    
    # Screenshot per Tablet 10" (16:10 aspect ratio)  
    tablet_10_screenshots = [
        {
            'title': 'Produttività Massima',
            'description': 'Sfrutta lo schermo grande per gestire multiple certificazioni contemporaneamente con interfaccia multi-colonna.',
            'filename': f'{base_path}/tablet_10_inch/01_tablet_10_overview.png'
        },
        {
            'title': 'Gestione Professionale',
            'description': 'Ideale per uso professionale con gestione avanzata di documenti, certificati e cassaforte digitale.',
            'filename': f'{base_path}/tablet_10_inch/02_tablet_10_professional.png'
        }
    ]
    
    for screenshot in tablet_10_screenshots:
        create_mock_screenshot(1600, 2560, screenshot['title'], 
                             screenshot['description'], screenshot['filename'])
    
    print(f"\n✅ Tutti gli screenshot sono stati generati!")
    print(f"📁 Percorso: {base_path}")

if __name__ == "__main__":
    main()