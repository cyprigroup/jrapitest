# set MBS, start of first block, and number of minutes before deadline to submit
# first calcuation

MBS = 46
GENESIS = "2022-01-01T00:00:00Z"
MINBEFORE = 10

# set the path to your SDK install below
COMMAND = "/usr/local/bin/docker-compose -f /path/to/judgeresearchsdk/docker-compose.yaml run jupyter /opt/conda/bin/python /home/jovyan/JudgeResearchNotebooks/headless.py &> jrcron.out"

import os
from datetime import date, datetime, timedelta

# determine current minute
now = datetime.now().replace(microsecond=0, second=0)
print("Current time: " + now.strftime("%Y-%m-%dT%H:%M:%SZ"))

# anchor deadline to genesis time
deadline = datetime.strptime(GENESIS, "%Y-%m-%dT%H:%M:%SZ")

# create timedelta object based on MBS parameter
window = timedelta(minutes=int(MBS))

# iterate through block times until current time is passed, set deadline
while now > deadline:
    deadline = deadline + window

print("Next Block End: " + deadline.strftime("%Y-%m-%dT%H:%M:%SZ"))

# calculate time remaining until window close
remaining = deadline - now

if remaining.total_seconds() / 60 == MINBEFORE:
    os.system(COMMAND)
    print(
        "Ran headless script with: "
        + str(remaining.total_seconds() / 60)
        + " seconds remaining until deadline."
    )
else:
    print(
        "Passing with "
        + str(remaining.total_seconds() / 60)
        + " minutes until first submission."
    )
