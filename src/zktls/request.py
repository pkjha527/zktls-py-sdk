"""
Attestation request implementation
"""
from typing import Dict, Any, Optional, List, cast
import json
import time

from .types import (
    BaseAttestationParams,
    AttMode,
    AttConditions,
    AttModeAlgorithmType,
    AttModeResultType,
    FullAttestationParams,
    AttSubCondition,
    AttCondition,
    OpType
)

class AttRequest:
    """Attestation request"""
    
    def __init__(self, base_params: Dict[str, str]):
        """
        Initialize attestation request
        
        Args:
            base_params: Base parameters including appId,
                        attTemplateID, and userAddress
        """
        self.base_params = BaseAttestationParams(**base_params)
        self.timestamp = int(time.time() * 1000)  # milliseconds
        self.att_mode = AttMode(
            algorithm_type=AttModeAlgorithmType.PROXY_TLS,
            result_type=AttModeResultType.PLAIN
        )
        self.att_conditions: Optional[AttConditions] = None
        self.addition_params: Optional[str] = None
        
    def set_addition_params(self, addition_params: Dict[str, Any]):
        """Set additional parameters"""
        self.addition_params = json.dumps(addition_params)
        
    def set_att_mode(self, att_mode: Dict[str, str]):
        """Set attestation mode"""
        self.att_mode = AttMode(
            algorithm_type=att_mode['algorithm_type'],
            result_type=att_mode.get('result_type', 'plain')
        )
        
    def set_att_conditions(self, conditions: Dict[str, Any]):
        """
        Set attestation conditions
        
        Args:
            conditions: List of conditions in the format:
                [
                    [  # AttCondition (AND)
                        {  # AttSubCondition
                            'field': 'field_name',
                            'op': '=',
                            'value': 'value'
                        }
                    ]
                ]
        """
        parsed_conditions: List[AttCondition] = []
        
        for condition_group in conditions:
            sub_conditions: List[AttSubCondition] = []
            for condition in condition_group:
                sub_conditions.append(
                    AttSubCondition(
                        field=condition['field'],
                        op=condition['op'],
                        value=condition.get('value')
                    )
                )
            parsed_conditions.append(sub_conditions)
            
        self.att_conditions = parsed_conditions
        
    def to_full_params(self) -> FullAttestationParams:
        """Convert to full attestation parameters"""
        return FullAttestationParams(
            appId=self.base_params.app_id,
            attTemplateID=self.base_params.att_template_id,
            userAddress=self.base_params.user_address,
            timestamp=self.timestamp,
            attMode=self.att_mode,
            attConditions=self.att_conditions,
            additionParams=self.addition_params
        )
        
    def to_json_string(self) -> str:
        """Convert request to JSON string"""
        return self.to_full_params().model_dump_json(by_alias=True)
