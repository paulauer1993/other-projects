import json
import requests
import re
import csv
import datetime
import pandas as pd


class TestInfo:

    # Add more branches here, if needed.
    BRANCHES = ""
    ACCEPTED_STATUSES = ("success", "failed")
    # Endpoint for the remote project.
    URL = ""
    FILE_PATH = "artifacts/test_reports/test_info.json"

    def __init__(self, gl_api_token, path, excel_file_name):
        self.gl_api_token = gl_api_token
        self.headers = {"PRIVATE-TOKEN": self.gl_api_token, "Content-Type": "application/json"}
        self.path = path
        self.excel = excel_file_name

    def get_artifact_json_file(self, start_page, end_page):
        test_files = []
        for page_nr in range(start_page, end_page + 1):
            jobs = []
            response = requests.get(f"{TestInfo.URL}/pipelines", headers=self.headers, params={"per_page": 100, "page": f"{page_nr}"})
            payload = json.loads(response.text)
            pipelines = [pipeline["id"] for pipeline in payload if pipeline["ref"] in TestInfo.BRANCHES]
            for pipeline_id in pipelines:
                payload = json.loads((requests.get(f"{TestInfo.URL}/pipelines/{pipeline_id}/jobs", headers=self.headers)).text)
                job_id = payload[-1]["id"]
                if payload[-1]["status"] in TestInfo.ACCEPTED_STATUSES and job_id not in jobs:
                    jobs.append(job_id)
            for job_id in jobs:
                try:
                    response = requests.get(f"{TestInfo.URL}/jobs/{job_id}/{TestInfo.FILE_PATH}", headers=self.headers)
                except Exception as exception:
                    print(f"The following exception occurred:\n>>>>>>>>>>>>>>>>{exception}<<<<<<<<<<<<<<")
                    print(f"Related job id is: {job_id}")
                    continue

                if response.status_code == 200:
                    payload = json.loads(response.text)
                    payload["JOB_ID"] = f"{job_id}"
                    info_response = requests.get(f"{TestInfo.URL}/jobs/{job_id}", headers=self.headers)
                    info_payload = json.loads(info_response.text)
                    try:
                        payload["Username"] = info_payload["user"]["username"]
                        payload["Job URL"] = info_payload["web_url"]
                    except KeyError:
                        continue
                    finally:
                        test_files.append(payload)

        return test_files

    def read_excel(self):
        column_heads = ("Test case name", "Bench", "Duration")
        values = list()
        real_durations = list()
        for _ in range(2, 5):
            file = pd.read_excel(io=f"{self.path}/{self.excel}", sheet_name="General_Table", header=_)
            if "Test case name" or "Bench" in file.columns.ravel():
                break

        for head in column_heads:
            if head == "Duration":
                durations = file[head].values
                for duration in durations:
                    duration = str(duration)
                    if len(duration) > 8:
                        time = re.findall(r"\d{2}:\d{2}:\d{2}", duration)[0].split(":")
                        hours = int(re.findall(r"\d{4}-\d{2}-\d{2}", duration)[0].split("-")[2]) * 24
                        duration = ":".join([str(int(time[0]) + hours), time[1], time[2]])
                    real_durations.append(duration)
                values.append(real_durations)
                continue
            values.append(file[head].values)

        return values

    def write_csv(self, original_file, files, head=False):
        with open(f"{self.path}/CSV_imp.csv", "w+", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for file in files:
                try:
                    duration = file["DURATION"]
                except KeyError:
                    continue
                if not head:
                    writer.writerow(file.keys())
                    head = True
                try:
                    if duration in original_file[2]:
                        index = original_file[2].index(duration)
                        if file["test_plan_folder"] == original_file[0][index] and file["BENCH_NR"] == original_file[1][index]:
                            continue
                except IndexError:
                    print("Probably wrong path.")

                end_date = datetime.datetime.strptime(file["ENDDATE"], "%Y/%m/%d").strftime("%d-%m-%Y")
                start_date = datetime.datetime.strptime(file["STARTDATE"], "%Y/%m/%d").strftime("%d-%m-%Y")
                file["ENDDATE"] = end_date
                file["STARTDATE"] = start_date
                writer.writerow(file.values())


if __name__ == '__main__':
    ti = TestInfo("", "", "file.xlsm")
    # original_file = ti.read_excel()
    files = ti.get_artifact_json_file(1, 3)
    ti.write_csv("original_file", files)
