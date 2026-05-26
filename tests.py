import shutil
import src.initialize as init
import src.print as print

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
            print.log(f"Testing {framework} {v}...")
            init.start(
                "Project Test",
                "project-test",
                "io.github.pinpointtools",
                "GTK",
                framework,
                v,
                "pnpm",
                True,
            )
            shutil.rmtree("project-test", ignore_errors=True)
            print.success(f"{framework} with {v} successfully tested.")

if __name__ == "__main__":
    print.warning("THIS IS MEANT FOR TESTING ONLY. DO NOT USE THIS IN PRODUCTION.")
    print.warning("THIS WILL TAKE A TOLL OF YOUR INTERNET. SO BE WEARY.")
    
    try:
        startTest()
        print.success("All tests completed successfully.")
    except Exception as e:
        print.error(e)
