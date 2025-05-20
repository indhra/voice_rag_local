import importlib.util
import pkg_resources
import sys
import subprocess
import platform

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def check_gpu():
    """Check if GPU is available based on operating system."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        try:
            # Check for Metal GPU support on Apple Silicon/Intel Macs
            from subprocess import check_output
            gpu_info = check_output(["system_profiler", "SPDisplaysDataType"]).decode()
            metal_capable = any("Metal" in line for line in gpu_info.split("\n"))
            if metal_capable:
                return "mps"  # Metal Performance Shaders
        except:
            return "cpu"
    
    elif system == "Windows":
        try:
            # Check for CUDA GPU on Windows
            import torch
            if torch.cuda.is_available():
                return "cuda"
            else:
                # Try nvidia-smi as fallback
                try:
                    subprocess.check_output('nvidia-smi')
                    return "cuda"
                except:
                    return "cpu"
        except ImportError:
            try:
                subprocess.check_output('nvidia-smi')
                return "cuda"
            except:
                return "cpu"
    
    return "cpu"

def main():
    requirements_file = "requirements.txt"
    
    try:
        with open(requirements_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"{RED}Error: requirements.txt not found!{RESET}")
        sys.exit(1)

    
    print("Installing remaining packages...")
    installed = []
    failed = []

    for package in packages:
        if install_package(package):
            installed.append(package)
            print(f"{GREEN}Successfully installed {package}{RESET}")
        else:
            failed.append(package)
            print(f"{RED}Failed to install {package}{RESET}")

    print("Checking GPU availability...")
    gpu_type = check_gpu()
    
    if gpu_type == "cuda":
        print(f"{GREEN}NVIDIA GPU detected! Installing CUDA-enabled PyTorch...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "torch", "torchaudio", 
                             "--index-url", "https://download.pytorch.org/whl/cu118"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
    elif gpu_type == "mps":
        print(f"{GREEN}Apple Silicon/Metal GPU detected! Installing native PyTorch...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "torch", "torchaudio"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
    else:
        print(f"{RED}No GPU detected! Installing CPU-only PyTorch...{RESET}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "torch", "torchaudio"],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)

    # Remove torch from packages list since we just installed it
    packages = [pkg for pkg in packages if pkg != 'torch']
    
    print("\nInstallation Summary:")
    if installed:
        print(f"{GREEN}Successfully installed {len(installed)} packages{RESET}")
    if failed:
        print(f"{RED}Failed to install {len(failed)} packages:{RESET}")
        for package in failed:
            print(f"- {package}")

if __name__ == "__main__":
    main()
