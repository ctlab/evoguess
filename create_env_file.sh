cd ..
printf "# Node settings\nROOT_PATH=" > "evoguess/.env"
pwd >> "evoguess/.env"
printf "MAIN_PATH=\${ROOT_PATH}/evoguess\n" >> "evoguess/.env"
printf "DATA_PATH=\${ROOT_PATH}/evoguess_data\n" >> "evoguess/.env"
printf "TEMPLATE_PATH=\${DATA_PATH}/templates\n" >> "evoguess/.env"
printf "EXPERIMENT_PATH=\${DATA_PATH}/experiments\n" >> "evoguess/.env"