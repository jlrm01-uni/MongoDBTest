import logging
from urllib.parse import urlparse, urljoin

import flask
from flask import Flask, render_template, request, redirect, url_for
from creature import Creature, Ability
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import flask_discord

app = Flask(__name__)

app.secret_key = "creature den secret website"

app.config["DISCORD_CLIENT_ID"] = 1090340767857393664    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "MCedydMbwEGyargpUOc8nPFybeBunGCE"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "MTA5MDM0MDc2Nzg1NzM5MzY2NA.GDMOHL.lSP2CWxjYHWOUve_3h2qT0BVAgYQ7OcDJEzr88" # Required to access BOT resources.

discord = DiscordOAuth2Session(app)


@app.route("/login")
def login():
    return discord.create_session(data=dict(next=request.args.get("next")),
                                  scope=["identify"], permissions=8)


@app.route("/callback")
def callback():
    try:
        data = discord.callback()

        return redirect(data.get("next", url_for(".home")))
    except Exception as exc:
        logging.error(f"Error during callback: {exc}")
        return redirect(url_for("home"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    next = flask.request.args.get("next")

    if not is_safe_url(next):
        return flask.abort(400)

    return redirect(url_for("login", next=request.full_path))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route("/logout")
def logout():
    discord.revoke()
    return redirect(url_for("login"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/den")
@requires_authorization
def den():
    all_creatures = Creature.objects()

    return render_template("den.html",
                           all_creatures=all_creatures)


@app.route("/creature")
@requires_authorization
def creature():
    name = request.args.get("name")

    creature = Creature.objects(name=name).first()

    return render_template("creature.html", name=name, creature=creature)


@app.route("/abilities")
@requires_authorization
def abilities():
    all_abilities = Ability.objects()

    return render_template("abilities.html", all_abilities=all_abilities)


@app.route("/ability")
@requires_authorization
def ability():
    name = request.args.get("name")

    current_ability = Ability.objects(name=name).first()

    creatures_with_ability = Creature.objects(ability=current_ability)

    return render_template("ability_info.html", current_ability=current_ability,
                           all_creatures=creatures_with_ability)


if __name__ == '__main__':
    app.run(debug=True)
