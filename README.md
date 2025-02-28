# ZK TLS Python SDK

A Python SDK wrapper for Primus Labs' Zero-Knowledge TLS (ZK TLS) protocol. This SDK provides a Python interface to the official `@primuslabs/zktls-core-sdk` Node.js package, enabling secure attestation and proxy TLS functionality.

## System Requirements

- Python 3.8+
- Node.js 14+

## Overview

The ZK TLS Python SDK provides a robust interface for interacting with Primus Labs' attestation infrastructure through the official Node.js SDK. It supports:

- **Zero-Knowledge Attestations**: Create and verify attestations without exposing underlying data
- **Proxy TLS**: Secure communication channel for attestation requests
- **Ethereum Integration**: Sign requests using Ethereum private keys
- **Async Support**: Built with modern async/await patterns
- **Type Safety**: Comprehensive type hints and Pydantic models for reliable development

## Installation

```bash
# Install Node.js package
npm install @primuslabs/zktls-core-sdk

# Install Python package
pip install zktls-py-sdk
```

## Quick Start

```python
import asyncio
from zktls import NodeWrapper

async def main():
    # Initialize wrapper
    wrapper = NodeWrapper()
    await wrapper.init("your_app_id", "your_app_secret")
    
    # Create request
    request = {
        "url": "https://api.example.com",
        "method": "GET",
        "header": {"Authorization": "Bearer token"},
        "body": ""
    }
    
    # Start attestation
    attestation = await wrapper.start_attestation(request)
    
    # Verify attestation
    is_valid = await wrapper.verify_attestation(attestation)
    print(f"Attestation valid: {is_valid}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

```python
from zktls import ZKAttestationError

try:
    attestation = await wrapper.start_attestation(request)
except ZKAttestationError as e:
    print(f"Error: {e.error_data.title} - {e.error_data.desc}")
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Type Checking

```bash
# Run type checker
mypy src/

# Run linter
pylint src/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
