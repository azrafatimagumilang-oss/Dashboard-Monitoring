from flask import Flask, render_template, request
from excel_reader import load_data

app = Flask(__name__)


@app.route("/")
def home():

    df = load_data()

    # Ambil filter
    tanggal = request.args.get("tanggal")
    cluster = request.args.get("cluster")
    tim = request.args.get("tim")

    # Dropdown
    clusters = sorted(
        df["CLUSTER"].dropna().unique().tolist()
    )

    tims = sorted(
        df["TIM"].dropna().unique().tolist()
    )

    # Filter tanggal
    if tanggal:
        df = df[
            df["Tanggal"].dt.strftime("%Y-%m-%d") == tanggal
        ]

    # Filter cluster
    if cluster and cluster != "Semua":
        df = df[
            df["CLUSTER"] == cluster
        ]

    # Filter TIM
    if tim and tim != "Semua":
        df = df[
            df["TIM"] == tim
        ]

    # Summary
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
    ) if len(df) > 0 else 0

    max_deviasi = round(
        df["Deviasi"].abs().max(),
        2
    ) if len(df) > 0 else 0

    summary = {
    "total_front": total_front,
    "overcut": overcut,
    "undercut": undercut,
    "ongrade": ongrade,
    "exposes": exposes,
    "avg_deviasi": avg_deviasi,
    "max_deviasi": max_deviasi
}

    # Ringkasan Area
    area_summary = {}

    for area in ["UTARA", "TENGAH", "SELATAN"]:

        area_df = df[
            df["CLUSTER"] == area
        ]

        area_summary[area] = {
    "total": len(area_df),
    "overcut": len(area_df[area_df["Status"] == "OVERCUT"]),
    "undercut": len(area_df[area_df["Status"] == "UNDERCUT"]),
    "ongrade": len(area_df[area_df["Status"] == "ON GRADE"]),
    "exposes": len(area_df[area_df["Status"] == "EXPOSES"])
}

        data = df.to_dict(
        orient="records"
    )

    # Trend Chart
    trend_chart = {
        "labels": [],
        "overcut": [],
        "undercut": []
    }

    trend_df = load_data()

    for tgl in sorted(trend_df["Tanggal"].unique()):

        tgl_df = trend_df[
            trend_df["Tanggal"] == tgl
        ]

        trend_chart["labels"].append(
            tgl.strftime("%d-%m-%Y")
        )

        trend_chart["overcut"].append(
            len(
                tgl_df[
                    tgl_df["Status"] == "OVERCUT"
                ]
            )
        )

        trend_chart["undercut"].append(
            len(
                tgl_df[
                    tgl_df["Status"] == "UNDERCUT"
                ]
            )
        )

    return render_template(
        "index.html",
        data=data,
        summary=summary,
        clusters=clusters,
        cluster=cluster,
        tims=tims,
        tim=tim,
        tanggal=tanggal,
        area_summary=area_summary,
        trend_chart=trend_chart
    )


if __name__ == "__main__":
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)