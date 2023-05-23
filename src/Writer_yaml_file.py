class Yaml_file_Writer:
    def write(self, file_name, content):
        try:
            with open(file_name, "w") as file:
                file.write(content)
        except:
            with open(file_name, "x") as file:
                file.write(content)
        return True
