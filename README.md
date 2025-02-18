# Team5-Software-Engineering Setup Instructions

To run this program, you need to install a Debian Virtual Machine. The .iso download can be found on the Debian website. We used virtual box for VM capabilities

  1. Install a Debian Virtual Machine
     - Install Virtual Box if you haven't already
     - Download a Debian amd64 .iso from the Debian webiste
     - Create a new virtual machine in Virtual Box and install Debian
    
  2. Dowload all files from git
     - client.py
     - main.py
     - player_entry_screen.py
     - server.py
     - splash.py
     - database.py
     - graphics (folder) - if unable to download graphics folder, download logo.jpg located inside the graphics folder
    
  3. Create a directory
     - Open the terminal
     - mkdir project
     - move all dowloaded files to project (mv /home/student/Downloads/filename project/)
     - cd project
  
  4. Step only required if unable to download graphics folder
     - mkdir graphics
     - mv /home/student/Downloads/logo.jpg graphics/ (move the logo into a folder called graphics
    
  5. Install required libraries
     - sudo apt update (password: student)
     - sudo apt install python3-pip
     - pip install PyQt6
     - sudo pip3 install pynput
     - pip install psycopg2
     - pip install psycopg2-binary
     - sudo pip3 install keyboard
     - sudo apt install libxcb-cursor0
    
  6. Running the application
     - python3 main.py
