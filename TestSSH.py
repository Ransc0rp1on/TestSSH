import paramiko
import socket
import getpass
import os

def get_ips(input_arg):
    ips = []
    if input_arg.endswith('.txt'):
        try:
            with open(input_arg, 'r') as f:
                ips = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {input_arg} not found.")
            exit(1)
    else:
        ips = [input_arg]
    return ips

def main():
    input_arg = input("Enter IP address or path to IPs.txt file: ").strip()
    ips = get_ips(input_arg)
    if not ips:
        print("No IP addresses provided. Exiting.")
        exit(1)

    auth_method = input("Is it key-based or username/password authentication? (key/password): ").strip().lower()
    if auth_method not in ['key', 'password']:
        print("Invalid authentication method. Exiting.")
        exit(1)

    username = input("Enter SSH username: ").strip()
    private_key = None
    password = None

    if auth_method == 'key':
        key_path = input("Enter the path to the private key file: ").strip()
        if not os.path.isfile(key_path):
            print(f"Error: Private key file {key_path} not found.")
            exit(1)
        passphrase = None
        has_passphrase = input("Does the private key have a passphrase? (yes/no): ").strip().lower()
        if has_passphrase == 'yes':
            passphrase = getpass.getpass("Enter the passphrase for the private key: ")
        try:
            private_key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
        except paramiko.ssh_exception.PasswordRequiredException:
            print("Error: Private key requires a passphrase.")
            exit(1)
        except Exception as e:
            print(f"Error loading private key: {e}")
            exit(1)
    else:
        password = getpass.getpass("Enter SSH password: ")

    success_count = 0

    print("\nChecking SSH connectivity...")
    for ip in ips:
        print(f"\nAttempting connection to {ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if auth_method == 'key':
                ssh.connect(hostname=ip, port=22, username=username, pkey=private_key, timeout=10)
            else:
                ssh.connect(hostname=ip, port=22, username=username, password=password, timeout=10)
            print(f"Success: Logged into {ip}")
            success_count += 1
            ssh.close()
        except socket.timeout:
            print(f"Error: Connection to {ip} timed out.")
        except socket.error as e:
            if e.errno == 111:
                print(f"Error: Port 22 is closed on {ip}.")
            elif e.errno == 113:
                print(f"Error: IP {ip} is not reachable.")
            else:
                print(f"Socket error occurred: {e}")
        except paramiko.AuthenticationException:
            print(f"Error: Authentication failed for {ip}.")
        except paramiko.SSHException as e:
            print(f"SSH error occurred on {ip}: {e}")
        except Exception as e:
            print(f"Unexpected error connecting to {ip}: {e}")
        finally:
            try:
                ssh.close()
            except:
                pass

    print(f"\nSummary: Successful logins: {success_count}/{len(ips)}")

if __name__ == "__main__":
    main()
