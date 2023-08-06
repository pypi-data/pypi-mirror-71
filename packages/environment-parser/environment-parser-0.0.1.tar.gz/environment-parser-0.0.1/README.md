# Environment-Parser

> A lightweight python library to parse environment variables from current shell or .env files.

## Installation


## Usage

Create a new environment parser from shell context.

```
from environment import Environment, SHELL
env = Environment(sources=[SHELL])
```


You can also create a new environment parser from variables starting with a given prefix.
For example, to find all variables starting with `XDG_`, you could use the code below...

```
xdgenv = env.extract_child_from_prefix('XDG_', remove_prefix=True)
print(xdgenv)
```

... and this will output something like the following :

```
CONFIG_DIRS                   /etc/xdg/xdg-budgie-desktop:/etc/xdg
SESSION_PATH                  /org/freedesktop/DisplayManager/Session0
MENU_PREFIX                   gnome-              
SESSION_DESKTOP               budgie-desktop      
SESSION_TYPE                  x11                 
GREETER_DATA_DIR              /var/lib/lightdm-data/sylvan
```
