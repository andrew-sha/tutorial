from __future__ import annotations

import logging
import os
from pathlib import Path

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

SQLMESH_VERSION = "0.82.2"
SQLMESH = f"sqlmesh[{os.environ.get('_SQLMESH_EXTRAS', '')}]=={SQLMESH_VERSION}"


def get_sqlmesh_extras_require() -> dict[str, list[str]]:
    if Path("sqlmesh_extras_require.txt").exists():
        with open("sqlmesh_extras_require.txt", "r") as f:
            return {r.strip(): [f"sqlmesh[{r.strip()}]"] for r in f}
    logger.warning("File `sqlmesh_extras_require.txt` not found.")
    return {}


setup(
    name="sqlmesh-enterprise",
    author="TobikoData Inc.",
    author_email="engineering@tobikodata.com",
    packages=find_packages(
        include=[
            "sqlmesh_enterprise",
            "services",
        ],
    ),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "sqlmesh = sqlmesh_enterprise.cli.main:cli",
            "sqlmesh_cicd = sqlmesh_enterprise.cli.bot:bot",
        ],
        "airflow.plugins": [
            "sqlmesh_airflow = sqlmesh_enterprise.schedulers.airflow.plugin:EnterpriseSqlmeshAirflowPlugin",
        ],
    },
    use_scm_version={
        "write_to": "sqlmesh_enterprise/_version.py",
        "fallback_version": "0.0.0",
        "local_scheme": "no-local-version",
    },
    setup_requires=["setuptools_scm"],
    install_requires=[
        ("sqlmesh" if os.environ.get("_INSTALL_SQLMESH_DEV") else SQLMESH),
        # Until we are on a release with this fix: https://github.com/TobikoData/sqlmesh/pull/2296
        "duckdb<0.10.1",
        "fastapi",
        "httpx==0.24.0",
        "humanize",
        "hyperscript~=0.0.3",
        "inflect",
        "pydantic>=2.0.0",
        "python-multipart",
        "uvicorn[standard]",
        "web-common",
        # Issue with Snowflake connector and cryptography 42+
        # Check here if they have added support: https://github.com/dbt-labs/dbt-snowflake/blob/main/dev-requirements.txt#L12
        "cryptography~=41.0.7",
    ],
    extras_require={
        **get_sqlmesh_extras_require(),
        "dev": [
            f"apache-airflow=={os.environ.get('AIRFLOW_VERSION', '2.4.3')}",
            "autoflake==1.7.7",
            "black==24.1.1",
            "freezegun",
            "isort==5.10.1",
            "mypy~=1.8.0",
            "pandas-stubs",
            "pre-commit",
            "pyarrow>=10.0.1,<10.1.0",
            "pydantic<2.6.0",
            "pyspark==3.4.0",
            "pytest",
            "pytest-mock",
            "pytest-xdist",
            f"sqlmesh-tests=={SQLMESH_VERSION}",
            "types-requests==2.28.8",
        ],
        "cloud": [
            "tobiko-auth",
        ],
    },
)
