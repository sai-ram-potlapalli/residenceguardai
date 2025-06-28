import os
import uuid
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from PIL import Image
import io

def generate_unique_filename(original_filename: str, prefix: str = "") -> str:
    """Generate a unique filename to avoid conflicts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(original_filename)
    return f"{prefix}{timestamp}_{unique_id}{ext}"

def create_upload_folder(folder_path: str) -> None:
    """Create upload folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)

def generate_report_filename(incident_id: str) -> str:
    """Generate a filename for incident reports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"incident_report_{incident_id}_{timestamp}.pdf"

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file type based on extension."""
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_extensions

def validate_image_file(file_path: str) -> bool:
    """Validate that the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            # Try to load the image data (more reliable than verify())
            img.load()
            return True
    except Exception as e:
        print(f"Image validation failed for {file_path}: {e}")
        return False

def validate_pdf_file(file_path: str) -> bool:
    """Validate that the file is a valid PDF."""
    try:
        # First check the header
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                print(f"PDF header check failed for {file_path}: {header}")
                return False
        
        # Then try to open with PyMuPDF for more thorough validation
        import fitz
        doc = fitz.open(file_path)
        page_count = len(doc)
        doc.close()
        
        if page_count == 0:
            print(f"PDF has no pages: {file_path}")
            return False
            
        return True
    except Exception as e:
        print(f"PDF validation failed for {file_path}: {e}")
        return False

def get_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove potentially dangerous characters."""
    # Remove or replace dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    return filename

def create_thumbnail(image_path: str, max_size: tuple = (300, 300)) -> bytes:
    """Create a thumbnail of an image."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (for JPEG output)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)
            return buffer.getvalue()
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return b""

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display."""
    return timestamp.strftime("%B %d, %Y at %I:%M %p")

def extract_metadata_from_image(image_path: str) -> Dict[str, Any]:
    """Extract metadata from an image file."""
    try:
        with Image.open(image_path) as img:
            metadata = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
            }
            
            # Extract EXIF data if available
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                if exif:
                    metadata["exif"] = {
                        "datetime": exif.get(36867),  # DateTime
                        "make": exif.get(271),        # Make
                        "model": exif.get(272),       # Model
                    }
            
            return metadata
    except Exception as e:
        return {"error": str(e)}

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Null characters
    text = text.replace('\x0c', ' ')  # Form feed
    
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for processing."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            for i in range(end, max(start, end - 100), -1):
                if text[i] in '.!?':
                    end = i + 1
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def merge_chunks(chunks: List[str]) -> str:
    """Merge text chunks back together, removing overlaps."""
    if not chunks:
        return ""
    
    if len(chunks) == 1:
        return chunks[0]
    
    merged = chunks[0]
    
    for i in range(1, len(chunks)):
        current_chunk = chunks[i]
        
        # Find overlap between previous chunk and current chunk
        overlap_found = False
        for j in range(min(len(merged), len(current_chunk)), 0, -1):
            if merged[-j:] == current_chunk[:j]:
                merged += current_chunk[j:]
                overlap_found = True
                break
        
        if not overlap_found:
            merged += " " + current_chunk
    
    return merged

def extract_confidence(conf):
    """Safely extract a float confidence value from possibly nested dicts or other types."""
    if isinstance(conf, dict):
        # Try common keys
        for key in ['value', 'score', 'confidence']:
            if key in conf and isinstance(conf[key], (float, int)):
                return conf[key]
        # Fallback: try to get the first float/int value
        for v in conf.values():
            if isinstance(v, (float, int)):
                return v
        return 0.0
    elif isinstance(conf, (float, int)):
        return conf
    else:
        return 0.0 