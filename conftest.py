import pytest
import logging
from pathlib import Path
from utils.logger import get_logger
import datetime


@pytest.fixture(scope="session")
def project_root():
    # conftest.py is in project root
    return Path(__file__).resolve().parent


@pytest.fixture
def test_logger(request, project_root):
    """
    Full fixture:
    - Creates logs folder
    - Creates per-test log file
    - Uses your get_logger() utility
    - Attaches file handler to ROOT logger
    - Ensures ALL loggers used in the test write into the same log file
    - Cleans up after test
    """
    logs_dir = project_root / "reports" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    test_name = request.node.name
    logfile = logs_dir / f"{test_name}.log"
    logger = get_logger(test_name)
    file_handler = logging.FileHandler(logfile, mode="w", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)

    yield logger

    root_logger.removeHandler(file_handler)
    file_handler.close()


def pytest_configure(config):
    """
    Called before the test session starts.
    Create reports folder and set HTML report path.
    """

    # Create folder
    project_root = Path(__file__).resolve().parent
    report_dir = project_root / "reports"

    report_dir.mkdir(exist_ok=True)

    # Automatically name the report based on timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = report_dir / f"test_report_{timestamp}.html"

    # Tell pytest-html where to output the report
    config.option.htmlpath = str(report_path)

    # Optional: Add environment information
    config._metadata = {
        "Project": "Pytest Framework",
        "Report Generated": timestamp,
        "Platform": config.getoption("--maxfail"),
    }


def pytest_sessionfinish(session, exitstatus):
    """
    Runs after all tests finish.
    Perfect place to finalize the report or print paths.
    """
    print("\n=== Test run complete ===")

    html_report = session.config.option.htmlpath
    print(f"HTML report generated at: {html_report}\n")