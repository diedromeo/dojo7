#!/usr/bin/env python3
from flask import Flask, Response, render_template_string, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "samurai_secret_key_2025"

SECRET_DIR = "panel_9f3b"
LOG_SUBDIR = "logs"
STATIC_ROOT = os.path.join(app.root_path, "static")

# create structure
LOG_DIR = os.path.join(STATIC_ROOT, SECRET_DIR, LOG_SUBDIR)
os.makedirs(LOG_DIR, exist_ok=True)

# --- fake log ---
LOG_CONTENT = """[2025-10-28T05:01:22Z] INFO  - user - login ok user=bladeshadow pass=moonlitsteel@2025 from 102.54.13.88
[2025-10-28T06:07:11Z] INFO  - system - cleanup done
"""
with open(os.path.join(LOG_DIR, "access.log"), "w") as f:
    f.write(LOG_CONTENT)

# --- main ascii ---
ASCII_ART = r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⢀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⢠⡇⢀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⢸⡇⣼⢃⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣷⣸⠁⣿⣸⣿⡿⠀⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⣎⣿⣿⣰⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢃⣿⣿⣿⣿⣿⢋⣶⣶⣶⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣶⣤⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡇⣿⣿⣿⠿⣛⣩⣭⣭⣭⣭⣉⣙⡛⣋⣩⣥⣴⣶⣶⣶⣶⣶⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠇⣾⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⣛⡛⠛⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠁⠚⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣡⣴⣾⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣏⣼⣿⣿⣿⣿⣿⣯⣍⣛⠿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⠏⢻⣿⣿⣿⣿⣿⣿⣿⠿⠛⢛⣛⠛⠻⠿⣷⣤⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⣿⣿⣶⣷⣦⣝⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣍⣝⡛⠿⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⢰⡿⣫⣿⣿⣿⡟⣿⣿⡇⢸⣿⣿⣿⣿⠿⢿⣿⣷⣦⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣇⣡⢾⣿⣿⣿⡟⣸⣿⣿⡇⢸⣿⣿⣿⣿⣿⣷⣦⣌⡙⠛⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⢋⣵⣿⣿⣿⣿⢡⣿⣿⣿⠃⢸⣿⣿⣿⣿⣤⣬⣙⡛⠿⢷⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣶⣿⣿⣿⣿⣿⠇⣘⣩⣿⣿⠀⢸⣿⣿⣿⣿⡛⡻⠿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣵⣾⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣷⣦⣌⡙⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠿⠟⠛⠻⢿⣿⣿⣿⣿⠀⢾⣿⣿⣿⣿⣴⣮⣍⡛⠻⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠿⠛⠉⣠⣴⣾⠟⣃⣤⠙⣿⣿⣿⡀⠻⠿⢿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⡿⢛⣩⣴⣿⣿⣿⣧⠘⣿⣿⣿⣶⣦⣤⣄⣀⣈⠉⠙⠻⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠙⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⡛⢁⣼⣿⣿⣿⡿⠟⣋⣵⣿⣿⡇⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⡟⣿⣿⣿⣿⣿⡿⠟⣠⣿⣿⣿⣿⣿⣿⣿⣟⢻⡉⣛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠀⠈⠁⠉⠙⠉⠀⠀⠉⠉⠉⢛⠛⠛⠿⠿⠿⢠⢇⣿⣿⣿⣿⣿⣿⡿⢋⣉⣉⠛⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣡⣴⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣭⣭⣿⣿⣿⣿⠿⢿⣿⣿⣿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡿⣿⣟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠉⠙⠛⠿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣙⣋⣭⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⣿⣿⣿⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⡟⠰⠿⠿⠿⠿⠿⣿⢿⣿⣿⣿⣿⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⢣⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⡸⠿⠿⠿⢿⣿⡇⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢿⣿⣿⣷⣦⣀⠀
⠀⠀⠀⠀⠀⠀⣾⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⠧
⠀⠀⠀⠀⠀⠀⣿⡇⠾⢿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⠇⣶⣶⣶⣶⣶⣶⣦⣼⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⡇⠿⠿⠿⠿⠿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣤⣤⣤⣤⣥⣾⣿⣿⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠿⠿⠿⠿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢼⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# --- html templates ---

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>The Watchful Gate</title>
  <link href="https://fonts.googleapis.com/css2?family=MedievalSharp&family=Spectral+SC:wght@600&display=swap" rel="stylesheet">
  <style>
    html,body{height:100%;margin:0;background:#0b0303;color:#f5e6e6;font-family:'Spectral SC','MedievalSharp',serif;}
    .wrap{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:30px;}
    .panel{width:100%;max-width:1200px;padding:20px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);}
    h1{color:#ff3b3b;margin:0 0 12px;font-size:32px;text-align:center;}
    pre{white-space:pre;overflow:visible;font-size:12px;line-height:12px;font-family:'Courier New',monospace;color:#b31919;margin:0 auto 16px auto;text-align:center;}
    .type{background:rgba(0,0,0,0.3);padding:16px;border-left:5px solid #5c0000;border-radius:8px;text-align:center;}
    .type-text{color:#ff4d4d;font-size:20px;letter-spacing:1px;}
    .caret{display:inline-block;width:8px;height:22px;background:#ff4d4d;margin-left:6px;animation:blink 1s steps(2) infinite;}
    @keyframes blink{50%{opacity:0}}
    #samuraiImage{width:100%;max-width:600px;margin:20px auto 0;display:none;border-radius:10px;box-shadow:0 10px 30px rgba(255,0,0,0.3);opacity:0;transform:translateY(40px);transition:all 1.5s ease;}
    #samuraiImage.show{display:block;opacity:1;transform:translateY(0);}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <h1>The Watchful Gate</h1>
      <pre>{{ ascii }}</pre>
      <div class="type">
        <div class="type-text" id="txt"></div><div class="caret"></div>
      </div>
      <img id="samuraiImage" src="https://images.squarespace-cdn.com/content/v1/5610aa0fe4b0b4bcd8d049d4/1444599476948-W18OS5OCHO7BZIKWW6IJ/image-asset.jpeg?format=2500w" alt="samurai">
    </div>
  </div>
<script>
const lines=[
  "You stand before the Watchful Gate.",
  "The air hums with forgotten steel.",
  "Whispers of battles past echo in silence...",
  "Those who seek must see without sight.",
  "—"
];
const txt=document.getElementById('txt');
async function typeLines(){
  for(const line of lines){await typeLine(line);await sleep(700);}
  const img=document.getElementById('samuraiImage');
  img.classList.add('show');
}
function typeLine(line){
  return new Promise(res=>{
    let i=0;
    (function step(){
      if(i<=line.length){txt.textContent=line.slice(0,i++);setTimeout(step,40+Math.random()*40);}
      else res();
    })();
  });
}
function sleep(ms){return new Promise(r=>setTimeout(r,ms));}
window.addEventListener('load',typeLines);
</script>
</body>
</html>
"""

LOGIN_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"><title>Hidden Samurai Panel</title>
  <link href="https://fonts.googleapis.com/css2?family=Spectral+SC:wght@600&display=swap" rel="stylesheet">
  <style>
    body{background:#0b0303;color:#f6e6e6;font-family:'Spectral SC',serif;text-align:center;padding-top:100px;}
    input{background:#1a0505;border:1px solid #800000;color:#ff4d4d;font-size:18px;padding:10px 14px;margin:5px;border-radius:6px;}
    button{background:#5c0000;color:white;border:none;padding:10px 18px;font-size:18px;border-radius:8px;cursor:pointer;}
    h2{color:#ff4d4d;}
    .error{color:#ff6060;}
  </style>
</head>
<body>
  <h2>Hidden Samurai Panel</h2>
  <form method="POST">
    <input name="username" placeholder="username"><br>
    <input type="password" name="password" placeholder="password"><br>
    <button type="submit">Enter</button>
  </form>
  {% if error %}<p class="error">{{ error }}</p>{% endif %}
</body></html>
"""

FLAG_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>⚔️ The Samurai Flag ⚔️</title>
  <link href="https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap" rel="stylesheet">
  <style>
    body{background:#0b0303;color:#f8e9b0;font-family:'UnifrakturCook',serif;text-align:center;padding-top:100px;}
    .scroll{display:inline-block;border:2px solid #b8860b;padding:30px 60px;border-radius:10px;box-shadow:0 0 30px rgba(255,200,0,0.3);}
    h1{font-size:40px;margin-bottom:20px;color:#ffcc33;}
    p{font-size:22px;line-height:1.6;}
  </style>
</head>
<body>
  <div class="scroll">
    <h1>⚔️ FLAG ⚔️</h1>
    <p>CTF7{SPIRIT_OF_THE_BLADE_2025}</p>
  </div>
</body></html>
"""

# --- Routes ---
@app.route("/")
def home():
    return render_template_string(INDEX_HTML, ascii=ASCII_ART)

@app.route("/robots.txt")
def robots():
    return Response(f"User-agent: *\nDisallow: /{SECRET_DIR}/\n", mimetype="text/plain")

@app.route(f"/{SECRET_DIR}/")
def panel():
    return """<h2 style='color:red;font-family:monospace;background:#0b0303;padding:20px'>
    Forbidden Access<br><a href='/panel_9f3b/login' style='color:#ff4d4d'>Login</a><br>
    <a href='/panel_9f3b/logs/access.log' style='color:#ff4d4d'>Logs</a></h2>"""

@app.route(f"/{SECRET_DIR}/logs/<path:filename>")
def serve_log(filename):
    return send_from_directory(LOG_DIR, filename)

@app.route(f"/{SECRET_DIR}/login", methods=["GET","POST"])
def login():
    error=None
    if request.method=="POST":
        user=request.form.get("username","")
        pw=request.form.get("password","")
        if user=="bladeshadow" and pw=="moonlitsteel@2025":
            session["flag"]=True
            return redirect(url_for("flag"))
        else:
            error="Access Denied — the gate rejects you."
    return render_template_string(LOGIN_HTML, error=error)

@app.route(f"/{SECRET_DIR}/flag")
def flag():
    if not session.get("flag"):
        return redirect(url_for("login"))
    return render_template_string(FLAG_HTML)

if __name__ == "__main__":
    print("⚔️  Samurai CTF full version running at http://127.0.0.1:5000")
    app.run(debug=True)
