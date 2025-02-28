# ZK TLS Python SDK Examples

This directory contains example scripts demonstrating how to use the ZK TLS Python SDK.

## Examples Overview

1. `basic_usage.py`: Basic example showing how to:
   - Initialize the SDK
   - Create an attestation request
   - Set attestation mode and conditions
   - Request attestation

2. `proxy_tls.py`: Example demonstrating proxy TLS functionality:
   - Setting up proxy TLS mode
   - Making HTTP requests through the proxy
   - Handling proxy responses

3. `advanced_usage.py`: Advanced usage examples including:
   - Custom attestation parameters
   - Multiple attestation conditions
   - Comprehensive error handling
   - Using custom networks (e.g., testnet)

## Running the Examples

1. Make sure you have installed the SDK:
   ```bash
   pip install -e ".[test]"
   ```

2. Set up your credentials:
   - Replace `your_app_id` and `your_app_secret` with your actual credentials
   - For testing, you can use the testnet network ("goerli")

3. Run an example:
   ```bash
   python examples/basic_usage.py
   ```

## Notes

- These examples are for demonstration purposes and may need to be modified for your specific use case
- Always handle errors appropriately in production code
- Refer to the main SDK documentation for complete API details
