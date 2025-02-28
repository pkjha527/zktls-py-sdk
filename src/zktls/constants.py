"""
Constants for ZK TLS SDK
"""

# Time constants in milliseconds
ONE_SECOND_MS = 1000
ONE_MINUTE_MS = 60 * ONE_SECOND_MS

# Attestation polling time constants
ATTESTATION_POLLING_INTERVAL_MS = 1 * ONE_SECOND_MS
ATTESTATION_POLLING_TIMEOUT_MS = 2 * ONE_MINUTE_MS

# Pado contract addresses
PADO_ADDRESS_MAP = {
    'development': '0xe02bd7a6c8aa401189aebb5bad755c2610940a73',
    'production': '0xDB736B13E2f522dBE18B2015d0291E4b193D8eF6'
}
