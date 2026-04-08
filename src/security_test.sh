#!/bin/bash

RESULTS_DIR="/tmp/security_tests"
mkdir -p "$RESULTS_DIR"

echo "=== Security Assessment Started at $(date) ===" | tee "$RESULTS_DIR/test_report.txt"

# Test 1: MITM Attack
echo -e "\n[TEST 1] MITM Attack Test" | tee -a "$RESULTS_DIR/test_report.txt"
timeout 30s python3 ~/iot-attacks/mqtt_attack.py <<< "1" > "$RESULTS_DIR/mitm_test.log" 2>&1 &
MITM_PID=$!
sleep 35
if ps -p $MITM_PID > /dev/null; then
    echo "MITM Attack: SUCCESS (Not blocked)" | tee -a "$RESULTS_DIR/test_report.txt"
    kill $MITM_PID
else
    echo "MITM Attack: FAILED (Blocked or prevented)" | tee -a "$RESULTS_DIR/test_report.txt"
fi

# Test 2: Anonymous Connection
echo -e "\n[TEST 2] Anonymous Connection Test" | tee -a "$RESULTS_DIR/test_report.txt"
mosquitto_pub -h 192.168.56.10 -p 1883 -t "test/anonymous" -m "test" > "$RESULTS_DIR/anon_test.log" 2>&1
if [ $? -eq 0 ]; then
    echo "Anonymous Connection: SUCCESS (Vulnerable)" | tee -a "$RESULTS_DIR/test_report.txt"
else
    echo "Anonymous Connection: FAILED (Secured)" | tee -a "$RESULTS_DIR/test_report.txt"
fi

# Test 3: TLS Encryption
echo -e "\n[TEST 3] TLS Encryption Test" | tee -a "$RESULTS_DIR/test_report.txt"
timeout 10s sudo tcpdump -i eth1 -c 100 port 1883 or port 8883 -w "$RESULTS_DIR/tls_test.pcap" 2>&1 &
sleep 2
mosquitto_pub -h 192.168.56.10 -p 8883 --cafile /etc/mosquitto/certs/ca.crt \
    -u iot_user -P password -t "test/tls" -m "test" 2>&1
sleep 5
PLAINTEXT=$(tshark -r "$RESULTS_DIR/tls_test.pcap" -Y "mqtt" 2>/dev/null | wc -l)
if [ "$PLAINTEXT" -eq 0 ]; then
    echo "TLS Encryption: ENABLED (Secure)" | tee -a "$RESULTS_DIR/test_report.txt"
else
    echo "TLS Encryption: DISABLED (Vulnerable)" | tee -a "$RESULTS_DIR/test_report.txt"
fi

# Test 4: DoS Resistance
echo -e "\n[TEST 4] DoS Resistance Test" | tee -a "$RESULTS_DIR/test_report.txt"
BEFORE_CPU=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
timeout 30s sudo hping3 -S --flood -V -p 1883 192.168.56.10 > /dev/null 2>&1 &
sleep 35
AFTER_CPU=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
CPU_IMPACT=$(echo "$AFTER_CPU - $BEFORE_CPU" | bc)
echo "DoS Impact: CPU increased by ${CPU_IMPACT}%" | tee -a "$RESULTS_DIR/test_report.txt"

echo -e "\n=== Security Assessment Completed at $(date) ===" | tee -a "$RESULTS_DIR/test_report.txt"