import os

def main():
    os.system("echo Building espeasy-manager")
    cur_dir = os.getcwd()
    os.chdir("frontend")
    os.system("ng build")
    os.system("echo Frontend build done")
    os.chdir(cur_dir)
    os.system("echo Building docker image")
    os.system("docker build -t espeasy-manager .")
    os.system("echo Docker image build done")

if __name__ == "__main__":
    main()
