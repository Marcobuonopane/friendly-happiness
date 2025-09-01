# 🚀 AUTENTICO v2.2 - Guida Deployment

## 📋 Prerequisiti

### Ambiente di Sviluppo
- **Node.js**: 14+ 
- **Git**: Per versioning
- **Android Studio**: Per build Android (opzionale)
- **Xcode**: Per build iOS (solo macOS)

### Account Necessari
- **GitHub**: Repository hosting
- **Google Play Console**: Distribuzione Android
- **Apple Developer Program**: Distribuzione iOS  
- **Netlify/Vercel**: Hosting PWA (opzionale)

## 🔧 Setup Locale

### 1. Clone Repository
```bash
git clone https://github.com/Marcobuonopane/friendly-happiness.git
cd friendly-happiness
```

### 2. Installazione Dipendenze
```bash
# Se usi Node.js per build tools
npm install -g @capacitor/cli
npm install -g cordova

# Oppure con yarn
yarn global add @capacitor/cli
```

### 3. Build del Progetto
```bash
# Build per produzione
node build/build.js

# I file sono ora in ./dist/
```

## 📱 Deployment Mobile

### Android (Google Play Store)

#### Setup Capacitor
```bash
# Aggiungi piattaforma Android
npx cap add android

# Sincronizza codice
npx cap sync android

# Apri in Android Studio
npx cap open android
```

#### Configurazione Signing
1. **Genera Keystore**:
```bash
keytool -genkey -v -keystore build/android/keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias autentico
```

2. **Configura Build**:
```gradle
// android/app/build.gradle
android {
    signingConfigs {
        release {
            storeFile file('../../build/android/keystore.jks')
            storePassword 'autentico2024'
            keyAlias 'autentico'
            keyPassword 'autentico2024'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

#### Build Release
```bash
# Build APK
cd android
./gradlew assembleRelease

# Build AAB (Play Store)
./gradlew bundleRelease
```

#### Upload Google Play
1. Accedi a [Google Play Console](https://play.google.com/console)
2. Crea nuova applicazione
3. Carica AAB file
4. Compila store listing
5. Invia per review

### iOS (App Store)

#### Setup iOS
```bash
# Aggiungi piattaforma iOS (solo macOS)
npx cap add ios
npx cap sync ios
npx cap open ios
```

#### Configurazione Xcode
1. Apri progetto in Xcode
2. Configura Team ID e Bundle ID
3. Configura certificati di signing
4. Build per archivio

#### Upload App Store
1. Archive build in Xcode
2. Upload tramite Xcode Organizer
3. Compila App Store Connect
4. Invia per review

## 🌐 Deployment Web (PWA)

### Netlify Deployment

#### Setup automatico
```bash
# Collega repository GitHub
# File netlify.toml già configurato
```

#### Configurazione Netlify
```toml
[build]
  publish = "dist"
  command = "node build/build.js"

[build.environment]
  NODE_VERSION = "16"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/sw.js"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[headers]]
  for = "/manifest.json"
  [headers.values]
    Content-Type = "application/manifest+json"
```

### Vercel Deployment
```json
{
  "version": 2,
  "builds": [
    {
      "src": "build/build.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/sw.js",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    }
  ]
}
```

### GitHub Pages
```bash
# Build statico
node build/build.js

# Deploy su gh-pages branch
git subtree push --prefix dist origin gh-pages
```

## 🔄 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy AUTENTICO
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Build project
      run: node build/build.js
    
    - name: Deploy to Netlify
      uses: netlify/actions/cli@master
      with:
        args: deploy --dir=dist --prod
      env:
        NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## 🛡️ Security Checklist

### Pre-Deployment
- ✅ HTTPS configurato
- ✅ Headers di sicurezza impostati
- ✅ Service Worker firmato
- ✅ Manifest validato
- ✅ API keys non esposte
- ✅ Debug mode disabilitato
- ✅ Codice minificato
- ✅ Dependencies aggiornate

### Post-Deployment
- ✅ SSL certificate valido
- ✅ PWA installabile
- ✅ Performance > 90
- ✅ Accessibility AA
- ✅ SEO ottimizzato
- ✅ Offline funzionante

## 📊 Monitoring

### Performance Monitoring
```javascript
// Google Analytics (opzionale)
gtag('config', 'GA_MEASUREMENT_ID', {
  // Performance tracking
  custom_map: {'dimension1': 'certificate_generation_time'}
});
```

### Error Tracking
```javascript
// Sentry (opzionale)
window.addEventListener('error', function(event) {
  console.error('Application error:', event.error);
});
```

## 🎯 Store Submission

### Google Play Store
1. **Preparazione**:
   - AAB file < 150MB
   - Target API level aggiornato
   - Permissions minimali
   - Privacy policy URL

2. **Store Listing**:
   - Screenshots (almeno 2)
   - Icona 512x512
   - Feature graphic
   - Descrizione breve/lunga

3. **Review Process**:
   - Tempo: 1-3 giorni
   - Test automatici
   - Review manuale

### Apple App Store
1. **Preparazione**:
   - IPA file
   - iOS compatibility
   - App Transport Security
   - Privacy manifest

2. **App Store Connect**:
   - Screenshots per device
   - Icona 1024x1024
   - App description
   - Keywords

3. **Review Process**:
   - Tempo: 1-7 giorni
   - Human review
   - Guidelines compliance

---

**🚀 Deploy with Confidence!**  
*Per supporto deployment: marco.buonopane@example.com*  
*Guida aggiornata: Agosto 2024*