import os
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor

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
    """Create a directory for the domain (e.g., 'nyc_scan')"""
    directory = f"{domain}_scan"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

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

# Main function to run the tool for each program
def main():
    programs = load_program_config()

    for program in programs:
        domain = program["domain"]
        discord_webhook = program["discord_webhook"]

        # Create directory for each domain (e.g., 'nyc_scan')
        directory = create_directory(domain)

        subdomains_file_path = os.path.join(directory, "subdomains.txt")
        subdomains_txt_file_path = os.path.join(directory, "databases.txt")

        # Run subdomain discovery tools
        tools = program.get("tools", ["subfinder", "assetfinder", "sublist3r", "findomain"])
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
                send_notify_notification(discord_webhook, temp_file)
                
                # Clean up the temporary file after sending the notification
                os.remove(temp_file)

            print(f"[✓] New live subdomains saved and notification sent.")
        else:
            print("[✓] No new live subdomains, skipping notification.")

if __name__ == "__main__":
    main()
