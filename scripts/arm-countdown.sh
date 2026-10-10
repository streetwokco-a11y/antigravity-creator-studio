#!/usr/bin/env bash
# scripts/arm-countdown.sh - Terminal Countdown Simulation for Episode #6
# Simulates high-stakes root teardown timer with automated or manual disarm trigger.

SECONDS_TOTAL="${1:-60}"
AUTO_DISARM=false
if [[ "$2" == "--auto-disarm" || "$1" == "--auto-disarm" ]]; then
    AUTO_DISARM=true
fi
if [[ "$1" == "--auto-disarm" ]]; then
    SECONDS_TOTAL=60
fi

DISARM_FILE="/tmp/disarm_cron"
rm -f "$DISARM_FILE"

clear 2>/dev/null || true
echo -e "\033[1;31m========================================================================\033[0m"
echo -e "\033[1;31m   CRITICAL ALERT: DESTRUCTIVE ROOT CRON TRIGGER ARMED                 \033[0m"
echo -e "\033[1;31m   COMMAND: rm -rf --no-preserve-root /var/lib/postgresql/data          \033[0m"
echo -e "\033[1;31m========================================================================\033[0m"
echo -e "\033[1;33m[STATUS]\033[0m TARGET: LIVE PRODUCTION CLUSTER (PORT: 5432)"
echo -e "\033[1;33m[SAFETY]\033[0m Disarm signal file: \033[1;36m$DISARM_FILE\033[0m or press \033[1;32m[D]\033[0m to cancel"
echo ""

for ((i=SECONDS_TOTAL; i>=0; i--)); do
    MINS=$((i / 60))
    SECS=$((i % 60))
    TIME_STR=$(printf "%02d:%02d" $MINS $SECS)

    # Check for disarm signal file or auto-disarm condition
    if [ -f "$DISARM_FILE" ] || { [ "$AUTO_DISARM" = true ] && [ $i -le 3 ]; }; then
        echo -e "\n\n\033[1;32m========================================================================\033[0m"
        echo -e "\033[1;32m   ✔✔✔ CRON JOB DISARMED: PRODUCTION SYSTEM SAVED                      \033[0m"
        echo -e "\033[1;32m   REASON: Antigravity Agent resolved PostgreSQL deadlock (00:${TIME_STR})\033[0m"
        echo -e "\033[1;32m   ZERO BYTES CORRUPTED | RE-ROUTED 50,000 CONCURRENT CONNECTIONS       \033[0m"
        echo -e "\033[1;32m========================================================================\033[0m"
        exit 0
    fi

    # Display dynamic color based on time left
    if [ $i -le 10 ]; then
        COLOR="\033[1;5;31m" # Flashing red
    elif [ $i -le 25 ]; then
        COLOR="\033[1;31m"   # Solid red
    else
        COLOR="\033[1;33m"   # Yellow
    fi

    echo -ne "\r${COLOR}[CRON ARMED: rm -rf IN ${TIME_STR}] [CPU: 99.4%] [LOCKS: 4102 DEADLOCKED]\033[0m "
    sleep 1
done

echo -e "\n\n\033[1;31m[TEARDOWN TRIGGERED]\033[0m (Simulated sandbox environment - safe)\n"
