#!/bin/bash
##############################################################################
# AUTENTICO v2.2 - One-Click Google Play Store Deployment
# Deploy Automatico su Google Play Store con un solo comando
# © 2024 Marco Buonopane
##############################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# App configuration
APP_NAME="AUTENTICO v2.2"
PACKAGE_NAME="com.marcobuonopane.autentico"
DEFAULT_TRACK="internal"

echo -e "${PURPLE}🚀 AUTENTICO v2.2 - One-Click Play Store Deploy${NC}"
echo -e "${PURPLE}=================================================${NC}"
echo ""

# Parse command line arguments
TRACK=${1:-$DEFAULT_TRACK}
SKIP_BUILD=${2:-false}

echo -e "${BLUE}📱 App:${NC} $APP_NAME"
echo -e "${BLUE}📦 Package:${NC} $PACKAGE_NAME" 
echo -e "${BLUE}🎯 Track:${NC} $TRACK"
echo -e "${BLUE}⏩ Skip Build:${NC} $SKIP_BUILD"
echo ""

# Validate track
case $TRACK in
  "internal"|"beta"|"production")
    echo -e "${GREEN}✅ Valid deployment track: $TRACK${NC}"
    ;;
  *)
    echo -e "${RED}❌ Invalid track: $TRACK${NC}"
    echo -e "${YELLOW}Valid tracks: internal, beta, production${NC}"
    exit 1
    ;;
esac

# Function to check if command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to install missing dependencies
install_dependencies() {
  echo -e "${YELLOW}📦 Checking dependencies...${NC}"
  
  # Check Node.js
  if ! command_exists node; then
    echo -e "${YELLOW}Installing Node.js...${NC}"
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
  fi
  
  # Check Java
  if ! command_exists java; then
    echo -e "${YELLOW}Installing OpenJDK 11...${NC}"
    sudo apt-get update
    sudo apt-get install -y openjdk-11-jdk
  fi
  
  # Check Android SDK tools
  if ! command_exists android; then
    echo -e "${YELLOW}Setting up Android SDK...${NC}"
    # This would need more setup for a complete Android SDK installation
    echo -e "${YELLOW}⚠️  Android SDK setup may be needed${NC}"
  fi
  
  # Check Capacitor CLI
  if ! command_exists cap; then
    echo -e "${YELLOW}Installing Capacitor CLI...${NC}"
    npm install -g @capacitor/cli
  fi
  
  # Check Fastlane
  if ! command_exists fastlane; then
    echo -e "${YELLOW}Installing Fastlane...${NC}"
    sudo gem install fastlane
  fi
  
  echo -e "${GREEN}✅ Dependencies check complete${NC}"
  echo ""
}

# Function to build the app
build_app() {
  if [ "$SKIP_BUILD" = "true" ]; then
    echo -e "${YELLOW}⏩ Skipping build step${NC}"
    return
  fi
  
  echo -e "${BLUE}🔨 Building AUTENTICO v2.2...${NC}"
  
  # Run automated build script
  if [ -f "scripts/auto-build-playstore.js" ]; then
    node scripts/auto-build-playstore.js
  else
    echo -e "${YELLOW}⚠️  Using manual build process${NC}"
    
    # Manual build steps
    echo -e "${BLUE}🌐 Building web assets...${NC}"
    node build/build.js
    
    echo -e "${BLUE}📱 Setting up Capacitor...${NC}"
    if [ ! -d "android" ]; then
      npx cap add android
    fi
    npx cap sync android
    
    echo -e "${BLUE}📦 Building AAB...${NC}"
    cd android
    ./gradlew clean bundleRelease
    cd ..
  fi
  
  # Verify AAB exists
  AAB_PATH="android/app/build/outputs/bundle/release/app-release.aab"
  if [ -f "$AAB_PATH" ]; then
    AAB_SIZE=$(du -h "$AAB_PATH" | cut -f1)
    echo -e "${GREEN}✅ AAB built successfully - Size: $AAB_SIZE${NC}"
  else
    echo -e "${RED}❌ AAB build failed - file not found${NC}"
    exit 1
  fi
  
  echo ""
}

# Function to deploy to Play Store
deploy_to_playstore() {
  echo -e "${BLUE}🚀 Deploying to Google Play Store...${NC}"
  
  # Check for Google Play API key
  if [ ! -f "fastlane/google-play-api-key.json" ]; then
    echo -e "${RED}❌ Google Play API key not found${NC}"
    echo -e "${YELLOW}Please ensure fastlane/google-play-api-key.json exists${NC}"
    echo -e "${YELLOW}Download it from Google Play Console > Setup > API access${NC}"
    exit 1
  fi
  
  # Deploy using Fastlane
  case $TRACK in
    "internal")
      fastlane android deploy_internal
      ;;
    "beta")
      fastlane android deploy_beta
      ;;
    "production")
      fastlane android deploy_playstore
      ;;
  esac
  
  echo -e "${GREEN}✅ Deployment to $TRACK track completed!${NC}"
  echo ""
}

# Function to show deployment summary
show_summary() {
  echo -e "${PURPLE}🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
  echo -e "${PURPLE}===================================${NC}"
  echo ""
  echo -e "${GREEN}📱 App:${NC} $APP_NAME"
  echo -e "${GREEN}🎯 Track:${NC} $TRACK"
  echo -e "${GREEN}⏰ Time:${NC} $(date)"
  echo ""
  
  case $TRACK in
    "internal")
      echo -e "${BLUE}📋 Next steps:${NC}"
      echo -e "   1. Check Google Play Console for internal testing"
      echo -e "   2. Share internal testing link with team"
      echo -e "   3. Collect feedback and test thoroughly"
      ;;
    "beta")
      echo -e "${BLUE}📋 Next steps:${NC}"
      echo -e "   1. Wait for Play Store review (usually 2-4 hours)"
      echo -e "   2. Share beta testing link with users"
      echo -e "   3. Monitor crash reports and user feedback"
      ;;
    "production")
      echo -e "${BLUE}📋 Next steps:${NC}"
      echo -e "   1. Wait for Play Store review (usually 1-3 days)"
      echo -e "   2. Monitor app performance and reviews"
      echo -e "   3. Celebrate! 🎉"
      ;;
  esac
  
  echo ""
  echo -e "${YELLOW}💡 Useful commands:${NC}"
  echo -e "   • Deploy to internal: ./scripts/deploy-playstore.sh internal"
  echo -e "   • Deploy to beta: ./scripts/deploy-playstore.sh beta"
  echo -e "   • Deploy to production: ./scripts/deploy-playstore.sh production"
  echo -e "   • Skip build: ./scripts/deploy-playstore.sh internal true"
  echo ""
}

# Function to handle errors
handle_error() {
  echo -e "${RED}❌ Deployment failed!${NC}"
  echo -e "${YELLOW}Error occurred in: $1${NC}"
  echo ""
  echo -e "${BLUE}💡 Troubleshooting tips:${NC}"
  echo -e "   • Check your Google Play Console API key"
  echo -e "   • Verify your app signing configuration"  
  echo -e "   • Ensure all required metadata is present"
  echo -e "   • Check the build logs for specific errors"
  echo ""
  exit 1
}

# Main execution flow
main() {
  # Trap errors
  trap 'handle_error "main execution"' ERR
  
  # Install dependencies
  install_dependencies
  
  # Build the app
  build_app
  
  # Deploy to Play Store
  deploy_to_playstore
  
  # Show summary
  show_summary
}

# Usage information
show_usage() {
  echo "Usage: $0 [TRACK] [SKIP_BUILD]"
  echo ""
  echo "TRACK options:"
  echo "  internal   - Deploy to internal testing (default)"
  echo "  beta       - Deploy to beta testing"
  echo "  production - Deploy to production"
  echo ""
  echo "SKIP_BUILD options:"
  echo "  false      - Build the app (default)"
  echo "  true       - Skip build, use existing AAB"
  echo ""
  echo "Examples:"
  echo "  $0                    # Deploy to internal with build"
  echo "  $0 beta               # Deploy to beta with build"
  echo "  $0 production         # Deploy to production with build"
  echo "  $0 internal true      # Deploy to internal, skip build"
  echo ""
}

# Check for help flag
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  show_usage
  exit 0
fi

# Run main function
main

echo -e "${GREEN}🏁 All done! AUTENTICO v2.2 is live on Google Play Store!${NC}"