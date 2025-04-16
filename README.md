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

  3. Install required libraries
     - sudo apt update (password: student)
     - sudo apt install python3-pip -y
     - pip install PyQt6
     - pip install psycopg2-binary
     - sudo apt install libxcb-cursor0
     - sudo apt install tcpdump -y
     - pip install playsound
     - pip3 install pygame
    
  4. Running the application (must be inside project folder)
     - python3 main.py
    
  5. Test running the generator (you can use a different terminal window and must be inside project folder)
     - python3 traffic_generator.py 

  6. What happens in main.py?
     - First 3 seconds is the loading screen
     - After that, the player entry screen loads
     - In the player entry screen, you can insert the player_id into a player id textbox
     - To confirm the player id, press enter (player id must be a number)
     - If the player id is in the photon database, it will load the code name for the player
     - If the player id is not in the database, you must enter it yourself 
     - Again, you can press enter to confirm the codename
     - Lastly, you must insert and confirm the equipment id (equipment id must be a number)
     - Pressing enter, will then add the player completely (broadcasts equipment id) and moves the user to the next player to enter
     - If equipment ID feild is missing, the player will not be added to the game
     - If you want to to move sides or to a specific textbox, you can click the text box with your cursor
     - You can clear all players from the game by clicking the button "f12 Clear Game" or by pressing f12
     - After you have enteted all players that you want, you can click f5 or the button labeled "f5 Start Game" to start the game
     - You can only enter the game if at least one player ia on each side
     - After starting the game, a 30 second timer will start 
     - Once that timer is done, it will start the game and open the play action screen (server broadcasts 202 to the client)
     - While the game is playing, music will be in the background playing as well
     - The game timer will count down every second.
     - Red team scores, green team scores, and individual scores will be updated by client (traffic_generator.py )
     - THe highest scoring team will be blinking
     - If a player hits a base, they get a B beside their name and 100 points for thier team and their individual score
     - If it is a normal hit, the player gets 10 points for thier team and individual score (-10 to the attacker if they are on the same team)
     - The middle of the screen shows the all of the game actions (what player hit who)
     - The game will last 6 minutes long, and then ends the game (server broadcasts 221 to client)
     - You can return to the player entry screen as well by clicking the "Return to Player Entry Screen" button (server sends 221 to client)
     - Clicking the button "Change IP" allows you to change the IP address
         - (if you do this, make sure to change these 2 lines in your traffic_generator.py)
         - serverAddressPort   = ("127.0.0.1", 7500) 
         - clientAddressPort   = ("127.0.0.1", 7501) to the ip you changed in the game
   
  7. To verify that the udp set up is correct, run these commands
     - sudo tcpdump -i lo -n udp port 7500 -X
     - sudo tcpdump -i lo -n udp port 7501 -X

