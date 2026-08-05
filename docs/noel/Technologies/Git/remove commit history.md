1. Create orphan branch (no parents)
`git checkout --orphan fresh`

2.  Stage everything currently in the working tree
`git add -A`

3. Single commit
`git commit -m "Initial commit"`

4. Replace main
`git branch -D main && git branch -m main`

5. Force-push (rewrites public history)
`git push -f origin main`