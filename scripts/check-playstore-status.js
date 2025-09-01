#!/usr/bin/env node
/**
 * AUTENTICO v2.2 - Google Play Store Status Checker
 * Verifica se l'app è pubblicata e visibile su Google Play Store
 * © 2024 Marco Buonopane
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configurazione app
const config = {
  packageName: 'com.marcobuonopane.autentico',
  appName: 'AUTENTICO v2.2',
  playStoreUrl: 'https://play.google.com/store/apps/details?id=com.marcobuonopane.autentico',
  playStoreApiUrl: 'https://play.google.com/store/apps/details',
  internalTestingUrl: 'https://play.google.com/apps/internaltest',
  betaTestingUrl: 'https://play.google.com/apps/test'
};

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  purple: '\x1b[35m',
  cyan: '\x1b[36m'
};

class PlayStoreChecker {
  constructor(config) {
    this.config = config;
    this.results = {};
  }

  log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  async run() {
    this.log('🔍 AUTENTICO v2.2 - Play Store Status Check', 'purple');
    this.log('===========================================', 'purple');
    this.log('');
    
    await this.checkPublicStore();
    await this.checkAppMetadata();
    await this.checkInstallLinks();
    await this.generateStatusReport();
    
    this.showSummary();
  }

  async checkPublicStore() {
    this.log('📱 Checking Google Play Store public visibility...', 'blue');
    
    try {
      const response = await this.makeRequest(this.config.playStoreUrl);
      
      if (response.includes('Install') || response.includes('Installa')) {
        this.log('   ✅ App is PUBLIC and installable!', 'green');
        this.results.publicStore = {
          status: 'live',
          installable: true,
          url: this.config.playStoreUrl
        };
      } else if (response.includes('Pre-register')) {
        this.log('   ⏳ App is in PRE-REGISTRATION mode', 'yellow');
        this.results.publicStore = {
          status: 'pre-register',
          installable: false,
          url: this.config.playStoreUrl
        };
      } else if (response.includes('Not available')) {
        this.log('   ❌ App not available in this region', 'red');
        this.results.publicStore = {
          status: 'region-locked',
          installable: false,
          url: this.config.playStoreUrl
        };
      } else {
        this.log('   ❌ App not found on public Play Store', 'red');
        this.results.publicStore = {
          status: 'not-found',
          installable: false,
          url: null
        };
      }
    } catch (error) {
      this.log(`   ❌ Error checking public store: ${error.message}`, 'red');
      this.results.publicStore = {
        status: 'error',
        installable: false,
        error: error.message
      };
    }
    
    this.log('');
  }

  async checkAppMetadata() {
    this.log('📋 Extracting app metadata from Play Store...', 'blue');
    
    try {
      const response = await this.makeRequest(this.config.playStoreUrl);
      
      // Extract app info using regex patterns
      const titleMatch = response.match(/<title[^>]*>([^<]+)<\/title>/i);
      const ratingMatch = response.match(/"aggregateRating":{"@type":"AggregateRating","ratingValue":([^,}]+)/);
      const reviewsMatch = response.match(/"reviewCount":(\d+)/);
      const versionMatch = response.match(/"softwareVersion":"([^"]+)"/);
      const downloadsMatch = response.match(/"numDownloads":"([^"]+)"/);
      const updateDateMatch = response.match(/"datePublished":"([^"]+)"/);
      
      this.results.metadata = {
        title: titleMatch ? titleMatch[1].trim() : 'Unknown',
        rating: ratingMatch ? parseFloat(ratingMatch[1]) : null,
        reviews: reviewsMatch ? parseInt(reviewsMatch[1]) : null,
        version: versionMatch ? versionMatch[1] : null,
        downloads: downloadsMatch ? downloadsMatch[1] : null,
        lastUpdate: updateDateMatch ? updateDateMatch[1] : null
      };
      
      this.log(`   📱 Title: ${this.results.metadata.title}`, 'cyan');
      this.log(`   ⭐ Rating: ${this.results.metadata.rating || 'No ratings yet'}`, 'cyan');
      this.log(`   💬 Reviews: ${this.results.metadata.reviews || '0'}`, 'cyan');
      this.log(`   🔢 Version: ${this.results.metadata.version || 'Unknown'}`, 'cyan');
      this.log(`   📥 Downloads: ${this.results.metadata.downloads || 'Not available'}`, 'cyan');
      this.log(`   📅 Last Update: ${this.results.metadata.lastUpdate || 'Unknown'}`, 'cyan');
      
    } catch (error) {
      this.log(`   ⚠️  Could not extract metadata: ${error.message}`, 'yellow');
      this.results.metadata = { error: error.message };
    }
    
    this.log('');
  }

  async checkInstallLinks() {
    this.log('🔗 Generating installation links...', 'blue');
    
    const links = {
      public: `https://play.google.com/store/apps/details?id=${this.config.packageName}`,
      directInstall: `https://play.app.goo.gl/?link=https://play.google.com/store/apps/details?id=${this.config.packageName}`,
      marketUrl: `market://details?id=${this.config.packageName}`,
      webInstall: `https://play.google.com/store/apps/details?id=${this.config.packageName}&launch=true`
    };
    
    this.results.installLinks = links;
    
    this.log('   🌐 Public Store:', 'cyan');
    this.log(`      ${links.public}`, 'reset');
    this.log('   📱 Direct Install:', 'cyan');
    this.log(`      ${links.directInstall}`, 'reset');
    this.log('   📲 Market URL:', 'cyan');
    this.log(`      ${links.marketUrl}`, 'reset');
    this.log('   ⚡ Web Install:', 'cyan');
    this.log(`      ${links.webInstall}`, 'reset');
    
    this.log('');
  }

  async generateStatusReport() {
    this.log('📊 Generating status report...', 'blue');
    
    const report = {
      timestamp: new Date().toISOString(),
      app: {
        name: this.config.appName,
        packageName: this.config.packageName
      },
      status: this.results.publicStore,
      metadata: this.results.metadata,
      links: this.results.installLinks,
      checks: {
        publicStore: this.results.publicStore.status === 'live',
        installable: this.results.publicStore.installable,
        hasMetadata: !!this.results.metadata && !this.results.metadata.error
      }
    };
    
    // Save report to file
    const reportPath = path.join(__dirname, '../reports/playstore-status.json');
    await this.ensureDirectoryExists(path.dirname(reportPath));
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    this.log(`   ✅ Report saved to: ${reportPath}`, 'green');
    this.results.report = report;
    
    this.log('');
  }

  showSummary() {
    this.log('📈 PLAY STORE STATUS SUMMARY', 'purple');
    this.log('============================', 'purple');
    this.log('');
    
    const status = this.results.publicStore.status;
    
    switch (status) {
      case 'live':
        this.log('🎉 SUCCESS! AUTENTICO v2.2 is LIVE on Google Play Store!', 'green');
        this.log('');
        this.log('✅ Your app is:', 'green');
        this.log('   • Publicly visible on Google Play Store', 'green');
        this.log('   • Available for installation by users', 'green');
        this.log('   • Searchable in the Play Store', 'green');
        this.log('');
        this.log('🔗 Share these links:', 'blue');
        this.log(`   ${this.results.installLinks.public}`, 'cyan');
        break;
        
      case 'pre-register':
        this.log('⏳ App is in PRE-REGISTRATION mode', 'yellow');
        this.log('   Users can pre-register but not install yet', 'yellow');
        break;
        
      case 'region-locked':
        this.log('🌍 App is published but not available in this region', 'yellow');
        this.log('   Check your app\'s country availability settings', 'yellow');
        break;
        
      case 'not-found':
        this.log('❌ App not found on Google Play Store', 'red');
        this.log('');
        this.log('Possible reasons:', 'yellow');
        this.log('   • App is still in review process', 'yellow');
        this.log('   • App was rejected and needs fixes', 'yellow');
        this.log('   • App is in internal/beta testing only', 'yellow');
        this.log('   • Wrong package name or not published yet', 'yellow');
        break;
        
      case 'error':
        this.log('❌ Could not check Play Store status', 'red');
        this.log(`   Error: ${this.results.publicStore.error}`, 'red');
        break;
    }
    
    this.log('');
    this.log('💡 Next steps:', 'blue');
    
    if (status === 'live') {
      this.log('   • Monitor app reviews and ratings', 'cyan');
      this.log('   • Track download statistics', 'cyan');
      this.log('   • Update app store listing if needed', 'cyan');
      this.log('   • Plan next version releases', 'cyan');
    } else {
      this.log('   • Check Google Play Console for app status', 'cyan');
      this.log('   • Review any rejection reasons', 'cyan');
      this.log('   • Verify app meets Play Store policies', 'cyan');
      this.log('   • Re-submit if necessary', 'cyan');
    }
    
    this.log('');
    this.log('🔧 Useful commands:', 'blue');
    this.log('   • npm run deploy:internal  # Deploy to internal testing', 'cyan');
    this.log('   • npm run deploy:beta     # Deploy to beta testing', 'cyan');  
    this.log('   • npm run deploy:production # Deploy to production', 'cyan');
    this.log('   • node scripts/check-playstore-status.js # Run this check again', 'cyan');
  }

  async makeRequest(url) {
    return new Promise((resolve, reject) => {
      const options = {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
      };
      
      https.get(url, options, (response) => {
        let data = '';
        
        response.on('data', (chunk) => {
          data += chunk;
        });
        
        response.on('end', () => {
          if (response.statusCode === 200) {
            resolve(data);
          } else {
            reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage}`));
          }
        });
      }).on('error', (error) => {
        reject(error);
      });
    });
  }

  async ensureDirectoryExists(dirPath) {
    try {
      await fs.promises.access(dirPath);
    } catch {
      await fs.promises.mkdir(dirPath, { recursive: true });
    }
  }
}

// Export for use in other scripts
module.exports = PlayStoreChecker;

// Run if called directly
if (require.main === module) {
  const checker = new PlayStoreChecker(config);
  checker.run().catch(console.error);
}