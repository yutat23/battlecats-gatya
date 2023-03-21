import requests
from datetime import datetime, timedelta

def curl_command_to_request(curl_command: str):
    parts = curl_command.split()
    url = ""
    headers = {}
    method = "GET"
    for i, part in enumerate(parts):
        if part == "-X":
            method = parts[i + 1]
        elif part == "-H":
            header = parts[i + 1].split(":")
            headers[header[0]] = header[1].strip()
        elif part.startswith("http"):
            url = part

    return method, url, headers

def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_tsv(tsv):
    lines = tsv.split("\n")
    now = datetime.now()
    last_date_object = None
    for line in lines:
        if line.startswith("[start]"):
          continue
        if line.startswith("[end]"):
            break
        cells = line.split("\t")
        startdate = cells[0][:4] + '-' + cells[0][4:6] + '-' + cells[0][6:8]
        enddate = cells[2][:4] + '-' + cells[2][4:6] + '-' + cells[2][6:8]

        for col in  range(1, len(cells)):
            if not is_number(cells[-col]):
                title = cells[-col]
                break
        startdate_object = datetime.strptime(startdate, "%Y-%m-%d") + timedelta(hours=11)
        enddate_object = datetime.strptime(enddate, "%Y-%m-%d") + timedelta(hours=11)
            
        # now gatya
        if enddate_object > now >= startdate_object:
          print(f"\033[38;5;210m{startdate} {title}\033[0m")

        # future gatya
        elif enddate_object > now < startdate_object:
          print(f"\033[38;5;216m{startdate} {title}\033[0m")
        else:
          print(f"\033[38;5;245m{startdate} {title}\033[0m")
        

def main():
    command_url = "https://bc-seek.godfat.org/seek/jp/gatya.tsv"
    headers = {
        'referer' : 'https://bc.godfat.org/',
        }
    response = requests.get(command_url, headers=headers)

    if response.status_code == 200:
        tsv = response.text
        parse_tsv(tsv)

    else:
        print(f"failed request: {response.status_code}")

if __name__ == "__main__":
    main()

