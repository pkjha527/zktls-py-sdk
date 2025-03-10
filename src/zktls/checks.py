"""Installation and runtime checks for ZK TLS SDK"""
import os
import sys
import json
import subprocess
from typing import Tuple, Optional

class InstallationError(Exception):
    """Raised when installation requirements are not met"""
    pass

def check_node_version() -> Tuple[bool, str]:
    """Check if Node.js is installed and version >= 14"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Node.js not found"
        
        version = result.stdout.strip().lstrip("v").split(".")
        major = int(version[0])
        if major < 14:
            return False, f"Node.js version {result.stdout.strip()} is too old (need >= 14)"
            
        return True, f"Node.js {result.stdout.strip()} found"
    except Exception as e:
        return False, str(e)

def check_npm_version() -> Tuple[bool, str]:
    """Check if npm is installed and version >= 6"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "npm not found"
        
        version = result.stdout.strip().split(".")
        major = int(version[0])
        if major < 6:
            return False, f"npm version {result.stdout.strip()} is too old (need >= 6)"
            
        return True, f"npm {result.stdout.strip()} found"
    except Exception as e:
        return False, str(e)

def check_sdk_installation() -> Tuple[bool, str]:
    """Check if @primuslabs/zktls-core-sdk is installed"""
    try:
        # Try to require the SDK with basic initialization test
        script = """
try {
    console.log('Loading SDK...');
    const { PrimusCoreTLS } = require('@primuslabs/zktls-core-sdk');
    
    // Test basic SDK instantiation without initialization
    const sdk = new PrimusCoreTLS();
    console.log('SDK instantiated successfully');
    
    // Exit immediately after basic test
    process.exit(0);
} catch(e) {
    console.error('SDK Error:', e);
    process.exit(1);
}

// Force exit after 1 second in case SDK has hanging promises
setTimeout(() => {
    console.error('SDK check timed out');
    process.exit(1);
}, 1000);
"""
        result = subprocess.run(
            ["node", "-e", script],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=5  # Reduced timeout since we have an internal timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return False, f"Node.js SDK is not installed correctly: {error_msg}"
            
        return True, "ZK TLS SDK found and basic instantiation successful"
    except subprocess.TimeoutExpired:
        return False, "SDK check timed out - this may indicate an issue with the SDK initialization"
    except Exception as e:
        return False, str(e)

def check_node_scripts() -> Tuple[bool, Optional[str]]:
    """Check if Node.js wrapper scripts are present"""
    script_path = os.path.join(os.getcwd(), "node_scripts", "wrapper.js")
    if not os.path.exists(script_path):
        return False, "Node.js wrapper script is missing"
    return True, None

def verify_installation() -> None:
    """Verify all installation requirements are met"""
    # Check Node.js
    node_ok, node_msg = check_node_version()
    if not node_ok:
        raise InstallationError(
            f"Node.js check failed: {node_msg}\n"
            "Please install Node.js 14+ from https://nodejs.org/"
        )

    # Check npm
    npm_ok, npm_msg = check_npm_version()
    if not npm_ok:
        raise InstallationError(
            f"npm check failed: {npm_msg}\n"
            "Please install npm 6+ by updating Node.js"
        )

    # Check SDK installation
    sdk_ok, sdk_msg = check_sdk_installation()
    if not sdk_ok:
        raise InstallationError(
            f"SDK check failed: {sdk_msg}\n"
            "Please run: npm install @primuslabs/zktls-core-sdk"
        )

def check_runtime_environment() -> None:
    """Check runtime environment before executing commands"""
    # Check wrapper scripts first
    scripts_ok, scripts_msg = check_node_scripts()
    if not scripts_ok:
        raise InstallationError(
            f"Wrapper script check failed: {scripts_msg}\n"
            "Please reinstall the package"
        )
        
    # Verify Node.js process can be started
    try:
        process = subprocess.Popen(
            ["node", "-e", "process.exit(0)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.wait(timeout=5)
        if process.returncode != 0:
            raise InstallationError("Failed to start Node.js process")
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        raise InstallationError(f"Node.js process check failed: {str(e)}")

    # Verify SDK can be loaded
    try:
        process = subprocess.Popen(
            ["node", "-e", "const sdk = require('@primuslabs/zktls-core-sdk'); process.exit(0)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.wait(timeout=5)
        if process.returncode != 0:
            raise InstallationError("Failed to load Node.js SDK")
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        raise InstallationError(f"SDK load check failed: {str(e)}")

def print_environment_info() -> None:
    """Print information about the environment"""
    node_ok, node_version = check_node_version()
    npm_ok, npm_version = check_npm_version()
    
    print("\nEnvironment Information:")
    print(f"Python version: {sys.version}")
    print(f"Node.js version: {node_version if node_ok else 'Not installed'}")
    print(f"npm version: {npm_version if npm_ok else 'Not installed'}")
    
    # Get SDK version
    try:
        result = subprocess.run(
            ["npm", "list", "@primuslabs/zktls-core-sdk"],
            capture_output=True,
            text=True
        )
        print(f"SDK version: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("SDK version: Not installed")
