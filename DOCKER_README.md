# OCR File Converter

A powerful Python-based document converter application that performs Optical Character Recognition (OCR) on PDF documents and images, extracting text content with high accuracy.

## 🚀 Features

- **Multi-format Support**: Process PDF files and various image formats
- **Advanced OCR**: Powered by Tesseract OCR and EasyOCR for superior text extraction
- **Multi-language Support**: Supports English, French, German, and Spanish text recognition
- **REST API**: FastAPI-based web service for easy integration
- **Docker Ready**: Fully containerized for consistent deployment
- **ARM64 Optimized**: Built specifically for ARM64 architecture

## 📋 Dependencies

### System Dependencies
- Tesseract OCR with multiple language packs
- Poppler utilities for PDF processing
- OpenGL and graphics libraries for image processing

### Python Dependencies
- OpenCV for image processing
- PyTesseract for OCR integration
- Pillow for image manipulation
- PyPDF2 and pdf2image for PDF processing
- EasyOCR for advanced text recognition
- FastAPI and Uvicorn for web API

## 🏃‍♂️ Quick Start

### Pull and Run
```bash
# Pull the latest image
docker pull truongginjs/ocr-file:latest

# Run the container
docker run -d \
  --name ocr-converter \
  -p 8000:8000 \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  truongginjs/ocr-file:latest
```

### Using with API
Once running, the FastAPI service will be available at `http://localhost:8000`

### Direct File Processing
```bash
# Process files directly
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  truongginjs/ocr-file:latest
```

## 📁 Volume Mounts

- `/app/input` - Place your PDF files and images here for processing
- `/app/output` - Processed text files will be saved here

## 🔧 Usage Examples

### Example 1: Process a PDF file
```bash
# Place your PDF in the input directory
mkdir -p input output
cp your-document.pdf input/

# Run the container
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  truongginjs/ocr-file:latest

# Check the output directory for extracted text
ls output/
```

### Example 2: Using the API
```bash
# Start the API server
docker run -d -p 8000:8000 --name ocr-api truongginjs/ocr-file:latest

# Upload and process via API
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-document.pdf"
```

## 🌐 Supported Languages

- English (eng)
- French (fra)
- German (deu)
- Spanish (spa)

## 🛠️ Configuration

The application can be configured through environment variables:

- `INPUT_DIR`: Input directory path (default: `/app/input`)
- `OUTPUT_DIR`: Output directory path (default: `/app/output`)
- `API_PORT`: API server port (default: `8000`)

## 📊 Performance

- **Architecture**: Optimized for ARM64 processors
- **Size**: ~1.4GB (includes all OCR dependencies)
- **Memory**: Recommended minimum 2GB RAM
- **Processing**: Supports batch processing of multiple files

## 🔍 Example Output

Input: PDF document with text and images
Output: Clean text file with extracted content, maintaining structure and formatting where possible.

## 📝 Version History

- **v0.1**: Initial release with core OCR functionality
  - Tesseract OCR integration
  - PDF and image support
  - Multi-language recognition
  - FastAPI web service
  - Docker containerization

## 🤝 Contributing

This image is maintained and updated regularly. For issues or feature requests, please contact the maintainer.

## 📄 License

This Docker image contains open-source components. Please refer to individual component licenses for specific terms.

## 🏷️ Tags

- `truongginjs/ocr-file:latest` - Latest stable version
- `truongginjs/ocr-file:0.1` - Version 0.1

## 🔗 Links

- Docker Hub: `https://hub.docker.com/r/truongginjs/ocr-file`
- Architecture: ARM64
- Base Image: python:3.11-slim

---

**Built with ❤️ for efficient document processing**
