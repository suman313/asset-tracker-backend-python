import subprocess
import os
import platform

def main():
    command = 'ls'
    command4 =None
    if platform.system() != "Windows":
        if os.path.exists("migrations"):
            command4 = 'python3 -m flask db downgrade'
            command = 'rm -r migrations/'
        command0 = 'python3 -m flask db init'
        comment = input("Enter your comment: ")
        command1 = f'python3 -m flask db migrate -m "{comment}"'
        command2 = 'python3 -m flask db upgrade'
    else:
        command = 'dir'
        if os.path.exists("migrations"):
            command4 = 'python -m flask db downgrade'
            command = 'del /s /q migrations'
        command0 = 'python -m flask db init'
        comment = input("Enter your comment: ")
        command1 = f'python -m flask db migrate -m "{comment}"'
        command2 = 'python -m flask db upgrade'

    # Execute the command and wait for it to complete
    try:
        try:
            if command4:
                subprocess.run(command4, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(e)
        subprocess.run(command, shell=True, check=True,)
        subprocess.run(command0, shell=True, check=True)
        subprocess.run(command1, shell=True, check=True)
        subprocess.run(command2, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e}")

main()

# mtu010
# operator check update 