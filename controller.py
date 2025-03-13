class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self, curr="dkk"):
        data = self.model.get_data(curr)

        if "error" in data:
            # Print error message with appropriate colors (RED and BOLD).
            print("\x1b[31m\x1b[1mError: {}\x1b[0m\x1b[22m".format(data["error"]))
        else:
            self.view.run(data)