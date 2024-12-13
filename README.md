# TestSSH
# SSH Status Check Script

## Purpose
This script allows users to check the SSH connectivity status of one or more IP addresses. It provides detailed feedback on the status of each connection, such as successful login, permission denial, port closure, or timeout. The script supports both password-based and key-based authentication.

---

## Features
- **Interactive Input**: Accepts either a single IP address or a file containing multiple IP addresses.
- **Flexible Authentication**: Supports both password and key file-based authentication.
- **Detailed Connection Status**: Provides descriptive output for each IP connection attempt.

---

## How to Download
1. Clone this repository or download the script file directly:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Ensure the script file (`check_ssh.sh`) has execute permissions:
   ```bash
   chmod +x check_ssh.sh
   ```

---

## How to Use
1. Run the script:
   ```bash
   ./check_ssh.sh
   ```
2. The script will prompt for the following inputs:
   - **IP Address or File Path**: Provide a single IP (e.g., `192.168.1.1`) or a path to a text file (e.g., `IP.txt`) containing a list of IP addresses.
   - **Authentication Method**: Choose between `password` or `key` for authentication.
     - For `password`, enter the SSH password when prompted.
     - For `key`, provide the path to the SSH key file.
   - **Username**: Enter the SSH username to be used for connection.
3. The script will then attempt to connect to each IP and display the status:
   - **Example Output**:
     ```
     192.168.1.1 - SSH Log in Successful
     192.168.1.2 - SSH Port Closed
     192.168.1.3 - Permission Denied or Connection Timeout
     ```

---

## Input File Format
When providing a file of IP addresses (e.g., `IP.txt`), ensure each IP address is on a new line:
```
192.168.1.1
192.168.1.2
192.168.1.3
```

---

## Requirements
- `sshpass` (for password-based authentication)
- `ssh` command available on the system

---

## Notes
- Ensure your IPs and authentication details are accurate.
- For key-based authentication, the private key file must have the appropriate permissions (e.g., `chmod 600 <key_file>`).
- This script is designed for testing and monitoring purposes; handle credentials securely.

---

## Disclaimer
Use this script responsibly. Unauthorized access to systems is illegal and unethical.

