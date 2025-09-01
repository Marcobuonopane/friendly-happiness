#!/usr/bin/env node
/**
 * AUTENTICO v2.2 - Store Links & QR Code Generator
 * Genera tutti i link necessari per Google Play Store e QR codes
 * © 2024 Marco Buonopane
 */

const fs = require('fs');
const path = require('path');

const config = {
  packageName: 'com.marcobuonopane.autentico',
  appName: 'AUTENTICO v2.2',
  developerName: 'Marco Buonopane'
};

class StoreLinkGenerator {
  constructor(config) {
    this.config = config;
  }

  generateAllLinks() {
    console.log('🔗 AUTENTICO v2.2 - Store Links Generator');
    console.log('=======================================');
    console.log('');
    
    const links = this.createLinks();
    const qrCodes = this.createQRCodes(links);
    const socialShareLinks = this.createSocialLinks(links);
    
    this.displayLinks(links, qrCodes, socialShareLinks);
    this.saveToFiles(links, qrCodes, socialShareLinks);
    
    return { links, qrCodes, socialShareLinks };
  }

  createLinks() {
    const packageName = this.config.packageName;
    
    return {
      // Google Play Store Links
      playStore: `https://play.google.com/store/apps/details?id=${packageName}`,
      playStoreShort: `https://play.app.goo.gl/?link=https://play.google.com/store/apps/details?id=${packageName}`,
      
      // Market Links (for Android deep linking)
      marketDetails: `market://details?id=${packageName}`,
      marketSearch: `market://search?q=${packageName}`,
      
      // Direct Install Links
      webInstall: `https://play.google.com/store/apps/details?id=${packageName}&launch=true`,
      
      // Developer Page
      developerPage: `https://play.google.com/store/apps/developer?id=${encodeURIComponent(this.config.developerName)}`,
      
      // Testing Links (require special access)
      internalTesting: `https://play.google.com/apps/internaltest/${packageName}`,
      betaTesting: `https://play.google.com/apps/test/${packageName}`,
      
      // Alternative App Stores
      amazonAppstore: `https://www.amazon.com/gp/mas/dl/android?p=${packageName}`,
      samsungGalaxyStore: `https://galaxystore.samsung.com/detail/${packageName}`,
      
      // APK Download (if hosted elsewhere)
      apkDirect: `https://github.com/Marcobuonopane/friendly-happiness/releases/latest/download/autentico-v2.2.0.apk`,
      
      // Social Proof Links
      githubRepo: 'https://github.com/Marcobuonopane/friendly-happiness',
      
      // Support Links
      support: 'mailto:marco.buonopane@example.com',
      website: 'https://marcobuonopane.github.io/autentico'
    };
  }

  createQRCodes(links) {
    // QR Code URLs using Google Charts API (free service)
    const qrBaseUrl = 'https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl=';
    
    return {
      playStore: `${qrBaseUrl}${encodeURIComponent(links.playStore)}`,
      playStoreShort: `${qrBaseUrl}${encodeURIComponent(links.playStoreShort)}`,
      webInstall: `${qrBaseUrl}${encodeURIComponent(links.webInstall)}`,
      githubRepo: `${qrBaseUrl}${encodeURIComponent(links.githubRepo)}`,
      website: `${qrBaseUrl}${encodeURIComponent(links.website)}`
    };
  }

  createSocialLinks(links) {
    const appUrl = encodeURIComponent(links.playStore);
    const appName = encodeURIComponent(this.config.appName);
    const message = encodeURIComponent(`Scopri ${this.config.appName} - Sistema di Certificazione Digitale Sicura!`);
    
    return {
      // Social Media Sharing
      twitter: `https://twitter.com/intent/tweet?text=${message}&url=${appUrl}`,
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${appUrl}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${appUrl}`,
      whatsapp: `https://wa.me/?text=${message}%20${appUrl}`,
      telegram: `https://t.me/share/url?url=${appUrl}&text=${message}`,
      
      // Email Sharing
      email: `mailto:?subject=${appName}&body=${message}%20${appUrl}`,
      
      // Reddit
      reddit: `https://reddit.com/submit?url=${appUrl}&title=${message}`,
      
      // Other Platforms
      pinterest: `https://pinterest.com/pin/create/button/?url=${appUrl}&description=${message}`,
      tumblr: `https://www.tumblr.com/share/link?url=${appUrl}&name=${appName}&description=${message}`
    };
  }

  displayLinks(links, qrCodes, socialShareLinks) {
    console.log('📱 GOOGLE PLAY STORE LINKS:');
    console.log('============================');
    console.log(`🏪 Play Store:          ${links.playStore}`);
    console.log(`🔗 Short Link:          ${links.playStoreShort}`);
    console.log(`⚡ Web Install:         ${links.webInstall}`);
    console.log(`📱 Market Deep Link:    ${links.marketDetails}`);
    console.log(`👨‍💻 Developer Page:      ${links.developerPage}`);
    console.log('');
    
    console.log('🧪 TESTING LINKS:');
    console.log('==================');
    console.log(`🔒 Internal Testing:    ${links.internalTesting}`);
    console.log(`🔬 Beta Testing:        ${links.betaTesting}`);
    console.log('');
    
    console.log('🏬 ALTERNATIVE STORES:');
    console.log('======================');
    console.log(`📦 Amazon Appstore:     ${links.amazonAppstore}`);
    console.log(`🌟 Samsung Galaxy Store: ${links.samsungGalaxyStore}`);
    console.log(`📲 Direct APK:          ${links.apkDirect}`);
    console.log('');
    
    console.log('📋 QR CODES:');
    console.log('=============');
    console.log(`🏪 Play Store QR:       ${qrCodes.playStore}`);
    console.log(`🔗 Short Link QR:       ${qrCodes.playStoreShort}`);
    console.log(`🌐 Website QR:          ${qrCodes.website}`);
    console.log(`💻 GitHub QR:           ${qrCodes.githubRepo}`);
    console.log('');
    
    console.log('📢 SOCIAL SHARING:');
    console.log('==================');
    console.log(`🐦 Twitter:             ${socialShareLinks.twitter}`);
    console.log(`📘 Facebook:            ${socialShareLinks.facebook}`);
    console.log(`💼 LinkedIn:            ${socialShareLinks.linkedin}`);
    console.log(`💬 WhatsApp:            ${socialShareLinks.whatsapp}`);
    console.log(`✈️  Telegram:            ${socialShareLinks.telegram}`);
    console.log(`📧 Email:               ${socialShareLinks.email}`);
    console.log('');
    
    console.log('🔗 SUPPORT & INFO:');
    console.log('==================');
    console.log(`💻 GitHub Repository:   ${links.githubRepo}`);
    console.log(`🌐 Website:             ${links.website}`);
    console.log(`📧 Support:             ${links.support}`);
    console.log('');
  }

  saveToFiles(links, qrCodes, socialShareLinks) {
    const outputData = {
      timestamp: new Date().toISOString(),
      app: {
        name: this.config.appName,
        packageName: this.config.packageName,
        developer: this.config.developerName
      },
      links,
      qrCodes,
      socialShareLinks
    };
    
    // Save as JSON
    const jsonPath = path.join(__dirname, '../reports/store-links.json');
    fs.writeFileSync(jsonPath, JSON.stringify(outputData, null, 2));
    console.log(`✅ Links saved to: ${jsonPath}`);
    
    // Generate HTML page with all links
    const htmlContent = this.generateHTML(outputData);
    const htmlPath = path.join(__dirname, '../reports/store-links.html');
    fs.writeFileSync(htmlPath, htmlContent);
    console.log(`✅ HTML page saved to: ${htmlPath}`);
    
    // Generate markdown for documentation
    const markdownContent = this.generateMarkdown(outputData);
    const mdPath = path.join(__dirname, '../docs/STORE_LINKS.md');
    fs.writeFileSync(mdPath, markdownContent);
    console.log(`✅ Markdown saved to: ${mdPath}`);
    
    console.log('');
    console.log('🎉 All store links generated successfully!');
  }

  generateHTML(data) {
    return `<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${data.app.name} - Store Links</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        .link-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .link-card { background: #f9f9f9; padding: 15px; border-radius: 8px; }
        .qr-code { text-align: center; margin: 10px 0; }
        .qr-code img { width: 150px; height: 150px; }
        h1, h2 { color: #333; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📱 ${data.app.name} - Store Links</h1>
    <p><strong>Package:</strong> ${data.app.packageName}</p>
    <p><strong>Developer:</strong> ${data.app.developer}</p>
    <p><strong>Generated:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
    
    <div class="section">
        <h2>🏪 Google Play Store</h2>
        <div class="link-grid">
            <div class="link-card">
                <h3>Play Store Link</h3>
                <a href="${data.links.playStore}" target="_blank">${data.links.playStore}</a>
                <div class="qr-code">
                    <img src="${data.qrCodes.playStore}" alt="Play Store QR">
                </div>
            </div>
            <div class="link-card">
                <h3>Short Link</h3>
                <a href="${data.links.playStoreShort}" target="_blank">${data.links.playStoreShort}</a>
                <div class="qr-code">
                    <img src="${data.qrCodes.playStoreShort}" alt="Short Link QR">
                </div>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>📢 Social Sharing</h2>
        <div class="link-grid">
            <div class="link-card"><a href="${data.socialShareLinks.twitter}" target="_blank">🐦 Share on Twitter</a></div>
            <div class="link-card"><a href="${data.socialShareLinks.facebook}" target="_blank">📘 Share on Facebook</a></div>
            <div class="link-card"><a href="${data.socialShareLinks.linkedin}" target="_blank">💼 Share on LinkedIn</a></div>
            <div class="link-card"><a href="${data.socialShareLinks.whatsapp}" target="_blank">💬 Share on WhatsApp</a></div>
            <div class="link-card"><a href="${data.socialShareLinks.email}" target="_blank">📧 Share via Email</a></div>
        </div>
    </div>
</body>
</html>`;
  }

  generateMarkdown(data) {
    return `# 📱 ${data.app.name} - Store Links

**Package:** \`${data.app.packageName}\`  
**Developer:** ${data.app.developer}  
**Generated:** ${new Date(data.timestamp).toLocaleString()}

## 🏪 Google Play Store Links

### Primary Links
- **Play Store:** ${data.links.playStore}
- **Short Link:** ${data.links.playStoreShort}
- **Web Install:** ${data.links.webInstall}

### Deep Links
- **Market Details:** \`${data.links.marketDetails}\`
- **Market Search:** \`${data.links.marketSearch}\`

### QR Codes
- **Play Store QR:** ![QR](${data.qrCodes.playStore})
- **Short Link QR:** ![QR](${data.qrCodes.playStoreShort})

## 🧪 Testing Links
- **Internal Testing:** ${data.links.internalTesting}
- **Beta Testing:** ${data.links.betaTesting}

## 🏬 Alternative Stores
- **Amazon Appstore:** ${data.links.amazonAppstore}
- **Samsung Galaxy Store:** ${data.links.samsungGalaxyStore}
- **Direct APK:** ${data.links.apkDirect}

## 📢 Social Sharing Links
- **Twitter:** ${data.socialShareLinks.twitter}
- **Facebook:** ${data.socialShareLinks.facebook}
- **LinkedIn:** ${data.socialShareLinks.linkedin}
- **WhatsApp:** ${data.socialShareLinks.whatsapp}
- **Email:** ${data.socialShareLinks.email}

## 🔗 Support & Resources
- **GitHub Repository:** ${data.links.githubRepo}
- **Website:** ${data.links.website}
- **Support Email:** ${data.links.support}
- **Developer Page:** ${data.links.developerPage}

---
*Generated by AUTENTICO v2.2 Store Links Generator*`;
  }
}

// Export for use in other scripts
module.exports = StoreLinkGenerator;

// Run if called directly
if (require.main === module) {
  const generator = new StoreLinkGenerator(config);
  generator.generateAllLinks();
}