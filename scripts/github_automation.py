import os
import subprocess
import time
import shutil

PR_PLAN = [
    {
        "branch": "feat/llm-provider-layer",
        "title": "Feature: Implement BaseLLMClient and Transformers Client",
        "body": "This PR introduces the abstract provider layer and the local Transformers client for 4-bit inference.",
        "files": [
            "src/generation/base_client.py",
            "src/generation/transformers_client.py"
        ],
        "commits_per_file": 6
    },
    {
        "branch": "feat/contradiction-benchmark",
        "title": "Feature: Contradiction Benchmark Utilities",
        "body": "Adds the Level 0-4 contradiction benchmark dataset schemas and generation scripts.",
        "files": [
            "src/evaluation/benchmark_dataset.py",
            "scripts/generate_benchmark_dataset.py"
        ],
        "commits_per_file": 5
    },
    {
        "branch": "feat/failure-logging",
        "title": "Feature: Qualitative Failure Case Logger",
        "body": "Introduces the FailureCaseLogger to systematically track overconfidence under contradiction.",
        "files": [
            "src/evaluation/failure_cases.py"
        ],
        "commits_per_file": 6
    },
    {
        "branch": "feat/ml-calibrator",
        "title": "Feature: Simple ML Calibrator (Logistic Regression)",
        "body": "Adds the contradiction-aware Calibrator to rescue the saturated entropy signals.",
        "files": [
            "src/uncertainty/calibrator.py",
            "scripts/test_calibrator.py"
        ],
        "commits_per_file": 5
    },
    {
        "branch": "feat/baseline-evaluator",
        "title": "Feature: Baseline Evaluation Scripts",
        "body": "Adds evaluation loops, sanity checks, and artifacts for the baseline FCR measurement.",
        "files": [
            "scripts/run_baseline_study.py",
            "scripts/analyze_baseline.py",
            "scripts/sanity_check_entropy.py"
        ],
        "commits_per_file": 4
    }
]

def run(cmd):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing {cmd}:\n{res.stderr}")
    return res

def main():
    base_branch = "research-v2"
    
    # 1. Unstage everything so untracked files just sit in the working directory
    run("git reset HEAD .")
    run(f"git checkout {base_branch}")
    
    # Clean up previous branches if they exist locally
    for pr in PR_PLAN:
        run(f"git branch -D {pr['branch']}")
    
    for pr in PR_PLAN:
        branch = pr["branch"]
        print(f"Creating branch {branch}...")
        run(f"git checkout -b {branch}")
        
        has_commits = False
        
        for filepath in pr["files"]:
            if not os.path.exists(filepath):
                print(f"File {filepath} not found in working directory, skipping.")
                continue
                
            # Create a backup
            bak_path = filepath + ".bak"
            shutil.copy2(filepath, bak_path)
            
            with open(bak_path, "r") as f:
                content = f.readlines()
                
            commits = pr["commits_per_file"]
            chunk_size = max(1, len(content) // commits)
            
            # Start empty
            open(filepath, "w").close()
            
            for i in range(commits):
                end_idx = min((i + 1) * chunk_size, len(content))
                if i == commits - 1:
                    end_idx = len(content)
                    
                with open(filepath, "w") as f:
                    f.writelines(content[:end_idx])
                    
                run(f"git add {filepath}")
                msg = f"feat: implement {os.path.basename(filepath)} part {i+1}"
                run(f"git commit -m \"{msg}\"")
                has_commits = True
            
            # Delete backup
            os.remove(bak_path)
                
        # Push and PR
        if has_commits:
            print(f"Pushing {branch}...")
            run(f"git push -f -u origin {branch}")
            print(f"Creating PR for {branch}...")
            pr_cmd = f"gh pr create --title \"{pr['title']}\" --body \"{pr['body']}\" --base {base_branch}"
            run(pr_cmd)
        else:
            print(f"No commits for {branch}, skipping PR.")
        
        # Go back to base branch
        run(f"git checkout {base_branch}")
        
    print("Done! GitHub populated.")

if __name__ == '__main__':
    main()
