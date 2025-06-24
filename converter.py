#!/usr/bin/env python3
"""
PDF and Image to Text/JSON Converter
Supports multiple OCR engines and output formats
"""

import os
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
from pdf2image import convert_from_path
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentConverter:
    def __init__(self, ocr_engine: str = "tesseract"):
        """Initialize the converter with specified OCR engine."""
        self.ocr_engine = ocr_engine
        if ocr_engine == "easyocr":
            self.reader = easyocr.Reader(['en', 'fr', 'de', 'es'])
        
    def extract_text_from_pdf_direct(self, pdf_path: str) -> str:
        """Extract text directly from PDF if it contains selectable text."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.warning(f"Direct PDF text extraction failed: {e}")
            return ""
    
    def extract_text_from_pdf_ocr(self, pdf_path: str) -> str:
        """Extract text from PDF using OCR on converted images."""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            text = ""
            
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}/{len(images)}")
                page_text = self.extract_text_from_image(image)
                text += f"\n--- Page {i+1} ---\n{page_text}\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"PDF OCR extraction failed: {e}")
            return ""
    
    def extract_text_from_image(self, image: Union[str, Image.Image]) -> str:
        """Extract text from image using specified OCR engine."""
        try:
            if isinstance(image, str):
                image = Image.open(image)
            
            # Preprocess image for better OCR
            image = self.preprocess_image(image)
            
            if self.ocr_engine == "tesseract":
                return pytesseract.image_to_string(image, config='--psm 6')
            elif self.ocr_engine == "easyocr":
                # Convert PIL to numpy array for EasyOCR
                img_array = np.array(image)
                results = self.reader.readtext(img_array)
                return "\n".join([result[1] for result in results])
            
        except Exception as e:
            logger.error(f"Image text extraction failed: {e}")
            return ""
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image to improve OCR accuracy."""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Convert back to PIL Image
        return Image.fromarray(thresh)
    
    def extract_text_with_confidence(self, image: Union[str, Image.Image]) -> Dict:
        """Extract text with confidence scores (Tesseract only)."""
        if self.ocr_engine != "tesseract":
            logger.warning("Confidence scores only available with Tesseract")
            return {"text": self.extract_text_from_image(image), "confidence": None}
        
        try:
            if isinstance(image, str):
                image = Image.open(image)
            
            image = self.preprocess_image(image)
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Filter out low confidence detections
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            words = [data['text'][i] for i, conf in enumerate(data['conf']) if int(conf) > 30]
            
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": " ".join(words),
                "confidence": avg_confidence,
                "word_count": len(words),
                "total_detections": len([c for c in data['conf'] if int(c) > 0])
            }
            
        except Exception as e:
            logger.error(f"Text extraction with confidence failed: {e}")
            return {"text": "", "confidence": 0}
    
    def convert_file(self, input_path: str, output_format: str = "txt", 
                    include_metadata: bool = True) -> Dict:
        """Convert a single file to specified format."""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        result = {
            "filename": input_path.name,
            "file_type": input_path.suffix.lower(),
            "success": False,
            "text": "",
            "metadata": {}
        }
        
        try:
            # Handle PDF files
            if input_path.suffix.lower() == '.pdf':
                # Try direct text extraction first
                direct_text = self.extract_text_from_pdf_direct(str(input_path))
                if direct_text and len(direct_text.strip()) > 50:
                    result["text"] = direct_text
                    result["metadata"]["extraction_method"] = "direct"
                else:
                    # Fall back to OCR
                    result["text"] = self.extract_text_from_pdf_ocr(str(input_path))
                    result["metadata"]["extraction_method"] = "ocr"
            
            # Handle image files
            elif input_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
                if include_metadata and self.ocr_engine == "tesseract":
                    ocr_result = self.extract_text_with_confidence(str(input_path))
                    result["text"] = ocr_result["text"]
                    result["metadata"].update(ocr_result)
                else:
                    result["text"] = self.extract_text_from_image(str(input_path))
                
                result["metadata"]["extraction_method"] = self.ocr_engine
            
            else:
                raise ValueError(f"Unsupported file type: {input_path.suffix}")
            
            result["success"] = True
            result["metadata"]["character_count"] = len(result["text"])
            result["metadata"]["word_count"] = len(result["text"].split())
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Failed to convert {input_path}: {e}")
        
        return result
    
    def convert_directory(self, input_dir: str, output_dir: str, 
                         output_format: str = "txt") -> List[Dict]:
        """Convert all supported files in a directory."""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        supported_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        files = [f for f in input_dir.iterdir() 
                if f.is_file() and f.suffix.lower() in supported_extensions]
        
        results = []
        
        for file_path in files:
            logger.info(f"Converting: {file_path.name}")
            
            result = self.convert_file(str(file_path), output_format)
            results.append(result)
            
            if result["success"]:
                # Save output file
                output_file = output_dir / f"{file_path.stem}.{output_format}"
                
                if output_format == "txt":
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result["text"])
                elif output_format == "json":
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Saved: {output_file}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Convert PDF and images to text or JSON')
    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output directory (default: ./output)')
    parser.add_argument('-f', '--format', choices=['txt', 'json'], default='txt',
                       help='Output format (default: txt)')
    parser.add_argument('-e', '--engine', choices=['tesseract', 'easyocr'], 
                       default='tesseract', help='OCR engine (default: tesseract)')
    parser.add_argument('--no-metadata', action='store_true', 
                       help='Exclude metadata from output')
    
    args = parser.parse_args()
    
    # Set default output directory
    if not args.output:
        args.output = './output'
    
    # Initialize converter
    converter = DocumentConverter(ocr_engine=args.engine)
    
    input_path = Path(args.input)
    
    try:
        if input_path.is_file():
            # Convert single file
            result = converter.convert_file(
                str(input_path), 
                args.format, 
                include_metadata=not args.no_metadata
            )
            
            # Save result
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = output_dir / f"{input_path.stem}.{args.format}"
            
            if args.format == "txt":
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result["text"])
            elif args.format == "json":
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Conversion completed. Output saved to: {output_file}")
            
        elif input_path.is_dir():
            # Convert directory
            results = converter.convert_directory(str(input_path), args.output, args.format)
            
            # Save summary
            summary_file = Path(args.output) / "conversion_summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_files": len(results),
                    "successful": sum(1 for r in results if r["success"]),
                    "failed": sum(1 for r in results if not r["success"]),
                    "results": results
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Batch conversion completed. Summary saved to: {summary_file}")
        
        else:
            raise FileNotFoundError(f"Input path not found: {input_path}")
    
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
