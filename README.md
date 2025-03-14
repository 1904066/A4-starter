# a4-starter
## Instructions 
**STEP 1 With server connected**
1. delete store folder and myjounal.dsu
2. navigate to the a4-starter folder and run server.py in terminal 1
3. in terminal 2, run a4.py, it will prompt a GUI window with empty contact
    * goto settings, select `configure DS server`
    * input 127.0.0.1, Alice, 5678 for password then select ok. password can be anything but make sure enter the same password as before otherwise serever will not record your message
    * now we are connected with server
    * goto settings again, select `add contact`, enter "Bob"
    * now Bob will listed in contact
4. in terminal 3, run a4.py, it will prompt a GUI window with empty contact
    * goto settings, select `configure DS server`
    * input 127.0.0.1, Bob, 1234 for password then select ok,  password can be anything but make sure enter the same password as before otherwise serever will not record your message
    * now we are connected with server for bob
    * goto settings again, select `add contact`, enter "Alice"
    * now Alice will listed in contact
    * select Alice in contact frame, type message to bob
5. Go back to Alice window, select bob, you will receive the message
6. Go back to Bob window, select Alice, you will receive the message from Alice   

**STEP 2 Without server**
1. close Alice window, Close bob window
2. use ctrl + C to quit the server
3. turn off Bob terminal and Server terminal
4. Go back to VS code, now there is no server connected and run a4.py
5. wait for 2 secondes
6. goto settings, select `add contact` enter "Bob"
7. click Bob on the contact frame, local message is listed here
