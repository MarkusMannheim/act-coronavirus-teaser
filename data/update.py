import pandas as pd, numpy as np

def cases(date):
    ''' prompts user for ACT case data '''

    print()
    print(f"Input case data for {date:%A, %B %-#, %Y}:")
    caseData.at[date, "dead"] = float(input("Deaths in past day: "))
    caseData.at[date, "pcr"] = float(input("New cases from PCR tests: "))
    caseData.at[date, "rat"] = float(input("New cases from RATs: "))
    caseData.at[date, "active"] = float(input("Active cases: "))
    caseData.at[date, "hospitalised"] = float(input("In hospital: "))
    caseData.at[date, "intensive care"] = float(input("In intensive care: "))
    caseData.at[date, "ventilated"] = float(input("On ventilation: "))

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
            clean()

    else:
        cases(date)

def clean():
    print()
    print("Cleaning irregular data ...")
    caseData["new"] = caseData["pcr"] + caseData["rat"]
    for i, date in enumerate(caseData.index):
        caseData.at[date, "total"] = caseData.at[date, "new"] + caseData.iloc[0:i]["new"].sum()
        caseData.at[date, "recovered"] = caseData.at[date, "total"] - caseData.at[date, "active"] - caseData.iloc[0:i + 1]["dead"].sum()
        caseData.at[date, "average"] = caseData.iloc[max([i - 6, 0]):i + 1]["new"].sum() / 7

    print("Cleaning complete; caseData.csv written to file.")
    caseData.to_csv("caseData.csv")

# prepare data
caseData = pd.read_csv("caseData.csv", parse_dates=["date"], index_col="date")
lastDate = caseData.index[-1]
today = pd.to_datetime(pd.Timestamp("now").date())

# commence program
print()

if today == lastDate:
    print("Case data are up-to-date.")

else:
    date = lastDate + pd.Timedelta(days=1)
    checkToday(date)
