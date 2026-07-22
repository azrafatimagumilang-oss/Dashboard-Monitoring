import requests
import pandas as pd

THRESHOLD = 0.10


def hitung_deviasi(row):

    design = row["RL Design"]
    aktual = row["RL Aktual"]

    if pd.isna(design) or str(design).strip() == "-":
        return None

    return float(design) - float(aktual)


def get_status(row):

    design = row["RL Design"]
    aktual = row["RL Aktual"]

    if pd.isna(design) or str(design).strip() == "-":
        return "EXPOSES"

    dev = float(design) - float(aktual)

    if dev > THRESHOLD:
        return "OVERCUT"

    elif dev < -THRESHOLD:
        return "UNDERCUT"

    else:
        return "ON GRADE"
def download_excel():

    file_id = "182RrAL01KOmNClW1QKf2hOX2KBsQPP9a"

    url = (
        f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    )

    response = requests.get(url)

    with open(
        "Dashboard_online.xlsx",
        "wb"
    ) as file:

        file.write(response.content)

    return "Dashboard_online.xlsx"
def load_data():

    file = download_excel()

    df = pd.read_excel(
        file,
        sheet_name="DATA"
    )

    # format tanggal
    df["Tanggal"] = pd.to_datetime(
        df["Tanggal"]
    )

    df["Tanggal_Tampil"] = (
        df["Tanggal"]
        .dt.strftime("%d-%m-%Y")
    )

    # hitung ulang deviasi
    df["Deviasi"] = df.apply(
        hitung_deviasi,
        axis=1
    )

    # hitung ulang status
    df["Status"] = df.apply(
        get_status,
        axis=1
    )

    return df

def get_summary():

    df = load_data()

    total_front = len(df)

    overcut = len(
        df[df["Status"] == "OVERCUT"]
    )

    undercut = len(
        df[df["Status"] == "UNDERCUT"]
    )

    ongrade = len(
        df[df["Status"] == "ON GRADE"]
    )

    exposes = len(
        df[df["Status"] == "EXPOSES"]
    )

    avg_deviasi = round(
        df["Deviasi"].abs().mean(),
        2
    )

    max_deviasi = round(
        df["Deviasi"].abs().max(),
        2
    )

    return {
        "total_front": total_front,
        "overcut": overcut,
        "undercut": undercut,
        "ongrade": ongrade,
        "exposes": exposes,
        "avg_deviasi": avg_deviasi,
        "max_deviasi": max_deviasi
    }