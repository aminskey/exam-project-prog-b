class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.model.controller = self
        self.view.controller = self
        self.datafile = "playerdata.json"
        self.backupFile = "_backup_data.json"
        self.current_player = None
        self.all_coins = None

        self.view.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self, errMode=False):
        self.model.save_to_file()
        self.view.root.destroy()
        quit()

    def listCoins(self):
        tmp = [i for i in self.model.get_coins().items()]
        return tmp

    def retrieveCoinData(self, save_bckp=True):
        print("Retrieving coin data from CoinGecko")
        data = self.model.get_data()

        if save_bckp:
            self.model.save_to_file("_backup_data.json")

        if "error" in data:
            # Print error message with appropriate formatting (RED and BOLD).
            print("\x1b[31m\x1b[1mError: {} {}".format(data["error"], data["msg"]), end="\x1b[0m\x1b[22m\n")
            self.view.error_window(data)
        self.model.load_coins(data)


    def run(self, curr="dkk"):

        self.retrieveCoinData(False)

        # if the playerdata.json file is corrupted, then load all backup data and run
        if not self.model.load_from_file(self.datafile):
            self.model.load_from_file(self.backupFile)

        self.all_coins = self.model.get_coins()

        self.view.run(curr)