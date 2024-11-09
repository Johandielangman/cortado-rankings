import os


def _file(file: str):
    return os.path.basename(file)


class PageUtils:
    @staticmethod
    def page(file: str):
        return f"pages/{_file(file)}"

    @staticmethod
    def title(file: str):
        return _file(file).replace(".py", "").capitalize()

    @staticmethod
    def icon():
        return "📄"

    @staticmethod
    def url_path(file: str):
        return f"/{_file(file).replace('.py', '')}"
