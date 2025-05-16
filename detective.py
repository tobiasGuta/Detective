import os
import subprocess
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import re

# List of required tools
required_tools = ["go", "subfinder", "assetfinder", "httpx", "gowitness", "naabu"]

missing_tools = []

def check_tool_availability(tool):
    result = subprocess.run(["which", tool], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None

# Install functions (I'll leave these short, assume you already have the longer versions in your project)
def install_go():
    # Install Go if needed
    pass

def install_sublist3r():
    # Install sublist3r if needed
    pass

def install_assetfinder():
    # Install assetfinder if needed
    pass

def install_subfinder():
    # Install subfinder if needed
    pass

def install_httpx():
    # Install httpx if needed
    pass

def install_gowitness():
    # Install gowitness if needed
    pass

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
        with open(os.path.expanduser("~/.bashrc"), "a") as file:
            file.write('\nexport PATH=$PATH:/usr/local/go/bin\n')
            file.write('\nexport PATH=$PATH:$HOME/go/bin\n')
        print("[✓] Go path added to ~/.bashrc")

        # Apply changes
        print("[!] Restart your terminal or run `source ~/.bashrc` to apply the changes.")
        print("[✓] Go installation completed successfully!")

    except Exception as e:
        print(f"[✗] Failed to install Go: {e}")

def install_naabu():
    print(f"\n[!] naabu is missing.")
    user_choice = input("[?] Do you want to install naabu using Go? (yes/no): ").strip().lower()
    if user_choice == "yes":
        try:
            print("[!] Installing naabu...")
            subprocess.run(["go", "install", "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"], check=True)
            print("[✓] naabu installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing naabu: {e}")
    else:
        print("[✗] Skipping naabu installation.")

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

            # Install pip3
            subprocess.run(["sudo" ,"apt" ,"install" ,"python3-pip" ,"-y"], check=True)
            print("[✓] Dependencies installed successfully.")

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

def install_gowitness():
    print(f"\n[!] gowitness is missing.")
    user_choice = input("[?] Do you want to install gowitness using Go? (yes/no): ").strip().lower()

    if user_choice == "yes":
        try:
            print("[!] Installing gowitness...")
            subprocess.run(["go", "install", "github.com/sensepost/gowitness@latest"], check=True)
            print("[✓] gowitness installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[✗] Error installing gowitness: {e}")
    else:
        print("[✗] Skipping gowitness installation.")

def clean_screenshot_folder():
    screenshot_folder = "screenshots"
    if os.path.exists(screenshot_folder):
        for file in os.listdir(screenshot_folder):
            file_path = os.path.join(screenshot_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

def take_screenshot(subdomain):
    try:
        output_dir = "screenshots"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        url = subdomain if subdomain.startswith("http") else f"https://{subdomain}"
        command = f"echo '{url}' | gowitness scan file -f - --screenshot-path {output_dir} --screenshot-format png"
        subprocess.run(command, shell=True, check=True)

        image_files = [f for f in os.listdir(output_dir) if f.endswith('.png') or f.endswith('.jpeg')]
        if image_files:
            image_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)))
            screenshot_path = os.path.join(output_dir, image_files[-1])
            return screenshot_path
        else:
            return None
    except Exception as e:
        print(f"[\u2717] Failed to take screenshot of {subdomain}: {e}")
        return None

def send_subdomain_with_screenshot_to_discord(webhook_url, domain, subdomain, screenshot_path, tech_info="Unknown", ports="Unknown"):
    try:
        with open(screenshot_path, 'rb') as f:
            files = {
                'file': (os.path.basename(screenshot_path), f)
            }
            data = {
                "content": (
                    f"**Program:** `{domain}`\n"
                    f"**Subdomain:** {subdomain}\n"
                    f"**Tech Stack:** `{tech_info}`\n"
                    f"**Open Ports:** `{ports}`"
                )
            }
            response = requests.post(webhook_url, data=data, files=files)

        if response.status_code == 204:
            os.remove(screenshot_path)
            print(f"[✓] Sent {subdomain} to Discord and deleted screenshot.")
        else:
            print(f"[✗] Failed to send {subdomain} to Discord. Status code: {response.status_code}, response: {response.text}")

    except Exception as e:
        print(f"[✗] Exception while sending {subdomain} to Discord: {e}")


def create_directory(domain):
    directory = f"{domain}_scan"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def load_program_config(config_path='config/programs_config.json'):
    with open(config_path, 'r') as f:
        return json.load(f)["programs"]

def run_tool(tool, domain):
    if tool == "subfinder":
        command = ["subfinder", "-silent", "-d", domain]
    elif tool == "assetfinder":
        command = ["assetfinder", "--subs-only", domain]
    else:
        return set()
    result = subprocess.run(command, capture_output=True, text=True)
    return set(result.stdout.strip().splitlines()) if result.returncode == 0 else set()

def run_subdomain_discovery(domain, tools):
    all_subdomains = set()
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda tool: run_tool(tool, domain), tools)
    for result in results:
        if result:
            all_subdomains.update(result)
    return all_subdomains

def filter_httpx(subdomains, output_file):
    tech_map = {}
    try:
        temp_file_path = "temp_subdomains.txt"
        with open(temp_file_path, "w") as f:
            f.write("\n".join(subdomains))

        httpx_command = ["httpx", "-silent", "-l", temp_file_path, "-tech-detect", "-json"]
        httpx_result = subprocess.run(httpx_command, capture_output=True, text=True)

        live_subdomains = set()
        for line in httpx_result.stdout.strip().splitlines():
            try:
                data = json.loads(line)
                url = data.get("url")
                tech = ", ".join(data.get("tech", [])) if data.get("tech") else "Unknown"
                if url:
                    live_subdomains.add(url)
                    tech_map[url] = tech
            except json.JSONDecodeError:
                continue

        with open(output_file, "w") as f:
            f.write("\n".join(live_subdomains))

        return live_subdomains, tech_map
    finally:
        if os.path.exists("temp_subdomains.txt"):
            os.remove("temp_subdomains.txt")

def scan_ports_with_naabu(subdomain):
    try:
        domain_only = subdomain.replace("http://", "").replace("https://", "").split("/")[0]

        # Step 1: Run Naabu and collect ports
        naabu_cmd = ["naabu", "-host", domain_only, "-ports", "top-1000", "-json"]
        naabu_result = subprocess.run(naabu_cmd, capture_output=True, text=True)
        if naabu_result.returncode != 0:
            return "Naabu error"

        ports = set()
        for line in naabu_result.stdout.strip().splitlines():
            try:
                data = json.loads(line)
                ports.add(str(data["port"]))
            except json.JSONDecodeError:
                continue

        if not ports:
            return "None"

        # Step 2: Run Nmap for detailed service detection
        port_list = ",".join(sorted(ports))
        nmap_cmd = ["nmap", "-sV", "-p", port_list, domain_only]
        nmap_result = subprocess.run(nmap_cmd, capture_output=True, text=True)
        if nmap_result.returncode != 0:
            return f"Ports: {port_list} (Nmap error)"

        # Step 3: Extract results
        service_info = []
        for line in nmap_result.stdout.splitlines():
            if "/tcp" in line and "open" in line:
                parts = line.split()
                port_proto = parts[0]
                service = parts[2] if len(parts) > 2 else "unknown"
                version = " ".join(parts[3:]) if len(parts) > 3 else "unknown"
                service_info.append(f"{port_proto} → {service} ({version})")

        return "\n".join(service_info) if service_info else f"Ports: {port_list} (No version info)"

    except Exception as e:
        return f"Exception: {e}"



def load_existing_subdomains_from_txt(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_subdomains_to_txt(subdomains, file_path):
    with open(file_path, 'a') as f:
        for subdomain in subdomains:
            f.write(subdomain + "\n")

def main():
    clean_screenshot_folder()

    # Check if tools are installed
    for tool in required_tools:
        tool_path = check_tool_availability(tool)
        if tool_path:
            print(f"[✓] {tool} is installed at {tool_path}.")
        else:
            print(f"[✗] {tool} is missing.")
            missing_tools.append(tool)

    if missing_tools:
        print(f"\n[!] Missing tools: {', '.join(missing_tools)}")
        for tool in missing_tools:
            user_choice = input(f"[?] {tool} is missing. Do you want to install {tool}? (yes/no): ").strip().lower()
            if user_choice == "yes":
                if tool == "go":
                    install_go()
                elif tool == "subfinder":
                    install_subfinder()
                elif tool == "assetfinder":
                    install_assetfinder()
                elif tool == "sublist3r":
                    install_sublist3r()
                elif tool == "httpx":
                    install_httpx()
                elif tool == "gowitness":
                    install_gowitness()
                elif tool == "naabu":
                    install_naabu()
                else:
                    print(f"[✗] No installer function available for {tool}.")
            else:
                print(f"[!] Skipping installation for {tool}.")

        print("\n[*] Installation step finished. Please re-run the script to continue.")
        exit(0)
    else:
        print("\n[✓] All required tools are installed. Continuing...\n")

    programs = load_program_config()

    for program in programs:
        domain = program["domain"]
        discord_webhook = program["discord_webhook"]

        directory = create_directory(domain)

        subdomains_file_path = os.path.join(directory, "subdomains.txt")
        subdomains_txt_file_path = os.path.join(directory, "databases.txt")

        # Discover subdomains
        tools = program.get("tools", ["subfinder", "assetfinder"])
        print(f"[*] Discovering subdomains for {domain}...")
        subdomains = run_subdomain_discovery(domain, tools)

        save_subdomains_to_txt(subdomains, subdomains_file_path)

        # Filter live subdomains and extract tech
        print(f"[*] Checking live subdomains for {domain}...")
        live_subdomains, tech_map = filter_httpx(subdomains, os.path.join(directory, "live_subdomains.txt"))

        # Load existing subdomains database
        existing_subdomains = load_existing_subdomains_from_txt(subdomains_txt_file_path)

        # Find only new ones
        new_live_subdomains = [subdomain for subdomain in live_subdomains if subdomain not in existing_subdomains]

        print(f"[DEBUG] New live subdomains: {new_live_subdomains}")

        if new_live_subdomains:
            save_subdomains_to_txt(new_live_subdomains, subdomains_txt_file_path)

            for subdomain in new_live_subdomains:
                print(f"[*] Taking screenshot of {subdomain}...")
                screenshot_path = take_screenshot(subdomain)
                if screenshot_path:
                    tech_info = tech_map.get(subdomain, "Unknown")
                    print(f"[*] Scanning ports with Naabu for {subdomain}...")
                    ports = scan_ports_with_naabu(subdomain)

                    print(f"[*] Sending {subdomain} with screenshot, tech stack, and ports to Discord...")
                    send_subdomain_with_screenshot_to_discord(
                        webhook_url=discord_webhook,
                        domain=domain,
                        subdomain=subdomain,
                        screenshot_path=screenshot_path,
                        tech_info=tech_info,
                        ports=ports
                    )
                else:
                    print(f"[✗] Failed to screenshot {subdomain}, skipping sending.")

            print(f"[✓] All new live subdomains processed and sent with screenshots.")
        else:
            print("[✓] No new live subdomains, skipping notification.")

if __name__ == "__main__":
    main()
