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
        if [$
