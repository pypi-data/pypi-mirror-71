import click
import sys
import json
from mpm.pm import (
    Package,
    UniversalePackage,
    NAMES_TO_PACKAGE_MANAGERS,
    PACKAGE_MANAGERS_NAMES,
    get_installed_pms,
)
from mpm.core.logging import getLogger
from mpm.core.exceptions import PackageManagerNotInatalled
from mpm.shell import AutoShell
from mpm.core.configs import get_known_packages, update_user_known_package

logger = getLogger(__name__)


def print_info(info: dict()):
    for pm_name, data in info.items():
        click.echo(f"\n\t{pm_name}:", color="green")
        for key, val in data.items():
            click.echo(f"- {key}: {val}", color="green")


@click.group()
def main():
    pass


@main.command()
@click.argument("package_name")
@click.option("-a", "--all", "all_flag", is_flag=True, help="")
@click.option(
    "-of",
    "--offline",
    "offline",
    is_flag=True,
    help="Search for information not only in local the known_packages",
)
# TODO: parse URL
@click.option(
    "-k",
    "--known-packages-json",
    type=click.Path(exists=True),
    help="known_packages.json file",
)
@click.option(
    "-pm",
    "--package-manager",
    "pm_name",
    multiple=False,
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)  # Не возможен мультивызов
def install(
    package_name, pm_name, known_packages_json, all_flag, offline
):  # install kit
    """
    Установить пакет
    """
    logger.debug(
        f"Args:\n\tpackage_name = {package_name},\n\pm_name = {pm_name}\n\tall = {all_flag}\n\toffline = {offline}"
    )
    known_packages = get_known_packages(offline=offline)
    if known_packages_json:
        known_packages.update(json.load(known_packages_json))
    shell = AutoShell()
    PMs = get_installed_pms(shell=shell)
    if pm_name:
        pm_fliter = lambda PM: PM.name == pm_name
        PMs = list(filter(pm_fliter, PMs))
        if PMs == []:
            raise PackageManagerNotInatalled(f"{pm_name} don't installed")
    package = UniversalePackage(package_name, shell=shell, pms_classes=PMs)
    package.install()


@main.command()
@click.argument("package_name")
@click.option(
    "-a",
    "--all",
    "all_flag",
    is_flag=True,
    help="Search for information not only the known_packages",
)
@click.option(
    "-of",
    "--offline",
    "offline",
    is_flag=True,
    help="Search for information not only in local the known_packages",
)
# TODO: parse URL
@click.option(
    "-k",
    "--known-packages-json",
    type=click.Path(exists=True),
    help="known_packages.json file",
)
@click.option(
    "-pm",
    "--package-manager",
    "pm_names",
    multiple=True,
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)  # Возможен мультивызов, например: -pm apt -pm pip
def info(package_name, pm_names, known_packages_json, all_flag, offline):
    """
    Показать дополнительные данные о пакете
    """
    logger.debug(
        f"Args:\n\tpackage_name = {package_name},\n\tpm_names = {pm_names}\n\tall = {all_flag}\n\toffline = {offline}"
    )
    known_packages = get_known_packages(offline=offline)
    if known_packages_json:
        known_packages.update(json.load(known_packages_json))

    shell = AutoShell()
    PMs = get_installed_pms(shell=shell)
    if len(pm_names) > 0:
        pm_fliter = lambda PM: PM.name in pm_names
        PMs = list(filter(pm_fliter, PMs))
        logger.debug(f"PMs after filtering: {PMs}")

    package = UniversalePackage(
        package_name, shell=shell, pms_classes=PMs, known_packages=known_packages
    )

    info = package.get_info(all_pm=all_flag)
    if info == {}:
        logger.error("Package Does Not Found")
        return

    print_info(info)
    if package_name not in known_packages:
        update_user_known_package(package_name, package.config)


@main.command()
@click.argument("package_name")
@click.option(
    "-pm",
    "--package-manager",
    "pm_name",
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)
def remove(package_name, pm_name):
    """
    Удалить пакет
    """
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
    click.echo("Syncing")


@main.command()
@click.argument("package_name")
@click.option(
    "-pm",
    "--package-manager",
    "pm_names",
    multiple=True,
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)  # Возможен мультивызов, например: -pm apt -pm pip
def search(package_name, pm_names):
    """
    Найти пакет
    """
    logger.debug(f"package_name = {package_name}, pm_names = {pm_names}")
    shell = AutoShell()
    PMs = get_installed_pms(shell=shell)
    if len(pm_names) > 0:
        pm_fliter = lambda PM: PM.name in pm_names
        PMs = list(filter(pm_fliter, PMs))
        logger.debug(f"PMs after filtering: {PMs}")
    data = {}
    for pm in PMs:
        try:
            data[pm.name] = pm(shell=shell).search(package_name)
        except NotImplementedError as e:
            logger.warn(f"{pm.name} not have search method!")  # , exc_info=True)
    print_info(data)


@main.command()
@click.argument("package_name")
@click.option(
    "-pm",
    "--package-manager",
    "pm_name",
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)
def reinstall(package_name, pm_name):
    """
    Переустановить пакет
    """
    logger.debug(f"package_name = {package_name}, pm_name = {pm_name}")
    click.echo("Syncing")


@main.command()
@click.argument("package_name")
@click.option(
    "-pm",
    "--package-manager",
    "pm_name",
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)
def update(package_name, pm_name):
    """
    Обновить пакет
    """
    logger.debug(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.info(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.warn(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.success(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.error(f"package_name = {package_name}\n\tpm_name = {pm_name}")
    logger.critical(f"package_name = {package_name}\n\tpm_name = {pm_name}")


@main.command(name="list")
@click.option(
    "-a",
    "--all",
    "all_flag",
    is_flag=True,
    help="Search for information not only the known_packages",
)
@click.option(
    "-of",
    "--offline",
    "offline",
    is_flag=True,
    help="Search for information not only in local the known_packages",
)
# TODO: parse URL
@click.option(
    "-k",
    "--known-packages-json",
    type=click.Path(exists=True),
    help="known_packages.json file",
)
@click.option(
    "-pm",
    "--package-manager",
    "pm_names",
    multiple=True,
    type=click.Choice(PACKAGE_MANAGERS_NAMES, case_sensitive=False),
)  # Возможен мультивызов, например: -pm apt -pm pip
def list_command(pm_names, offline, known_packages_json, all_flag):
    """
    Список пакетов
    """
    logger.debug(
        f"Args:\n\tpm_names = {pm_names}\n\tall_flag = {all_flag}\n\toffline = {offline}\n\tknown_packages_json= {known_packages_json}"
    )
    known_packages = get_known_packages(offline=offline)
    if known_packages_json:
        known_packages.update(json.load(known_packages_json))

    shell = AutoShell()
    PMs = get_installed_pms(shell=shell)
    if len(pm_names) > 0:

        def pm_fliter(PM):
            return PM.name in pm_names

        PMs = list(filter(pm_fliter, PMs))
        logger.debug(f"PMs after filtering: {PMs}")

    out_list = []
    if all_flag:
        for PM in PMs:
            pm = PM()
            out_list.extend(pm.get_all_packages())
    else:
        for package_name in known_packages.keys():
            package = UniversalePackage(
                package_name,
                shell=shell,
                pms_classes=PMs,
                known_packages=known_packages,
            )
            if package.is_installed():
                ver = package.info.get("version", None)
                if not ver:
                    out_list.append([f"{package_name}"])
                else:
                    out_list.append([f"{package_name}@{ver}"])

    for line in out_list:
        click.echo(f"- {line}")


if __name__ == "__main__":
    main()
