# package manager update and pip install
    sudo dnf install python3-pip

# check installation
    pip --version3

# Build an isolated environment to maintain the independence of the project
#  and prevent conflicts between libraries.

    # python virtual environment
        python3 -m venv .venv
    # check 
        ls -a

# activate
    source .venv/bin/activate

    # install pandas
        pip install pandas
