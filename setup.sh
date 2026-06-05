#!/bin/bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/1xk0tzk-dN-sgqNoGK4ruHK9Uwc2emfwUFcfU1cNXs_o/edit?gid=0#gid=0"
EOF
streamlit run app.py --server.port $PORT --server.address 0.0.0.0