#!/bin/bash

# Build script for ARM64 architecture (Apple Silicon)

set -e

echo "Building Document Converter for ARM64..."

# Build the Docker image
docker build --platform linux/arm64 -t document-converter:latest .

echo "Build completed successfully!"
echo ""
echo "Usage examples:"
echo "1. Start web service:"
echo "   docker-compose up document-converter"
echo ""
echo "2. Convert files via CLI:"
echo "   docker-compose run --rm document-converter-cli /app/input -o /app/output -f json"
echo ""
echo "3. Convert your PDF:"
echo "   docker run --rm -v $(pwd)/data:/app/input -v $(pwd)/output:/app/output \\"
echo "     document-converter python converter.py /app/input/1.pdf -o /app/output -f txt"
