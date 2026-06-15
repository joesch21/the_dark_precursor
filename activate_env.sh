#!/usr/bin/env bash
# Buchanan Platform environment activator.
# Use with: source ./activate_env.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Run this with:"
    echo "  source ./activate_env.sh"
    echo ""
    echo "Reason: executing ./activate_env.sh cannot activate the parent shell."
    exit 1
fi

cd "$(dirname "${BASH_SOURCE[0]}")" || return 1

if [ ! -d "venv" ]; then
    echo "Virtual environment 'venv' not found."
    echo "Create it with:"
    echo "  python3 -m venv venv"
    return 1
fi

source venv/bin/activate

echo "Virtual environment activated."
echo "Current directory: $(pwd)"
echo "Python: $(command -v python)"
echo ""
echo "Recommended command:"
echo "  python -m streamlit run frontend/dark_precursor.py"
