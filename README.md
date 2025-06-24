# OCR File Converter 📄🔍

A powerful Python-based document converter application that performs Optical Character Recognition (OCR) on PDF documents and images, extracting text content with high accuracy.

## Features

- **Multiple Input Formats**: PDF, JPG, PNG, BMP, TIFF, WEBP
- **Multiple Output Formats**: Plain text (TXT) or structured JSON
- **OCR Engines**: Tesseract and EasyOCR support
- **ARM64 Optimized**: Built specifically for Apple Silicon chips
- **Batch Processing**: Convert multiple files at once
- **REST API**: Web service for programmatic access
- **CLI Interface**: Command-line tool for batch operations
- **Image Preprocessing**: Automatic image enhancement for better OCR accuracy

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t document-converter .
```

### 2. Using Docker Compose (Recommended)

**Start the web service:**
```bash
docker-compose up document-converter
```

**Use CLI for batch processing:**
```bash
docker-compose run --rm document-converter-cli /app/input -o /app/output -f json
```

### 3. Direct Docker Usage

**Convert files via CLI:**
```bash
# Convert single file
docker run --rm -v $(pwd)/data:/app/input -v $(pwd)/output:/app/output \
  document-converter python converter.py /app/input/1.pdf -o /app/output -f txt

# Convert entire directory
docker run --rm -v $(pwd)/data:/app/input -v $(pwd)/output:/app/output \
  document-converter python converter.py /app/input -o /app/output -f json
```

**Run web service:**
```bash
docker run --rm -p 8000:8000 -v $(pwd)/data:/app/input -v $(pwd)/output:/app/output \
  document-converter python api.py
```

## Usage Examples

### CLI Usage

```bash
# Basic conversion
python converter.py input.pdf

# Specify output format and directory
python converter.py input.pdf -o ./output -f json

# Use EasyOCR engine
python converter.py image.jpg -e easyocr -f txt

# Batch convert directory
python converter.py ./images/ -o ./output -f json

# Exclude metadata
python converter.py input.pdf --no-metadata
```

### API Usage

Once the web service is running (http://localhost:8000), you can:

1. **Visit the API documentation**: http://localhost:8000/docs
2. **Upload files via curl**:

```bash
# Convert single file
curl -X POST "http://localhost:8000/convert" \
  -F "files=@data/1.pdf" \
  -F "output_format=json" \
  -F "ocr_engine=tesseract"

# Convert multiple files
curl -X POST "http://localhost:8000/convert" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "output_format=txt"
```

## Configuration Options

### CLI Arguments

- `input`: Input file or directory path
- `-o, --output`: Output directory (default: ./output)
- `-f, --format`: Output format - txt or json (default: txt)
- `-e, --engine`: OCR engine - tesseract or easyocr (default: tesseract)
- `--no-metadata`: Exclude metadata from output

### API Parameters

- `files`: List of files to upload
- `output_format`: txt or json (default: txt)
- `ocr_engine`: tesseract or easyocr (default: tesseract)
- `include_metadata`: Include extraction metadata (default: true)

## Output Formats

### Text Format (.txt)
Plain text extraction of the document content.

### JSON Format (.json)
Structured output including:
```json
{
  "filename": "document.pdf",
  "file_type": ".pdf",
  "success": true,
  "text": "Extracted text content...",
  "metadata": {
    "extraction_method": "direct",
    "character_count": 1234,
    "word_count": 200,
    "confidence": 95.5
  }
}
```

## Supported File Types

- **PDF**: .pdf
- **Images**: .jpg, .jpeg, .png, .bmp, .tiff, .webp

## OCR Engines

### Tesseract
- Fast and reliable
- Good for clean, high-quality documents
- Provides confidence scores
- Multiple language support

### EasyOCR
- Better for complex layouts
- Handles skewed text well
- Good for handwritten text
- Slower but more accurate for difficult images

## Architecture Notes

- **ARM64 Optimized**: Built specifically for Apple Silicon
- **Multi-stage Processing**: Tries direct PDF text extraction before OCR
- **Image Preprocessing**: Automatic denoising and thresholding
- **Memory Efficient**: Processes files one at a time to minimize memory usage

## Development

### Local Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install system dependencies (macOS):
```bash
brew install tesseract poppler
```

3. Run locally:
```bash
python converter.py data/1.pdf
python api.py  # For web service
```

### Building for Different Platforms

```bash
# Build for ARM64 (Apple Silicon)
docker buildx build --platform linux/arm64 -t document-converter:arm64 .

# Build for AMD64
docker buildx build --platform linux/amd64 -t document-converter:amd64 .
```

## Troubleshooting

### Common Issues

1. **Low OCR accuracy**: Try preprocessing the image or using a different OCR engine
2. **Memory issues**: Process files individually rather than in large batches
3. **Slow performance**: Use Tesseract for faster processing, EasyOCR for better accuracy

### Performance Tips

- Use direct PDF text extraction when possible (faster than OCR)
- Preprocess images for better OCR results
- Consider using smaller image resolutions for faster processing
- Use batch processing for multiple files

## License

MIT License - Feel free to use and modify as needed.
