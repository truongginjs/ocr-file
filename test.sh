#!/bin/bash

# Test script for the Document Converter

set -e

echo "🚀 Testing Document Converter..."
echo ""

# Ensure output directory exists
mkdir -p output

echo "📦 Building Docker image..."
docker build -t document-converter .

echo ""
echo "🔄 Testing PDF conversion..."

# Test 1: Convert PDF to text
echo "Test 1: Converting PDF to text format..."
docker run --rm \
  -v $(pwd)/data:/app/input \
  -v $(pwd)/output:/app/output \
  document-converter \
  python converter.py /app/input/1.pdf -o /app/output -f txt

# Test 2: Convert PDF to JSON with metadata
echo ""
echo "Test 2: Converting PDF to JSON with metadata..."
docker run --rm \
  -v $(pwd)/data:/app/input \
  -v $(pwd)/output:/app/output \
  document-converter \
  python converter.py /app/input/1.pdf -o /app/output -f json

echo ""
echo "✅ Conversion tests completed!"
echo ""
echo "📁 Check the output directory for results:"
ls -la output/

echo ""
echo "🌐 To start the web service, run:"
echo "   docker-compose up document-converter"
echo ""
echo "📚 Then visit: http://localhost:8000/docs for API documentation"
