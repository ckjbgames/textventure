#!/bin/bash
# textventure-launcher.sh
prompt1='(L) Log In\n\n(Q) Quit\n\n(H) Help\n\n\n'
prompt2='(P) Play Textventure\n\n(Q) Quit\n\n(H) Help\n\n\n'
login1='Please enter your username (email address). Abort with a blank entry.\n'
login2='Please enter your password. Abort with a blank entry.\n'
login() {
    echo "$login1"
    read username
    reset
    if [$username -ne '']; then
        echo "$login2"
        read -s password
        reset
        if [$password -ne '']; then
            # Note: Please insert your own database names here
            # and modify to comply with your database setup.
            query=printf -v 'SELECT handle 
            mysql -h localhost -u username -p password -D db_name       
}
