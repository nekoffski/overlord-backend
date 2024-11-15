import sys
import argparse
import subprocess
import os


CWD = os.getcwd()


def error(msg: str):
    print("\nERROR:", msg)
    sys.exit(-1)


def expect(condition, msg):
    if not condition:
        error(msg)


def run(cmd):
    out = subprocess.run(cmd.split(' '))
    expect(out.returncode == 0, out.stderr)


def get_services():
    services_path = CWD + "/services"
    return filter(lambda f: os.path.isdir(f),
                  map(lambda f: f"{services_path}/{f}",
                      os.listdir(services_path)))


def build():
    print("building...")
    for service in get_services():
        service_name = service.split('/')[-1]
        print("building service ->", service_name)
        dockerfile = service + "/Dockerfile"
        expect(os.path.isfile(dockerfile), "No docker file found")
        os.chdir(service)
        run(f"docker image build -t overlord-{
            service_name}:latest --file {dockerfile} .")
        os.chdir(CWD)
        print("built successfully!")
    print("all services built...")


def deploy():
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--deploy', action='store_true')
    args = parser.parse_args()

    print("working directory ->", CWD)

    if args.build:
        build()
    elif args.deploy:
        deploy()
    else:
        error(f"No input, pass either --deploy or --build")
