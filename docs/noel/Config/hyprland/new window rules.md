```lua
windowrule {
   name = kitty
   match:class = ^(kitty)$
   opacity = 0.8 0.8
}

windowrule {
  name = thunar
  match:class = ^(thunar)$
  opacity = 0.8 0.8
}
windowrule {
  name = jetbrains
  no_initial_focus = true
  match:class = (jetbrains-studio)
  match:title = ^win(.*)
}
```