#!/bin/bash

# Build script for ARM64 architecture (Apple Silicon) - OCR File Converter

set -e

echo "🏗️  Building OCR File Converter for ARM64..."
echo "📦 Features: English + Vietnamese language support"
echo ""

# Build the Docker image with latest tag
docker build --platform linux/arm64 -t truongginjs/ocr-converter:latest .

echo "✅ Build completed successfully!"
echo ""
echo "🔍 Language support check:"
docker run --rm truongginjs/ocr-converter:latest tesseract --list-langs
echo ""
echo "🚀 Usage examples:"
echo ""
echo "1. Start web service:"
echo "   docker-compose up document-converter"
echo ""
echo "2. Convert files via CLI (English):"
echo "   docker-compose run --rm document-converter-cli /app/input -o /app/output -f json -l eng"
echo ""
echo "3. Convert files via CLI (Vietnamese):"
echo "   docker-compose run --rm document-converter-cli /app/input -o /app/output -f json -l vie"
echo ""
echo "4. Convert with multiple languages:"
echo "   docker run --rm -v \$(pwd)/data:/app/input -v \$(pwd)/output:/app/output \\"
echo "     truongginjs/ocr-converter:latest python converter.py /app/input/1.pdf -o /app/output -l eng,vie"
echo ""
echo "🌐 API Documentation: http://localhost:8000/docs (when web service is running)"
echo ""
echo "📤 To push to Docker Hub:"
echo "   docker push truongginjs/ocr-converter:latest"
