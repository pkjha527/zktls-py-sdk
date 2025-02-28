# ZK TLS Python SDK

A Python SDK for integrating Primus Labs' Zero-Knowledge TLS (ZK TLS) protocol into your applications. This SDK enables secure attestation and proxy TLS functionality, allowing applications to verify and attest to specific conditions without revealing sensitive data.

## Overview

The ZK TLS Python SDK provides a robust interface for interacting with Primus Labs' attestation infrastructure. It supports:

- **Zero-Knowledge Attestations**: Create and verify attestations without exposing underlying data
- **Proxy TLS**: Secure communication channel for attestation requests
- **Ethereum Integration**: Sign requests using Ethereum private keys
- **Flexible Conditions**: Define complex attestation conditions using logical operators
- **Async Support**: Built with modern async/await patterns using aiohttp
- **Type Safety**: Comprehensive type hints and Pydantic models for reliable development

## Installation

```bash
pip install zktls-py-sdk
```

## Requirements

- Python 3.8 or higher
- Dependencies:
  - web3>=6.0.0
  - eth-account
  - eth-typing
  - aiohttp
  - pydantic
  - asyncio

## Quick Start

```python
import asyncio
from zktls import PrimusZKTLS
from eth_account import Account

async def main():
    # Initialize client
    client = PrimusZKTLS()
    
    # Initialize with your app credentials
    client.init(
        app_id="your_app_id",  # Hex String
        app_secret="your_app_secret"
    )
    
    # Create an attestation request
    result = await client.request_attestation(
        att_template_id="template_id",
        user_address="0x...",  # Ethereum address
        att_conditions=[
            [
                {
                    "field": "balance",
                    "op": ">=",
                    "value": "1000"
                }
            ]
        ]
    )
    
    print(f"Attestation request created: {result.data['requestId']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

### Zero-Knowledge Attestations

Create attestation requests with complex conditions while maintaining privacy:

```python
conditions = [
    [  # AND group
        {"field": "age", "op": ">=", "value": "18"},
        {"field": "country", "op": "=", "value": "US"}
    ],
    [  # OR group
        {"field": "membership", "op": "=", "value": "premium"}
    ]
]
```

### Proxy TLS Support

Secure communication channel for attestation requests with built-in TLS support:

```python
client.set_att_mode({
    "algorithm_type": "proxytls",
    "result_type": "plain"
})
```

### Custom Parameters

Add additional parameters to attestation requests:

```python
client.request_attestation(
    # ... other params ...
    addition_params={
        "custom_field": "value",
        "metadata": {"key": "value"}
    }
)
```

## Examples

Check out the `examples/` directory for more detailed examples:

- `basic_usage.py`: Basic SDK initialization and attestation requests
- `proxy_tls.py`: Using proxy TLS functionality
- `advanced_usage.py`: Advanced features and error handling

## Development

### Running Tests

```bash
pytest tests/
```

### Type Checking

The SDK uses type hints throughout. Use mypy for type checking:

```bash
mypy src/
```

## License

MIT License - see LICENSE file for details

## Support



## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.
