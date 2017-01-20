#!/bin/bash
# textventure-launcher.sh
prompt1='(L) Log In\n\n(Q) Quit\n\n(H) Help\n\n\n'
prompt2='(P) Play Textventure\n\n(Q) Quit\n\n(H) Help\n\n\n'
login1='Please enter your username . Abort with a blank entry.\n'
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
            query=printf -v 'SELECT username handle userid FROM users WHERE\
            username="%s" AND password="%s"' $username $password
            info=$(mysql -h localhost -u username -p password -D db_name -s -N -e "$query")
            return $info
        else
            return 0
        fi
    else
        return 0
    fi
}
help() {
    cat ../help/launcher.txt | more
}
launchgame() {
    # Pass username as parameter 1
    # and password as parameter 2
    # This is why there is a launcher
    python ../bin/textventure.py "$1" "$2"
    exit
}
