#!/bin/bash

# IDEEN:
# In Python besser machen
# Hintergrund ändern
# bessere nachbar erkennung
# Verschiedene Gebiete mit Regeln erstellen

clearScreen() {

	clear
}

clearScreen

hideCursor() {

	echo -e "\e[?25l"  # Cursor verstecken

}

main() {
	
	width=80
	height=25

	char=("#" "-")
	length=${#char[@]}
	column=()


	
	for (( i=0; i<width; i++ ));
	do
		columns[i]=$(( RANDOM % height ))
	done

	while true; do
		#clearScreen
		hideCursor


		randomIndex=$(( RANDOM % length ))
		random=${char[$randomIndex]}

		randomIndex2=$(( RANDOM % length ))
		random2=${char[$randomIndex2]}


		for (( x=1; x<width; x++));do
			tput cup "${columns[x]}" "$x"
			
			currentValue="$random"
			nextValue="$random2"

			#clear

			if [[ "$currentValue" == "#" && "$nextValue" == "#" ]];
			then
				sleep 0.01
				nextValue="-"
				echo -n "$currentValue $nextValue"

			else if [[ "$currentValue" == "-" && "$nextValue" == "-" ]];
			then
				sleep 0.01

			fi
			fi

		done
		
		#columns[x]=$(( columns[x] + 1000 ))

		
		sleep 0.1



	done

}
main


