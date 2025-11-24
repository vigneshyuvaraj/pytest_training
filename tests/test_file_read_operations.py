import csv
import json
import os
import subprocess
from logging import getLogger

import pytest, shutil

from pathlib import Path

from utils.logger import get_logger


class TestFileReadOperation():

    @pytest.mark.P0
    def test_file_with_valid_path(self, project_root):
        p = Path(project_root)

        tests_dir = p / "utils"
        tests_dir.mkdir(exist_ok=True)

        for g in p.glob("*"):
            print(g.name)

        data_dir = p / "test_sample_data"
        data_dir.mkdir(exist_ok=True)

        # Clean the directory safely
        for f in data_dir.iterdir():
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)

        # Read and overwrite files in utils/
        for f in tests_dir.iterdir():
            if f.is_file() and f.name == "hello.txt":
                print(f.name)
                print(f.read_text())
                f.write_text(
                    "**** this text is from the utils folder file \n"
                    "this text is post reading ******"
                )
                print(f.read_text())

        # shutil.make_archive("arichve",base_dir = tests_dir, format="zip")
        ar = project_root / "reports"
        shutil.make_archive(
            base_name=str(ar / "archive"),  # where archive.zip will be created
            format="zip",
            root_dir=str(p),
            base_dir="tests"
        )


    def test_json_operation(self, project_root):
        p = Path(project_root)
        test_sample_data_dir = p.joinpath("test_sample_data")
        for f in test_sample_data_dir.iterdir():
            if f.is_file() and f.name == "products.json":
                with f.open() as fs:
                    data = json.loads(f.read_text())
                    print(data)
                    for d in data:
                        for k, v in d.items():
                            print(k , v)
                    data.append({"product_id": 103, "name": "Mouse", "price": 1200})
                    f.write_text(json.dumps(data, indent=4))
                    data = json.loads(f.read_text())
                    data = [item for item in data if item.get("product_id") != 103]
                    print(data)
                    f.write_text(json.dumps(data, indent=4))
                    data = json.loads(f.read_text())
                    print(data)

    @pytest.mark.P1
    def test_cvs_operations(self, project_root):
        root = Path(project_root)
        test_sample_data_dir = root.joinpath("test_sample_data")
        test_sample_data_dir.mkdir(exist_ok=True)

        fields = ['Name', 'Branch', 'Year', 'CGPA']
        rows = [
            ['Nikhil', 'COE', '2', '9.0'],
            ['Sanchit', 'COE', '2', '9.1'],
            ['Aditya', 'IT', '2', '9.3'],
            ['Sagar', 'SE', '1', '9.5'],
            ['Prateek', 'MCE', '3', '7.8'],
            ['Sahil', 'EP', '2', '9.1']
        ]

        with open(test_sample_data_dir / "test.csv", "a") as csvreader:
            data = csv.writer(csvreader)
            data.writerow(fields)
            data.writerows(rows)

        with open(test_sample_data_dir / "test.csv") as csvfile:
            csvreader = csv.reader(csvfile)  # Reader object
            fields = next(csvreader)  # Read header
            for row in csvreader:     # Read rows
                rows.append(row)

            print("Total no. of rows: %d" % csvreader.line_num)  # Row count

        print('Field names are: ' + ', '.join(fields))

        print('\nFirst 5 rows are:\n')
        for row in rows[:5]:
            for col in row:
                print("%10s" % col, end=" ")
            print('\n')

    @pytest.mark.P1
    def test_subprocess(self, project_root, test_logger):
        test_logger.info("Running subprocess test")
        # OR — explicit new named logger using your utility
        logger2 = get_logger("custom_logger")
        logger2.info("Additional logging")
        logger = get_logger("test_subprocess_1")
        logger.info("Testing subprocess test commands using pytest framework")
        root = Path(project_root)
        test_sample_data_dir = root.joinpath("test_sample_data")

        try :
            data = subprocess.check_output(["ls"], text=True)
            logger.debug(data)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with return code {e.returncode}")

        lsProcess = subprocess.Popen(["ls"], stdout=subprocess.PIPE, text=True)
        grepProcess = subprocess.Popen(
            ["cat", "pytest.ini"], stdin=lsProcess.stdout,
            stdout=subprocess.PIPE, text=True)
        output, error = grepProcess.communicate()
        logger.info(output)
        logger.error(error)











