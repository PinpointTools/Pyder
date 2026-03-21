import os
import subprocess
import time

from InquirerPy import inquirer
import src.print as print
import src.initialize as initialize

class Calls:
    def __init__(self):
        self.cwd = os.getcwd()
    
    def projectName(self):
        projectName = inquirer.text(
            message="Enter a project name (e.g; pyder-project)\n  >",
        ).execute()
        
        if projectName == "":
            print.error("Project name cannot be empty.")
            exit()
        
        return projectName
    
    def domainSystem(self):
        domainSystem = inquirer.text(
            message="Enter a domain system (e.g; io.github.pinpointtools)\n  >",
        ).execute()
        
        if domainSystem == "":
            print.error("Domain system cannot be empty.")
            exit()
        
        return domainSystem
    
    def qtorgtk(self):
        qtorgtk = inquirer.select(
            message="For Linux, do you want to use Qt or GTK?",
            choices=[
                "GTK",
                "Qt",
            ],
        ).execute()
        return qtorgtk
    
    def framework(self):        
        framework = inquirer.select(
            message="Select a framework",
            choices=[
                "Vanilla",
                "Svelte",
                "React",
                "Vue",
            ],
        ).execute()
        
        return framework
    
    def variant(self):        
        variant = inquirer.select(
            message="Select a variant",
            choices=[
                "JavaScript",
                "TypeScript"
            ],
        ).execute()
        return variant
    
    def packageManager(self):
        packageManager = inquirer.select(
            message="Select a package manager",
            choices=[
                "npm",
                "pnpm",
            ],
        ).execute()
        return packageManager

class Checks:
    def __init__(self):
        pass
    
    def npm(self):
        try:
            subprocess.run(["npm", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print.success("npm is installed.")
            return True
        except subprocess.CalledProcessError:
            print.error("npm is not installed.")
            return False
    
    def pnpm(self):
        try:
            subprocess.run(["pnpm", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print.success("pnpm is installed.")
            return True
        except subprocess.CalledProcessError:
            print.error("pnpm is not installed.")
            return False

    def python(self):
        try:
            subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print.success("Python is installed.")
            return True
        except subprocess.CalledProcessError:
            print.error("Python is not installed.")
            return False

def inOrder():
    calls = Calls()
    
    projectName = calls.projectName()
    domainSystem = calls.domainSystem()
    qtorgtk = calls.qtorgtk()
    framework = calls.framework()
    variant = calls.variant()
    packageManager = calls.packageManager()
    return projectName, domainSystem, qtorgtk, framework, variant, packageManager

def check(packageManager):
    check = Checks()
    
    # package manager
    if packageManager == "npm":
        check.npm()
    elif packageManager == "pnpm":
        check.pnpm()
    
    # python
    check.python()

def start():
    projectName, domainSystem, qtorgtk, framework, variant, packageManager = inOrder()
    print.empty()
    check(packageManager)
    
    print.empty()
    _continue = inquirer.confirm(
        message=f"Continue with {framework}? This will start {packageManager}.",
    ).execute()
    
    if _continue:
        initialize.start(projectName, domainSystem, qtorgtk, framework, variant, packageManager)
    else:
        print.log("Pyder selection cancelled.")