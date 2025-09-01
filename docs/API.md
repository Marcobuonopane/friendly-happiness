# 📡 AUTENTICO v2.2 - Documentazione API

## 🎯 Panoramica

AUTENTICO v2.2 è principalmente un'applicazione client-side, ma fornisce API JavaScript per sviluppatori che vogliono integrare le funzionalità di certificazione digitale.

## 🔧 API JavaScript Interne

### Authentication API

#### `requestBiometric()`
Richiede autenticazione biometrica usando WebAuthn.

**Sintassi:**
```javascript
const success = await requestBiometric();
```

**Returns:**
- `Promise<boolean>` - true se autenticazione riuscita

**Esempio:**
```javascript
if (await requestBiometric()) {
    console.log('Autenticazione biometrica riuscita');
} else {
    console.log('Autenticazione fallita, usa PIN');
}
```

#### `requestPin()`
Richiede autenticazione tramite PIN.

**Sintassi:**
```javascript
const success = requestPin();
```

**Returns:**
- `boolean` - true se PIN valido

### Cryptography API

#### `generateHash(data)`
Genera hash SHA-256 per i dati forniti.

**Parameters:**
- `data` (string) - Dati da crittografare

**Sintassi:**
```javascript
const hash = await generateHash("dati da crittografare");
```

**Returns:**
- `Promise<string>` - Hash SHA-256 esadecimale

#### `encryptFile(fileBuffer, password)`
Cripta un file usando AES-256-GCM.

**Parameters:**
- `fileBuffer` (ArrayBuffer) - Buffer del file
- `password` (string) - Password per crittografia

**Sintassi:**
```javascript
const fileBuffer = await file.arrayBuffer();
const encrypted = await encryptFile(fileBuffer, "password");
```

**Returns:**
- `Promise<{encrypted: Uint8Array, iv: Uint8Array}>`

#### `decryptFile(encryptedData, iv, password)`
Decripta un file crittografato.

**Parameters:**
- `encryptedData` (Uint8Array) - Dati crittografati
- `iv` (Uint8Array) - Vettore di inizializzazione
- `password` (string) - Password per decrittografia

**Returns:**
- `Promise<Uint8Array>` - File decrittografato

### Certificate API

#### `generateCertificate()`
Genera un nuovo certificato digitale.

**Sintassi:**
```javascript
await generateCertificate();
```

**Prerequisiti:**
- Utente autenticato
- Scopo certificato inserito
- Autenticazione completata

**Returns:**
- `Promise<void>` - Il certificato viene visualizzato automaticamente

### Vault API

#### `uploadFiles()`
Carica e cripta file nella cassaforte digitale.

**Sintassi:**
```javascript
await uploadFiles();
```

**Prerequisiti:**
- File selezionati tramite input
- Utente autenticato

#### `downloadFile(index)`
Scarica e decripta un file dalla cassaforte.

**Parameters:**
- `index` (number) - Indice del file nell'array

**Sintassi:**
```javascript
await downloadFile(0); // Scarica il primo file
```

## 🔄 Event System

### Custom Events

#### `certificate-generated`
Emesso quando un certificato è stato generato.

```javascript
document.addEventListener('certificate-generated', function(event) {
    console.log('Certificato generato:', event.detail);
});
```

#### `file-encrypted`
Emesso quando un file è stato crittografato.

```javascript
document.addEventListener('file-encrypted', function(event) {
    console.log('File crittografato:', event.detail.filename);
});
```

## 🗃️ Storage API

### LocalStorage Schema

#### User Data
```javascript
// Chiave: 'user_' + email
{
    id: number,
    fullName: string,
    birthDate: string,
    birthPlace: string, 
    email: string,
    pin: string,
    registrationDate: string
}
```

#### Certificates
```javascript
// Chiave: 'certificates'
[
    {
        number: string,
        user: UserObject,
        purpose: string,
        gps: string,
        localTime: string,
        internetTime: string,
        timestamp: string,
        hash: string
    }
]
```

#### Vault Files
```javascript
// Chiave: 'vaultFiles_' + userId
[
    {
        name: string,
        size: number,
        type: string,
        uploadDate: string,
        encrypted: boolean,
        data: number[],  // Encrypted data as array
        iv: number[]     // IV as array
    }
]
```

## 🌐 PWA API

### Service Worker Events

#### Installation
```javascript
self.addEventListener('install', function(event) {
    // Cache delle risorse essenziali
});
```

#### Fetch Intercept
```javascript
self.addEventListener('fetch', function(event) {
    // Gestione cache-first per performance
});
```

### Manifest Integration
```javascript
// Controllo installabilità PWA
window.addEventListener('beforeinstallprompt', (e) => {
    // Gestione prompt installazione
});
```

## 🔌 Estensibilità

### Plugin System (Futuro)
```javascript
// API per plugin esterni (v2.3)
AUTENTICO.plugin.register('blockchain-verify', {
    verify: function(certificate) {
        // Verifica su blockchain
    }
});
```

### Webhook Integration (Futuro)
```javascript
// Notifiche esterne (v2.3)
AUTENTICO.webhook.on('certificate-created', 'https://api.example.com/webhook');
```

## 🛠️ Developer Tools

### Debug Mode
```javascript
// Abilita logging dettagliato
localStorage.setItem('autentico-debug', 'true');
```

### Performance Monitoring
```javascript
// Metriche performance
console.time('certificate-generation');
await generateCertificate();
console.timeEnd('certificate-generation');
```

---

**📡 API in continua evoluzione**  
*Per supporto: marco.buonopane@example.com*  
*Documentazione aggiornata: Agosto 2024*