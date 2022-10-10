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


@app.route("/current_location")
def current_location():
    return render_template("current_location.html")


@app.route("/location_picker")
def location_picker():
    return render_template("location_picker.html")


@app.route("/sites")
def sites():
    location_name = request.args.get("location_name")
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
    return render_template("sites.html", details=details, total=total, location_name=location_name, range=range, start=start, end=end, prev_url=prev_url, next_url=next_url)


@app.route("/site/<site_id>")
def site(site_id):
    detail = wowo.get_wowo_detail(site_id)
    sub_site=detail["subSite"]
    comments = wowo.get_wowo_comments(site_id)
    icons = wowo.get_wowo_icons()

    def get_icon_key(icon):
        return "selectedIcon" if icon["id"] in sub_site["iconList"] else "unselectedIcon"

    icons = [i[get_icon_key(i)] for i in icons]
    return render_template("site.html", site_id=site_id, detail=detail, sub_site=sub_site, comments=comments, icons=icons)


@app.route("/raw_site/<site_id>")
def raw_site(site_id):
    detail = wowo.get_wowo_detail(site_id)
    return detail
