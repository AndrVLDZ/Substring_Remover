import os
from glob import glob
from rich.console import Console
from typing import List
from dataclasses import dataclass

DIR: str = os.getcwd()
SCRIPT: str = os.path.basename(__file__)
EXE: str = "Substring_Remover.exe"

@dataclass()
class Data:
    recursive = False
    substr: str = ""
    menu = {
        1: "Recursive search: Off",
        2: "Set substring to remove",
        3: "View found files",
        4: "Remove substring from file names",
        5: "Exit",
    }

console = Console()
 

def menu() -> None:
    if Data.substr != "":
        Data.menu[2] = f"Change substring to remove: {Data.substr}"

    if Data.recursive is True:
        Data.menu[1] = f"Recursive search: On"
    else:
        Data.menu[1] = f"Recursive search: Off"
    
    print('\n')
    for key in Data.menu.keys():
        console.print(key, '--', Data.menu[key])
    print('\n')


def recursive_mode():
    if Data.recursive is False:
        Data.recursive = True
    else:
        Data.recursive = False


def search_files() -> List[str]:
    search_res:List[str] = []
    files = [x for x in (glob(DIR + "/**", recursive=Data.recursive))]
    for f in files:
        # -1 means that the substring in the string was not found
        is_substr: bool = f.find(Data.substr) != -1
        not_this_script: bool = f.find(SCRIPT) == -1 
        not_this_exe: bool = f.find(EXE) == -1 
        is_file: bool = os.path.isfile(f)
        
        if  is_file and not_this_script and not_this_exe and is_substr:
            search_res.append(f)
            
    return search_res


def show_files() -> None:
    search_res = search_files()
    for string in search_res:
        console.print(string, style="bold cyan")


def del_substr(substring: str) -> None:
    search_res = search_files()
    for string in search_res:
            try:
                os.rename(string, string.replace(substring,""))
                file = os.path.basename(string)
                console.print(f"Removal in {file} completed!", style="bold green")
            except FileExistsError:
                file = os.path.basename(string)
                console.print(
                    f"Cannot create a file when that file already exists: {file}", 
                    style="bold red",
                )


def print_logo(logo=''):
    LOGO_DAFAULT = """
   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
   `      \(/|\)/        `
           " ` "
 Substring_Remover_By_VLDZ 
"""
    if logo != '':
        print(logo)
    else:
        print(LOGO_DAFAULT)


def show_info() -> None:
        console.print(
            "This app removes a substring from all filenames in the folder in which it was launched \
            \nEnter 1 if you want to enable or disable recursive search for files in subfolders", 
            style='bold cyan',
        )


def dialog():
    menu()
    while True:
        command = input("Choose an action: ")
        match command.split():
            case ["1"]: # Change recursive search mode
                recursive_mode()
                menu()
            case ["2"]: # Set substring to remove
                Data.substr = str(input("Enter what you want to delete: "))
                menu()
            case ["3"]: # View found files
                show_files()
                menu()
            case ["4"]: # Remove substring from file names
                del_substr(Data.substr)
                menu()
            case ["5"]: # Exit
                console.print("The program has ended", style="bold cyan")
                return False


def main():
    print_logo()
    show_info()
    dialog()


if __name__ == "__main__":
    main()