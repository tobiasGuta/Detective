# Detective

![image](https://github.com/user-attachments/assets/baa2e5ec-18f1-4d6c-859b-56208836dc05)

## Overview:
This tool is designed to manage subdomains discovered from a file, store them in a local SQLite database, and notify a specified service (like Discord) about new subdomains. It does so by comparing subdomains in the input file with the ones stored in the database and sends notifications if new subdomains are found.

## Detailed Explanation:
Initialization (init_db function):

The init_db() function sets up an SQLite database (subdomains.db) with a table to store subdomains. If the table already exists, it doesn’t create a new one.

## The table has two fields:

id: A unique identifier for each subdomain (auto-incremented).

subdomain: The actual subdomain as a string, which must be unique.

## Reading Subdomains from File (read_subdomains_file function):

The function attempts to read subdomains from a file called subdomains.txt.

It returns a set of subdomains (using {} for uniqueness), and any empty or whitespace-only lines are discarded.

If the file isn't found, it prints an error message.

## Fetching Existing Subdomains (get_existing_subdomains function):

This function fetches and returns all subdomains already stored in the database (subdomains.db).

It performs a SELECT query to get all the subdomains and stores them in a set for easy comparison.

## Saving New Subdomains to File (save_subdomains_to_file function):

Any new subdomains discovered (those not already in the database) are saved to a new file (h1.txt).

It writes each subdomain from the set to the file, with each on a new line.

If there’s an issue while writing to the file, an error message is displayed.

## Sending Bulk Notifications (send_notify_notification function):

Once new subdomains are detected, the tool triggers the notify command from Project Discovery, which is used for sending bulk notifications.

It uses the h1.txt file (which contains the new subdomains) and a configuration file (discord.yaml) to send the notification to Discord.

If successful, it prints a success message; otherwise, it shows an error message.

## Adding New Subdomains to Database (add_new_subdomains function):

After new subdomains are saved to a file and the notification is sent, these subdomains are added to the database to ensure they aren't processed again.

The function uses the INSERT OR IGNORE SQL command to avoid adding duplicates.

## Main Function (main function):

## The main function orchestrates the entire process:

It initializes the database.

Reads subdomains from the file.

Compares the read subdomains with those already in the database.

If new subdomains are found, they’re saved to a file, notifications are sent, and the database is updated.

If no new subdomains are found, a message is printed indicating this.

# How to Use:
## Prerequisites:

You need Python installed along with the sqlite3 library (which is standard in Python).

The notify command should be in your system's PATH.

A subdomains.txt file containing discovered subdomains.

A discord.yaml file with the necessary configuration for sending notifications via Discord (Project Discovery's notify).

## Running the Tool:

Simply run the script by executing python script_name.py.

It will automatically handle the rest, processing the subdomains, comparing them with the database, and sending notifications if new subdomains are found.

## Use Case:
This tool could be useful for cybersecurity professionals or penetration testers who are tracking subdomains of a target domain. It automates the process of detecting new subdomains, notifying relevant parties, and keeping the database of discovered subdomains updated.
