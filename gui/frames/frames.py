from gui.frames.file_frame import FileFrame


class Frames:
    def __init__(self, master=None):
        self.master = master
        self.file_frame = FileFrame(master)

    def get_file_frame(self):
        return self.file_frame
