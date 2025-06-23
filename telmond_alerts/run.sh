#!/bin/bash

CORRECT_PASS="codedesign"
CITY_NAME="תל מונד"

if [ "$LICENSE_PASSCODE" != "$CORRECT_PASS" ]; then
  echo "❌ Incorrect passcode. Please contact Elisha Design."
  exit 1
fi

echo "✅ Passcode accepted. Starting Tel Mond alert monitor..."

while true; do
  RESPONSE=$(curl -s -H "Referer: https://www.oref.org.il/12481-he/Pakar.aspx" \
    -H "User-Agent: Mozilla" \
    https://www.oref.org.il/WarningMessages/alert/alerts.json)

  # Check if Tel Mond appears in the alert list
  if echo "$RESPONSE" | grep -q "$CITY_NAME"; then
    echo "🔴 ALERT IN TEL MOND!"
  else
    echo "✅ No alert in Tel Mond."
  fi

  sleep 30
done
