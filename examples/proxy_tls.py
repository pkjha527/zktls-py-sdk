"""
Example of using ZK TLS SDK with proxy TLS mode
"""
import asyncio
import logging
from zktls import PrimusZKTLS, AttestationMode, AttestationCondition

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Example of making requests through ZK TLS proxy"""
    try:
        # Initialize the SDK
        app_id = "your_app_id"
        app_secret = "your_app_secret"  # Optional
        
        client = PrimusZKTLS()
        await client.init(app_id, app_secret)
        
        # Create an attestation request with proxy TLS mode
        att_request = client.create_attestation_request()
        att_request.set_mode(AttestationMode.PROXY_TLS)
        
        # Add conditions for the attestation
        att_request.add_condition(AttestationCondition.SECURE_BOOT)
        att_request.add_condition(AttestationCondition.DEBUG_DISABLED)
        
        # Request attestation with proxy TLS
        result = await client.request_attestation(att_request)
        logger.info("Proxy TLS attestation successful!")
        logger.info("Result: %s", result)
        
        # Make a GET request through the proxy
        response = await client.get("https://api.example.com/data")
        data = await response.json()
        logger.info("Data received through proxy: %s", data)
        
    except Exception as e:
        logger.error("Error in proxy TLS example: %s", str(e))

if __name__ == "__main__":
    asyncio.run(main())
