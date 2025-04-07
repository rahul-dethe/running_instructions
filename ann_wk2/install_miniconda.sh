#!/bin/bash

my_wk_dir="$(dirname "$0")"
cd "$my_wk_dir"

echo "Do you have Miniconda already installed? (YES or NO)"
read answer

answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

if [[ "$answer" == "yes" || "$answer" == "y" ]]; then
    echo -e "Enter the full path to the installed Miniconda's directory to verify the installation:\nEg. /home/nirav/miniconda3 or /root/miniconda"
    read existing_path

    if [[ -d "$existing_path/condabin" ]]; then
        echo -e "Miniconda found at $existing_path.\nKindly run the command 'source $existing_path/bin/activate' then\nNavigate to conda_environment directory & run the command: conda env create -f ann_parallel_environment.yml"
    else
        echo "Error: Miniconda not found at $existing_path. Please check the path and try again."
        exit 1
    fi

elif [[ "$answer" == "no" || "$answer" == "n" ]]; then
    echo -e "Enter the base path where you want to install Miniconda.\nEg. /home/hardik or /scratch/vaibhav/software/\nA directory named 'miniconda3' will be created in the specified path & will start the installation."
    read base_path
    existing_path="$base_path/miniconda3"
    mkdir -p "$existing_path"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O "$existing_path/miniconda.sh"
    bash "$existing_path/miniconda.sh" -b -u -p "$existing_path"
    rm "$existing_path/miniconda.sh"
    echo -e "Miniconda installed successfully at $existing_path.\nKindly run the command 'source $existing_path/bin/activate' then\nNavigate to conda_environment directory & run the command: conda env create -f ann_parallel_environment.yml"
else
    echo "Invalid input. Please enter YES or NO."
    exit 1
fi
