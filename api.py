#!/usr/bin/env python3
"""
FastAPI Web Service for PDF and Image to Text/JSON Conversion
Provides REST API endpoints for document conversion
"""

import os
import json
import tempfile
from pathlib import Path
from typing import List, Optional
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from converter import DocumentConverter

app = FastAPI(
    title="Document Converter API",
    description="Convert PDF and image files to text or JSON format",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Document Converter API", 
        "version": "1.0.0",
        "endpoints": {
            "convert": "/convert - Upload and convert files",
            "health": "/health - Service health check",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "document-converter"}

@app.post("/convert")
async def convert_document(
    files: List[UploadFile] = File(...),
    output_format: str = Form(default="txt", regex="^(txt|json)$"),
    ocr_engine: str = Form(default="tesseract", regex="^(tesseract|easyocr)$"),
    include_metadata: bool = Form(default=True)
):
    """
    Convert uploaded PDF or image files to text or JSON format.
    
    Parameters:
    - files: List of files to convert (PDF, JPG, PNG, etc.)
    - output_format: Output format (txt or json)
    - ocr_engine: OCR engine to use (tesseract or easyocr)
    - include_metadata: Include extraction metadata in results
    """
    
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # Initialize converter
    converter = DocumentConverter(ocr_engine=ocr_engine)
    results = []
    
    for file in files:
        # Check file type
        allowed_types = {
            'application/pdf',
            'image/jpeg', 'image/jpg', 'image/png', 
            'image/bmp', 'image/tiff', 'image/webp'
        }
        
        if file.content_type not in allowed_types:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": f"Unsupported file type: {file.content_type}",
                "text": ""
            })
            continue
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Convert file
            result = converter.convert_file(
                tmp_file_path, 
                output_format, 
                include_metadata=include_metadata
            )
            results.append(result)
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e),
                "text": ""
            })
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
    
    return JSONResponse(content={
        "results": results,
        "total_files": len(files),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"])
    })

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
