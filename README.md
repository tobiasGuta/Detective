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
