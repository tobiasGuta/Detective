import os
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

# List of required tools
required_tools = ["go", "subfinder", "assetfinder", "sublist3r", "httpx"]

# Check each tool and print its status
missing_tools = []

# If Go is missing, ask user before installing
if "go" in missing_tools:
    install_go()
    missing_tools.remove("go") 

if "sublist3r" in missing_tools:
    install_sublist3r()
    missing_tools.remove("sublist3r") 

if "assetfinder" in missing_tools:
    install_assetfinder()
    missing_tools.remove("assetfinder")

if "subfinder" in missing_tools:
    install_subfinder()
    missing_tools.remove("subfinder")

if "httpx" in missing_tools:
    install_httpx()
    missing_tools.remove("httpx")

art = """
                                     @@@@@@@                               
                                   @@       @                              
                                 @         @@@                             
                             @@@@@     @@@  @@                             
                            @@    @@@@@@@@@@                               
                         @@@@@@@@@@@@       @  @@                          
                             @@@@    @@@     @@  @                         
                           @@ @ @@@   @@  @@     @                         
              @@@@@      @@   @@    @@@ @@       @                         
             @@  @@@    @@      @@@@    @        @                         
             @@    @@@ @@                @      @@                         
             @@@ @@ @@@ @       @@@@     @      @@                         
              @@@   @@@  @@@@@@ @@@      @@     @                          
               @@@@  @@         @ @@      @@    @                          
                 @@@@@          @  @@@  @@@@    @@@@@                      
                      @@        @       @@    @@@@@ @                      
                      @@@        @@     @@     @@@ @@ @@                   
                       @@@@@@      @@@@@@@      @    @@  @@                
                      @  @  @@@@@@     @    @@@@@ @@@ @@@                  
                        @@@@@ @  @   @@ @@@@    @@    @@                   
                          @@@@     @@  @   @        @@                     
                                       @  @@@@@@  @@@@                     
                               @@@     @ @@@    @@@ @@@                    
                               @@@@     @@@          @@@@                  
                                 @@@@@ @@@            @@@@                 
                                  @@@@@@@@              @@@@               
                                    @@@@@@      @@@@@@@@@@@@@@             
"""

print(art)

# Install tools

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
        with open(os.path.expanduser("~/.bashrc"), "a") as file:
            file.write('\nexport PATH=$PATH:/usr/local/go/bin\n')
            file.write('\nexport PATH=$PATH:$HOME/go/bin\n')
        print("[✓] Go path added to ~/.bashrc")

        # Apply changes
        print("[!] Restart your terminal or run `source ~/.bashrc` to apply the changes.")
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

# Function to check live subdomains using httpx
def filter_httpx(subdomains, output_file):
    """Check live subdomains with httpx and store only URLs in the database."""
    try:
        temp_file_path = "temp_subdomains.txt"
        # Save subdomains to temporary file
        with open(temp_file_path, "w") as f:
            f.write("\n".join(subdomains))
        
        # Run httpx to check live subdomains
        httpx_command = [
            "httpx", "-silent", "-l", temp_file_path
        ]
        httpx_result = subprocess.run(httpx_command, capture_output=True, text=True)

        if httpx_result.returncode != 0:
            print(f"[✗] httpx error: {httpx_result.stderr}")
            return set()

        live_subdomains = set(httpx_result.stdout.strip().splitlines())

        # Save live URLs only (remove extra data like status codes, headers, etc.)
        with open(output_file, "w") as f:
            f.write("\n".join(live_subdomains))

        return live_subdomains

    except Exception as e:
        print(f"[✗] Error in filtering live subdomains: {e}")
        return set()

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# Function to create directory for the target domain
def create_directory(domain):
    """Create a directory for the domain"""
    directory = f"{domain}_scan"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# Load program configuration from JSON file
def load_program_config(config_path='/home/kali/Desktop/detective/programs_config.json'):
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
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[✗] Error running {tool}: {result.stderr}")
        return set()

    return set(result.stdout.strip().splitlines())

# Function to load existing subdomains from a .txt file
def load_existing_subdomains_from_txt(file_path):
    """Load existing subdomains from a .txt file."""
    existing_subdomains = set()

    try:
        with open(file_path, 'r') as f:
            existing_subdomains = set(f.read().splitlines())
        print(f"[✓] Loaded {len(existing_subdomains)} existing subdomains from {file_path}")
    except FileNotFoundError:
        print(f"[✗] File {file_path} not found. Starting with an empty list.")
    except Exception as e:
        print(f"[✗] Error loading subdomains from file: {e}")

    return existing_subdomains

# Function to save all discovered subdomains to a file
def save_subdomains_to_txt(live_subdomains, file_path):
    """Save live subdomains to a .txt file."""
    try:
        with open(file_path, 'a') as f:
            for subdomain in live_subdomains:
                f.write(subdomain + "\n")
        print(f"[✓] Live subdomains saved to {file_path}")
    except Exception as e:
        print(f"[✗] Error saving live subdomains to file: {e}")

# Function to send bulk notification using Project Discovery's notify
def send_notify_notification(discord_webhook, file_path, domain):
    """Send bulk notification using the 'notify' tool from Project Discovery."""
    try:
        # Assuming 'discord.yaml' is correctly configured and exists
        result = subprocess.run(
            ["notify", "-provider-config", "/home/kali/Desktop/detective/discord.yaml", "-id", domain, "-data", file_path, "-bulk"], 
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[✓] Notification sent successfully for {domain}!")
        else:
            print(f"[✗] Error sending notification for {domain}: {result.stderr}")
    except Exception as e:
        print(f"[✗] Failed to execute 'notify' command for {domain}: {e}")

# Main function to run the tool for each program
def main():

    if missing_tools:
        print(f"\n[!] Missing tools: {', '.join(missing_tools)}")
    else:
        print("\n[✓] All required tools are installed.")

    programs = load_program_config()

    for program in programs:
        domain = program["domain"]
        discord_webhook = program["discord_webhook"]

        # Create directory for each domain (e.g., 'nyc_scan')
        directory = create_directory(domain)

        subdomains_file_path = os.path.join(directory, "subdomains.txt")
        subdomains_txt_file_path = os.path.join(directory, "databases.txt")

        # Run subdomain discovery tools
        tools = program.get("tools", ["subfinder", "assetfinder", "sublist3r"])
        print(f"[*] Discovering subdomains for {domain}...")
        subdomains = run_subdomain_discovery(domain, tools)

        # Save discovered subdomains to file
        save_subdomains_to_txt(subdomains, subdomains_file_path)

        # Check for live subdomains
        print(f"[*] Checking live subdomains for {domain}...")
        live_subdomains = filter_httpx(subdomains, os.path.join(directory, "live_subdomains.txt"))

        # Load existing subdomains from the .txt file
        existing_subdomains = load_existing_subdomains_from_txt(subdomains_txt_file_path)

        # Filter out already existing subdomains
        new_live_subdomains = [subdomain for subdomain in live_subdomains if subdomain not in existing_subdomains]

        # Debugging: Print the new live subdomains
        print(f"[DEBUG] New live subdomains: {new_live_subdomains}")

        # Save new live subdomains to the .txt file if any
        if new_live_subdomains:
            save_subdomains_to_txt(new_live_subdomains, subdomains_txt_file_path)

            # Send notification with new live subdomains
            
            if new_live_subdomains:
                temp_file = "new_live_subdomains.txt"
                with open(temp_file, 'w') as f:
                    for subdomain in new_live_subdomains:
                        f.write(subdomain + "\n")
                
                # Send notification with the new live subdomains file
                send_notify_notification(discord_webhook, temp_file, domain)
                
                # Clean up the temporary file after sending the notification
                os.remove(temp_file)

            print(f"[✓] New live subdomains saved and notification sent.")
        else:
            print("[✓] No new live subdomains, skipping notification.")

if __name__ == "__main__":
    main()
