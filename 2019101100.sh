if [ $# -ne 1 ]; then
    echo "Incorrect usage! Syntax: ./2019101100.sh \"SQL QUERY\""
    exit 1
fi
python3 2019101100.py "$1"