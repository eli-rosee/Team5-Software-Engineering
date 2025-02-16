# Team5-Software-Engineering Setup Instructions

To run this program, you need to install a Debian Virtual Machine. The .iso download can be found on the Debian website. We used virtual box for VM capabilities

  1. Install a Debian Virtual Machine
     - Install Virtual Box if you haven't already
     - Download a Debian amd64 .iso from the Debian webiste
     - Create a new virtual machine in Virtual Box and install Debian
       
  2. Enable pip for Python Package installations and management
     - sudo apt update
     - sudo apt install python3-pip -y
     - pip3 --version (check for correct installation)
      
  3. Create a virtual environment
     - python3 -m venv venv
     - source venv/bin/activate
    
  4. Install required libraries
     - pip install PyQt6
     - pip install keyboard
     - pip install pynup
    
  5. Running the application
     - python3 main.py
