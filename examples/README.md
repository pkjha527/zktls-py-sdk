# ZK TLS SDK Examples

This directory contains example code demonstrating how to use the ZK TLS Python SDK.

## Examples

### Basic Usage (`basic_usage.py`)
Shows the core functionality of the SDK:
- Initializing the client
- Creating an attestation request
- Setting attestation mode and conditions
- Making an attestation request

### Proxy TLS (`proxy_tls.py`)
Demonstrates using the SDK in proxy TLS mode:
- Setting up proxy TLS mode
- Making attestation requests
- Making HTTP requests through the ZK TLS proxy

## Running the Examples

1. Install the SDK:
```bash
pip install zktls-py-sdk
```

2. Set your credentials:
Replace `your_app_id` and `your_app_secret` in the examples with your actual credentials.

3. Run an example:
```bash
python examples/basic_usage.py
# or
python examples/proxy_tls.py
```

## Notes
- The examples use logging to show what's happening
- Error handling is included to demonstrate best practices
- The examples are kept simple to focus on core functionality
