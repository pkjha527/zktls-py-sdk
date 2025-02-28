"""
Basic example of using the ZK TLS SDK
"""
import asyncio
import logging
from pathlib import Path
from zktls import PrimusZKTLS, AttestationMode, AttestationCondition

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Example of making secure requests with ZK TLS"""
    try:
        # Initialize the SDK
        app_id = "your_app_id"
        app_secret = "your_app_secret"  # Optional
        
        client = PrimusZKTLS()
        await client.init(app_id, app_secret)
        
        # Create an attestation request
        att_request = client.create_attestation_request()
        
        # Set attestation parameters
        att_request.set_mode(AttestationMode.STANDARD)
        att_request.add_condition(AttestationCondition.SECURE_BOOT)
        att_request.add_condition(AttestationCondition.DEBUG_DISABLED)
        
        # Request attestation
        try:
            result = await client.request_attestation(att_request)
            logger.info("Attestation successful!")
            logger.info("Result: %s", result)
        except Exception as e:
            logger.error("Attestation failed: %s", str(e))
            
    except Exception as e:
        logger.error("Error in example: %s", str(e))

if __name__ == "__main__":
    asyncio.run(main())
