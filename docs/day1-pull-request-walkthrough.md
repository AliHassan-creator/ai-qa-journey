# Day 1: Pull request walkthrough

Use this workflow to make a small change on a branch and merge it through GitHub.

## 1. Start from an up-to-date main branch

```powershell
git switch main
git pull origin main
```

## 2. Create a feature branch

Choose a short name that describes the change.

```powershell
git switch -c day1/my-change
```

## 3. Make and commit a focused change

Review the changed files before committing. Keep local secrets and unrelated files out of the commit.

```powershell
git status
git add README.md
git diff --cached
git commit -m "docs: describe my change"
```

Replace `README.md` and the commit message with the files and purpose of your change.

## 4. Push the branch

```powershell
git push -u origin day1/my-change
```

## 5. Open a pull request on GitHub

Open the repository on GitHub. Select **Compare & pull request** for the pushed branch, or use **Pull requests** > **New pull request**. Set the base to `main` and the compare branch to `day1/my-change`. Add a clear title and summary, inspect the diff, then create the pull request.

## 6. Review and merge

Review the PR diff and confirm it contains only the intended change. Wait for required checks, address review comments, and then select **Merge pull request**. Confirm the merge method, complete the merge, and verify that the PR shows **Merged**.

## 7. Update the local main branch

```powershell
git switch main
git pull origin main
git status
```

The local `main` branch should be up to date with `origin/main`.
