#!/bin/bash
source venv/bin/activate

echo "Starting Multi-Model Baseline Study..."

echo "========================================="
echo "Running Qwen1.5-1.8B-Chat Baseline..."
echo "========================================="
python scripts/run_baseline_study.py --model Qwen/Qwen1.5-1.8B-Chat

echo "========================================="
echo "Running Qwen1.5-4B-Chat Baseline..."
echo "========================================="
python scripts/run_baseline_study.py --model Qwen/Qwen1.5-4B-Chat

echo "Multi-Model Evaluation Complete."
