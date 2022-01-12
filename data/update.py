import io, requests
import pandas as pd, numpy as np
from PyPDF2 import PdfFileReader

def vax(date):
    ''' collects vaccine data from the federal Health Department '''

    print(f"Checking vaccine data for {date:%A, %B %-d} ...")
    url = f"https://www.health.gov.au/sites/default/files/documents/{date:%Y}/{date:%m}/covid-19-vaccine-rollout-update-{date:%-d-%B-%Y}.pdf".lower()

    try:
        request = requests.get(url)
        file = io.BytesIO(request.content)
        reader = PdfFileReader(file)
        contents = reader.getPage(6).extractText().split("\n")

        try:
            first_16 = float(contents[contents.index("dose 1") + 2].strip().replace(",", ""))
            second_16 = float(contents[contents.index("dose 2") + 2].strip().replace(",", ""))
            first_12 = float(contents[len(contents) - contents[::-1].index("dose 1") + 1].strip().replace(",", ""))
            second_12 = float(contents[len(contents) - contents[::-1].index("dose 2") + 1].strip().replace(",", ""))
            count = 0
            for i, string in enumerate(contents):
                if string == "dose 1":
                    count = count + 1
                    if count == 2:
                        first_5 = float(contents[i + 2].strip().replace(",", ""))
                        break

        except:
            first_16 = float(contents[contents.index("-dose 1") + 2].strip().replace(",", ""))
            second_16 = float(contents[contents.index("-dose 2") + 2].strip().replace(",", ""))
            first_12 = float(contents[len(contents) - contents[::-1].index("-dose 1") + 1].strip().replace(",", ""))
            second_12 = float(contents[len(contents) - contents[::-1].index("-dose 2") + 1].strip().replace(",", ""))
            count = 0
            for i, string in enumerate(contents):
                if string == "-dose 1":
                    count = count + 1
                    if count == 2:
                        first_5 = float(contents[i + 2].strip().replace(",", ""))
                        break

        first = first_16 + first_12 + first_5
        second = second_16 + second_12

        contents = reader.getPage(2).extractText().split("\n")
        boosters = float(contents[contents.index("Number of doses administered as part of the Commonwealth aged and disability care rollout") + 7].strip().replace(",", ""))

        vaxData.loc[0] = [first, second, boosters, date - pd.Timedelta(days=1)]
        print("Data found; vaxdata.csv written to file.")
        vaxData.to_csv("vaxData.csv", index=False)

    except:
        print(f"Data unavailable for this date.")
        date = date - pd.Timedelta(days=1)
        vax(date)

def cases(date):
    ''' prompts user for ACT case data '''

    print()
    print(f"Input case data for {date:%A, %B %-d, %Y}:")
    caseData.at[date, "dead"] = float(input("Deaths in past day: "))
    caseData.at[date, "new"] = float(input("New cases: "))
    caseData.at[date, "active"] = float(input("Active cases: "))
    caseData.at[date, "hospitalised"] = float(input("In hospital: "))
    caseData.at[date, "intensive care"] = float(input("In intensive care: "))
    caseData.at[date, "ventilated"] = float(input("On ventilation: "))
    caseData.at[date, "tests"] = float(input("Negative tests returned: "))

    if today > date:
        checkToday(date + pd.Timedelta(days=1))

    else:
        clean()

def checkToday(date):
    ''' checks whether today's data is available '''

    if today == date:
        print()
        ready = input("Are today's case data available yet? (Y/N) ")

        if ready.lower() == "y":
            cases(date)

        else:
            print("Remember to check later today.")

    else:
        cases(date)

def clean():
    print()
    print("Cleaning irregular data ...")
    for i, date in enumerate(caseData.index):
        caseData.at[date, "total"] = caseData.at[date, "new"] + caseData.iloc[0:i]["new"].sum()
        caseData.at[date, "recovered"] = caseData.at[date, "total"] - caseData.at[date, "active"] - caseData.iloc[0:i + 1]["dead"].sum()
        caseData.at[date, "average"] = caseData.iloc[max([i - 6, 0]):i + 1]["new"].sum() / 7
        caseData.at[date, "positivity"] = caseData.at[date, "new"] / (caseData.at[date, "new"] + caseData.at[date, "tests"]) if pd.notna(caseData.at[date, "tests"]) else np.nan

    print("Cleaning complete; caseData.csv written to file.")
    caseData.to_csv("caseData.csv")

# prepare data
vaxData = pd.DataFrame(columns=["first", "second", "boosters", "date"])
caseData = pd.read_csv("caseData.csv", parse_dates=["date"], index_col="date")
lastDate = caseData.index[-1]
today = pd.to_datetime(pd.Timestamp("now").date())

# commence program
print()
vax(today)

if today == lastDate:
    print()
    print("Case data are up-to-date.")

else:
    date = lastDate + pd.Timedelta(days=1)
    checkToday(date)
