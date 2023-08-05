import os
import sys
import logging
import re

import requests
from requests.exceptions import RequestException


logging.basicConfig()
logger = logging.getLogger("PypiVersions")
logger.setLevel(logging.INFO)

# https://pypi.org/simple
# https://pypi.org/simple/monero/
# https://pypi.python.org/pypi/monero/json <- {"json": {"version": vx.y.z}}
# https://pypi.python.org/pypi/monero/0.7.3/json
PYPI_PACKAGES_URL = "https://pypi.python.org/pypi/{project}/json"


def read_local_requirements(local_requirements):
    """

    Does not consider dependencies from git URLs.

    If duplicates are found, the more recent version is considered.
    """

    requirements = {}

    for local_requirement in local_requirements:
        if os.path.exists(local_requirement):
            with open(local_requirement, "r") as req:
                logger.info(f"Checking {local_requirement}.")
                for line in req.readlines():
                    line = line.strip("\n")
                    if (
                        line
                        and not line.startswith("#")
                        and not line.startswith("git+")
                    ):
                        # Remove comments at the end of the line.
                        match = re.match(r"^([^#]*)#(.*)$", line)
                        if match:  # The line contains a hash / comment
                            line = match.group(1).rstrip()
                        logger.debug(f"'{repr(line)}'")
                        project, version = line.split("==")
                        if project in requirements:
                            versions = [
                                version,
                                requirements[project]["local_version"],
                            ]
                            versions.sort(
                                key=lambda x: [int(u) for u in x.split(".")]
                            )
                            version = versions[-1]
                        requirements[project] = {"local_version": version}

    return requirements


def read_remote_requirements(requirements):
    requirements_ = dict(requirements)

    for project in requirements:
        logger.info(f"Get remote version for '{project}'.")
        response = None
        try:
            complete_url = PYPI_PACKAGES_URL.format(project=project)
            response = requests.get(complete_url)
        except (RequestException) as e:
            logger.error(f"{str(e)}")

        if response is not None:
            response_json = response.json()
            # if project.lower() == "django":
            version = response_json["info"]["version"]
            major_version = version[: version.find(".")]
            local_version = requirements[project]["local_version"]
            local_major_version = local_version[: local_version.find(".")]
            if local_major_version != major_version:
                logger.info(
                    f"'{project}': Major version difference. Local version '{local_version}' and remote version '{version}' differ."
                )
                requirements_[project].update(
                    {"more_recent_major_version": version}
                )

                releases = response_json["releases"]
                released_versions = [
                    key
                    for key in releases
                    if key.startswith(local_major_version)
                    and key.replace(".", "0").isdigit()
                ]
                released_versions.sort(
                    key=lambda x: [int(u) for u in x.split(".")]
                )
                logger.debug(released_versions)
                version = released_versions[-1]

            logger.info(f"'{project}': Version '{version}'.")

            requirements_[project].update({"remote_version": version})
        else:
            logger.error(
                f"Not the expected response: {response.status_code} // {response}."
            )

    return requirements_


def main():
    from _version import __version__
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare local depdenencies against Pypi.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    parser.add_argument(
        "--requirements",
        required=True,
        nargs="+",
        help="Requirements files to consider.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Return result (version differences) as JSON.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show debug info."
    )

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    local_requirements = args.requirements
    return_json = args.json

    requirements = read_local_requirements(
        local_requirements=local_requirements
    )
    complete_requirements = read_remote_requirements(requirements=requirements)
    logger.debug(complete_requirements)

    if return_json:
        result_json = {}

    print()

    for project, v in complete_requirements.items():
        if "remote_version" not in v:
            if return_json:
                result_json[project] = v
            else:
                print(f"'{project}': No remote version found.")
        if v["local_version"] != v["remote_version"]:
            if return_json:
                result_json[project] = v
            else:
                extra = ""
                if "more_recent_major_version" in v:
                    extra = f" There is a more recent major version available: '{v['more_recent_major_version']}'."
                print(
                    f"'{project}': Local version '{v['local_version']}' and remote version '{v['remote_version']}' differ.{extra}"
                )

    if return_json:
        print(result_json)


if __name__ == "__main__":
    sys.exit(main())
