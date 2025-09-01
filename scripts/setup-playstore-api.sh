#!/bin/bash
##############################################################################
# AUTENTICO v2.2 - Google Play Console API Setup
# Script per configurare l'API Google Play Console
# © 2024 Marco Buonopane
##############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🔧 Google Play Console API Setup${NC}"
echo -e "${PURPLE}================================${NC}"
echo ""

# Function to create service account instructions
show_service_account_instructions() {
  echo -e "${BLUE}📋 Setting up Google Play Console API Access:${NC}"
  echo ""
  echo -e "${YELLOW}Step 1: Create Service Account${NC}"
  echo "1. Go to Google Cloud Console (https://console.cloud.google.com/)"
  echo "2. Create a new project or select existing one"
  echo "3. Enable Google Play Developer API"
  echo "4. Go to IAM & Admin > Service Accounts"
  echo "5. Create Service Account with name: autentico-playstore-deploy"
  echo ""
  
  echo -e "${YELLOW}Step 2: Generate JSON Key${NC}"
  echo "1. Click on the created service account"
  echo "2. Go to Keys tab"
  echo "3. Add Key > Create new key > JSON"
  echo "4. Download the JSON file"
  echo "5. Save as: fastlane/google-play-api-key.json"
  echo ""
  
  echo -e "${YELLOW}Step 3: Grant Permissions in Play Console${NC}"
  echo "1. Go to Google Play Console (https://play.google.com/console/)"
  echo "2. Go to Setup > API access"
  echo "3. Link your Google Cloud project"
  echo "4. Grant access to the service account email"
  echo "5. Set permissions: Release apps to production and testing tracks"
  echo ""
}

# Function to validate API key
validate_api_key() {
  local api_key_file="./fastlane/google-play-api-key.json"
  
  echo -e "${BLUE}🔍 Validating Google Play API key...${NC}"
  
  if [ ! -f "$api_key_file" ]; then
    echo -e "${RED}❌ API key file not found: $api_key_file${NC}"
    echo -e "${YELLOW}Please follow the setup instructions above${NC}"
    return 1
  fi
  
  # Validate JSON format
  if ! python3 -m json.tool "$api_key_file" > /dev/null 2>&1; then
    echo -e "${RED}❌ Invalid JSON format in API key file${NC}"
    return 1
  fi
  
  # Check required fields
  local required_fields=("type" "project_id" "private_key_id" "private_key" "client_email")
  for field in "${required_fields[@]}"; do
    if ! grep -q "\"$field\":" "$api_key_file"; then
      echo -e "${RED}❌ Missing required field '$field' in API key file${NC}"
      return 1
    fi
  done
  
  echo -e "${GREEN}✅ API key file format is valid${NC}"
  
  # Get service account email for reference
  local service_email=$(python3 -c "import json; print(json.load(open('$api_key_file'))['client_email'])" 2>/dev/null || echo "Unknown")
  echo -e "${BLUE}📧 Service Account:${NC} $service_email"
  
  return 0
}

# Function to test API connection
test_api_connection() {
  echo -e "${BLUE}🔌 Testing Google Play API connection...${NC}"
  
  # Check if we have the required Ruby gems
  if ! command -v fastlane >/dev/null 2>&1; then
    echo -e "${YELLOW}Installing Fastlane...${NC}"
    sudo gem install fastlane
  fi
  
  # Test API connection with a simple fastlane command
  cd "$(dirname "$0")/.."
  
  if fastlane run validate_play_store_json_key json_key:./fastlane/google-play-api-key.json 2>/dev/null; then
    echo -e "${GREEN}✅ Google Play API connection successful${NC}"
  else
    echo -e "${RED}❌ Failed to connect to Google Play API${NC}"
    echo -e "${YELLOW}Please check:${NC}"
    echo "• API key file is correctly formatted"
    echo "• Service account has correct permissions"
    echo "• Google Play Developer API is enabled"
    echo "• You have access to the Play Console"
    return 1
  fi
}

# Function to setup GitHub secrets
setup_github_secrets() {
  echo -e "${BLUE}🔐 GitHub Secrets Setup${NC}"
  echo ""
  echo -e "${YELLOW}Required GitHub Repository Secrets:${NC}"
  echo ""
  
  echo -e "${GREEN}1. GOOGLE_PLAY_API_KEY${NC}"
  echo "   Base64 encoded content of google-play-api-key.json"
  echo "   Command: base64 -w 0 fastlane/google-play-api-key.json"
  echo ""
  
  echo -e "${GREEN}2. ANDROID_KEYSTORE_BASE64${NC}"
  echo "   Base64 encoded Android keystore file"
  echo "   Command: base64 -w 0 android/keystore/autentico-keystore.jks"
  echo ""
  
  echo -e "${GREEN}3. KEYSTORE_PASSWORD${NC}"
  echo "   Password for the keystore (default: autentico2024)"
  echo ""
  
  echo -e "${GREEN}4. KEY_ALIAS${NC}"
  echo "   Alias for the signing key (default: autentico)"
  echo ""
  
  echo -e "${GREEN}5. KEY_PASSWORD${NC}"
  echo "   Password for the signing key (default: autentico2024)"
  echo ""
  
  echo -e "${GREEN}6. SLACK_WEBHOOK_URL (optional)${NC}"
  echo "   Slack webhook for deployment notifications"
  echo ""
  
  echo -e "${BLUE}How to add secrets:${NC}"
  echo "1. Go to your GitHub repository"
  echo "2. Settings > Secrets and variables > Actions"
  echo "3. Click 'New repository secret'"
  echo "4. Add each secret with its value"
  echo ""
}

# Function to generate secrets helper script
generate_secrets_helper() {
  local helper_script="./scripts/generate-github-secrets.sh"
  
  cat > "$helper_script" << 'EOF'
#!/bin/bash
# Helper script to generate GitHub secrets values

echo "🔐 GitHub Secrets Generator for AUTENTICO v2.2"
echo "=============================================="
echo ""

# Function to encode file to base64
encode_file() {
  local file_path="$1"
  local secret_name="$2"
  
  if [ -f "$file_path" ]; then
    echo "✅ $secret_name:"
    echo "$(base64 -w 0 "$file_path")"
    echo ""
  else
    echo "❌ File not found: $file_path"
    echo ""
  fi
}

# Generate base64 for API key
encode_file "./fastlane/google-play-api-key.json" "GOOGLE_PLAY_API_KEY"

# Generate base64 for keystore
encode_file "./android/keystore/autentico-keystore.jks" "ANDROID_KEYSTORE_BASE64"

echo "📋 Other secrets to set manually:"
echo "KEYSTORE_PASSWORD=autentico2024"
echo "KEY_ALIAS=autentico"  
echo "KEY_PASSWORD=autentico2024"
echo ""
echo "Copy these values to your GitHub repository secrets"
EOF

  chmod +x "$helper_script"
  echo -e "${GREEN}✅ Created helper script: $helper_script${NC}"
}

# Main menu
show_menu() {
  echo -e "${BLUE}What would you like to do?${NC}"
  echo ""
  echo "1. Show API setup instructions"
  echo "2. Validate existing API key"
  echo "3. Test API connection"
  echo "4. Setup GitHub secrets"
  echo "5. Generate secrets helper script"
  echo "6. All of the above"
  echo "0. Exit"
  echo ""
  read -p "Enter your choice [0-6]: " choice
  
  case $choice in
    1)
      show_service_account_instructions
      ;;
    2)
      validate_api_key
      ;;
    3)
      test_api_connection
      ;;
    4)
      setup_github_secrets
      ;;
    5)
      generate_secrets_helper
      ;;
    6)
      show_service_account_instructions
      echo ""
      validate_api_key && echo ""
      test_api_connection && echo ""
      setup_github_secrets
      generate_secrets_helper
      ;;
    0)
      echo -e "${GREEN}👋 Goodbye!${NC}"
      exit 0
      ;;
    *)
      echo -e "${RED}❌ Invalid choice${NC}"
      show_menu
      ;;
  esac
}

# Check if running with arguments
if [ $# -eq 0 ]; then
  show_menu
else
  case $1 in
    "instructions")
      show_service_account_instructions
      ;;
    "validate")
      validate_api_key
      ;;
    "test")
      test_api_connection
      ;;
    "secrets")
      setup_github_secrets
      ;;
    "generate")
      generate_secrets_helper
      ;;
    *)
      echo "Usage: $0 [instructions|validate|test|secrets|generate]"
      ;;
  esac
fi
EOF