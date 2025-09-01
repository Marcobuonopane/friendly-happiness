#!/bin/bash
##############################################################################
# AUTENTICO v2.2 - Play Store Continuous Monitor
# Monitoraggio continuo dello stato Google Play Store
# © 2024 Marco Buonopane
##############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Configuration
PACKAGE_NAME="com.marcobuonopane.autentico"
APP_NAME="AUTENTICO v2.2"
CHECK_INTERVAL=300  # 5 minutes
LOG_FILE="./reports/monitor.log"
STATUS_FILE="./reports/current-status.json"

echo -e "${PURPLE}🔄 AUTENTICO v2.2 - Play Store Monitor${NC}"
echo -e "${PURPLE}====================================${NC}"
echo ""

# Function to log with timestamp
log_message() {
    local message="$1"
    local level="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "ERROR")
            echo -e "${RED}[$timestamp] ERROR: $message${NC}" | tee -a "$LOG_FILE"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[$timestamp] SUCCESS: $message${NC}" | tee -a "$LOG_FILE"
            ;;
        "WARNING")
            echo -e "${YELLOW}[$timestamp] WARNING: $message${NC}" | tee -a "$LOG_FILE"
            ;;
        "INFO")
            echo -e "${BLUE}[$timestamp] INFO: $message${NC}" | tee -a "$LOG_FILE"
            ;;
        *)
            echo "[$timestamp] $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Function to check Play Store status
check_play_store_status() {
    log_message "Checking Google Play Store status for $APP_NAME" "INFO"
    
    # Run our Node.js status checker
    if node scripts/check-playstore-status.js > /tmp/playstore-check.log 2>&1; then
        log_message "Status check completed successfully" "SUCCESS"
        
        # Check if app is live
        if grep -q "SUCCESS! AUTENTICO v2.2 is LIVE" /tmp/playstore-check.log; then
            log_message "🎉 App is LIVE on Google Play Store!" "SUCCESS"
            return 0
        elif grep -q "App not found" /tmp/playstore-check.log; then
            log_message "❌ App not found on Play Store" "ERROR"
            return 1
        elif grep -q "Pre-register" /tmp/playstore-check.log; then
            log_message "⏳ App in pre-registration mode" "WARNING"
            return 2
        else
            log_message "⚠️ Unknown app status" "WARNING"
            return 3
        fi
    else
        log_message "❌ Failed to check Play Store status" "ERROR"
        return 4
    fi
}

# Function to send notification (if webhook configured)
send_notification() {
    local message="$1"
    local status="$2"
    
    # Check if we have a webhook URL configured
    if [ ! -z "$WEBHOOK_URL" ]; then
        local payload="{\"text\": \"🤖 AUTENTICO v2.2 Monitor: $message\", \"status\": \"$status\"}"
        
        if curl -s -X POST -H "Content-Type: application/json" -d "$payload" "$WEBHOOK_URL" > /dev/null; then
            log_message "Notification sent successfully" "INFO"
        else
            log_message "Failed to send notification" "WARNING"
        fi
    fi
}

# Function to update status file
update_status_file() {
    local status="$1"
    local message="$2"
    
    local json_data=$(cat << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "app": {
        "name": "$APP_NAME",
        "packageName": "$PACKAGE_NAME"
    },
    "status": "$status",
    "message": "$message",
    "lastCheck": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "monitor": {
        "running": true,
        "checkInterval": $CHECK_INTERVAL,
        "logFile": "$LOG_FILE"
    }
}
EOF
    )
    
    echo "$json_data" > "$STATUS_FILE"
}

# Function to show current status
show_status() {
    echo -e "${BLUE}📊 Current Status:${NC}"
    echo -e "${BLUE}==================${NC}"
    
    if [ -f "$STATUS_FILE" ]; then
        local status=$(cat "$STATUS_FILE" | grep '"status"' | cut -d'"' -f4)
        local message=$(cat "$STATUS_FILE" | grep '"message"' | cut -d'"' -f4)
        local lastCheck=$(cat "$STATUS_FILE" | grep '"lastCheck"' | cut -d'"' -f4)
        
        echo -e "Status: $status"
        echo -e "Message: $message"  
        echo -e "Last Check: $lastCheck"
    else
        echo -e "${YELLOW}No status file found${NC}"
    fi
    echo ""
}

# Function to handle different monitoring modes
run_single_check() {
    log_message "Running single status check" "INFO"
    
    check_play_store_status
    local exit_code=$?
    
    case $exit_code in
        0)
            update_status_file "live" "App is successfully published and available"
            send_notification "App is LIVE on Google Play Store! 🎉" "success"
            ;;
        1)
            update_status_file "not-found" "App not found on Play Store"
            send_notification "App not found on Play Store ❌" "error"
            ;;
        2)
            update_status_file "pre-register" "App in pre-registration mode"
            send_notification "App in pre-registration mode ⏳" "warning"
            ;;
        *)
            update_status_file "unknown" "Unable to determine app status"
            send_notification "Unable to determine app status ⚠️" "warning"
            ;;
    esac
    
    show_status
}

run_continuous_monitor() {
    log_message "Starting continuous monitoring (interval: ${CHECK_INTERVAL}s)" "INFO"
    log_message "Press Ctrl+C to stop monitoring" "INFO"
    
    # Trap SIGINT for graceful shutdown
    trap 'log_message "Monitoring stopped by user" "INFO"; exit 0' SIGINT
    
    local check_count=0
    
    while true; do
        ((check_count++))
        log_message "Check #$check_count" "INFO"
        
        run_single_check
        
        log_message "Waiting ${CHECK_INTERVAL} seconds until next check..." "INFO"
        sleep $CHECK_INTERVAL
    done
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  check     Run single status check"
    echo "  monitor   Start continuous monitoring (default)"
    echo "  status    Show current status"
    echo "  logs      Show recent log entries"
    echo "  help      Show this help message"
    echo ""
    echo "Options:"
    echo "  -i, --interval SECONDS    Set check interval for monitoring (default: 300)"
    echo "  -w, --webhook URL         Set webhook URL for notifications"
    echo ""
    echo "Examples:"
    echo "  $0 check                  # Single check"
    echo "  $0 monitor                # Continuous monitoring"
    echo "  $0 monitor -i 60          # Monitor every minute"
    echo "  $0 status                 # Show current status"
    echo ""
}

# Function to show recent logs
show_logs() {
    echo -e "${BLUE}📋 Recent Log Entries:${NC}"
    echo -e "${BLUE}======================${NC}"
    
    if [ -f "$LOG_FILE" ]; then
        tail -20 "$LOG_FILE"
    else
        echo -e "${YELLOW}No log file found${NC}"
    fi
}

# Parse command line arguments
COMMAND="monitor"
while [[ $# -gt 0 ]]; do
    case $1 in
        check)
            COMMAND="check"
            shift
            ;;
        monitor)
            COMMAND="monitor"
            shift
            ;;
        status)
            COMMAND="status"
            shift
            ;;
        logs)
            COMMAND="logs"
            shift
            ;;
        help|-h|--help)
            show_usage
            exit 0
            ;;
        -i|--interval)
            CHECK_INTERVAL="$2"
            shift 2
            ;;
        -w|--webhook)
            WEBHOOK_URL="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# Create reports directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$STATUS_FILE")"

# Execute the requested command
case $COMMAND in
    "check")
        run_single_check
        ;;
    "monitor")
        run_continuous_monitor
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    *)
        echo -e "${RED}Invalid command: $COMMAND${NC}"
        show_usage
        exit 1
        ;;
esac