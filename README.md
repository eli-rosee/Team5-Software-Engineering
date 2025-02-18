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
     - graphics (folder) - if unable to download graphics folder, download logo.jpg located inside the graphics folder
    
  3. Create a directory named project and move all python files and folders into it
     - Open the terminal
     - mkdir project
     - move all dowloaded files to project (mv /home/student/Downloads/filename project/)
     - cd project
  
  4. Create a folder called graphics inside project and move logo into graphics - Step only required if unable to download graphics folder
     - mkdir graphics
     - mv /home/student/Downloads/logo.jpg graphics/
  
  project directory should look like this: ![image](https://github.com/user-attachments/assets/59fbe672-e726-4402-a866-fc87c456699c)
  
  
  graphics directory should look like this:                                                                                         
  ![image](https://github.com/user-attachments/assets/a1b09c8e-ce23-4807-93cc-081b7acebe5f)
    
  5. Install required libraries
     - sudo apt update (password: student)
     - sudo apt install python3-pip (Y to continue)
     - pip install PyQt6
     - sudo pip3 install pynput
     - pip install psycopg2-binary
     - sudo apt install libxcb-cursor0
    
  6. Running the application (must be inside project folder)
     - python3 server.py (must run server file first)
     - python3 main.py (open another terminal instance)
    
  7. Testing client-server interaction (must be inside project folder)
     - python3 server.py (must run server file first)
     - python3 client.py (open another terminal instance)
    

  8. What happens in main.py?
     - First 15 seconds is the loading screen
     - In those 15 seconds that the game is loading, you can choose what ip address you want (in the terminal)
     - After that, the player entry screen loads
     - In the player entry screen, you can insert the player_id into a player id textbox
     - To confirm the player id, press enter or click the add checkbox
     - If the player id is in the photon database, it will load the code name for the player
     - If the player id is not in the database, you must enter it yourself
     - Again, you can press enter or click the add checkbox to confirm the codename
     - Lastly, you must insert and confirm the equipment id 
     - Pressing enter or the add checkbox, will then add the player completely (sends information to the server)
     - If you want to to move sides or to a specific textbox, you can either press tab or click the text box with your cursor
     - After the second player is entered, it automatically starts the game and receives data from server.py
    
  9. What happens in server.py?
     - The first thing you enter is the ip address you want
     - Then server listens for data sent by client or application
     - After server recieves 2 players from application, it starts generating traffic

  10. What happens in client.py?
     - Client talks to the server and the server talks back to client
