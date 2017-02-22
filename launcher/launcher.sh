#!/bin/bash
# textventure-launcher.sh
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
            handle="%s" AND username="%s"' $username $password
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
menu1() {
    reset
    local menu=( 'Login' 'Help' 'Quit' )
    select $option in $menu; do
        case $option in
            1 ) local logininfo=$(login)
                if [ ! $logininfo -o -z $logininfo ]; then
                    echo 'That is not a valid login.'
                    echo 'Sorry about that.'
                    sleep 3
                    menu1
                else
                    menu2 $logininfo
                fi ;;
            2 ) help
                menu1 ;;
            3 ) exit ;;
            * ) printf "I don't know how to %i." $option
                sleep 3
                menu1 ;;
        esac
    done
}
menu2() {
    reset
    local menu=( 'Play textventure' 'Help' 'Quit' )
    select $option in $menu; do
        case $option in
            1 ) launchgame $1 ;;
            2 ) help
                menu2 $1 ;;
            3 ) exit ;;
            * ) printf "I don't know how to %i." $option
                sleep 3
                menu2 $1 ;;
        esac
    done
}
