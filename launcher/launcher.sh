#!/bin/bash
# textventure-launcher.sh
prompt1="(L) Log in\n\n(Q) Quit\n\n\n\n"
choices1='
prompt2="(P) Play textventure\n\n(Q) Quit\n\n\n\n"
gamepath="/var/games/textventure.py" # This is an example
echo "$prompt1"
read choice
reset
case ${choice in
[L|l]*)
  login()
  ;;
[Q|q
