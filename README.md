# Sigmas Little Helper

- File `commandLab.json` will hold the setup for items. 
- First lineedit in each page ist hardcoded and will filter buttons by title.

## Possible Tags:
### Grouping / In order of hirarchy:
- `"page_<name>"` - Tabs, on top of the window 
    - `"title"` - Text on the tab
    - `"elements"` - Multiple element, `group` or `items`
- `"group_<name>"` - Each page can have groups of elements
    - `"title"` - Text on the group 
    - `"elements"` - Array of `controls`
- `"items_<name>"` - These elements will be on the base 
layout with no grouping.
    - `"elements"` - Array of `controls`

### Controls 
These can be used under `"group_<name>"` or `"items_<name>"`.
Controls have a combination of these Tags.
- `"type"` of these elements 
    - `"combobox"` - dropdown with single choice from a list of values
    - `"lineedit"` - edit box, single line
    - `"button"` - clickable button that send a command to the terminal 
    - `"label"` - text
    - `"split"` - just an empty space
- `"title"` - The text is written on the control 
- `"name"` - Name how to refrence the controls value/text. Use `{name}` in the commands.
- `"values"` - Array of pickable values in a dropdown
- `"command"` - string that will be sent to the Terminal. Can use these https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html


## Examples and Tips

- Enter in commands
```
{
    "type":"button", 
    "title":"vpn epa",
    "command":"vpn epa{ENTER}"
}
```
- Clipboard in commands
```
{
    "type":"button", 
    "title":"kubectl grep {cliploard}",
    "command":"kubectl get pods -A | grep {VK_LCONTROL down}v{VK_LCONTROL up}{ENTER}"
}  
```
- Reference dropdown or lineedit 
```
{
    "type":"combobox", 
    "name":"env",
    "values":["pu","ru","prod","preprod"]
},
{
    "type":"combobox", 
    "name":"tenant",
    "values":["ibm","kbs","tk","viactiv"]
},
{
    "type":"lineedit", 
    "name":"kvnr"
},
{
    "type":"button", 
    "title":"CheckMinimal",
    "command":"checkminimal -e {env} -t {tenant} -k {kvnr}{ENTER}"
}
```