#!/bin/bash

echo "🔐 Checking license code..."

RESPONSE=$(curl -s -X POST https://auth.elishadesign.com/validate -d "code=${LICENSE_CODE}")

if echo "$RESPONSE" | grep -q "VALID"; then
    echo "✅ License valid. Starting Tel Mond alert integration..."
    # Your real logic goes here
else
    echo "❌ Invalid license. Exiting."
    exit 1
fi
