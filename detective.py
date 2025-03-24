#!/usr/bin/env python3

import subprocess
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
import re
import json
import sqlite3

# List of required tools
required_tools = ["go", "subfinder", "assetfinder", "sublist3r", "findomain", "httpx"]

art = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⠹⡆⢀⣤⣤⡀⢠⣤⢠⣤⣿⡤⣴⡆⠀⣴⠀⠀⠀⢠⣄⠀⢠⡄⠀⠀⠀⣤⣄⣿⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠰⠆⠀⣷⢸⣧⣀⡀⢸⢹⡆⠀⢸⡇⠠⣧⢤⣿⠀⠀⠀⢸⡟⣦⣸⡇⡞⡙⢣⡀⢠⡇⠀⢿⠋⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⣠⠟⢸⣇⣀⡀⣿⠉⢻⡀⢸⡇⠀⣿⠀⣿⠀⠀⠀⣸⡇⠘⢿⡏⢇⣁⡼⠃⣼⠃⠀⣼⡓⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⡿⠒⠋⠁⠀⠈⠉⠉⠁⠉⠀⠀⠀⠀⠉⠀⠉⠀⠉⠀⠀⠀⠉⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠛⠓⠲⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣴⣶⣾⣿⣿⣾⣷⣦⣤⣿⣶⣶⣤⣄⣀⢤⡀⠀⠀⠀⠀⢰⣴⣶⣷⣴⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣀⣀⣀⣤⣤⣶⣶⣶⣦⣤⠤
⠠⠔⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⢀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠂⠀⠀
⠀⠀⠀⠘⠋⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⢻⣿⣿⣿⣿⡏⠀⠀⠀⢀⣤⣾⣿⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⠀⡿⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠛⠟⠋⣿⣿⡿⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⠋⠙⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡿⠀⠸⠋⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⣿⣿⣿⠋⠛⠇⠀⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⢀⣿⣿⠁⠀⠈⢻⣿⣿⣿⣿⣿⡿⠋⠈⣿⣿⡏⠃⠀⠘⣿⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡏⠀⠀⠀⠈⣿⣿⣿⣿⣿⠀⠀⠀⠸⣿⣇⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⣼⣿⣿⣿⣿⣿⡄⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠁⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠋⠉⠉⠛⠉⠋⠻⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⣤⣾⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⡇⠙⠀⠀⠀⢸⠋⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⢿⣷⡢⡀⠀⠀⢀⣰⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⠀⠁⠁⠀⠀⠀⠀⠉⢠⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡄⠀⠀⠀⠀⠀⠀⠀⣾⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣇⠀⠀⠀⠀⠀⠀⢸⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠀⠀⠀⠀⠀⠀⠘⢿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀2.0⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
'''

print(art)

# Function to check if a tool is installed
def check_tool_availability(tool):
    result = subprocess.run(["which", tool], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None

# Function to install Go if missing
def install_go():
    default_version = "go1.23.6.linux-amd64.tar.gz"  # Check for the latest version before using this
    default_url = f"https://go.dev/dl/{default_version}"

    print(f"\n[!] Go is missing. The default version to install is: {default_version}")
    user_choice = input("[?] Do you want to install this version? (yes/no): ").strip().lower()

    if user_choice != "yes":
        custom_url = input("[?] Enter the download URL for a newer Go version: ").strip()
        if custom_url:
            default_url = custom_url
            default_version = custom_url.split("/")[-1]
        else:
            print("[✗] No valid URL provided. Skipping Go installation.")
            return

    print(f"[!] Installing Go version: {default_version}")

    try:
        # Download Go
        subprocess.run(["wget", default_url], check=True)
        print("[✓] Go downloaded.")

        # Extract Go
        subprocess.run(["sudo", "tar", "-C", "/usr/local", "-xzf", default_version], check=True)
        print("[✓] Go extracted to /usr/local.")

        # Remove tar file
        os.remove(default_version)
        print("[✓] Installation file removed.")

        # Add Go to PATH
        with open(os.path.expanduser("~/.zshrc"), "a") as file:
            file.write('\nexport PATH=$PATH:/usr/local/go/bin\n')
            file.write('\nexport PATH=$PATH:$HOME/go/bin\n')
        print("[✓] Go path added to ~/.zshrc.")

        # Apply changes
        print("[!] Restart your terminal or run `source ~/.zshrc` to apply the changes.")
        print("[✓] Go installation completed successfully!")

    except Exception as e:
        print(f"[✗] Failed to install Go: {e}")

def install_sublist3r():
    print(f"\n[!] sublist3r is missing.")
    user_choice = input("[?] Do you want to install using git? (yes/no): ").strip().lower()

    if user_choice == "yes":
        # Install git if not already installed
        try:
            subprocess.run(["sudo", "apt", "install", "git", "-y"], check=True)
            print("[✓] Git installed successfully.")

            # Change to the Desktop directory
            os.chdir(os.path.expanduser("~/Desktop"))
            print(f"[✓] Changed directory to {os.getcwd()}")

            # Clone the sublist3r repository
            subprocess.run(["git", "clone", "https://github.com/aboul3la/Sublist3r.git"], check=True)
            print("[✓] sublist3r cloned from GitHub.")

            # Change to the sublist3r directory
            os.chdir(os.path.expanduser("~/Desktop/Sublist3r"))
            print(f"[✓] Changed directory to {os.getcwd()}")

            # Install the required dependencies
            subprocess.run(["sudo", "pip3", "install", "-r", "requirements.txt", "--break-system-packages"], check=True)
            print("[✓] Dependencies installed successfully.")

            # Check if the sublist3r executable exists or needs to be built
            if not os.path.isfile("./sublist3r.py"):
                print("[!] sublist3r executable not found. Attempting to build it.")
                subprocess.run(["sudo", "python3", "setup.py", "install"], check=True)
                print("[✓] sublist3r built and installed successfully.")
            else:
                print("[✓] sublist3r executable found.")

            # Move the executable to /usr/local/bin and set permissions
            subprocess.run(["sudo", "mv", "subbrute", "/usr/local/bin/"], check=True)
            subprocess.run(["sudo", "mv", "./sublist3r.py", "/usr/local/bin/sublist3r"], check=True)
            subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/sublist3r"], check=True)

            print("[✓] sublist3r installation completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing sublist3r: {e}")
    else:
        print("[✗] Skipping sublist3r installation.")
        return

def install_assetfinder():
    print(f"\n[!] assetfinder is missing.")
    
    # Check if Go is installed
    try:
        subprocess.run(["go", "version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("[✓] Go is already installed.")
    except subprocess.CalledProcessError:
        print("[✗] Go is not installed.")
        user_choice = input("[?] Do you want to install Go? (yes/no): ").strip().lower()
        if user_choice == "yes":
            install_go()  # Assuming you have already defined the install_go function
        else:
            print("[✗] Skipping assetfinder installation as Go is required.")
            return

    # Install assetfinder using Go
    try:
        print("[!] Installing assetfinder using Go...")
        subprocess.run(["go", "install", "github.com/tomnomnom/assetfinder@latest"], check=True)
        print("[✓] assetfinder installation completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Error installing assetfinder: {e}")  

def install_subfinder():
    print(f"\n[!] subfinder is missing.")
    user_choice = input("[?] Do you want to install using Go? (yes/no): ").strip().lower()

    if user_choice == "yes":
        try:
            # Install subfinder using Go
            print("[✓] Installing Subfinder...")
            subprocess.run(["go", "install", "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], check=True)
            print("[✓] subfinder installed successfully!")

        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing subfinder: {e}")
    else:
        print("[✗] Skipping subfinder installation.")
        return

def install_findomain():
    print(f"\n[!] Findomain is missing.")
    user_choice = input("[?] Do you want to install Findomain? (yes/no): ").strip().lower()

    if user_choice == "yes":
        try:
            # Install dependencies
            print("[✓] Installing dependencies...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "git", "curl", "build-essential"], check=True)
            print("[✓] Dependencies installed.")

            # Install Rust (if not already installed)
            print("[✓] Checking for Rust installation...")
            rust_check = subprocess.run(["which", "rustc"], capture_output=True, text=True)

            if rust_check.returncode != 0:  # Rust is not installed
                print("Rust not found, installing Rust...")
                subprocess.run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh", shell=True, check=True)

                # Ensure Cargo is in the PATH by adding it to ~/.zshrc
                with open(os.path.expanduser("~/.zshrc"), "a") as file:
                    file.write('\n# Adding Cargo to PATH\n')
                    file.write('. "$HOME/.cargo/env"\n')
                print("[✓] Rust installed successfully.")
                print("[✓] Cargo added to ~/.zshrc.")
                
                # Apply the changes immediately by sourcing the ~/.zshrc file
                subprocess.run("source ~/.zshrc", shell=True, check=True)
                
            else:
                print("[✓] Rust is already installed.")

            # Change to Desktop directory
            desktop_path = os.path.expanduser("~/Desktop")
            os.chdir(desktop_path)
            print(f"[✓] Changed directory to {os.getcwd()}")

            # Clone the Findomain repository
            print("[✓] Cloning Findomain repository...")
            subprocess.run(["git", "clone", "https://github.com/findomain/findomain.git"], check=True)

            # Navigate to the Findomain directory
            os.chdir("findomain")
            print(f"[✓] Changed directory to {os.getcwd()}")

            # Build Findomain - Update subprocess call to use shell=True
            print("[✓] Building Findomain...")
            subprocess.run("cargo build --release", shell=True, check=True)

            # Copy the binary to /usr/bin
            print("[✓] Copying Findomain binary to /usr/bin...")
            subprocess.run(["sudo", "cp", "target/release/findomain", "/usr/bin/"], check=True)
            print("[✓] Findomain installation completed successfully!")

        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing Findomain: {e}")
    else:
        print("[✗] Skipping Findomain installation.")
        return


def install_httpx():
    print(f"\n[!] httpx is missing.")
    user_choice = input("[?] Do you want to install httpx using Go? (yes/no): ").strip().lower()

    if user_choice == "yes":
        try:
            # Install httpx using Go
            print("[✓] Installing httpx...")
            subprocess.run(["go", "install", "github.com/projectdiscovery/httpx/cmd/httpx@latest"], check=True)
            print("[✓] httpx installed successfully!")

        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing httpx: {e}")
    else:
        print("[✗] Skipping httpx installation.")
        return


# Check each tool and print its status
missing_tools = []

for tool in required_tools:
    tool_path = check_tool_availability(tool)
    if tool_path:
        print(f"[✓] {tool} is installed at {tool_path}.")
        
        # Check if httpx is specifically in /usr/bin/httpx and remove it using sudo
        if tool == "httpx" and tool_path == "/usr/bin/httpx":
            print("[!] Removing httpx from /usr/bin/httpx with sudo...")
            try:
                subprocess.run(["sudo", "rm", "-f", "/usr/bin/httpx"], check=True)
                print("[✓] httpx has been removed.")
            except subprocess.CalledProcessError as e:
                print(f"[✗] Failed to remove httpx: {e}")
    else:
        print(f"[✗] {tool} is missing.")
        missing_tools.append(tool)

# If Go is missing, ask user before installing
if "go" in missing_tools:
    install_go()
    missing_tools.remove("go")  # Remove from missing tools list after installation

if "sublist3r" in missing_tools:
    install_sublist3r()
    missing_tools.remove("sublist3r") 

if "assetfinder" in missing_tools:
    install_assetfinder()
    missing_tools.remove("assetfinder")

if "subfinder" in missing_tools:
    install_subfinder()
    missing_tools.remove("subfinder")

if "findomain" in missing_tools:
    install_findomain()
    missing_tools.remove("findomain")

if "httpx" in missing_tools:
    install_httpx()
    missing_tools.remove("httpx")

# Tools

# Function to create a directory for each domain (if it doesn't exist)
def create_directory(domain):
    """Create a directory for the domain."""
    directory = f"{domain}_scan"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Function to send bulk notification using Project Discovery's notify
def send_notify_notification(discord_webhook, file_path):
    """Send bulk notification using the 'notify' tool from Project Discovery."""
    try:
        # Assuming 'discord.yaml' is correctly configured and exists
        result = subprocess.run(
            ["notify", "-provider-config", "discord.yaml", "-data", file_path, "-bulk"], 
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("[✓] Notification sent successfully!")
        else:
            print(f"[✗] Error sending notification: {result.stderr}")
    except Exception as e:
        print(f"[✗] Failed to execute 'notify' command: {e}")

# Load program configuration from JSON file
def load_program_config(config_path='programs_config.json'):
    """Load configuration from programs_config.json."""
    with open(config_path, 'r') as f:
        return json.load(f)["programs"]

# Run subdomain discovery tools in parallel
def run_subdomain_discovery(domain, tools):
    """Run subdomain discovery tools and return the discovered subdomains."""
    all_subdomains = set()

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda tool: run_tool(tool, domain), tools)

    for result in results:
        if result:
            all_subdomains.update(result)

    return all_subdomains

# Run a specific tool for subdomain discovery
def run_tool(tool, domain):
    """Run an individual subdomain discovery tool."""
    print(f"[+] Running {tool}...")
    if tool == "subfinder":
        command = ["subfinder", "-silent", "-d", domain]
    elif tool == "assetfinder":
        command = ["assetfinder", "--subs-only", domain]
    elif tool == "sublist3r":
        command = ["sublist3r", "-d", domain, "-o", "/dev/stdout"]
    elif tool == "findomain":
        command = ["findomain", "-t", domain]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[✗] Error running {tool}: {result.stderr}")
        return set()

    return set(result.stdout.strip().splitlines())

# Function to check live subdomains using httpx
def filter_httpx(subdomains, output_file):
    """Check live subdomains with httpx."""
    try:
        temp_file_path = "temp_subdomains.txt"
        # Save subdomains to temporary file
        with open(temp_file_path, "w") as f:
            f.write("\n".join(subdomains))
        
        # Run httpx to check live subdomains
        httpx_command = [
            "httpx", "-ip", "-cdn", "-title", "-status-code", "-tech-detect", "-silent", "-l", temp_file_path
        ]
        httpx_result = subprocess.run(httpx_command, capture_output=True, text=True)

        if httpx_result.returncode != 0:
            print(f"[✗] httpx error: {httpx_result.stderr}")
            return set()

        live_subdomains = set(httpx_result.stdout.strip().splitlines())

        # Extract URLs and write to output file
        urls = set()
        for line in live_subdomains:
            match = re.match(r'^(https?://[^ ]+)', line)
            if match:
                urls.add(match.group(1))

        # Write live URLs to the specified output file
        with open(output_file, "w") as f:
            f.write("\n".join(urls))

        return live_subdomains

    except Exception as e:
        print(f"[✗] Error in filtering live subdomains: {e}")
        return set()

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Function to save subdomains to a file and database
def save_subdomains_to_file_and_db(subdomains, file_path, db_file):
    """Save subdomains to a file and SQLite database."""
    try:
        # Save to file
        with open(file_path, 'w') as f:
            f.write("\n".join(sorted(subdomains)))
        print(f"[✓] Subdomains saved to {file_path}")

        # Save to database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS subdomains (domain TEXT)")
        cursor.executemany("INSERT INTO subdomains (domain) VALUES (?)", [(subdomain,) for subdomain in subdomains])
        conn.commit()
        conn.close()
        print(f"[✓] Subdomains saved to database {db_file}")
    except Exception as e:
        print(f"[✗] Error saving subdomains: {e}")

# Main function to run the tool for each program
def main():
    programs = load_program_config()

    for program in programs:
        domain = program["domain"]
        subdomains_file = program["subdomains_file"]
        db_file = program["db_file"]
        discord_webhook = program["discord_webhook"]

        # Create directory for each domain (e.g., 'nyc_scan')
        directory = create_directory(domain)

        # Update file paths to be inside the domain-specific directory
        subdomains_file_path = os.path.join(directory, subdomains_file)
        db_file_path = os.path.join(directory, db_file)

        # Run subdomain discovery tools
        tools = program.get("tools", ["subfinder", "assetfinder", "sublist3r", "findomain"])
        print(f"[*] Discovering subdomains for {domain}...")
        subdomains = run_subdomain_discovery(domain, tools)

        # Save discovered subdomains to file and DB
        save_subdomains_to_file_and_db(subdomains, subdomains_file_path, db_file_path)

        # Check for live subdomains
        print(f"[*] Checking live subdomains for {domain}...")
        live_subdomains = filter_httpx(subdomains, os.path.join(directory, "live_" + subdomains_file))

        # Send notification with live subdomains file
        if live_subdomains:
            send_notify_notification(discord_webhook, os.path.join(directory, "live_" + subdomains_file))

if __name__ == "__main__":
    main()
