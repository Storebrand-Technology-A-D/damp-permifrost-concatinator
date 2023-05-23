class Yaml_file_Writer:
    def write(self, file_name, content):
        with open(file_name, "w") as file:
            file.write(content)
        return True
