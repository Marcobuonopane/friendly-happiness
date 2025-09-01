# 🤖 AUTENTICO v2.2 - Sistema Automatizzato Play Store

## 🎯 Panoramica

Questo sistema consente di pubblicare AUTENTICO v2.2 su Google Play Store con **UN SOLO COMANDO**, automatizzando tutto il processo di build, signing e deployment.

## 🚀 Quick Start (One-Click Deploy)

### Prerequisito Minimo
```bash
# Configura l'API Google Play (solo la prima volta)
npm run setup:playstore

# Deploy immediato su Google Play Store
npm run deploy:internal
```

### Comandi Principali
```bash
# Deploy su track interno (testing team)
npm run deploy:internal

# Deploy su track beta (utenti beta)
npm run deploy:beta

# Deploy in produzione (pubblico)
npm run deploy:production

# Deploy veloce (salta build, usa AAB esistente)
npm run deploy:quick
```

## 🔧 Setup Completo (Prima Volta)

### 1. Configurazione Google Play Console API

```bash
# Avvia configurazione guidata
./scripts/setup-playstore-api.sh
```

**Passi automatici:**
1. **Istruzioni Service Account**: Guida step-by-step
2. **Validazione API Key**: Controllo formato JSON
3. **Test Connessione**: Verifica accesso Google Play
4. **GitHub Secrets**: Lista secrets necessari
5. **Helper Scripts**: Generazione automatica valori

### 2. Download API Key da Google Play Console

1. **Google Cloud Console**: https://console.cloud.google.com/
2. **Abilita Google Play Developer API**
3. **Crea Service Account**: `autentico-playstore-deploy`
4. **Download JSON Key** → Salva come `fastlane/google-play-api-key.json`
5. **Google Play Console**: Collega progetto e concedi permessi

### 3. Configurazione GitHub Secrets (Per CI/CD)

```bash
# Genera automaticamente i valori base64
./scripts/generate-github-secrets.sh
```

**Secrets Richiesti:**
- `GOOGLE_PLAY_API_KEY` - Base64 del file JSON
- `ANDROID_KEYSTORE_BASE64` - Base64 del keystore 
- `KEYSTORE_PASSWORD` - Password keystore
- `KEY_ALIAS` - Alias chiave di signing
- `KEY_PASSWORD` - Password chiave

## 📦 Build Automatico

### Sistema di Build Intelligente

```bash
# Build completo automatico per Play Store
node scripts/auto-build-playstore.js
```

**Funzionalità:**
- ✅ **Validazione Ambiente**: Node.js, Java, Android SDK
- ✅ **Gestione Versioni**: Auto-increment versionCode  
- ✅ **Web Assets**: Build e ottimizzazione
- ✅ **Capacitor Setup**: Configurazione Android automatica
- ✅ **Keystore**: Generazione automatica se mancante
- ✅ **Gradle Signing**: Configurazione firma digitale
- ✅ **AAB Build**: Generazione bundle per Play Store
- ✅ **Validazione**: Controllo dimensione e formato
- ✅ **Metadata**: Informazioni build complete

### Output Build
```
dist/playstore/
├── autentico-v2.2.0-X.aab     # Bundle per Play Store  
├── autentico-v2.2.0-X.apk     # APK per testing
└── build-metadata.json        # Informazioni build
```

## 🚀 Deployment Automatico con Fastlane

### Tracks Supportati

#### Internal Testing
```bash
fastlane android deploy_internal
# O con shortcut:
npm run deploy:internal
```
- **Scopo**: Testing interno team
- **Tempo deploy**: Immediato
- **Review**: Nessuna review necessaria

#### Beta Testing  
```bash
fastlane android deploy_beta
# O con shortcut:
npm run deploy:beta
```
- **Scopo**: Testing pubblico limitato
- **Tempo deploy**: 2-4 ore per review
- **Utenti**: Lista testers beta

#### Production
```bash
fastlane android deploy_playstore  
# O con shortcut:
npm run deploy:production
```
- **Scopo**: Pubblico generale
- **Tempo deploy**: 1-3 giorni per review
- **Visibilità**: Google Play Store pubblico

### Aggiornamento Solo Metadata
```bash
# Aggiorna descrizioni, screenshot, etc senza nuovo AAB
npm run update:metadata
```

## 🔄 CI/CD con GitHub Actions

### Workflow Automatico

Il file `.github/workflows/deploy-playstore.yml` abilita deployment automatico:

**Trigger:**
- Push su branch `main` → Deploy automatic su `internal`  
- Tag `v*` → Deploy su track configurato
- Manual dispatch → Scelta track

**Pipeline:**
1. **Test** → Validazione codice e sicurezza
2. **Build** → Generazione AAB firmato
3. **Deploy** → Pubblicazione su Google Play Store

### Manual Dispatch

Nel repository GitHub:
1. Actions → Deploy AUTENTICO to Google Play Store  
2. Run workflow → Scegli track
3. Deploy automatico completo

## 📱 Gestione Versioni Automatica

### Auto-Increment System

```javascript
// build/version.json
{
  "versionCode": 123,      // Auto-incrementato
  "versionName": "2.2.0",  // Manuale
  "buildDate": "2024-09-01T14:30:00.000Z"
}
```

**Comportamento:**
- `versionCode`: Incrementato automaticamente ad ogni build
- `versionName`: Aggiornato manualmente per major releases
- `buildDate`: Timestamp automatico

## 🔍 Testing e Validazione

### Pre-Deploy Checks
```bash
# Validazione completa AAB
npm run validate:aab

# Test locale prima di deploy
npm run build:android
```

### Automated Tests (GitHub Actions)
- **HTML Validation**: Controllo sintassi
- **JavaScript Syntax**: Validazione codice  
- **PWA Manifest**: Formato corretto
- **Security Scan**: Ricerca secrets hardcoded

## 📊 Monitoring e Notifiche

### Notifiche Slack (Opzionale)
```bash
# Aggiungi SLACK_WEBHOOK_URL ai GitHub secrets
# Ricevi notifiche automatiche per deploy success/failure
```

### Build Artifacts
- **Retention**: 30 giorni su GitHub Actions
- **Download**: AAB e APK disponibili per testing
- **Metadata**: Log completi per debugging

## 🛠️ Troubleshooting

### Errori Comuni

#### "Google Play API key not found"
```bash
# Verifica file API key
./scripts/setup-playstore-api.sh validate
```

#### "AAB build failed"
```bash
# Check setup Android
java -version
./android/gradlew --version
```

#### "Keystore not found"  
```bash
# Rigenera keystore
rm -rf android/keystore/
node scripts/auto-build-playstore.js
```

#### "Upload failed"
```bash
# Verifica permessi service account
./scripts/setup-playstore-api.sh test
```

### Debug Mode
```bash
# Build con logs dettagliati
DEBUG=1 ./scripts/deploy-playstore.sh internal

# Test API senza deploy
fastlane android build_and_validate
```

## 🔒 Sicurezza

### Protezione Secrets
- **API Keys**: Mai committate in repository
- **Keystore**: Encoded in GitHub secrets
- **Passwords**: Stored in environment variables
- **Service Account**: Permessi minimi necessari

### Best Practices
- ✅ API key con permessi limitati
- ✅ Keystore backup sicuro  
- ✅ Rotazione periodica secrets
- ✅ Audit accessi Google Play Console

## 📈 Workflow Consigliato

### Development → Production

1. **Sviluppo**: Commit su feature branch
2. **Testing**: Deploy automatico su `internal` 
3. **Beta**: Merge su main → Deploy su `beta`
4. **Production**: Tag release → Deploy su `production`

### Release Cycle
```bash
# 1. Sviluppo locale
git commit -m "feat: nuova funzionalità"

# 2. Test interno  
npm run deploy:internal

# 3. Test beta (dopo feedback)
git tag v2.2.1
git push origin v2.2.1  # Trigger automatico GitHub Actions

# 4. Production (dopo review Play Store)
# Deploy automatico da GitHub Actions
```

## 🎉 Vantaggi Sistema Automatico

### Per Sviluppatori
- ⚡ **Deploy in 5 minuti** vs 30 minuti manuali
- 🔄 **Zero errori umani** nel processo
- 📱 **Multi-track support** con un comando
- 🔍 **Validazione automatica** pre-deploy

### Per Business  
- 🚀 **Time-to-market** ridotto drasticamente
- 📈 **Release frequency** aumentata
- 🛡️ **Sicurezza** garantita da automation
- 📊 **Tracciabilità** completa deployments

---

**🤖 Automation at its finest!**  
*Deploy AUTENTICO v2.2 in one click* 🚀

*Documentazione aggiornata: Settembre 2024*