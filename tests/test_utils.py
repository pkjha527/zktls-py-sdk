"""
Tests for utility functions
"""
import pytest
from pathlib import Path
from zktls.utils import (
    generate_challenge,
    hash_message,
    validate_file_path,
    get_timestamp,
    format_hex,
    parse_hex
)

def test_generate_challenge():
    """Test challenge generation"""
    size = 32
    challenge = generate_challenge(size)
    assert isinstance(challenge, bytes)
    assert len(challenge) == size
    
    # Should generate different challenges
    assert generate_challenge() != generate_challenge()

def test_hash_message():
    """Test message hashing"""
    message = "test message"
    hash1 = hash_message(message)
    hash2 = hash_message(message.encode())
    
    assert isinstance(hash1, bytes)
    assert len(hash1) == 32  # SHA-256 hash length
    assert hash1 == hash2

def test_validate_file_path(tmp_path):
    """Test file path validation"""
    test_file = tmp_path / "test.txt"
    
    # Test with string path
    path = validate_file_path(str(test_file))
    assert isinstance(path, Path)
    assert path == test_file.resolve()
    
    # Test with Path object
    path = validate_file_path(test_file)
    assert isinstance(path, Path)
    assert path == test_file.resolve()
    
    # Test directory creation
    nested_file = tmp_path / "a" / "b" / "c" / "test.txt"
    path = validate_file_path(nested_file, create_dirs=True)
    assert nested_file.parent.exists()

def test_get_timestamp():
    """Test timestamp generation"""
    ts = get_timestamp()
    assert isinstance(ts, int)
    assert ts > 0

def test_hex_formatting():
    """Test hex string formatting and parsing"""
    data = b"test data"
    hex_str = format_hex(data)
    
    assert isinstance(hex_str, str)
    assert all(c in '0123456789abcdef' for c in hex_str)
    
    # Test roundtrip
    assert parse_hex(hex_str) == data

def test_invalid_hex():
    """Test parsing invalid hex string"""
    with pytest.raises(ValueError):
        parse_hex("invalid hex")
