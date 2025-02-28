"""
Test type definitions
"""
import pytest
from pydantic import ValidationError

from zktls.types import (
    AttModeAlgorithmType,
    AttModeResultType,
    AttMode,
    AttNetworkRequest,
    AttNetworkResponseResolve,
    Attestor,
    Attestation,
    ErrorData,
    StartAttestationReturn,
    VerifyParamsReturn,
    InitAttestationReturn,
    AttestationParams,
    ComparisonOp,
    OpType,
    AttSubCondition,
    BaseAttestationParams,
    FullAttestationParams,
    SignedAttRequest
)

def test_att_mode():
    """Test AttMode validation"""
    # Test valid modes
    mode = AttMode(
        algorithm_type=AttModeAlgorithmType.PROXY_TLS,
        result_type=AttModeResultType.PLAIN
    )
    assert mode.algorithm_type == AttModeAlgorithmType.PROXY_TLS
    assert mode.result_type == AttModeResultType.PLAIN
    
    # Test invalid algorithm type
    with pytest.raises(ValidationError):
        AttMode(algorithm_type='invalid', result_type='plain')

def test_att_network_request():
    """Test AttNetworkRequest validation"""
    request = AttNetworkRequest(
        url='https://test.com',
        header='{"Content-Type": "application/json"}',
        method='GET',
        body='{}'
    )
    assert request.url == 'https://test.com'
    assert request.method == 'GET'

def test_attestation():
    """Test Attestation validation"""
    attestation = Attestation(
        recipient='0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        request=AttNetworkRequest(
            url='https://test.com',
            header='{}',
            method='GET',
            body='{}'
        ),
        response_resolve=[
            AttNetworkResponseResolve(
                key_name='test',
                parse_type='json',
                parse_path='$.test'
            )
        ],
        data='{}',
        att_conditions='{}',
        timestamp=1234567890,
        addition_params='{}',
        attestors=[
            Attestor(
                attestor_addr='0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
                url='https://test.com'
            )
        ],
        signatures=['0x123']
    )
    assert attestation.recipient == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    assert len(attestation.signatures) == 1

def test_error_data():
    """Test ErrorData validation"""
    error = ErrorData(
        code='TEST_ERROR',
        title='Test Error',
        desc='Test error description'
    )
    assert error.code == 'TEST_ERROR'
    assert error.title == 'Test Error'

def test_start_attestation_return():
    """Test StartAttestationReturn validation"""
    result = StartAttestationReturn(result=True)
    assert result.result is True
    assert result.data is None
    assert result.error_data is None

def test_verify_params_return():
    """Test VerifyParamsReturn validation"""
    result = VerifyParamsReturn(
        result=True,
        message='Success'
    )
    assert result.result is True
    assert result.message == 'Success'

def test_init_attestation_return():
    """Test InitAttestationReturn validation"""
    result = InitAttestationReturn(result=True)
    assert result.result is True
    assert result.error_data is None

def test_attestation_params():
    """Test AttestationParams validation"""
    params = AttestationParams(
        chain_id=1,
        wallet_address='0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        attestation_type_id='test',
        attestation_parameters=[],
        algorithm_type='proxytls'
    )
    assert params.chain_id == 1
    assert params.wallet_address == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'

def test_att_sub_condition():
    """Test AttSubCondition validation"""
    condition = AttSubCondition(
        field='test',
        op=OpType.EQ,
        value='value'
    )
    assert condition.field == 'test'
    assert condition.op == OpType.EQ
    assert condition.value == 'value'

def test_base_attestation_params():
    """Test BaseAttestationParams validation"""
    params = BaseAttestationParams(
        appId='test_app',
        attTemplateID='test_template',
        userAddress='0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    )
    assert params.app_id == 'test_app'
    assert params.att_template_id == 'test_template'
    assert params.user_address == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'

def test_full_attestation_params():
    """Test FullAttestationParams validation"""
    params = FullAttestationParams(
        appId='test_app',
        attTemplateID='test_template',
        userAddress='0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        timestamp=1234567890,
        attMode=AttMode(
            algorithm_type=AttModeAlgorithmType.PROXY_TLS,
            result_type=AttModeResultType.PLAIN
        )
    )
    assert params.app_id == 'test_app'
    assert params.timestamp == 1234567890
    assert params.att_mode.algorithm_type == AttModeAlgorithmType.PROXY_TLS

def test_signed_att_request():
    """Test SignedAttRequest validation"""
    request = SignedAttRequest(
        attRequest=FullAttestationParams(
            appId='test_app',
            attTemplateID='test_template',
            userAddress='0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
            timestamp=1234567890,
            attMode=AttMode(
                algorithm_type=AttModeAlgorithmType.PROXY_TLS,
                result_type=AttModeResultType.PLAIN
            )
        ),
        appSignature='0x123'
    )
    assert request.att_request.app_id == 'test_app'
    assert request.app_signature == '0x123'
