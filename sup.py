import os
import sys
import platform
import shutil
import distro
from simple_term_menu import TerminalMenu

def is_installed(program):
    return shutil.which(program) is not None


def print_system_info():
    system = platform.system()
    distro_name = distro.name(pretty=True)
    # distro_version = distro.version(best=True)
    print(f"Operating System: {system}")
    print(f"Distribution: {distro_name}")


def verify_operating_system():
    system = platform.system()
    distro_name = distro.id().lower()

    if system != "Linux" or ("debian" not in distro_name and "ubuntu" not in distro_name):
        print("Error: This script can only be run on Debian/Ubuntu systems.")
        sys.exit()

def update_ubuntu():
    print("Updating Ubuntu...")
    os.system("sudo apt-get update")
    print("Update completed.")

def install_docker():

    print("Installing Docker Dependencies...")
    os.system("sudo apt install apt-transport-https curl gnupg-agent ca-certificates software-properties-common -y")
    print("Dependencies Installed")

    print("Adding Key repositories")
    os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -")
    os.system('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"')
    print("Key added")

    print("Installing Docker...")
    os.system("sudo apt install docker-ce docker-ce-cli containerd.io -y")
    print("Docker installed.")

    print("Adding User")
    os.system("sudo usermod -aG docker $USER")
    os.system("newgrp docker")
    print("User Added")

    os.system("docker version")
    print("Docker Installed succesfully")


def install_unzip():
    print("Installing Unzip...")
    os.system("sudo apt-get update && sudo apt-get install -y unzip")
    print("Unzip installed successfully.")

def install_aws_cli():

    if not is_installed("unzip"):
        print("Unzip Not Installed, Cannot install AWS CLI")
        return

    print("Installing AWS CLI...")
    os.system('curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"')
    os.system("unzip awscliv2.zip")
    os.system("sudo ./aws/install")
    print("AWS CLI installed successfully.")

    print('\nIMPORTANT: RUN aws configure\n')

def raise_new_server():
    install_docker()
    install_unzip()
    install_aws_cli()
    print("New server setup completed.")

def install_nginx():
    print("Installing Nginx...")
    os.system("sudo apt update")
    os.system("sudo apt install nginx -y")
    os.system("sudo systemctl status nginx")
    print("Nginx Installed")

def add_ssl():
    print("Installing Certbot")
    os.system("sudo snap install --classic certbot")
    os.system("sudo ln -s /snap/bin/certbot /usr/bin/certbot")
    print("Certbot installed")

    print("\nIMPORTANT: Run sudo certbot --nginx -d url.com -d www.url.com to asociate ssl certificate\n")

def secondary_menu():
    options = ["Install Docker", "Install Unzip", "Install AWS CLI", "Exit"]
    terminal_menu = TerminalMenu(options)
    
    while True:
        menu_entry_index = terminal_menu.show()
        choice = options[menu_entry_index]
        
        if choice == "Install Docker":
            install_docker()
        elif choice == "Install Unzip":
            install_unzip()
        elif choice == "Install AWS CLI":
            install_aws_cli()
        elif choice == "Exit":
            print("Returning to the main menu...")
            break

def main_menu():
    options = ["Update Ubuntu", "Raise New Server", "More Options", "Exit"]
    terminal_menu = TerminalMenu(options)
    
    while True:
        menu_entry_index = terminal_menu.show()
        choice = options[menu_entry_index]
        
        if choice == "Update Ubuntu":
            update_ubuntu()
        elif choice == "Raise New Server":
            raise_new_server()
        elif choice == "Install Nginx":
            install_nginx()
        elif choice == "More Options":
            secondary_menu()
        elif choice == "Exit":
            print("Exiting the script...")
            sys.exit()

def main():
    print_system_info()
    verify_operating_system()
    main_menu()

if __name__ == "__main__":
    main()

