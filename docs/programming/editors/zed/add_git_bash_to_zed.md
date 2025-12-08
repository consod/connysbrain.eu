# Git Bash as default terminal in Zed - Windows

To add Git Bash as the default terminal in Zed for Windows, you need to add it to settings.json file.

First we need to open the Zed settings.json file.

The default file looks something like this:

```
{
  "icon_theme": "Catppuccin Mocha",
  "ui_font_size": 16,
  "buffer_font_size": 15,
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "Catppuccin Mocha"
  }
}
```

Here we need to add the Git Bash path to the terminal settings:[^1]
Note that I also added args --login so that git automatically logs you in.

```
{
 ...
  "terminal": {
    "shell": {
      "with_arguments": {
        "program": "C:\\Program Files\\Git\\bin\\bash.exe",
        "args": ["--login"]
      }
    }
  }
}
```

The complete settings should then look like:

```
{
  "icon_theme": "Catppuccin Mocha",
  "ui_font_size": 16,
  "buffer_font_size": 15,
  "theme": {
    "mode": "system",
    "light": "One Light",
    "dark": "Catppuccin Mocha"
  },
  "terminal": {
    "shell": {
      "with_arguments": {
        "program": "C:\\Program Files\\Git\\bin\\bash.exe",
        "args": ["--login"]
      }
    }
  }
}
```

[^1]:https://github.com/zed-industries/zed/discussions/11091
