def read_file_content_as_string(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.read()
