#!/usr/bin/env sh
set -eu

python app.py &
app_pid=$!
trap 'kill "$app_pid" 2>/dev/null || true' EXIT INT TERM

container_ip=$(hostname -i | awk '{print $1}')
exec socat "TCP-LISTEN:5005,bind=${container_ip},fork,reuseaddr" TCP:127.0.0.1:5005
