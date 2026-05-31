"""
GrowMap v0.5 - Deploy to GitHub Pages
Run: python v0.5/deploy.py
"""
import subprocess
import os
import sys

# Config
REPO_NAME = "growmap-v5"
BRANCH = "main"
DEPLOY_DIR = os.path.dirname(os.path.abspath(__file__))

def run(cmd, cwd=None):
    """Run a command and return output"""
    result = subprocess.run(cmd, shell=True, cwd=cwd or DEPLOY_DIR, 
                          capture_output=True, text=True)
    if result.returncode != 0 and result.stderr:
        print(f"  Warning: {result.stderr.strip()}")
    return result.stdout.strip(), result.returncode

def main():
    print("=" * 50)
    print("  GrowMap v0.5 - GitHub Pages Deploy")
    print("=" * 50)
    
    # Check if git is initialized
    _, code = run("git rev-parse --git-dir")
    if code != 0:
        print("\n[1/5] Initializing git repo...")
        run("git init")
        run(f"git branch -M {BRANCH}")
    else:
        print("\n[1/5] Git repo already initialized")
    
    # Create .gitignore
    gitignore_path = os.path.join(DEPLOY_DIR, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write("node_modules/\n.DS_Store\nThumbs.db\n*.pyc\n__pycache__/\n")
        print("  Created .gitignore")
    
    # Stage all files
    print("\n[2/5] Staging files...")
    run("git add -A")
    
    # Commit
    print("\n[3/5] Committing...")
    out, code = run('git commit -m "GrowMap v0.5 - Mobile-friendly PWA"')
    if code == 0:
        print("  Committed successfully")
    else:
        print("  Nothing new to commit (already up to date)")
    
    # Check if remote exists
    remote_out, _ = run("git remote -v")
    if "origin" not in remote_out:
        print(f"\n[4/5] No remote found.")
        print(f"\n  You need to create a GitHub repo first.")
        print(f"  Go to: https://github.com/new")
        print(f"  Create a repo named: {REPO_NAME}")
        print(f"  Then run these commands:")
        print(f"")
        print(f"  cd {DEPLOY_DIR}")
        print(f"  git remote add origin https://github.com/YOUR_USERNAME/{REPO_NAME}.git")
        print(f"  git push -u origin {BRANCH}")
        print(f"")
        print(f"  Then enable GitHub Pages:")
        print(f"  Repo Settings > Pages > Source: Deploy from branch > Branch: {BRANCH} / (root)")
        print(f"")
        print(f"  Your site will be at: https://YOUR_USERNAME.github.io/{REPO_NAME}/")
        
        # Ask if they want to set remote now
        username = input("\n  Enter your GitHub username (or press Enter to skip): ").strip()
        if username:
            remote_url = f"https://github.com/{username}/{REPO_NAME}.git"
            run(f"git remote add origin {remote_url}")
            print(f"  Remote set to: {remote_url}")
            print(f"\n[5/5] Pushing to GitHub...")
            out, code = run(f"git push -u origin {BRANCH}")
            if code == 0:
                print(f"  Pushed successfully!")
                print(f"\n  Now enable GitHub Pages:")
                print(f"  https://github.com/{username}/{REPO_NAME}/settings/pages")
                print(f"  Source: Deploy from branch > Branch: {BRANCH} / (root)")
                print(f"\n  Your app will be live at:")
                print(f"  https://{username}.github.io/{REPO_NAME}/")
            else:
                print(f"  Push failed. Make sure the repo exists at:")
                print(f"  https://github.com/{username}/{REPO_NAME}")
                print(f"  Create it first, then run: git push -u origin {BRANCH}")
        else:
            print("\n  Skipped. Run the commands above when ready.")
    else:
        print(f"\n[4/5] Remote already configured: {remote_out.split()[1]}")
        print(f"\n[5/5] Pushing to GitHub...")
        out, code = run(f"git push origin {BRANCH}")
        if code == 0:
            print("  Pushed successfully!")
            # Extract URL from remote
            url = remote_out.split()[1].replace(".git", "").replace("https://github.com/", "")
            if "/" in url:
                username, repo = url.split("/", 1)
                print(f"\n  Your app should be live at:")
                print(f"  https://{username}.github.io/{repo}/")
        else:
            print(f"  Push failed. Check your credentials.")
    
    print("\n" + "=" * 50)
    print("  Done! After enabling Pages, open on iPhone:")
    print("  Safari > your-url > Share > Add to Home Screen")
    print("=" * 50)

if __name__ == "__main__":
    main()
