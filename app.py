import urllib.parse
from flask import Flask, request, render_template
import wowo

app = Flask(__name__)
app.jinja_env.globals.update(bd09_to_gaode=wowo.bd09_to_gaode)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sites")
def sites():
    range = request.args.get("range", 20, type=int)
    longitude = request.args.get("longitude", type=float)
    latitude = request.args.get("latitude", type=float)
    page = request.args.get("page", 0, type=int)
    page_size = request.args.get("page_size", 10, type=int)
    sites = wowo.get_wowo_list(longitude, latitude, range=range)
    details = []
    for site in sites:
        detail = wowo.get_wowo_detail(site["siteId"])
        details.append(detail)
    details.sort(key=lambda x: x["countCollect"], reverse=True)
    total = len(details)
    start = page * page_size
    end = (page + 1) * page_size
    if start > total:
        start = total
    if end > total:
        end = total
    details = details[start:end]

    def create_page_url(page):
        url = urllib.parse.urlparse(request.url)
        qs = urllib.parse.parse_qs(url.query)
        qs["page"] = page
        return urllib.parse.urlunparse(url._replace(query=urllib.parse.urlencode(qs, doseq=True)))

    prev_url = create_page_url(page - 1) if page > 0 else None
    next_url = create_page_url(page + 1) if end < total else None
    return render_template("sites.html", details=details, total=total, range=range, start=start, end=end, prev_url=prev_url, next_url=next_url)


@app.route("/site/<site_id>")
def site(site_id):
    detail = wowo.get_wowo_detail(site_id)
    comments = wowo.get_wowo_comments(site_id)
    return render_template("site.html", detail=detail, sub_site=detail["subSite"], comments=comments)


@app.route("/raw_site/<site_id>")
def raw_site(site_id):
    detail = wowo.get_wowo_detail(site_id)
    return detail
