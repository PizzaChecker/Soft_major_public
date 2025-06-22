from flask import Blueprint, render_template, redirect
from flask_csp.csp import csp_header

main_route_blue = Blueprint('main_route', __name__)

@main_route_blue.route("/")
@csp_header({
    "base-uri": "'self'",
    "default-src": "'self'",
    "style-src": "'self'",
    "script-src": "'self'",
    "img-src": "'self' data:",
    "media-src": "'self'",
    "font-src": "'self'",
    "object-src": "'self'",
    "child-src": "'self'",
    "connect-src": "'self'",
    "worker-src": "'self'",
    "report-uri": "/csp_report",
    "frame-ancestors": "'none'",
    "form-action": "'self'",
    "frame-src": "'none'",
})
def index():
    return render_template("index.html")

@main_route_blue.route("/index", methods=["GET"])
@main_route_blue.route("/index.htm", methods=["GET"])
@main_route_blue.route("/index.html", methods=["GET"])
@main_route_blue.route("/index.asp", methods=["GET"])
@main_route_blue.route("/index.php", methods=["GET"])
def root():
    return redirect("/", 302)