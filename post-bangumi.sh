#!/bin/bash

hostname = ''

exec curl -v --noproxy '*' -H 'Content-Type: application/json' "http://${hostname}:8000/api/post_download" --data-raw "{ \"category\": \"$1\", \"save_path\": \"$2\", \"torrent_id\": \"$3\" }"
