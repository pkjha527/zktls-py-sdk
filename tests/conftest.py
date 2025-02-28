"""
Test configuration and fixtures
"""
import pytest
from eth_account import Account

@pytest.fixture
def app_credentials():
    """Test app credentials"""
    return {
        'appId': 'test_app_id',
        'appSecret': '0x' + '1' * 64  # Test private key
    }

@pytest.fixture
def test_account():
    """Test Ethereum account"""
    return Account.from_key('0x' + '2' * 64)

@pytest.fixture
def test_conditions():
    """Test attestation conditions"""
    return [
        [  # First condition group (AND)
            {  # First condition
                'field': 'balance',
                'op': '>',
                'value': '1000'
            },
            {  # Second condition
                'field': 'age',
                'op': '>=',
                'value': '18'
            }
        ],
        [  # Second condition group (AND)
            {
                'field': 'verified',
                'op': '=',
                'value': 'true'
            }
        ]
    ]

@pytest.fixture
def test_att_mode():
    """Test attestation mode"""
    return {
        'algorithm_type': 'proxytls',
        'result_type': 'plain'
    }
