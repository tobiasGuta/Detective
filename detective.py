import sqlite3
import subprocess

db_path = "subdomains.db"
notify_command = "notify"  # Assuming 'notify' is in the system path

# Initialize the database
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subdomains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subdomain TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

# Read subdomains from file
def read_subdomains_file():
    try:
        with open("subdomains.txt", "r") as file:
            return {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print("[✗] subdomains.txt not found!")
        return set()

# Get existing subdomains from the database
def get_existing_subdomains():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT subdomain FROM subdomains")
    existing = {row[0] for row in cursor.fetchall()}
    conn.close()
    return existing

# Save new subdomains to a file (h1.txt)
def save_subdomains_to_file(subdomains):
    try:
        with open("h1.txt", "w") as file:
            for sub in subdomains:
                file.write(sub + "\n")
        print("[✓] Subdomains saved to h1.txt")
    except Exception as e:
        print(f"[✗] Failed to write to h1.txt: {e}")

# Send bulk notification using Project Discovery's Notify
def send_notify_notification():
    try:
        # Execute the notify command with the bulk flag
        result = subprocess.run([notify_command, "-provider-config", "discord.yaml", "-data", "h1.txt", "-bulk"], capture_output=True, text=True)

        if result.returncode == 0:
            print("[✓] Notification sent successfully!")
        else:
            print(f"[✗] Error sending notification: {result.stderr}")
    except Exception as e:
        print(f"[✗] Failed to execute 'notify' command: {e}")

# Add new subdomains to the database
def add_new_subdomains(new_subdomains):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for sub in new_subdomains:
        cursor.execute("INSERT OR IGNORE INTO subdomains (subdomain) VALUES (?)", (sub,))
    conn.commit()
    conn.close()

def main():
    init_db()
    discovered_subdomains = read_subdomains_file()
    existing_subdomains = get_existing_subdomains()
    
    new_subdomains = discovered_subdomains - existing_subdomains
    
    if new_subdomains:
        save_subdomains_to_file(new_subdomains)
        send_notify_notification()
        print(f"[🆕] {len(new_subdomains)} new subdomains detected!")
        add_new_subdomains(new_subdomains)
    else:
        print("[✓] No new subdomains found.")

if __name__ == "__main__":
    main()
