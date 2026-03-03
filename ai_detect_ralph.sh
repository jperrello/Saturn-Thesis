#!/usr/bin/env bash
while :; do
    cat AI_DETECT_PROMPT.md | claude -p --dangerously-skip-permissions
    sleep 2
done
