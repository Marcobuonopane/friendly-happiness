# App Bundle (File AAB)

**Dove caricare:** `App bundles` → `Release management` → `App releases`

**Cosa inserire qui:**
- `com.marcobuonopane.autentico-2.2.0.aab` - Il file bundle dell'app Android

**Requisiti:**
- Formato: .aab (Android App Bundle)
- Dimensione massima: 150 MB
- Firmato digitalmente con keystore

**Generazione:**
```bash
# Build con Capacitor
npx cap build android --prod

# O usando il nostro script automatico
npm run build:android
```

**File da caricare:**
1. `autentico-v2.2.0.aab` - App bundle principale