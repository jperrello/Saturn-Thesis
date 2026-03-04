#!/usr/bin/env bash
while :; do
    cat RALPH_PROMPT.md | claude -p --dangerously-skip-permissions
    sleep 2
done
