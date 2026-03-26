import src.initialize as init

def startTest():
    init.start(
        "Project Test",
        "project-test",
        "io.github.pinpointtools",
        "GTK",
        "React",
        "TypeScript",
        "pnpm",
    )

if __name__ == "__main__":
    print("THIS IS MEANT FOR TESTING ONLY. DO NOT USE THIS IN PRODUCTION.")
    startTest()