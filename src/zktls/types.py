"""
Type definitions for ZK TLS SDK
"""
from typing import List, Optional, Any, Dict, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class AttModeAlgorithmType(str, Enum):
    """Attestation mode algorithm types"""
    MPC_TLS = 'mpctls'
    PROXY_TLS = 'proxytls'

class AttModeResultType(str, Enum):
    """Attestation mode result types"""
    PLAIN = 'plain'
    CIPHER = 'cipher'

class AttMode(BaseModel):
    """Attestation mode configuration"""
    algorithm_type: AttModeAlgorithmType
    result_type: AttModeResultType = AttModeResultType.PLAIN
    
    model_config = ConfigDict(populate_by_name=True)

class AttNetworkRequest(BaseModel):
    """Network request details"""
    url: str
    header: str  # json string
    method: str
    body: str
    
    model_config = ConfigDict(populate_by_name=True)

class AttNetworkResponseResolve(BaseModel):
    """Network response resolver"""
    key_name: str
    parse_type: str  # json or html
    parse_path: str
    
    model_config = ConfigDict(populate_by_name=True)

class Attestor(BaseModel):
    """Attestor information"""
    attestor_addr: str
    url: str
    
    model_config = ConfigDict(populate_by_name=True)

class Attestation(BaseModel):
    """Attestation data"""
    recipient: str
    request: AttNetworkRequest
    response_resolve: List[AttNetworkResponseResolve]
    data: str  # json string
    att_conditions: str  # json string
    timestamp: int
    addition_params: str  # json string
    attestors: List[Attestor]
    signatures: List[str]
    
    model_config = ConfigDict(populate_by_name=True)

class ErrorData(BaseModel):
    """Error information"""
    code: str
    title: str
    desc: str
    
    model_config = ConfigDict(populate_by_name=True)

class StartAttestationReturn(BaseModel):
    """Start attestation response"""
    result: bool
    data: Optional[Attestation] = None
    error_data: Optional[ErrorData] = None
    restart_flag: Optional[bool] = None
    
    model_config = ConfigDict(populate_by_name=True)

class VerifyParamsReturn(BaseModel):
    """Verify parameters response"""
    result: bool
    message: str
    
    model_config = ConfigDict(populate_by_name=True)

class InitAttestationReturn(BaseModel):
    """Init attestation response"""
    result: bool
    error_data: Optional[ErrorData] = None
    
    model_config = ConfigDict(populate_by_name=True)

class AttestationParams(BaseModel):
    """Attestation parameters"""
    chain_id: int
    wallet_address: str
    attestation_type_id: str
    attestation_parameters: List[Any]
    algorithm_type: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)

Env = Literal['development', 'test', 'production']

class ComparisonOp(str, Enum):
    """Comparison operators"""
    GT = '>'
    GTE = '>='
    EQ = '='
    NEQ = '!='
    LT = '<'
    LTE = '<='

class OpType(str, Enum):
    """Operation types"""
    GT = '>'
    GTE = '>='
    EQ = '='
    NEQ = '!='
    LT = '<'
    LTE = '<='
    SHA256 = 'SHA256'
    REVEAL_STRING = 'REVEAL_STRING'

class AttSubCondition(BaseModel):
    """Attestation sub-condition"""
    field: str
    op: OpType
    value: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)

AttCondition = List[AttSubCondition]
AttConditions = List[AttCondition]

class BaseAttestationParams(BaseModel):
    """Base attestation parameters"""
    app_id: str = Field(alias='appId')
    att_template_id: str = Field(alias='attTemplateID')
    user_address: str = Field(alias='userAddress')
    
    model_config = ConfigDict(populate_by_name=True)

class FullAttestationParams(BaseAttestationParams):
    """Full attestation parameters"""
    timestamp: int
    att_mode: Optional[AttMode] = Field(None, alias='attMode')
    att_conditions: Optional[AttConditions] = Field(None, alias='attConditions')
    addition_params: Optional[str] = Field(None, alias='additionParams')  # Store as JSON string
    
    model_config = ConfigDict(populate_by_name=True)

class SignedAttRequest(BaseModel):
    """Signed attestation request"""
    att_request: FullAttestationParams = Field(alias='attRequest')
    app_signature: str = Field(alias='appSignature')
    
    model_config = ConfigDict(populate_by_name=True)
