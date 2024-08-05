#!/bin/bash

# this works from Home or USB, top level or inside repo folder
if [ -f ./customer.bash_aliases ]; then
    \cp -v ./customer.bash_aliases ~/.bash_aliases
    printf "\n\e[1;35m   Restart terminal to load new aliases.\e[0m\n\n"
elif [ -f HJS/u22/customer.bash_aliases ]; then
    \cp -v HJS/u22/customer.bash_aliases ~/.bash_aliases
    printf "\n\e[1;35m   Restart terminal to load new aliases.\e[0m\n\n"
else
    printf "\n\e[1;35m   Alias file not found.\e[0m\n\n"
fi

cd ~/

# EOF
