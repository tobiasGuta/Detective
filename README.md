# Detective

![image](https://github.com/user-attachments/assets/baa2e5ec-18f1-4d6c-859b-56208836dc05)

## Overview:
This tool is designed to manage subdomains discovered from a file, store them in a local txt file, and notify a specified service (like Discord) about new subdomains. It does so by comparing subdomains in the input file with the ones stored in the database and sends notifications if new subdomains are found.


```
+------------------------+       +-------------------+       +------------------------+       +-----------------------+
|  Subdomain Enumeration | ---> |   Detection Tool  | --->   |     Database Check     |  ---> |     New Subdomain?    |
+------------------------+       +-------------------+       +------------------------+       +-----------------------+
                                                                         | Yes
                                                                         +v
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

Edit the crontab file:

Open the crontab configuration by running the following command:
```bash
*/30 * * * * PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/home/user/go/bin /usr/bin/python3 /home/user/Desktop/Detective/detective.py > /home/user/Desktop/Detective/cron_output.log 2>&1
```
