``` zsh
# git shortcuts
unalias gc gp 2>/dev/null
gc() { git add -A && git commit -m "$1"; }
gp() { git push origin "$(git branch --show-current)"; }
# automatic .env load
eval "$(direnv hook zsh)"
# misc
source /usr/share/fzf/key-bindings.zsh
alias top="btop"
alias vi="nvim"
```