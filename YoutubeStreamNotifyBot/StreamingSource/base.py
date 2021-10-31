import pathlib


class StreamIdCache:
    def __init__(self, path: pathlib.Path):
        self.file = path
        self.last_notified = self.file.read_text("utf8") if self.file.exists() else ""

        self.file.touch(exist_ok=True)

    def write(self, new_id):
        self.last_notified = new_id
        self.file.write_text(new_id, "utf8")

    def __contains__(self, item):
        return item in self.last_notified
