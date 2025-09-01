# 🔄 GitHub Actions Setup Manual

## ⚠️ Nota Importante

Il file GitHub Actions workflow non può essere pushato automaticamente a causa di restrizioni di permessi. Deve essere aggiunto manualmente nel repository.

## 📝 Come Aggiungere GitHub Actions

### 1. Nel Repository GitHub
1. Vai su https://github.com/Marcobuonopane/friendly-happiness
2. Crea directory: `.github/workflows/`
3. Crea file: `deploy-playstore.yml`

### 2. Contenuto del File

Copia il contenuto da: `.github/workflows/deploy-playstore.yml` (salvato localmente)

O usa questo template:

```yaml
name: 🚀 Deploy AUTENTICO to Google Play Store

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  workflow_dispatch:
    inputs:
      track:
        description: 'Deployment track'
        required: true
        default: 'internal'
        type: choice
        options:
        - internal
        - beta
        - production

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🔨 Build AAB
      run: |
        npm ci
        npm run build:android
        
    - name: 🚀 Deploy to Play Store
      env:
        GOOGLE_PLAY_API_KEY: \${{ secrets.GOOGLE_PLAY_API_KEY }}
      run: |
        npm run deploy:internal
```

### 3. Configurazione Secrets

Nel repository GitHub, vai in Settings → Secrets and variables → Actions:

```
GOOGLE_PLAY_API_KEY=<base64 del file JSON>
ANDROID_KEYSTORE_BASE64=<base64 del keystore>
KEYSTORE_PASSWORD=autentico2024
KEY_ALIAS=autentico
KEY_PASSWORD=autentico2024
```

### 4. Test Workflow

Dopo aver aggiunto il file:
1. Actions → Deploy AUTENTICO to Google Play Store
2. Run workflow → Scegli track
3. Verifica che funzioni correttamente

## 🔧 File Completo Disponibile

Il file completo `.github/workflows/deploy-playstore.yml` è disponibile in locale nella directory del progetto.

## ✅ Alternative senza GitHub Actions

Anche senza GitHub Actions, hai comunque:

```bash
# Deploy locale one-click
npm run deploy:internal
npm run deploy:beta  
npm run deploy:production

# Build automatico
npm run build:android

# Setup guidato
npm run setup:playstore
```

Il sistema funziona perfettamente anche senza CI/CD automatico!