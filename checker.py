import time

from checkers import RandomChecker

OUTPUT_DIR = "/home/akaiser/checker"

# Add checks
# add check


def check_disk_space():
    return (True, "")


if __name__ == "__main__":

    checks = []
    checks.append(RandomChecker())

    while True:
        print("Starting check loop")
        for check in checks:
            check_output = check.runCheck()
            if not check_output[0]:
                print("Check failed: {}".format(check_output[1]))
        time.sleep(10)