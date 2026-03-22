import src.initialize as init

def startTest():
    init.start(
        "projectTest",
        "io.github.pinpointtools",
        "GTK",
        "Vanilla",
        "TypeScript",
        "pnpm",
    )

if __name__ == "__main__":
    print("THIS IS MEANT FOR TESTING ONLY. DO NOT USE THIS IN PRODUCTION.")
    startTest()