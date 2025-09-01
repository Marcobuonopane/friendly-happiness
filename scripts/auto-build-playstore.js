#!/usr/bin/env node
/**
 * AUTENTICO v2.2 - Automated Google Play Store Build System
 * Sistema di Build Automatico per Google Play Store
 * © 2024 Marco Buonopane
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🤖 AUTENTICO v2.2 - Automated Play Store Build');
console.log('================================================');

const config = {
  appName: 'AUTENTICO v2.2',
  packageName: 'com.marcobuonopane.autentico',
  versionName: '2.2.0',
  versionCode: null,
  buildType: 'release',
  outputDir: './dist/playstore',
  keystoreFile: './android/keystore/autentico-keystore.jks',
  keystoreAlias: 'autentico',
  gradleBuildDir: './android'
};

class PlayStoreBuildSystem {
  constructor(config) {
    this.config = config;
    this.startTime = Date.now();
  }

  async run() {
    try {
      console.log('🚀 Starting automated build process...\n');
      
      await this.validateEnvironment();
      await this.incrementVersionCode();
      await this.prepareBuildEnvironment();
      await this.buildWebAssets();
      await this.setupCapacitor();
      await this.generateKeystore();
      await this.configureGradleSigning();
      await this.buildAAB();
      await this.validateAAB();
      await this.generateMetadata();
      
      this.showBuildSummary();
      
    } catch (error) {
      console.error('❌ Build failed:', error.message);
      process.exit(1);
    }
  }

  async validateEnvironment() {
    console.log('🔍 Validating build environment...');
    
    // Check Node.js
    try {
      const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
      console.log(`   ✅ Node.js: ${nodeVersion}`);
    } catch (error) {
      throw new Error('Node.js not found. Please install Node.js 14+');
    }

    // Check Java
    try {
      const javaVersion = execSync('java -version 2>&1', { encoding: 'utf8' });
      console.log('   ✅ Java: Installed');
    } catch (error) {
      console.log('   ⚠️  Java not found. Installing OpenJDK...');
      // Auto-install Java if needed
      try {
        execSync('apt-get update && apt-get install -y openjdk-11-jdk', { stdio: 'inherit' });
        console.log('   ✅ Java: Installed automatically');
      } catch (installError) {
        throw new Error('Failed to install Java. Please install manually.');
      }
    }

    // Check Capacitor CLI
    try {
      execSync('npx cap --version', { encoding: 'utf8' });
      console.log('   ✅ Capacitor CLI: Available');
    } catch (error) {
      console.log('   📦 Installing Capacitor CLI...');
      execSync('npm install -g @capacitor/cli', { stdio: 'inherit' });
      console.log('   ✅ Capacitor CLI: Installed');
    }

    console.log('');
  }

  async incrementVersionCode() {
    console.log('📊 Managing version numbers...');
    
    // Read current version code from file or generate new one
    const versionFile = './build/version.json';
    let versionData = { versionCode: 1 };
    
    if (fs.existsSync(versionFile)) {
      versionData = JSON.parse(fs.readFileSync(versionFile, 'utf8'));
    }
    
    // Increment version code
    versionData.versionCode += 1;
    versionData.versionName = this.config.versionName;
    versionData.buildDate = new Date().toISOString();
    
    this.config.versionCode = versionData.versionCode;
    
    // Save updated version
    fs.writeFileSync(versionFile, JSON.stringify(versionData, null, 2));
    
    console.log(`   ✅ Version: ${this.config.versionName} (${this.config.versionCode})`);
    console.log('');
  }

  async prepareBuildEnvironment() {
    console.log('🏗️  Preparing build environment...');
    
    // Clean previous builds
    if (fs.existsSync(this.config.outputDir)) {
      execSync(`rm -rf ${this.config.outputDir}`, { stdio: 'inherit' });
    }
    fs.mkdirSync(this.config.outputDir, { recursive: true });
    
    // Create necessary directories
    fs.mkdirSync('./android/keystore', { recursive: true });
    
    console.log('   ✅ Build directories prepared');
    console.log('');
  }

  async buildWebAssets() {
    console.log('🌐 Building web assets...');
    
    // Run our custom build script
    execSync('node build/build.js', { stdio: 'inherit' });
    
    console.log('   ✅ Web assets built successfully');
    console.log('');
  }

  async setupCapacitor() {
    console.log('📱 Setting up Capacitor...');
    
    // Initialize Capacitor if not already done
    if (!fs.existsSync('./capacitor.config.json')) {
      throw new Error('capacitor.config.json not found');
    }
    
    // Add Android platform if not exists
    if (!fs.existsSync('./android')) {
      console.log('   📦 Adding Android platform...');
      execSync('npx cap add android', { stdio: 'inherit' });
    }
    
    // Sync web assets to native
    console.log('   🔄 Syncing assets to Android...');
    execSync('npx cap sync android', { stdio: 'inherit' });
    
    console.log('   ✅ Capacitor setup complete');
    console.log('');
  }

  async generateKeystore() {
    console.log('🔐 Checking signing keystore...');
    
    if (fs.existsSync(this.config.keystoreFile)) {
      console.log('   ✅ Keystore already exists');
    } else {
      console.log('   🔑 Generating new keystore...');
      
      const keystoreCommand = [
        'keytool -genkey -v',
        `-keystore ${this.config.keystoreFile}`,
        '-keyalg RSA -keysize 2048 -validity 10000',
        `-alias ${this.config.keystoreAlias}`,
        '-dname "CN=AUTENTICO, OU=Marco Buonopane, O=AUTENTICO, L=Roma, ST=Lazio, C=IT"',
        '-storepass autentico2024',
        '-keypass autentico2024'
      ].join(' ');
      
      try {
        execSync(keystoreCommand, { stdio: 'inherit' });
        console.log('   ✅ Keystore generated successfully');
      } catch (error) {
        throw new Error('Failed to generate keystore');
      }
    }
    console.log('');
  }

  async configureGradleSigning() {
    console.log('📝 Configuring Gradle signing...');
    
    const buildGradlePath = './android/app/build.gradle';
    
    if (!fs.existsSync(buildGradlePath)) {
      throw new Error('Android build.gradle not found');
    }
    
    // Read current build.gradle
    let buildGradle = fs.readFileSync(buildGradlePath, 'utf8');
    
    // Add signing config if not present
    const signingConfigBlock = `
    signingConfigs {
        release {
            storeFile file('../../android/keystore/autentico-keystore.jks')
            storePassword 'autentico2024'
            keyAlias 'autentico'
            keyPassword 'autentico2024'
        }
    }`;
    
    if (!buildGradle.includes('signingConfigs')) {
      buildGradle = buildGradle.replace(
        'android {', 
        `android {\n${signingConfigBlock}`
      );
    }
    
    // Update buildTypes to use signing config
    if (!buildGradle.includes('signingConfig signingConfigs.release')) {
      buildGradle = buildGradle.replace(
        /buildTypes\s*{\s*release\s*{/g,
        `buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'`
      );
    }
    
    // Update version information
    buildGradle = buildGradle.replace(
      /versionCode\s+\d+/,
      `versionCode ${this.config.versionCode}`
    );
    buildGradle = buildGradle.replace(
      /versionName\s+"[^"]*"/,
      `versionName "${this.config.versionName}"`
    );
    
    fs.writeFileSync(buildGradlePath, buildGradle);
    
    console.log('   ✅ Gradle signing configured');
    console.log('');
  }

  async buildAAB() {
    console.log('🔨 Building signed AAB for Play Store...');
    
    process.chdir('./android');
    
    try {
      // Clean previous builds
      console.log('   🧹 Cleaning previous builds...');
      execSync('./gradlew clean', { stdio: 'inherit' });
      
      // Build signed AAB
      console.log('   📦 Building release AAB...');
      execSync('./gradlew bundleRelease', { stdio: 'inherit' });
      
      // Also build APK for testing
      console.log('   📱 Building release APK...');
      execSync('./gradlew assembleRelease', { stdio: 'inherit' });
      
    } finally {
      process.chdir('..');
    }
    
    // Copy outputs to our output directory
    const aabSource = './android/app/build/outputs/bundle/release/app-release.aab';
    const apkSource = './android/app/build/outputs/apk/release/app-release.apk';
    
    const aabDest = path.join(this.config.outputDir, `autentico-v${this.config.versionName}-${this.config.versionCode}.aab`);
    const apkDest = path.join(this.config.outputDir, `autentico-v${this.config.versionName}-${this.config.versionCode}.apk`);
    
    if (fs.existsSync(aabSource)) {
      fs.copyFileSync(aabSource, aabDest);
      console.log(`   ✅ AAB copied to: ${aabDest}`);
    }
    
    if (fs.existsSync(apkSource)) {
      fs.copyFileSync(apkSource, apkDest);
      console.log(`   ✅ APK copied to: ${apkDest}`);
    }
    
    console.log('');
  }

  async validateAAB() {
    console.log('🔍 Validating AAB file...');
    
    const aabFile = path.join(this.config.outputDir, `autentico-v${this.config.versionName}-${this.config.versionCode}.aab`);
    
    if (!fs.existsSync(aabFile)) {
      throw new Error('AAB file not found');
    }
    
    const stats = fs.statSync(aabFile);
    const fileSizeMB = (stats.size / 1024 / 1024).toFixed(2);
    
    console.log(`   ✅ AAB Size: ${fileSizeMB} MB`);
    
    if (stats.size > 150 * 1024 * 1024) { // 150MB limit
      console.log('   ⚠️  Warning: AAB size is quite large');
    }
    
    console.log('   ✅ AAB validation passed');
    console.log('');
  }

  async generateMetadata() {
    console.log('📄 Generating build metadata...');
    
    const metadata = {
      appName: this.config.appName,
      packageName: this.config.packageName,
      versionName: this.config.versionName,
      versionCode: this.config.versionCode,
      buildDate: new Date().toISOString(),
      buildDuration: Date.now() - this.startTime,
      files: {
        aab: `autentico-v${this.config.versionName}-${this.config.versionCode}.aab`,
        apk: `autentico-v${this.config.versionName}-${this.config.versionCode}.apk`
      },
      playStoreReady: true,
      signingConfigured: true
    };
    
    const metadataFile = path.join(this.config.outputDir, 'build-metadata.json');
    fs.writeFileSync(metadataFile, JSON.stringify(metadata, null, 2));
    
    console.log(`   ✅ Metadata saved to: ${metadataFile}`);
    console.log('');
  }

  showBuildSummary() {
    const duration = Math.round((Date.now() - this.startTime) / 1000);
    
    console.log('🎉 BUILD COMPLETED SUCCESSFULLY!');
    console.log('================================');
    console.log(`📱 App: ${this.config.appName}`);
    console.log(`📦 Package: ${this.config.packageName}`);
    console.log(`🔢 Version: ${this.config.versionName} (${this.config.versionCode})`);
    console.log(`⏱️  Duration: ${duration} seconds`);
    console.log(`📁 Output: ${this.config.outputDir}`);
    console.log('');
    console.log('📂 Generated Files:');
    console.log(`   • AAB: autentico-v${this.config.versionName}-${this.config.versionCode}.aab`);
    console.log(`   • APK: autentico-v${this.config.versionName}-${this.config.versionCode}.apk`);
    console.log(`   • Metadata: build-metadata.json`);
    console.log('');
    console.log('🚀 Ready for Google Play Store upload!');
    console.log('');
    console.log('Next steps:');
    console.log('1. Upload AAB to Google Play Console');
    console.log('2. Fill store listing information');
    console.log('3. Submit for review');
    console.log('');
    console.log('Or use automated deployment:');
    console.log('npm run deploy:playstore');
  }
}

// Run the build system
if (require.main === module) {
  const buildSystem = new PlayStoreBuildSystem(config);
  buildSystem.run();
}

module.exports = PlayStoreBuildSystem;