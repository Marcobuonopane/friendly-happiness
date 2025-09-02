# 🚀 Guida Completa Upload Google Play Console

## 📋 Checklist Pre-Upload

### ✅ File da Preparare
- [ ] App Bundle (.aab) firmato digitalmente
- [ ] Icona app (512x512 PNG)
- [ ] Feature graphic (1024x500 PNG)  
- [ ] Screenshot per phone, tablet 7", tablet 10"
- [ ] Testi store listing (titolo, descrizioni)
- [ ] Privacy policy pubblicata online
- [ ] Release notes in italiano e inglese

---

## 📁 Struttura Cartelle Upload

```
google_play_console_upload/
├── app_bundle/                    # 📱 FILE APP
│   ├── com.marcobuonopane.autentico-2.2.0.aab
│   └── README.md
├── app_icon/                      # 🎨 ICONA APP  
│   ├── app_icon_512.png          # ⭐ PRINCIPALE
│   └── README.md
├── feature_graphic/               # 🖼️ GRAFICA STORE
│   ├── feature_graphic_1024x500.png # ⭐ PRINCIPALE
│   └── README.md
├── screenshots/                   # 📸 SCREENSHOT
│   ├── phone/                     # 5 screenshot
│   ├── tablet_7_inch/            # 2 screenshot
│   ├── tablet_10_inch/           # 2 screenshot
│   └── README.md
├── store_listing/                 # 📝 TESTI STORE
│   ├── app_title.txt
│   ├── short_description.txt
│   ├── full_description.txt
│   └── README.md
├── privacy_policy/                # 🔒 PRIVACY
│   ├── privacy_policy.html
│   ├── privacy_policy_url.txt
│   └── README.md
├── release_notes/                 # 📋 NOTE RILASCIO
│   ├── release_notes_it.txt
│   ├── release_notes_en.txt
│   └── README.md
├── metadata/                      # ⚙️ METADATA
│   ├── app_category.txt
│   ├── content_rating.txt
│   └── README.md
└── content_rating/               # 🏷️ CONTENT RATING
    └── README.md
```

---

## 🎯 Processo Step-by-Step

### 1. SETUP INIZIALE
**Console:** https://play.google.com/console
1. Login con account Google Developer
2. Seleziona "Crea app"
3. Nome app: "AUTENTICO - Certificazione Digitale"
4. Lingua predefinita: Italiano
5. Tipo: App
6. Categoria: Business
7. Gratuita/a pagamento: Gratuita

### 2. APP BUNDLE UPLOAD
**Sezione:** `Release management` → `App releases` → `Internal testing`

📁 **Cartella:** `app_bundle/`
📄 **File:** `com.marcobuonopane.autentico-2.2.0.aab`

**Passi:**
1. Clicca "Crea nuova release"
2. Trascina il file .aab nell'area upload
3. Verifica che la firma sia valida
4. Procedi al passo successivo

### 3. STORE LISTING
**Sezione:** `Store listing`

#### 3.1 Dettagli Principali
📁 **Cartella:** `store_listing/`

- **Titolo app:** Copia da `app_title.txt`
- **Descrizione breve:** Copia da `short_description.txt`  
- **Descrizione completa:** Copia da `full_description.txt`

#### 3.2 Grafica Store
📁 **Cartelle:** `app_icon/`, `feature_graphic/`, `screenshots/`

**Icona app:**
- Upload: `app_icon/app_icon_512.png`
- Requisiti: 512x512 px, PNG, max 1MB

**Feature graphic:**
- Upload: `feature_graphic/feature_graphic_1024x500.png`
- Requisiti: 1024x500 px, PNG/JPEG, max 15MB

**Screenshot Phone:**
- Upload tutti i file da `screenshots/phone/`
- Minimo 2, massimo 8 screenshot

**Screenshot Tablet 7":**
- Upload da `screenshots/tablet_7_inch/`
- Minimo 1, massimo 8 screenshot

**Screenshot Tablet 10":**
- Upload da `screenshots/tablet_10_inch/`
- Minimo 1, massimo 8 screenshot

#### 3.3 Dettagli Aggiuntivi
📁 **Cartella:** `metadata/`

- **Categoria:** Business (da `app_category.txt`)
- **Tag:** certificazione, sicurezza, business, crittografia
- **Sito web:** https://github.com/Marcobuonopane/friendly-happiness
- **Email contatto:** marco.buonopane@example.com

### 4. APP CONTENT
**Sezione:** `App content`

#### 4.1 Privacy Policy
📁 **Cartella:** `privacy_policy/`

- **URL Privacy Policy:** Copia da `privacy_policy_url.txt`
```
https://3000-i6etv5c8ut13ardoaq63a-6532622b.e2b.dev/google_play_console_upload/privacy_policy/privacy_policy.html
```

#### 4.2 Content Rating
📁 **Cartella:** `content_rating/`

**Segui le istruzioni in:** `content_rating/README.md`

**Riassunto veloce:**
- Categoria: Utility/Productivity  
- Violenza: NO
- Contenuti sessuali: NO
- Linguaggio volgare: NO
- Sostanze: NO
- Horror: NO
- Gambling: NO
- Contenuti generati utenti: SÌ (limitato, crittografato)
- Comunicazione tra utenti: NO
- Informazioni sensibili: SÌ (protezione massima)

**Rating atteso:** Tutti (3+)

#### 4.3 Target Audience
- **Età target:** 18-65 anni
- **Pubblico:** Professionisti, aziende, privati
- **Mercati:** Globale

### 5. RELEASE NOTES
**Sezione:** `Release management` → `App releases`

📁 **Cartella:** `release_notes/`

**Quando fai upload del bundle, aggiungi:**
- **Note rilascio italiane:** Da `release_notes_it.txt` 
- **Note rilascio inglesi:** Da `release_notes_en.txt`

Se superi 500 caratteri, usa versioni abbreviate dal README.

### 6. CONFIGURAZIONI AVANZATE

#### 6.1 Distribuzione Paesi
**Consigliato per primo rilascio:**
- 🇮🇹 Italia (mercato principale)
- 🇺🇸 Stati Uniti  
- 🇬🇧 Regno Unito
- 🇩🇪 Germania
- 🇫🇷 Francia
- 🇪🇸 Spagna

#### 6.2 Prezzo
- **Modello:** Gratuito
- **Acquisti in-app:** Nessuno
- **Pubblicità:** Nessuna

#### 6.3 Dispositivi Supportati
- **Android minimo:** 7.0 (API level 24)
- **Architetture:** arm64-v8a, armeabi-v7a, x86_64
- **Caratteristiche richieste:** Camera (per biometrica), GPS (per certificati)

---

## ⚡ Quick Start Checklist

### Preparazione (15 minuti)
- [ ] Verifica tutti i file sono nella cartella `google_play_console_upload/`
- [ ] Controlla che l'URL privacy policy sia accessibile
- [ ] Verifica dimensioni e formati di icone e screenshot

### Upload Fase 1 - App Bundle (10 minuti)
- [ ] Login Google Play Console
- [ ] Crea nuova app "AUTENTICO - Certificazione Digitale"
- [ ] Upload file .aab da cartella `app_bundle/`
- [ ] Verifica signature e procedi

### Upload Fase 2 - Store Listing (20 minuti)  
- [ ] Titolo da `store_listing/app_title.txt`
- [ ] Descrizioni da `store_listing/`
- [ ] Upload icona da `app_icon/app_icon_512.png`
- [ ] Upload feature graphic da `feature_graphic/`
- [ ] Upload tutti screenshot da cartelle `screenshots/`

### Upload Fase 3 - Compliance (15 minuti)
- [ ] Privacy Policy URL da `privacy_policy/privacy_policy_url.txt`
- [ ] Content rating seguendo `content_rating/README.md`
- [ ] Target audience: Business/Productivity, 18+

### Upload Fase 4 - Release (10 minuti)
- [ ] Release notes da `release_notes/`  
- [ ] Seleziona paesi distribuzione
- [ ] Review finale e pubblica in Internal Testing

### Tempi Totali Stimati
- **Preparazione:** 15 min
- **Upload completo:** 55 min  
- **Review Google:** 24-48 ore
- **Pubblicazione:** 2-3 giorni

---

## 🚨 Troubleshooting Comuni

### Errore: "App bundle signature invalid"
- Verifica che il file .aab sia firmato correttamente
- Usa il keystore giusto per la firma
- Rigenera il bundle se necessario

### Errore: "Icon doesn't meet requirements"  
- Verifica dimensioni esatte: 512x512 px
- Formato PNG a 32-bit
- Dimensione file sotto 1MB

### Errore: "Screenshots wrong dimensions"
- Phone: minimo 320px, massimo 3840px  
- Rapporto aspetto 16:9 o 9:16
- Verifica che siano PNG/JPEG a 24-bit

### Errore: "Privacy policy URL not accessible"
- Verifica che l'URL sia pubblicamente raggiungibile
- Testa l'accesso da browser in incognito
- Controlla che restituisca HTTP 200

### Errore: "Content rating incomplete"
- Completa tutte le domande del questionario
- Salva le risposte prima di procedere
- Genera il certificate rating

---

## 📞 Supporto e Risorse

### Link Utili
- **Google Play Console:** https://play.google.com/console
- **Documentazione:** https://developer.android.com/distribute/console
- **Policy Developer:** https://play.google.com/about/developer-content-policy/

### Contatti
- **Developer:** Marco Buonopane
- **Email:** marco.buonopane@example.com  
- **Repository:** https://github.com/Marcobuonopane/friendly-happiness

---

## 🎉 Dopo la Pubblicazione

### Monitoraggio
1. Controlla statistiche download in Play Console
2. Monitora recensioni e valutazioni utenti  
3. Verifica crash report e feedback
4. Analizza performance e ottimizzazioni

### Aggiornamenti Futuri
1. Aggiorna versione in `capacitor.config.json`
2. Incrementa `versionCode` nel build
3. Genera nuovo .aab firmato
4. Upload via "App releases" → nuova release

**🚀 AUTENTICO è pronto per Google Play Store!**