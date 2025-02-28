"""
Custom exceptions for ZK TLS SDK
"""

class ZkAttestationError(Exception):
    """Base exception for ZK attestation errors"""
    pass

class AttestationRequestError(ZkAttestationError):
    """Error in attestation request"""
    pass

class AttestationTimeoutError(ZkAttestationError):
    """Attestation request timed out"""
    pass

class SigningError(ZkAttestationError):
    """Error in signing request"""
    pass

class EnvironmentError(ZkAttestationError):
    """Error in environment configuration"""
    pass
