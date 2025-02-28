"""
Advanced example showing more features of the ZK TLS SDK
"""
import asyncio
import logging
from pathlib import Path
from typing import Optional
from zktls import ZKTLSClient, ZKTLSConfig, PrimusZKTLS, AttestationMode, AttestationCondition, AttestationParams, AttestationError
from zktls.utils import generate_challenge, hash_message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Certificate paths - replace with your actual paths
CERT_DIR = Path("certs")
CA_CERT = CERT_DIR / "ca.crt"
CLIENT_CERT = CERT_DIR / "client.crt"
CLIENT_KEY = CERT_DIR / "client.key"
ZK_PROOF = CERT_DIR / "zk_proof.bin"

class APIClient:
    """Example API client using ZK TLS"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self._client: Optional[ZKTLSClient] = None
        
    async def __aenter__(self):
        """Setup client on context manager entry"""
        config = ZKTLSConfig(
            ca_cert_path=CA_CERT,
            client_cert_path=CLIENT_CERT,
            client_key_path=CLIENT_KEY,
            zk_proof_path=ZK_PROOF,
            timeout=30.0
        )
        self._client = ZKTLSClient(config)
        await self._client.create_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on context manager exit"""
        if self._client:
            await self._client.close()
            
    async def get_user(self, user_id: int):
        """Get user by ID"""
        url = f"{self.base_url}/users/{user_id}"
        response = await self._client.get(url)
        return await response.json()
        
    async def create_user(self, username: str, email: str):
        """Create new user"""
        url = f"{self.base_url}/users"
        data = {
            "username": username,
            "email": email
        }
        response = await self._client.post(url, json=data)
        return await response.json()
        
    async def update_user(self, user_id: int, **updates):
        """Update user fields"""
        url = f"{self.base_url}/users/{user_id}"
        response = await self._client.put(url, json=updates)
        return await response.json()
        
    async def delete_user(self, user_id: int):
        """Delete user"""
        url = f"{self.base_url}/users/{user_id}"
        response = await self._client.delete(url)
        return response.status == 204

async def main():
    """Example of advanced API usage with ZK TLS"""
    try:
        api_url = "https://api.example.com/v1"
        
        async with APIClient(api_url) as client:
            # Create user
            user = await client.create_user(
                username="testuser",
                email="test@example.com"
            )
            logger.info("Created user: %s", user)
            
            # Get user
            user_id = user['id']
            user_data = await client.get_user(user_id)
            logger.info("Retrieved user: %s", user_data)
            
            # Update user
            updated = await client.update_user(
                user_id,
                email="newemail@example.com"
            )
            logger.info("Updated user: %s", updated)
            
            # Delete user
            deleted = await client.delete_user(user_id)
            logger.info("User deleted: %s", deleted)
            
    except Exception as e:
        logger.error("Error in example: %s", str(e))

async def custom_attestation_example():
    """Example showing custom attestation parameters and error handling"""
    client = PrimusZKTLS()
    
    try:
        # Initialize with custom network (e.g., for testing)
        await client.init(
            app_id="your_app_id",
            app_secret="your_app_secret",
            network="goerli"  # Use testnet
        )
        
        # Create attestation request with custom parameters
        att_request = client.create_attestation_request()
        att_request.set_mode(AttestationMode.STANDARD)
        
        # Add multiple conditions
        conditions = [
            AttestationCondition.SECURE_BOOT,
            AttestationCondition.DEBUG_DISABLED,
            AttestationCondition.LATEST_OS
        ]
        for condition in conditions:
            att_request.add_condition(condition)
        
        # Set custom parameters
        custom_params = AttestationParams(
            timeout=60,  # Custom timeout in seconds
            retry_count=3,  # Number of retries
            polling_interval=5  # Polling interval in seconds
        )
        att_request.set_params(custom_params)
        
        # Request attestation with error handling
        try:
            result = await client.request_attestation(att_request)
            logger.info("Attestation successful!")
            logger.info("Attestation ID: %s", result.attestation_id)
            logger.info("Status: %s", result.status)
            logger.info("Timestamp: %s", result.timestamp)
            
        except AttestationError as ae:
            logger.error("Attestation failed: %s", str(ae))
            if ae.retry_possible:
                logger.info("Retrying attestation...")
                # Implement retry logic here
                
        except asyncio.TimeoutError:
            logger.error("Attestation timed out")
            
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            
    except Exception as e:
        logger.error("Client initialization failed: %s", str(e))

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.run(custom_attestation_example())
