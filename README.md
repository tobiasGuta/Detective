# Detective

## Overview:
This tool is designed to monitor the targets of your bug bounty programs, For example, it will alert you if new domains appear. It does this by running scans on the domains you specify, comparing them with those stored in the database. If a new domain is found, it will notify you and send you an alert.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9650e31a-5fec-49f6-b856-4276471bfe9b" width="400"/>
</p>

# Running the Script Automatically with a Cron Job
To have the script run automatically at scheduled intervals, you can set up a cron job. This is ideal for running the script regularly without manual intervention.

## Create a Discord Webhook:

To receive the messages in Discord, you need to create a webhook for your Discord server/channel:

Go to your Discord server and navigate to the channel settings.

Under the Integrations tab, create a Webhook.

Copy the Webhook URL and replace https://discord.com/api/webhooks/xxxxx with your actual webhook URL in the cron job command.

# Example

Program : nyc.gov

![Screenshot 2025-04-26 073918](https://github.com/user-attachments/assets/13b4eb10-e170-4c0b-92cc-d8f222985fba)
