class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.model.controller = self
        self.view.controller = self
        self.datafile = "playerdata.json"
        self.current_player = None
        self.all_coins = None

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, errMode=False):
        if not errMode:
            self.model.save_to_file()

        self.view.root.destroy()
        quit()

    def listCoins(self):
        tmp = [i for i in self.model.get_coins().items()]
        return tmp

    def retrieveCoinData(self):
        data = self.model.get_data()

        if "error" in data:
            # Print error message with appropriate formatting (RED and BOLD).
            print("\x1b[31m\x1b[1mError: {} {}".format(data["error"], data["msg"]), end="\x1b[0m\x1b[22m\n")
            self.view.error_window(data)
            # return -1
        self.model.load_coins(data)


    def run(self, curr="dkk"):

        self.retrieveCoinData()

        # if no error in the code then load all data and run
        self.model.load_from_file(self.datafile)
        self.all_coins = self.model.get_coins()

        self.view.run(curr)