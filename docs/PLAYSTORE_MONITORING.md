# 🔍 AUTENTICO v2.2 - Play Store Monitoring System

## 🎯 Come Controllare che l'App sia su Google Play Store

### ⚡ **Controllo Rapido (One-Click)**

```bash
# Controllo immediato dello stato
npm run check:playstore

# Visualizza stato corrente
npm run status:playstore

# Genera tutti i link e QR codes
npm run generate:links
```

### 🔄 **Monitoraggio Continuo**

```bash
# Avvia monitoraggio automatico (ogni 5 minuti)
npm run monitor:playstore

# Dashboard web interattiva
npm run dashboard:playstore
# Poi apri: http://localhost:8080/playstore-dashboard.html
```

## 🔍 **Metodi di Verifica**

### **1. Controllo Automatico con Script**

Il nostro sistema controlla automaticamente:

```bash
node scripts/check-playstore-status.js
```

**Cosa Verifica:**
- ✅ **Visibilità pubblica** su Google Play Store
- ✅ **Stato installazione** (installabile/pre-registrazione)
- ✅ **Metadata app** (titolo, rating, recensioni, downloads)
- ✅ **Versione pubblicata** e ultimo aggiornamento
- ✅ **Link funzionanti** per tutte le piattaforme

**Output del Controllo:**
```
🎉 SUCCESS! AUTENTICO v2.2 is LIVE on Google Play Store!

✅ Your app is:
   • Publicly visible on Google Play Store
   • Available for installation by users
   • Searchable in the Play Store

🔗 Share these links:
   https://play.google.com/store/apps/details?id=com.marcobuonopane.autentico
```

### **2. Dashboard Web Interattiva**

Avvia la dashboard:
```bash
npm run dashboard:playstore
```

Apri nel browser: `http://localhost:8080/playstore-dashboard.html`

**Features Dashboard:**
- 📊 **Status in tempo reale** con indicatori colorati
- 📱 **Statistiche app** (rating, recensioni, downloads)
- 🔗 **Link diretti** per installazione e condivisione
- 📱 **QR codes** per installazione mobile
- 🛠️ **Azioni rapide** (deploy, controlli)

### **3. Monitoraggio Continuo Automatico**

```bash
# Monitoraggio ogni 5 minuti
./scripts/monitor-playstore.sh monitor

# Monitoraggio personalizzato (ogni 1 minuto)
./scripts/monitor-playstore.sh monitor -i 60

# Con notifiche Slack
./scripts/monitor-playstore.sh monitor -w https://hooks.slack.com/your/webhook
```

**Cosa Monitora:**
- 🔄 **Check automatici** a intervalli regolari
- 📊 **Status changes** (da pending a live, errori, etc.)
- 📱 **Notifiche immediate** quando app diventa live
- 📋 **Log dettagliati** di tutti i controlli
- 💾 **Report JSON** con storico status

## 📱 **Link di Verifica Diretti**

### **Google Play Store Links**

```bash
# Genera tutti i link automaticamente
npm run generate:links
```

**Link Principali:**
- **🏪 Play Store:** https://play.google.com/store/apps/details?id=com.marcobuonopane.autentico
- **🔗 Link Breve:** https://play.app.goo.gl/?link=https://play.google.com/store/apps/details?id=com.marcobuonopane.autentico
- **📱 Deep Link:** `market://details?id=com.marcobuonopane.autentico`

### **Come Verificare Manualmente:**

#### **Metodo 1: Search Google Play Store**
1. Apri Google Play Store
2. Cerca "AUTENTICO Marco Buonopane"  
3. Cerca "com.marcobuonopane.autentico"
4. Se appare = App pubblicata ✅

#### **Metodo 2: Link Diretto**
1. Clicca: https://play.google.com/store/apps/details?id=com.marcobuonopane.autentico
2. Se vedi "Install" = App live ✅
3. Se vedi "Pre-register" = In pre-registrazione ⏳
4. Se vedi "Item not found" = Non pubblicata ❌

#### **Metodo 3: QR Code**
1. Genera QR: `npm run generate:links`
2. Scansiona con telefono
3. Dovrebbe aprire Google Play Store

## 📊 **Interpretazione degli Stati**

### **🎉 LIVE (Pubblicata)**
```
Status: live
Message: App is successfully published and available
```
- ✅ App visibile pubblicamente
- ✅ Utenti possono installarla
- ✅ Trovabile nelle ricerche
- ✅ Statistiche disponibili

### **⏳ PENDING (In Review)**
```
Status: pending  
Message: App is under review by Google
```
- 🔄 Google sta verificando l'app
- ⏱️ Tempo tipico: 1-3 giorni
- 📋 Controlla Play Console per dettagli

### **🔒 PRE-REGISTER (Pre-registrazione)**
```
Status: pre-register
Message: App in pre-registration mode
```
- 📅 App programmata per release futura
- 👥 Utenti possono pre-registrarsi
- 🚀 Installazione automatica al rilascio

### **❌ NOT FOUND (Non Trovata)**
```
Status: not-found
Message: App not found on Play Store
```
- 🔍 App non pubblicata ancora
- 📋 Controlla Play Console per status
- 🛠️ Potrebbe servire nuovo deploy

### **⚠️ ERROR (Errore)**
```
Status: error
Message: Unable to connect or check status  
```
- 🌐 Problemi di connessione
- 🔧 Errore nel checking script
- 📞 Potrebbe essere temporaneo

## 🛠️ **Troubleshooting**

### **Se l'App Non Appare:**

#### **1. Controlla Google Play Console**
```bash
# Apri Play Console
https://play.google.com/console/
```
- Verifica status dell'app
- Leggi eventuali rejection reasons
- Controlla review requirements

#### **2. Verifica Deployment**
```bash
# Controllo ultimo deployment
npm run status:playstore

# Re-deploy se necessario
npm run deploy:internal   # Test interno
npm run deploy:beta      # Test beta
npm run deploy:production # Produzione
```

#### **3. Check Logs Dettagliati**
```bash
# Visualizza log monitoraggio
./scripts/monitor-playstore.sh logs

# Check report JSON
cat reports/playstore-status.json
```

### **Tempi di Pubblicazione Tipici:**

- **Internal Testing:** Immediato (0-5 minuti)
- **Beta Testing:** 2-4 ore per review  
- **Production:** 1-3 giorni per review
- **First Time:** Può richiedere più tempo

## 📈 **Monitoraggio Avanzato**

### **Setup Notifiche Slack**
```bash
# Aggiungi webhook URL
export WEBHOOK_URL="https://hooks.slack.com/your/webhook"

# Avvia monitoring con notifiche
./scripts/monitor-playstore.sh monitor -w "$WEBHOOK_URL"
```

### **Setup Cron Job per Monitoring**
```bash
# Aggiungi al crontab per check ogni ora
echo "0 * * * * cd /path/to/autentico && ./scripts/monitor-playstore.sh check" | crontab -
```

### **Analytics e Metriche**
```bash
# Report completo con statistiche
node scripts/check-playstore-status.js > reports/daily-report.txt

# Storico status changes
grep "STATUS CHANGE" reports/monitor.log
```

## 📱 **Comandi Rapidi di Riferimento**

```bash
# CONTROLLO STATO
npm run check:playstore        # Check immediato
npm run status:playstore       # Status corrente  
npm run monitor:playstore      # Monitoring continuo

# GENERAZIONE LINK
npm run generate:links         # Tutti i link + QR codes

# DASHBOARD WEB
npm run dashboard:playstore    # Avvia dashboard web

# DEPLOYMENT
npm run deploy:internal        # Deploy testing
npm run deploy:beta           # Deploy beta
npm run deploy:production     # Deploy produzione

# TROUBLESHOOTING
./scripts/monitor-playstore.sh logs    # Visualizza log
cat reports/playstore-status.json      # Status JSON
```

## 🎉 **Risultati del Sistema**

### **Vantaggi del Monitoring:**
- ⚡ **Controllo immediato** in 30 secondi
- 🔄 **Monitoring automatico** 24/7
- 📱 **Dashboard visuale** user-friendly
- 📊 **Metriche dettagliate** (rating, downloads, etc.)
- 🔗 **Link pronti** per condivisione
- 📱 **QR codes** per installazione mobile
- 📧 **Notifiche automatiche** quando app diventa live

### **Peace of Mind:**
- ✅ Sempre sai se la tua app è live
- ✅ Notifiche immediate quando pubblicata
- ✅ Link pronti per marketing
- ✅ Troubleshooting automatico
- ✅ Storico completo cambiamenti status

---

**🔍 Monitor with Confidence!**  
*Know exactly when AUTENTICO v2.2 goes live on Google Play Store* 📱

*Documentazione aggiornata: Settembre 2024*