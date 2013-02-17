#!/bin/bash

if [[ $# != 2 ]] ;then
        echo "Wrong number of parameters."
        exit
fi

case "$1" in
        a)
	if [ -z "${EDITOR+xxx}" ]; then
                echo 'Variable $EDITOR not declared.'
        else
                echo '#!/bin/bash'>"$HOME/bin/$2"
                eval "$EDITOR $HOME/bin/$2" && chmod +x "$HOME/bin/$2"
        fi;;

        e)
	if [ -z "${EDITOR+xxx}" ]; then
                echo 'Variable $EDITOR not declared.'
        else
                eval "$EDITOR $HOME/bin/$2"
        fi;;

        r) rm $HOME/bin/$2 ;;

        *) echo "$1 - argument unknown" ;;
esac