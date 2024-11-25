class BaseApp:
    """Base class for all apps."""
    def __init__(self, **dependencies):
        self.dependencies = dependencies

    def generate_image(self, settings):
        print("CALLED GENERATE IMAGE IN BASE APP, SOMETHING ISNT WORKING")
        raise NotImplementedError("generate_image must be implemented by subclasses")