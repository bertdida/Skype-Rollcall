class RollCall:
    name = "rollcall"

    @staticmethod
    def execute(event):
        print(repr(event))