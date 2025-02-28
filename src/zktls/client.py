"""
Primus ZK TLS Client implementation
"""
import json
import time
import asyncio
from typing import Optional, Dict, Any, Union, cast
from pathlib import Path

from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_typing import Address

from .constants import (
    PADO_ADDRESS_MAP,
    ATTESTATION_POLLING_INTERVAL_MS,
    ATTESTATION_POLLING_TIMEOUT_MS
)
from .request import AttRequest
from .exceptions import ZkAttestationError
from .types import (
    StartAttestationReturn,
    SignedAttRequest,
    ErrorData,
    Attestation,
    AttNetworkRequest,
    InitAttestationReturn,
    Env,
    AttMode,
    AttModeAlgorithmType,
    AttModeResultType,
    AttConditions,
    FullAttestationParams
)

class PrimusZKTLS:
    """Client for ZK TLS attestation"""
    
    def __init__(self):
        """Initialize the client"""
        self.is_initialized = False
        self._env: Env = 'production'
        self._pado_address = PADO_ADDRESS_MAP[self._env]
        self.app_id = ''
        self.app_secret = None
        
    def init(self, app_id: str, app_secret: Optional[str] = None) -> InitAttestationReturn:
        """
        Initialize the client
        
        Args:
            app_id: Application ID
            app_secret: Application secret for signing requests
            
        Returns:
            InitAttestationReturn object
        """
        if not app_secret:
            return InitAttestationReturn(
                result=False,
                error_data=ErrorData(
                    code="INIT_ERROR",
                    title="Initialization Error",
                    desc="app_secret is required for signing requests"
                )
            )
            
        self.app_id = app_id
        self.app_secret = app_secret
        self.is_initialized = True
        return InitAttestationReturn(result=True)
            
    async def request_attestation(
        self,
        att_template_id: str,
        user_address: str,
        addition_params: Optional[str] = None,
        att_conditions: Optional[Dict] = None
    ) -> StartAttestationReturn:
        """
        Request attestation
        
        Args:
            att_template_id: Attestation template ID
            user_address: User's Ethereum address
            addition_params: Optional additional parameters
            att_conditions: Optional attestation conditions
            
        Returns:
            StartAttestationReturn object
        """
        if not self.is_initialized:
            raise ZkAttestationError("Client not initialized")
            
        # Create attestation request
        request = AttRequest({
            'appId': self.app_id,
            'attTemplateID': att_template_id,
            'userAddress': user_address
        })
        
        if addition_params:
            request.set_addition_params(addition_params)
            
        if att_conditions:
            request.set_att_conditions(att_conditions)
            
        # Sign request if app secret available
        signed_request = self._sign_request(request)
        
        # Make attestation request
        return await self._poll_attestation(signed_request)
        
    def _sign_request(self, request: AttRequest) -> SignedAttRequest:
        """Sign attestation request with app secret"""
        if not self.app_secret:
            raise ZkAttestationError("App secret required for signing request")
            
        full_params = request.to_full_params()
        message = full_params.model_dump_json()
        
        account = Account.from_key(self.app_secret)
        message_hash = encode_defunct(text=message)
        signed = account.sign_message(message_hash)
        
        return SignedAttRequest(
            attRequest=full_params,
            appSignature=signed.signature.hex()
        )
        
    async def _poll_attestation(self, signed_request: SignedAttRequest) -> StartAttestationReturn:
        """Poll for attestation result"""
        start_time = time.time()
        
        while True:
            if (time.time() - start_time) * 1000 > ATTESTATION_POLLING_TIMEOUT_MS:
                return StartAttestationReturn(
                    result=False,
                    error_data=ErrorData(
                        code="TIMEOUT",
                        title="Attestation Timeout",
                        desc="Attestation polling timed out"
                    )
                )
                
            # Make request to attestation service
            # Implementation needed
            # For now, return a mock response
            await asyncio.sleep(ATTESTATION_POLLING_INTERVAL_MS / 1000)
            
            return StartAttestationReturn(
                result=True,
                data=Attestation(
                    recipient=signed_request.att_request.user_address,
                    request=AttNetworkRequest(
                        url="",
                        header="{}",
                        method="GET",
                        body="{}"
                    ),
                    response_resolve=[],
                    data="{}",
                    att_conditions="{}",
                    timestamp=int(time.time() * 1000),
                    addition_params="",
                    attestors=[],
                    signatures=[]
                )
            )
            
    def set_env(self, env: Env):
        """Set environment (development/production)"""
        if env not in PADO_ADDRESS_MAP:
            raise ZkAttestationError("Invalid environment")
        self._env = env
        self._pado_address = PADO_ADDRESS_MAP[env]
