"""
Utility functions for ZK TLS SDK
"""
import os
import time
import hashlib
from typing import Union, Dict, Any
from pathlib import Path
import json

def generate_challenge(size: int = 32) -> bytes:
    """
    Generate a random challenge for ZK proof
    
    Args:
        size: Size of challenge in bytes
        
    Returns:
        Random bytes for challenge
    """
    return os.urandom(size)

def hash_message(message: Union[str, bytes], encoding: str = 'utf-8') -> bytes:
    """
    Create SHA-256 hash of message
    
    Args:
        message: Message to hash
        encoding: Encoding to use if message is string
        
    Returns:
        Message hash as bytes
    """
    if isinstance(message, str):
        message = message.encode(encoding)
    return hashlib.sha256(message).digest()

def validate_file_path(path: Union[str, Path], create_dirs: bool = False) -> Path:
    """
    Validate and normalize file path
    
    Args:
        path: File path as string or Path
        create_dirs: Whether to create parent directories
        
    Returns:
        Normalized Path object
    """
    path = Path(path).resolve()
    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)
    return path

def get_timestamp() -> int:
    """Get current Unix timestamp"""
    return int(time.time())

def format_hex(data: bytes) -> str:
    """Format bytes as lowercase hex string"""
    return data.hex().lower()

def parse_hex(hex_str: str) -> bytes:
    """Parse hex string to bytes"""
    return bytes.fromhex(hex_str)

def get_instance_properties(instance: Any) -> Dict[str, Any]:
    """
    Get instance properties as dictionary
    
    Args:
        instance: Class instance
        
    Returns:
        Dictionary of instance properties
    """
    return {
        key: value for key, value in instance.__dict__.items()
        if not key.startswith('_') and value is not None
    }

def encode_attestation(attestation: Dict[str, Any]) -> str:
    """
    Encode attestation data to string
    
    Args:
        attestation: Attestation data
        
    Returns:
        Encoded attestation string
    """
    return json.dumps(attestation, sort_keys=True)
