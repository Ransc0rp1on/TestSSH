#!/bin/bash

cat << "EOF"
 _ __ __ _ _ __  ___  ___ / _ \ _ __ _ __ / | ___  _ _ 
| '__/ _` | '_ \/ __|/ __| | | | '__| '_ \| |/ _ \| '_ \
| | | (_| | | | \__ \ (__| |_| | |  | |_) | | (_) | | | |
|_|  \__,_|_| |_|___/\___|\___/|_|  | .__/|_|\___/|_| |_|
                                    |_|                  
EOF
# Function to check SSH connection
check_ssh_connection() {
    local ip=$1
    sshpass -p "$PWD" ssh -o StrictHostKeyChecking=no -q -o ConnectTimeout=3 "$USR@$ip" exit
    local ret=$?

    case $ret in
        0)
            echo "$ip - SSH Log in Successful"
            ;;
        255)
            echo "$ip - Permission Denied or Connection Timeout"
            ;;
        6)
            echo "$ip - Network Error or IP Unreachable"
            ;;
        5)
            echo "$ip - SSH Port Closed"
            ;;
        *)
            echo "$ip - Unknown Error (Code: $ret)"
            ;;
    esac
}

# Ask for IP input or file
read -p "Enter IP address or path to IP.txt: " IP_INPUT
if [[ -f $IP_INPUT ]]; then
    IP_LIST=$(cat "$IP_INPUT")
else
    IP_LIST=$IP_INPUT
fi

# Ask for authentication method
read -p "Do you want to use a password or key file? (password/key): " AUTH_METHOD
if [[ $AUTH_METHOD == "password" ]]; then
    read -s -p "Enter SSH Password: " PWD
    echo
elif [[ $AUTH_METHOD == "key" ]]; then
    read -p "Enter path to SSH key file: " KEY_FILE
    if [[ ! -f $KEY_FILE ]]; then
        echo "Key file not found!"
        exit 1
    fi
    SSH_OPTIONS="-i $KEY_FILE"
else
    echo "Invalid authentication method. Please choose 'password' or 'key'."
    exit 1
fi

# Ask for SSH username
read -p "Enter SSH username: " USR

# Iterate through IP list
for IP in $IP_LIST; do
    if [[ $AUTH_METHOD == "password" ]]; then
        check_ssh_connection "$IP"
    elif [[ $AUTH_METHOD == "key" ]]; then
        ssh -q -o StrictHostKeyChecking=no -o ConnectTimeout=3 $SSH_OPTIONS "$USR@$IP" exit
        ret=$?

        case $ret in
            0)
                echo "$IP - SSH Log in Successful"
                ;;
            255)
                echo "$IP - Permission Denied or Connection Timeout"
                ;;
            6)
                echo "$IP - Network Error or IP Unreachable"
                ;;
            5)
                echo "$IP - SSH Port Closed"
                ;;
            *)
                echo "$IP - Unknown Error (Code: $ret)"
                ;;
        esac
    fi

done
     
