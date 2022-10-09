from flask import Flask, render_template
import wowo

app = Flask(__name__)
app.jinja_env.globals.update(bd09_to_gaode=wowo.bd09_to_gaode)

@app.route("/")
def hello():
    sites = wowo.get_wowo_list()
    details = []
    for site in sites:
        detail = wowo.get_wowo_detail(site["siteId"])
        if detail["countCollect"] >= 50:
            details.append(detail)
    details.sort(key=lambda x: x["countCollect"], reverse=True)
    return render_template("index.html", details=details)


@app.route("/site/<site_id>")
def site(site_id):
    detail = wowo.get_wowo_detail(site_id)
    comments = wowo.get_wowo_comments(site_id)
    return render_template("site.html", detail=detail, sub_site=detail["subSite"], comments=comments)
