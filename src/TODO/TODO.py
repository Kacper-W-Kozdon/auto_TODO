import pathlib
from typing import Union
excluded: Union[list[str], None] = None
todo_list_name: Union[str, None] = None
project_name: Union[str, None] = None

if __name__ == "__main__":
    proj_path = pathlib.Path(__file__).parent
    scripts_paths_generator = proj_path.glob("**/*.py")
    scripts = []

    for script in scripts_paths_generator:
        if not excluded:
            scripts.append(script)
            continue
        
        if all([excluded_item not in str(script) for excluded_item in excluded]):
            scripts.append(script)

    todo_text = f"# {project_name}\n\n ## {todo_list_name}:\n\n"

    old_todo_text = ""

    TODO_md_file = pathlib.Path(f"{proj_path}\\TODO.md")

    if not TODO_md_file.is_file():
        file = open(f"{proj_path}\\TODO.md", "w")
        file.close()

    TODO_txt_file = pathlib.Path(f"{proj_path}\\TODO.txt")
    if not TODO_txt_file.is_file():
        file = open(f"{proj_path}\\TODO.md", "w")
        file.close()

    with open(f"{proj_path}\\TODO.txt", "r") as old_todo:
        for line in old_todo:
            old_todo_text += f"{str(line)}"

    with open(f"{proj_path}\\TODO.txt", "w+") as todo_out:
        for script in scripts:
            with open(script) as todo_in:
                for line in todo_in:
                    if "TODO:" in str(line):
                        index_start = str(line).find("TODO: ")
                        index_stop = (
                            str(line).find(r" \endtodo")
                            if str(line).find(r" \endtodo") != -1
                            else str(line).find(r"\endtodo")
                        )

                        todo_text += f"{str(line)[index_start + 5 : index_stop]}\n"

        todo_out.write(todo_text)

    readmemd_text = f"# {project_name}\n\n## {todo_list_name}:\n\n"
    readmemd_text_old = ""

    with open(f"{proj_path}\\TODO.md", "r") as READMEmd_old:
        finished_marker = "[x]"

        for line_readme_old in READMEmd_old:
            try:
                if finished_marker in line_readme_old:
                    print(f"Finished marker in line: {line_readme_old=}")
                    formatted_line = f"{str(line_readme_old)}\n"
                    readmemd_text_old += f"{str(formatted_line)}"
            except Exception as exc:
                print("An issue occurred while opening the README.md.")
                print(exc)
                pass

    with open(f"{proj_path}\\TODO.md", "w+") as READMEmd_out:
        starting_index = len(" - [x] ")

        for line_readme in old_todo_text.split("\n"):
            print(f"{line_readme=}, {(line_readme[starting_index:] in todo_text)=}")
            try:
                if line_readme not in todo_text:
                    formatted_line = f" - [x] {str(line_readme)}\n"
                    readmemd_text += f"{str(formatted_line)}"
            except Exception as exc:
                print("An issue occurred while opening the README.md.")
                print(exc)
                pass

        with open(f"{proj_path}\\TODO.txt", "r") as READMEmd_in:
            for line_todo in READMEmd_in:
                if f"# {project_name}" in line_todo or f"## {todo_list_name}:" in line_todo:
                    continue

                elif line_todo not in readmemd_text:
                    formatted_line_todo = f"- [ ]{str(line_todo)}"
                    readmemd_text += f"{(formatted_line_todo)}"

        readmemd_text += readmemd_text_old[
            :-1
        ]  # Ignores the final blank line in the .txt file.
        READMEmd_out.write(readmemd_text)
