#!/bin/bash
# textventure-launcher.sh
prompt1="(L) Log In\n\n(Q) Quit\n\n(H) Help\n\n\n"
prompt2="(P) Play Textventure\n\n(Q) Quit\n\n(H) Help\n\n\n"
login() {
    echo "Please enter your username. Abort with a blank entry.\n"
    read username
    reset
    if [ -n $username  ]; then
        echo "Please enter your password. Abort with a blank entry.\n"
        read -s password
        reset
        if [ -n $password ]; then
            # Note: Please insert your own database names here
            # and modify to comply with your database setup.
            # The example query that I added is probably not your setup.
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
    # A help page for the launcher
    cat ../help/launcher.txt | more
}
launchgame() {
    # Pass username as parameter 1
    # and user ID as parameter 2
    # This is why there is a launcher
    python ../bin/textventure.py "$1" "$2"
    exit
}
mysql_escape() {
    # This is to play it safe
    # It escapes characters like quotation marks, newlines, returns, etc.
    # *WORK IN PROGRESS*
    escaped=$(echo $1 | sed 's/[\]//g')
    return $escaped
}
