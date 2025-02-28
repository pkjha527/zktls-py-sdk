"""
Test PrimusZKTLS client
"""
import pytest
from eth_account import Account
import json
from eth_utils import to_hex

from zktls import PrimusZKTLS
from zktls.types import (
    AttModeAlgorithmType,
    AttModeResultType,
    AttMode,
    ErrorData,
    InitAttestationReturn,
    StartAttestationReturn,
    OpType
)
from zktls.exceptions import ZkAttestationError

@pytest.fixture
def client():
    """Create test client"""
    return PrimusZKTLS()

@pytest.fixture
def app_credentials():
    """Test app credentials"""
    # Create a valid hex string for app_secret
    account = Account.create()
    return {
        "appId": "test_app_id",
        "appSecret": account.key.hex()  # This will be a valid hex string
    }

@pytest.fixture
def test_conditions():
    """Test conditions"""
    return [
        [
            {
                'field': 'test',
                'op': OpType.EQ,
                'value': 'value'
            }
        ]
    ]

@pytest.mark.asyncio
async def test_client_initialization(app_credentials):
    """Test client initialization"""
    client = PrimusZKTLS()
    
    # Test initialization without app secret
    init_result = client.init(app_credentials['appId'])
    assert isinstance(init_result, InitAttestationReturn)
    assert init_result.result is False
    assert isinstance(init_result.error_data, ErrorData)
    assert init_result.error_data.code == "INIT_ERROR"
    
    # Test proper initialization
    init_result = client.init(app_credentials['appId'], app_credentials['appSecret'])
    assert isinstance(init_result, InitAttestationReturn)
    assert init_result.result is True
    assert init_result.error_data is None
    assert client.is_initialized is True

@pytest.mark.asyncio
async def test_request_attestation_without_init():
    """Test attestation request without initialization"""
    client = PrimusZKTLS()
    account = Account.create()
    
    with pytest.raises(ZkAttestationError) as exc_info:
        await client.request_attestation(
            att_template_id="test_template",
            user_address=account.address
        )
    
    assert str(exc_info.value) == "Client not initialized"

@pytest.mark.asyncio
async def test_request_attestation(app_credentials):
    """Test attestation request"""
    client = PrimusZKTLS()
    client.init(app_credentials['appId'], app_credentials['appSecret'])
    
    # Generate a valid Ethereum address
    account = Account.create()
    user_address = account.address
    
    # Test basic attestation request
    result = await client.request_attestation(
        att_template_id="test_template",
        user_address=user_address
    )
    
    assert isinstance(result, StartAttestationReturn)
    assert result.result is True
    assert result.data is not None
    assert result.error_data is None

@pytest.mark.asyncio
async def test_request_attestation_with_conditions(app_credentials, test_conditions):
    """Test attestation request with conditions"""
    client = PrimusZKTLS()
    client.init(app_credentials['appId'], app_credentials['appSecret'])
    
    # Generate a valid Ethereum address
    account = Account.create()
    user_address = account.address
    
    result = await client.request_attestation(
        att_template_id="test_template",
        user_address=user_address,
        att_conditions=test_conditions
    )
    
    assert isinstance(result, StartAttestationReturn)
    assert result.result is True
    assert result.data is not None
    assert result.error_data is None

@pytest.mark.asyncio
async def test_request_attestation_with_additional_params(app_credentials):
    """Test attestation request with additional parameters"""
    client = PrimusZKTLS()
    client.init(app_credentials['appId'], app_credentials['appSecret'])
    
    # Generate a valid Ethereum address
    account = Account.create()
    user_address = account.address
    
    # Create additional params as a dict
    additional_params = {"custom": "value"}
    
    result = await client.request_attestation(
        att_template_id="test_template",
        user_address=user_address,
        addition_params=additional_params
    )
    
    assert isinstance(result, StartAttestationReturn)
    assert result.result is True
    assert result.data is not None
    assert result.error_data is None

def test_set_env():
    """Test environment setting"""
    client = PrimusZKTLS()
    
    # Test valid environment
    client.set_env('development')
    assert client._env == 'development'
    
    # Test invalid environment
    with pytest.raises(ZkAttestationError):
        client.set_env('invalid')
