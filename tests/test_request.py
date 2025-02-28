"""
Test attestation request
"""
import pytest
import json

from zktls.request import AttRequest
from zktls.types import (
    BaseAttestationParams,
    AttModeAlgorithmType,
    AttModeResultType,
    FullAttestationParams,
    AttSubCondition,
    OpType
)

@pytest.fixture
def app_credentials():
    """Create app credentials"""
    return {
        'appId': 'test_app',
        'appKey': 'test_key'
    }

@pytest.fixture
def test_conditions():
    """Create test conditions"""
    return [
        [
            {
                'field': 'test',
                'op': OpType.EQ,
                'value': 'value'
            }
        ]
    ]

def test_request_initialization(app_credentials):
    """Test request initialization"""
    request = AttRequest({
        'appId': app_credentials['appId'],
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    assert isinstance(request.base_params, BaseAttestationParams)
    assert request.base_params.app_id == app_credentials['appId']
    assert request.base_params.att_template_id == 'test_template'
    assert request.base_params.user_address == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'

def test_set_addition_params():
    """Test setting additional parameters"""
    request = AttRequest({
        'appId': 'test_app',
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    params = {'test': 'value'}
    request.set_addition_params(params)
    assert json.loads(request.addition_params) == params

def test_set_att_mode():
    """Test setting attestation mode"""
    request = AttRequest({
        'appId': 'test_app',
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    mode = {
        'algorithm_type': AttModeAlgorithmType.MPC_TLS,
        'result_type': AttModeResultType.CIPHER
    }
    request.set_att_mode(mode)
    
    assert request.att_mode.algorithm_type == AttModeAlgorithmType.MPC_TLS
    assert request.att_mode.result_type == AttModeResultType.CIPHER

def test_set_att_conditions(test_conditions):
    """Test setting attestation conditions"""
    request = AttRequest({
        'appId': 'test_app',
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    request.set_att_conditions(test_conditions)
    
    assert isinstance(request.att_conditions, list)
    for condition_group in request.att_conditions:
        assert isinstance(condition_group, list)
        for condition in condition_group:
            assert isinstance(condition, AttSubCondition)
            assert condition.op == OpType.EQ  

def test_to_full_params():
    """Test conversion to full parameters"""
    request = AttRequest({
        'appId': 'test_app',
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    params = request.to_full_params()
    
    assert isinstance(params, FullAttestationParams)
    assert params.app_id == 'test_app'
    assert params.att_template_id == 'test_template'
    assert params.user_address == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    assert isinstance(params.timestamp, int)
    assert params.att_mode.algorithm_type == AttModeAlgorithmType.PROXY_TLS  
    assert params.att_mode.result_type == AttModeResultType.PLAIN  

def test_to_json_string():
    """Test JSON string conversion"""
    request = AttRequest({
        'appId': 'test_app',
        'attTemplateID': 'test_template',
        'userAddress': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    })
    
    json_str = request.to_json_string()
    data = json.loads(json_str)
    
    assert data['appId'] == 'test_app'
    assert data['attTemplateID'] == 'test_template'
    assert data['userAddress'] == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'
    assert isinstance(data['timestamp'], int)
    assert data['attMode']['algorithm_type'] == AttModeAlgorithmType.PROXY_TLS  
    assert data['attMode']['result_type'] == AttModeResultType.PLAIN  
