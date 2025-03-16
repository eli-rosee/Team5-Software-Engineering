# Team5-Software-Engineering Setup Instructions

  1. Install the Debian virtual machine provided by Instructor Jim Strother
     - All instructions in read me assume access to this specific VM
    
  2. Dowload all files from git
     - Under Code, click Download ZIP
     - In terminal, go to directory /home/student/ (should be default)
     - cd Downloads
     - mv Team-5-Software-Engineering-main.zip ..
     - cd ..
     - unzip Team-5-Software-Engineering-main.zip
     - mv Team-5-Software-Engineering-main project (rename it for simplicity)
  
  project directory should look like this: ![image](https://github.com/user-attachments/assets/deffecee-e484-410f-b826-ac0375ac15e9)

  
  graphics directory should look like this:                                                                                         
  ![image](https://github.com/user-attachments/assets/6b49b89c-efde-4bbf-89f3-25672ffc4acc)

    
  3. Install required libraries
     - sudo apt update (password: student)
     - sudo apt install python3-pip -y
     - pip install PyQt6
     - sudo pip3 install pynput==1.7.6
     - pip install psycopg2-binary
     - sudo apt install libxcb-cursor0
     - sudo apt install tcpdump -y

    
  4. Running the application (must be inside project folder)
     - python3 main.py 

  5. What happens in main.py?
     - In the terminal, you can see what is coming through the server's receiving port
     - First 3 seconds is the loading screen
     - After that, the player entry screen loads
     - In the player entry screen, you can insert the player_id into a player id textbox
     - To confirm the player id, press enter
     - If the player id is in the photon database, it will load the code name for the player
     - If the player id is not in the database, you must enter it yourself
     - Again, you can press enter to confirm the codename
     - Lastly, you must insert and confirm the equipment id 
     - Pressing enter, will then add the player completely (sends information to the server)
     - If you want to to move sides or to a specific textbox, you can either press tab or click the text box with your cursor
     - After you have enteted all players that you want, you can click f5 or the button labeled "f5 Start Game" to start the game
     - You can only enter the game if all players have a equipment id linked to their player and there must be at least one player on eash side
     - After starting the game, a 30 second timer will start
     - Once that timer is done, it will start the game and up the play action screen
     - To return to the player entry screen, click the "Return to Player Entry Screen" button
     - Clicking the button "Change IP" allows you to change the IP address
     - pressing f12 or clicking the f12 button allows you to clear out all the players entered
   
  6. To verify that the udp set up is correct, run these commands
     - sudo tcpdump -i lo -n udp port 7500 -X
     - sudo tcpdump -i lo -n udp port 7501 -X


