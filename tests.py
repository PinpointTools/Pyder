import os
import src.initialize as init

def startTest():
    frameworks = [
        "Vanilla",
        "Svelte",
        "React",
        "Vue",
        "Preact",
        "Lit",
        "Solid",
        "Ember",
        "Qwik",
        "Amber",
        "Marko",
    ]
    variant = [
        "JavaScript",
        "TypeScript",
    ]
    
    for framework in frameworks:
        for v in variant:
            init.start(
                "Project Test",
                "project-test",
                "io.github.pinpointtools",
                "GTK",
                framework,
                v,
                "pnpm",
                False,
            )
            os.remove("project-test")

if __name__ == "__main__":
    print("THIS IS MEANT FOR TESTING ONLY. DO NOT USE THIS IN PRODUCTION.")
    print("THIS WILL TAKE A TOLL OF YOUR INTERNET. SO BE WEARY.")
    startTest()
    print("All tests completed successfully.")
