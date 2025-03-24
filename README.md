# Detective

![image](https://github.com/user-attachments/assets/baa2e5ec-18f1-4d6c-859b-56208836dc05)

## Overview:
This tool is designed to monitor the targets of your bug bounty programs, For example, it will alert you if new domains appear. It does this by running scans on the domains you specify, comparing them with those stored in the database. If a new domain is found, it will notify you and send you an alert.


```
+------------------------+       +-------------------+       +------------------------+   no    +-----------------------+
|  Subdomain Enumeration | --->  |  Detection Tool   | <---> |     Database Check     |  --->   |     No Notification   |
+------------------------+       +-------------------+       +------------------------+         +-----------------------+
                                                                         |
                                                           New SubDomain | Yes?
                                                                         v
                                                           +-------------------------------+
                                                           |  Send Notification to Discord |
                                                           +-------------------------------+
                                                                           |
                                                                           v
                                                              +--------------------------+
                                                              |       Discord Bot        |
                                                              +--------------------------+

```
# Running the Script Automatically with a Cron Job
To have the script run automatically at scheduled intervals, you can set up a cron job. This is ideal for running the script regularly without manual intervention.

## Edit the crontab file:

Open the crontab configuration by running the following command:
```bash
*/30 * * * * PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/home/user/go/bin /usr/bin/python3 /home/user/Desktop/Detective/detective.py > /home/user/Desktop/Detective/cron_output.log 2>&1
```
## Explanation:
*/30 * * * *:

This part specifies the schedule for the cron job. It means "run every 30 minutes."

## The five fields in a cron job represent:
```
(1) Minute (0-59) 
(2) Hour (0-23) 
(3) Day of the month (1-31) 
(4) Month (1-12) 
(5) Day of the week (0-6, where 0 is Sunday)
```

*/30 in the minute field means "every 30 minutes."

So this cron job runs at 00, 30 minutes of every hour, every day.
```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/home/user/go/bin:
```
This part sets the environment variable PATH to specify the directories where the system should look for executable files.

When cron jobs are run, they don’t always have the same environment variables as a normal user session. So, you explicitly set the PATH here to make sure all the necessary executables are found by the script.

For example, it includes directories like /usr/local/bin (common for system binaries) and /home/user/go/bin (specific to Go-related binaries).
```
/usr/bin/python3 /home/user/Desktop/Detective/detective.py:
```
This part runs the script itself. It calls Python 3 to execute the script detective.py located at /home/user/Desktop/Detective/detective.py.

The path to python3 is /usr/bin/python3, which ensures that the correct version of Python is used to execute the script.
```
> /home/user/Desktop/Detective/cron_output.log:
```
This redirects the standard output (stdout) of the script to a log file.

Any output generated by the script (like print statements or regular output) will be saved in the file cron_output.log located in /home/user/Desktop/Detective/.

This allows you to check the log file to see what the script has outputted during execution.
```
2>&1:
```
This part redirects standard error (stderr) to the same place as standard output (stdout).

2 refers to the file descriptor for stderr.

>&1 means redirect the error output to wherever stdout is going (in this case, to cron_output.log).

This ensures that both regular output and any error messages are logged in the same file.

# Extra

## Monitoring Cron Job Output with Discord Notifications
If you want to keep an eye on whether your cron job is running as expected, you can create a Discord bot that sends the latest output from the cron job (cron_output.log) to a Discord channel. This allows you to get real-time notifications of the script's output without having to manually check the log file.

## How to Set It Up
You can update your cron job to not only execute the script but also send the last few lines of the log file to Discord. Here’s how you can modify your cron job:

Modify your existing cron job to include a curl command that sends the output to Discord. Use the following cron job command:
```
*/30 * * * * PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/home/user/go/bin /usr/bin/python3 /home/user/Desktop/Detective/detective.py > /home/user/Desktop/Detective/cron_output.log 2>&1 ; curl -X POST -H "Content-Type: application/json" -d "{\"content\": \"$(tail -n 17 /home/user/Desktop/Detective/cron_output.log | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/\\n/\\n/g')\"}" "https://discord.com/api/webhooks/xxxxx"
```
## Explanation of the cron job command:

*/30 * * * *: Runs every 30 minutes.

PATH=...: Ensures all the required directories for executables are in the environment.

/usr/bin/python3 /home/user/Desktop/Detective/detective.py > /home/user/Desktop/Detective/cron_output.log 2>&1: Executes your script and logs both stdout and stderr to cron_output.log.

curl -X POST ...: Sends the last 17 lines of cron_output.log to a Discord webhook. Here's a breakdown of the curl command:

tail -n 17 /home/user/Desktop/Detective/cron_output.log: Retrieves the last 17 lines of the log.

sed 's/"/\\"/g': Escapes any quotes to ensure valid JSON.

tr '\n' ' ': Converts newlines into spaces, ensuring the output is in a single line.

sed 's/\\n/\\n/g': Ensures that newlines are properly formatted in the output string.

"https://discord.com/api/webhooks/xxxxx": This is where you put your actual Discord webhook URL.

## Create a Discord Webhook:

To receive the messages in Discord, you need to create a webhook for your Discord server/channel:

Go to your Discord server and navigate to the channel settings.

Under the Integrations tab, create a Webhook.

Copy the Webhook URL and replace https://discord.com/api/webhooks/xxxxx with your actual webhook URL in the cron job command.

