"""
QR Code utilities for generating scannable form URLs
"""
import qrcode # pyright: ignore[reportMissingModuleSource]
import io
import base64
from urllib.parse import urlencode
import json


def generate_qr_code(data, size=10, box_size=10):
    """
    Generate QR code and return as base64 encoded image
    
    Args:
        data: String data to encode in QR code (usually a URL)
        size: QR code version (1-40, default=10)
        box_size: Size of each box in pixels (default=10)
    
    Returns:
        Base64 encoded PNG image string
    """
    try:
        qr = qrcode.QRCode(
            version=size,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        return img_base64
    except Exception as e:
        print(f"QR Code generation error: {e}")
        return None


def generate_room_qr_url(url):
    """
    Generate QR code for room addition form URL
    
    Args:
        url: Full URL to the room addition form
    
    Returns:
        Base64 encoded QR code image
    """
    return generate_qr_code(url)


def generate_resident_qr_url(url):
    """
    Generate QR code for resident addition form URL
    
    Args:
        url: Full URL to the resident addition form
    
    Returns:
        Base64 encoded QR code image
    """
    return generate_qr_code(url)


