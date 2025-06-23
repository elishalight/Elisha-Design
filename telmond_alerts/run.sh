#!/bin/bash

CORRECT_PASS="codedesign"

if [ "$LICENSE_PASSCODE" == "$CORRECT_PASS" ]; then
  echo "✅ Passcode correct. Running Tel Mond alert logic..."
  # Add your logic here
  sleep 999999  # Keeps the container alive
else
  echo "❌ Incorrect passcode. Please contact Elisha Design."
  exit 1
fi
