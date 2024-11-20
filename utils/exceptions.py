class WrongDatasetError(Exception):
    def __init__(self, message="Provided dataset is not the one expected for this transformation."):
        self.message = message
        super().__init__(self.message)