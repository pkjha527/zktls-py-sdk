import asyncio
from zktls import PrimusZKTLS, AttestationMode, AttestationCondition

async def main():
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
    
    try:
        # Request attestation with proxy TLS
        result = await client.request_attestation(att_request)
        print("Proxy TLS attestation successful!")
        print("Result:", result)
        
        # Make a request through the proxy
        response = await client.get("https://api.example.com/data")
        data = await response.json()
        print("Data received through proxy:", data)
        
        # Post data through the proxy
        post_data = {"key": "value"}
        response = await client.post(
            "https://api.example.com/data",
            json=post_data
        )
        result = await response.json()
        print("Post result through proxy:", result)
        
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(main())
