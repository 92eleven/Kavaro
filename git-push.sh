#!/bin/bash
cd /workspace/qualifai
git push -u origin main 2>&1
echo "PUSH_EXIT_CODE=$?"