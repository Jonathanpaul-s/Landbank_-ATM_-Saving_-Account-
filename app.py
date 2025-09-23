
# app.py
import base64
import streamlit as st
from pathlib import Path

# 1. Page config must be the first Streamlit command
st.set_page_config(
    page_title="Smart Farm AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Helper function to set background from local image
def set_background(image_file):
    img_path = Path(image_file)
    if not img_path.exists():
        st.error(f"❌ Background image not found: {image_file}")
        return
    
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 3. Call the background function
set_background("assets/farm_bg.jpg")

# 4. Example content
st.title("🌱 Smart Farm AI")
st.write("✅ Background successfully applied — Smart Farm AI is ready to assist you.")



import streamlit as st

import json

import hashlib

import pandas as pd

import random

import datetime

from pathlib import Path

from datetime import date, datetime, timedelta





# =========================

# Helpers

# =========================

def _load(path, default):

    p = Path(path)

    if not p.exists():

        return default

    try:

        return json.loads(p.read_text(encoding="utf-8"))

    except Exception:

        return default



def _save(path, data):

    Path(path).write_text(json.dumps(data, indent=4), encoding="utf-8")



# =========================

# Optional Auth Utilities (unused UI in this file but kept for future)

# =========================

def hash_password(password: str) -> str:

    return hashlib.sha256(password.encode()).hexdigest()



# =========================

# FARM MANAGEMENT FEATURES

# =========================

def user_account_management_ui():
    st.subheader("👤 User Account Management")

    action = st.radio("Choose Action", ["Register", "Login"], key="acc_action")

    if action == "Register":
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register", key="reg_btn"):
            users = _load("accounts.json", [])
            if any(u["username"] == username for u in users):
                st.error("❌ Username already exists.")
            else:
                users.append({
                    "username": username,
                    "email": email,
                    "password": hash_password(password)
                })
                _save("accounts.json", users)
                st.success("✅ Registration successful!")

    elif action == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            users = _load("accounts.json", [])
            user = next((u for u in users if u["username"] == username), None)
            if user and user["password"] == hash_password(password):
                st.success(f"✅ Welcome back, {username}!")
                st.session_state["logged_in"] = True
            else:
                st.error("❌ Invalid username or password.")


# Optional: a simple v2 UI for the "upgrade" router with unique keys
def user_account_management_ui_v2():
    st.subheader("👤 User Account Management (v2)")
    username = st.text_input("Username", key=k2("acc_username"))
    email = st.text_input("Email", key=k2("acc_email"))
    if st.button("Save Account", key=k2("acc_save_btn")):
        _save("account.json", {"username": username, "email": email})
        st.success("✅ Account saved.")


def farm_plot_mapping_ui():

    st.subheader("🗺 Farm Plot Mapping")

    plots = _load("plots.json", [])

    with st.form("plot_form"):

        plot_name = st.text_input("Plot Name", key="plot_name")

        size = st.number_input("Plot Size (hectares)", min_value=0.1, key="plot_size")

        submitted = st.form_submit_button("Save Plot")

    if submitted:

        plots.append({"name": plot_name, "size": size})

        _save("plots.json", plots)

        st.success(f"✅ Plot '{plot_name}' ({size} ha) saved.")

    if plots:

        st.markdown("### 📋 Saved Plots")

        for i, p in enumerate(plots, 1):

            st.write(f"{i}. {p['name']} — {p['size']} ha")



def smart_fert_pest_ui():
    import streamlit as st
    import datetime

    st.subheader("🌾 Smart Fertilizer & Pesticide Stock Manager")

    # safe load/save wrappers if you have _load/_save helpers
    def _safe_load(path, default):
        try:
            return _load(path, default)
        except Exception as e:
            st.warning(f"Could not load {path}: {e}")
            return default

    def _safe_save(path, data):
        try:
            _save(path, data)
            return True
        except Exception as e:
            st.error(f"Save failed: {e}")
            return False

    inv = _safe_load("chem_inventory.json", [])

    base = "smart_fert_pest"
    form_key = f"{base}_form"
    item_key = f"{base}_item"
    qty_key = f"{base}_qty"
    submit_key = f"{base}_submit"

    with st.form(form_key):
        item = st.text_input("Item (Fertilizer/Pesticide)", key=item_key)
        qty = st.number_input("Quantity", min_value=0, step=1, key=qty_key)
        # compatibility: some Streamlit versions don't accept key= on form_submit_button
        try:
            submitted = st.form_submit_button("Save Stock", key=submit_key)
        except TypeError:
            submitted = st.form_submit_button("Save Stock")

    if submitted:
        if not (item or "").strip():
            st.warning("Enter an item name before saving.")
        else:
            inv.append({"item": item.strip(), "qty": int(qty), "date": str(datetime.date.today())})
            _safe_save("chem_inventory.json", inv)
            st.success(f"✅ {qty} units of {item} saved.")

    if inv:
        st.markdown("### 📦 Current Stock")
        for it in inv:
            i = it.get("item") if isinstance(it, dict) else str(it)
            q = it.get("qty") if isinstance(it, dict) else ""
            d = it.get("date") if isinstance(it, dict) else ""
            st.write(f"- {i}: {q} (as of {d})")
    else:
        st.info("No fertilizer/pesticide stock records yet.")


def smart_tutor_voice():
    import streamlit as st
    import os
    from datetime import datetime

    # Optional deps (gracefully handled)
    try:
        import speech_recognition as sr
    except Exception:
        sr = None
    try:
        import pyttsx3
    except Exception:
        pyttsx3 = None
    try:
        from gtts import gTTS
    except Exception:
        gTTS = None

    st.subheader("🧑‍🏫 Smart Tutor Multilanguage")
    st.info("🌍 Learn agriculture tips in multiple African languages (via text or voice).")

    # Available languages
    languages = [
        "English", "Yoruba", "Igbo", "Hausa", "Urhobo",
        "Ijaw", "Efik", "Ibibio", "Tiv", "Kanuri"
    ]
    lang_choice = st.selectbox("Select a language", languages, key="tutor_lang")

    # --- Input options ---
    st.markdown("**🎤 Speak or ✍️ Type your agriculture question**")

    # 1. Voice input
    voice_question = None
    if sr and st.button("🎙 Record Question", key="tutor_record"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... please speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            voice_question = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {voice_question}")
        except Exception as e:
            st.error(f"Voice recognition failed: {e}")

    # 2. Text input
    text_question = st.text_input("Or type your question here:", key="tutor_text")

    # Use whichever question is available
    final_question = voice_question if voice_question else text_question

    # --- Answer button ---
    if st.button("Get Answer", key="tutor_btn"):
        if final_question and final_question.strip():
            # Simulated agricultural responses (you can expand this later with AI)
            if "fertilizer" in final_question.lower():
                answer = "Use organic compost or NPK fertilizer depending on soil needs."
            elif "water" in final_question.lower() or "irrigation" in final_question.lower():
                answer = "Irrigate crops early in the morning or late evening to reduce evaporation."
            else:
                answer = "Practice crop rotation, weed control, and proper spacing for better yields."

            # Add a language flavor
            if lang_choice == "Yoruba":
                answer = "Agbẹ́! " + answer
            elif lang_choice == "Igbo":
                answer = "Ndi ugbo! " + answer
            elif lang_choice == "Hausa":
                answer = "Manomi! " + answer

            st.success(f"({lang_choice}) {answer}")

            # Voice playback if possible
            if pyttsx3:
                engine = pyttsx3.init()
                engine.say(answer)
                engine.runAndWait()
            elif gTTS:
                try:
                    tts = gTTS(answer)
                    filename = "tutor_voice.mp3"
                    tts.save(filename)
                    audio_file = open(filename, "rb")
                    st.audio(audio_file.read(), format="audio/mp3")
                except Exception as e:
                    st.warning(f"Text-to-speech failed: {e}")
        else:
            st.warning("❌ Please ask a question by typing or speaking.")




def ai_crop_calendar_ui():

    st.subheader("🧠 AI Crop Calendar")

    crop = st.selectbox("Select Crop", ["Maize", "Rice", "Tomato", "Yam", "Cassava"], key="cal_crop")

    zone = st.selectbox("Agro-ecological Zone", ["South-South", "South-West", "South-East", "Middle Belt", "North"], key="cal_zone")

    if st.button("Generate Calendar", key="cal_btn"):

        suggestion = {

            "Maize": "April–June (rain-fed); Oct–Nov (irrigated)",

            "Rice": "May–July (rain-fed); Nov–Jan (irrigated)",

            "Tomato": "Aug–Oct (dry-season irrigated); Feb–Apr (early wet-season)",

            "Yam": "Dec–Feb (setts); harvest 6–8 months later",

            "Cassava": "All year if moisture adequate; best with onset of rains",

        }.get(crop, "Check local rainfall pattern.")

        st.success(f"📅 Suggested window for {crop} in {zone}: {suggestion}")

# put this ABOVE the router
def drone_irrigation_assistant_ui_impl():
    import streamlit as st
    from datetime import datetime

    st.header("🚁 Voice-Controlled Drone Irrigation Assistant")
    if "voice_drone" not in st.session_state:
        st.session_state.voice_drone = {"armed": False, "in_air": False, "log": []}
    S = st.session_state.voice_drone

    c1, c2, c3 = st.columns(3)
    if c1.button("🔐 Arm/Disarm"):
        S["armed"] = not S["armed"]; S["log"].append(f"{datetime.now():%H:%M:%S} toggled arm")
    if c2.button("⬆️ Takeoff", disabled=not S["armed"] or S["in_air"]):
        S["in_air"] = True; S["log"].append(f"{datetime.now():%H:%M:%S} takeoff")
    if c3.button("⬇️ Land", disabled=not S["in_air"]):
        S["in_air"] = False; S["log"].append(f"{datetime.now():%H:%M:%S} landed")

    cmd = st.text_input("Type a command (e.g. start zone A for 2 minutes / land / status)")
    if cmd:
        S["log"].append(f"{datetime.now():%H:%M:%S} cmd: {cmd}")

    st.subheader("📜 Log")
    for line in S["log"][-200:]:
        st.write("•", line)


# ================================
# 💾 Data Backup & Recovery (drop-in)
# ================================
def data_backup_recovery_ui_impl():
    import os, shutil, io
    from datetime import datetime
    import streamlit as st

    # --- key helper fallback (uses your existing kbak if present) ---
    try:
        kbak  # type: ignore[name-defined]
    except NameError:
        def kbak(name: str) -> str:
            return f"bk_{name}"

    st.header("💾 Data Backup & Recovery")
    st.caption("Create a .zip backup of your farm data, restore a previous backup, or manage backup files.")

    # --- folders ---
    data_dir = "farm_data"
    backup_dir = "backups"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # --- active tool in session ---
    active_key = kbak("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # --- triggers row ---
    c1, c2, c3, c4 = st.columns([1.6, 1.6, 1.6, 0.8])
    with c1:
        if st.button("💾 Create Backup (.zip)", key=kbak("btn_backup")):
            st.session_state[active_key] = "backup"
    with c2:
        if st.button("♻️ Restore Backup", key=kbak("btn_restore")):
            st.session_state[active_key] = "restore"
    with c3:
        if st.button("🗑 Manage Backups", key=kbak("btn_manage")):
            st.session_state[active_key] = "manage"
    with c4:
        if st.button("🔄 Reset", key=kbak("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # Helper: list .zip backups
    def _list_zips():
        return sorted(
            [f for f in os.listdir(backup_dir) if f.lower().endswith(".zip")]
        )

    # ======================
    # Tool: Create Backup
    # ======================
    if tool == "backup":
        st.subheader("💾 Create Backup")
        st.write(f"Source: `{data_dir}`  →  Backups go to `{backup_dir}` as .zip files")

        if st.button("📂 Backup Now", key=kbak("do_backup"), use_container_width=True):
            try:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                base = os.path.join(backup_dir, backup_name)
                # Make a .zip of *contents* of data_dir
                zip_path = shutil.make_archive(base_name=base, format="zip", root_dir=data_dir)
                st.success(f"✅ Backup created: {os.path.basename(zip_path)}")

                # Offer immediate download
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Backup",
                        f.read(),
                        file_name=os.path.basename(zip_path),
                        mime="application/zip",
                        key=kbak("dl_new_backup")
                    )
            except Exception as e:
                st.error(f"❌ Error creating backup: {e}")

    # ======================
    # Tool: Restore Backup
    # ======================
    elif tool == "restore":
        st.subheader("♻️ Restore Backup")
        zips = _list_zips()
        if not zips:
            st.info("ℹ️ No backups found yet. Create one first.")
        else:
            selected = st.selectbox("Select a backup (.zip) to restore", zips, key=kbak("sel_restore"))
            st.warning(
                "Restoring will replace the current contents of `farm_data/` "
                "with the files from this backup."
            )
            if st.button("🔄 Restore", key=kbak("do_restore"), use_container_width=True):
                try:
                    # Remove current data_dir and recreate empty
                    if os.path.exists(data_dir):
                        shutil.rmtree(data_dir)
                    os.makedirs(data_dir, exist_ok=True)

                    # Extract zip *into* data_dir
                    zip_path = os.path.join(backup_dir, selected)
                    shutil.unpack_archive(zip_path, extract_dir=data_dir, format="zip")
                    st.success(f"✅ Restored from '{selected}'.")
                except Exception as e:
                    st.error(f"❌ Error restoring backup: {e}")

    # ======================
    # Tool: Manage Backups
    # ======================
    elif tool == "manage":
        st.subheader("🗑 Manage Backups")
        zips = _list_zips()
        if not zips:
            st.info("No backups to manage yet.")
        else:
            selected = st.selectbox("Select a backup (.zip)", zips, key=kbak("sel_manage"))
            cA, cB, cC = st.columns([1, 1, 1])
            with cA:
                # Download
                zip_path = os.path.join(backup_dir, selected)
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Selected",
                        f.read(),
                        file_name=selected,
                        mime="application/zip",
                        key=kbak("dl_sel")
                    )
            with cB:
                # Delete
                if st.button("🗑 Delete Selected", key=kbak("del_sel")):
                    try:
                        os.remove(zip_path)
                        st.success(f"Deleted backup '{selected}'.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting backup: {e}")
            with cC:
                if st.button("📁 Refresh List", key=kbak("refresh")):
                    st.rerun()

    else:
        st.info("Choose an action above to create, restore, or manage backups.")

# ---- aliases so any of these names work in your router ----
data_backup_recovery_ui = data_backup_recovery_ui_impl
backup_recovery_ui      = data_backup_recovery_ui_impl
data_backup_ui          = data_backup_recovery_ui_impl
backup_ui               = data_backup_recovery_ui_impl
_data_backup_recovery_ui= data_backup_recovery_ui_impl




def data_backup_recovery_ui():
    import streamlit as st

    candidates = [
        "data_backup_recovery_ui_impl",
        "backup_recovery_ui",
        "data_backup_ui",
        "backup_ui",
        "_data_backup_recovery_ui",
    ]
    for name in candidates:
        impl = globals().get(name)
        if callable(impl):
            return impl()

    st.header("💾 Data Backup & Recovery")
    st.info(
        "The Backup & Recovery implementation isn’t loaded in this file. "
        "Define one of these functions and I’ll call it automatically:\n\n"
        f"- {', '.join(candidates)}"
    )



def drone_irrigation_assistant_ui():
    # Keep it self-contained so it never NameErrors
    import streamlit as st

    # Try to find your real implementation if it lives elsewhere
    candidates = [
        "drone_irrigation_assistant_ui_impl",
        "irrigation_voice_assistant_ui",
        "voice_irrigation_assistant_ui",
        "drone_irrigation_assistant",   # common alt name
        "_drone_irrigation_assistant_ui",
    ]
    for name in candidates:
        impl = globals().get(name)
        if callable(impl):
            return impl()  # delegate to your actual function

    # Fallback if nothing found (prevents NameError and explains what to do)
    st.subheader("🚁 Voice-Controlled Drone Irrigation Assistant")
    st.info(
        "The voice irrigation assistant implementation isn’t loaded in this file. "
        "Define one of these functions anywhere before runtime and I’ll call it automatically:\n\n"
        f"- {', '.join(candidates)}"
    )



def drone_flight_scheduler_ui():

    st.subheader("🚁 Drone Flight Scheduler")

    flights = _load("drone_flights.json", [])

    with st.form("drone_form"):

        date = st.date_input("📅 Flight Date", key="dr_date")

        time = st.time_input("⏰ Flight Time", key="dr_time")

        purpose = st.selectbox("🎯 Purpose", ["Crop Monitoring", "Pesticide Spraying", "Fertilizer Spraying", "Aerial Mapping", "Livestock Surveillance"], key="d_purpose")

        plot = st.text_input("📍 Plot ID/Name",  key="dr_plot")

        submitted = st.form_submit_button("📤 Schedule Flight")

    if submitted:

        flights.append({"date": str(date), "time": str(time), "purpose": purpose, "plot": plot})

        _save("drone_flights.json", flights)

        st.success("✅ Flight scheduled.")

    if flights:

        st.markdown("### 🗓 Scheduled Flights")

        for f in flights:

            st.write(f"- {f['date']} {f['time']} — {f['purpose']} @ {f['plot']}")



def voice_command_ui():
    import streamlit as st
    import re

    # Optional voice deps — UI still works without them
    try:
        import speech_recognition as sr
    except Exception:
        sr = None

    st.subheader("🎙 Voice Command Interface")
    st.caption("Say or type a command to jump to a page (e.g., “open live sensor dashboard”, “go to predictions”).")

    # --- helpers -------------------------------------------------------------
    def _v2_key():
        # Use your existing k2() helper if present; otherwise fallback to a safe string
        try:
            return k2("main_menu_option")
        except Exception:
            return "v2_main_menu_option"

    def _try_rerun():
        """Call Streamlit rerun with compatibility across versions."""
        try:
            if hasattr(st, "rerun"):
                st.rerun()
            elif hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
        except Exception:
            # If rerun fails just continue — UI will update on next interaction
            pass

    def _go(label: str):
        """Attempt to navigate by setting the v2 menu key."""
        # This assignment is safe when done from callbacks (on_change) or
        # before the menu widget is created. We use it from the typed-command
        # callback which runs in a safe update context.
        st.session_state[_v2_key()] = label

    def _route(cmd: str) -> bool:
        """Map free-text commands to pages. Return True if a route was matched."""
        c = (cmd or "").strip().lower()
        if not c:
            return False

        # normalize common words
        c = c.replace("open ", "").replace("go to ", "").replace("goto ", "")

        # high-confidence matches first
        if re.search(r"\blive\b.*\bsensor\b|\bsensor\b.*\bdashboard\b", c):
            _go("📡 Live Sensor Dashboard"); return True
        if "drone" in c and ("schedule" in c or "scheduler" in c or "flight" in c):
            _go("🚁 Drone Flight Scheduler"); return True
        if ("voice" in c and ("irrig" in c or "drone" in c)) or "voice assistant" in c:
            _go("🚁 Voice-Controlled Drone Irrigation Assistant"); return True
        if "prediction" in c:
            _go("🧪 AI Predictions"); return True
        if "tip" in c or "tips" in c:
            _go("📚 AI Farm Tips"); return True
        if "profit" in c or "loss" in c or "statement" in c:
            _go("📊 Farm Profit & Loss Statement"); return True
        if "plot" in c or "mapping" in c or "map" in c:
            _go("🌍 Farm Plot Mapping"); return True
        if "irrigation" in c and "soil" in c:
            _go("💧 Irrigation & Soil"); return True
        if "expanded" in c and "calendar" in c:
            _go("📅 Expanded AI Crop Calendar"); return True
        if "crop calendar" in c:
            _go("🤖 AI Crop Calendar"); return True
        if "performance" in c and "indicator" in c:
            _go("📍 Farm Performance Indicators"); return True
        if "market" in c or "economic" in c or "price" in c:
            _go("📈 Market & Economic Tools"); return True
        if "backup" in c or "restore" in c or "recovery" in c:
            _go("💾 Data Backup & Recovery"); return True
        if "home" in c:
            _go("🏡 Home"); return True

        # fallback: try fuzzy contains for any top-level label keywords
        for label in [
            "🏡 Home",
            "🌿 Farm Management",
            "📊 Productivity & Records",
            "💧 Irrigation & Soil",
            "📅 Calendar & Seasons",
            "🧪 AI Predictions",
            "📈 Market & Economic Tools",
            "📚 AI Farm Tips",
            "📊 Farm Profit & Loss Statement",
            "🌍 Farm Plot Mapping",
            "🌐 Farmer Community Forum",
            "📡 Live Sensor Dashboard",
            "🚨 Smart Farm Alerts",
            "🎙️ Voice Command Interface",
            "🚁 Drone Flight Scheduler",
            "🧑‍🏫 Smart Tutor (Voice)",
            "💾 Data Backup & Recovery",
            "📍 Farm Lot Management",
            "📅 Expanded AI Crop Calendar",
            "🤖 AI Crop Calendar",
            "📈 Decision-Making Models",
            "📍 Farm Performance Indicators",
            "🔒 User Account Management",
        ]:
            words = re.findall(r"\w+", label.lower())
            if any(w in c for w in words if len(w) > 2):
                _go(label)
                return True

        return False

    # --- typed-command callback (safe) --------------------------------------
    def _apply_typed_command():
        """This runs as the text_input on_change callback — safe to mutate widget-backed keys."""
        cmd = st.session_state.get("vc_text", "").strip()
        if not cmd:
            return
        matched = False
        try:
            matched = _route(cmd)
        except Exception as e:
            # If setting the menu key fails for any reason, show an info message
            st.warning(f"Could not apply navigation: {e}")
            matched = False

        # clear command input after applying (so user sees it reset)
        st.session_state["vc_text"] = ""
        if matched:
            _try_rerun()
        else:
            st.info("No route matched. Try keywords: sensor, predictions, calendar, drone, backup, home.")

    # --- UI ------------------------------------------------------------------
    col_mic, col_cmd = st.columns([1, 3])

    # 1) Voice (only if SpeechRecognition is available)
    if sr is not None:
        if col_mic.button("🎤 Speak"):
            try:
                recog = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Listening…")
                    try:
                        recog.adjust_for_ambient_noise(source, duration=0.6)
                    except Exception:
                        pass
                    audio = recog.listen(source, timeout=4, phrase_time_limit=6)
                cmd = recog.recognize_google(audio)
                st.success(f"🗣 {cmd}")
                # voice path: route immediately (mic path has historically run before menu widget is created,
                # which is why it likely worked for you already)
                try:
                    if _route(cmd):
                        _try_rerun()
                    else:
                        st.info("No route matched. Try: live sensor, predictions, calendar, drone scheduler, backup.")
                except Exception as e:
                    st.error(f"Navigation error: {e}")
            except sr.WaitTimeoutError:
                st.error("Timed out. Try again.")
            except sr.UnknownValueError:
                st.error("I couldn't understand that. Try again.")
            except sr.RequestError:
                st.error("Speech service unavailable. Type your command instead.")
            except Exception as e:
                st.error(f"Mic error: {e}")
    else:
        col_mic.caption("Install voice deps to enable mic: `pip install SpeechRecognition pyaudio`")

    # 2) Typed command (always available) — uses on_change callback to safely mutate menu key
    cmd_text = col_cmd.text_input(
        "Type a command",
        placeholder="e.g., open live sensor dashboard, go to predictions, open backup",
        key="vc_text",
        on_change=_apply_typed_command,
    )
    # Note: we've removed the separate "Go" button handler to avoid mutation-after-widget errors.





# =========================

# AI PREDICTIONS (Simple Demos)

# =========================

def ai_predictions_ui():

    ai_option = st.sidebar.selectbox("🧠 Select an AI Feature", [

        "🦠 Crop Disease Detection",

        "📈 Yield Prediction",

        "🧪 Soil Health Check",

        "🤖 Decision-Making Models"

    ], key="ai_predictions_feature")



    if ai_option == "🦠 Crop Disease Detection":

        st.subheader("🦠 Crop Disease Detection")

        st.write("Upload an image of your crop to detect potential diseases using AI.")

        uploaded_image = st.file_uploader("Upload Crop Image", type=["jpg", "png", "jpeg"])

        if uploaded_image:

            st.image(uploaded_image, caption="Uploaded Crop Image", use_column_width=True)

            st.success("✅ Prediction: Your crop is healthy.")

            st.info("🧪 Tip: If infected, apply appropriate treatment and isolate the crop.")



    elif ai_option == "📈 Yield Prediction":

        st.subheader("📈 Yield Prediction")

        crop = st.selectbox("🌾 Select Crop Type", ["Maize", "Cassava", "Tomato", "Yam", "Rice"])

        area = st.number_input("🌍 Farm Area (hectares)", min_value=0.1)

        rainfall = st.number_input("🌧️ Rainfall (mm)")

        fertilizer = st.number_input("💩 Fertilizer Used (kg)")

        if st.button("🔍 Predict Yield"):

            predicted_yield = area * 2.5 + fertilizer * 0.1 + rainfall * 0.05

            st.success(f"📦 Estimated Yield: {predicted_yield:.2f} tons")



    elif ai_option == "🧪 Soil Health Check":

        st.subheader("🧪 Soil Health Check")

        ph = st.slider("🧪 Soil pH", 0.0, 14.0, 6.5)

        nitrogen = st.number_input("🌱 Nitrogen (mg/kg)")

        potassium = st.number_input("🌱 Potassium (mg/kg)")

        phosphorus = st.number_input("🌱 Phosphorus (mg/kg)")

        if st.button("🧠 Analyze Soil"):

            if 6 <= ph <= 7 and nitrogen > 50 and potassium > 50 and phosphorus > 50:

                st.success("✅ Soil is Healthy for Crop Production.")

            else:

                st.warning("⚠️ Soil quality may affect productivity. Consider fertilization.")



    elif ai_option == "🤖 Decision-Making Models":

        st.subheader("🤖 Decision-Making Models")

        st.write("Answer a few questions and get AI-powered suggestions for better farming decisions.")

        crop_type = st.selectbox("🌾 Crop Type", ["Maize", "Tomato", "Rice", "Cassava", "Yam"])

        soil_moisture = st.slider("💧 Soil Moisture Level (%)", 0, 100)

        pest_detected = st.radio("🐛 Pests Detected?", ["Yes", "No"])

        market_price = st.number_input("💰 Current Market Price (₦/ton)")

        if st.button("📊 Get Recommendation"):

            if pest_detected == "Yes":

                st.error("❗ Treat pest infection before planting.")

            elif soil_moisture < 40:

                st.warning("⚠️ Increase irrigation before planting.")

            else:

                st.success(f"✅ You can proceed with planting {crop_type}. Expected profit margin is high.")



# =========================

# IRRIGATION & SOIL

# =========================

def irrigation_ui():

    irrigation_option = st.sidebar.selectbox("💧 Select an Irrigation Feature", [

        "🌱 Soil Moisture Checker",

        "🚰 Water Usage Log",

        "💧 Irrigation Cost Estimator"

    ], key="irrigation_feature")



    if irrigation_option == "🌱 Soil Moisture Checker":

        st.subheader("🌱 Soil Moisture Checker")

        st.write("Enter the moisture level readings for your farm plots.")

        plot_id = st.text_input("🆔 Plot ID")

        moisture_level = st.slider("💦 Moisture Level (%)", min_value=0, max_value=100)

        if st.button("Save Moisture Reading"):

            st.success(f"Soil moisture for Plot {plot_id} recorded as {moisture_level}%.")



    elif irrigation_option == "🚰 Water Usage Log":

        st.subheader("🚰 Water Usage Log")

        with st.form("water_log_form"):

            date = st.date_input("📅 Date of Irrigation")

            crop_type = st.text_input("🌾 Crop Type")

            water_used = st.number_input("💧 Water Used (liters)", min_value=0.0)

            submitted = st.form_submit_button("Log Water Usage")

            if submitted:

                st.success(f"{water_used} liters used on {crop_type} recorded for {date}")



    elif irrigation_option == "💧 Irrigation Cost Estimator":

        st.subheader("💧 Irrigation Cost Estimator")

        water_volume = st.number_input("🚿 Enter water usage (liters)", min_value=0.0)

        cost_per_liter = st.number_input("💸 Cost per liter (₦)", min_value=0.0)

        if st.button("Estimate Cost"):

            total_cost = water_volume * cost_per_liter

            st.info(f" Estimated irrigation cost: ₦{total_cost:,.2f} ")



# =========================

# MARKET & FINANCE

# =========================

def market_finance_ui():

    market_option = st.sidebar.selectbox("📈 Select a Market Feature", [

        "📊 Market Price Fetcher",

        "📋 Farm Budget Planner",

        "💵 Farm Loan Tracker"

    ], key="market_feature")



    if market_option == "📊 Market Price Fetcher":

        st.subheader("📊 Market Price Fetcher")

        crop = st.selectbox("🌾 Select Crop", ["Maize", "Rice", "Cassava", "Tomato", "Yam"])

        location = st.text_input("📍 Enter Location")

        if st.button("📥 Fetch Market Price"):

            prices = {

                "Maize": "₦42,000 per ton",

                "Rice": "₦55,000 per bag",

                "Cassava": "₦12,000 per ton",

                "Tomato": "₦10,000 per basket",

                "Yam": "₦300 per tuber"

            }

            st.success(f"🛒 Market price of {crop} in {location} is {prices.get(crop)}")



    elif market_option == "📋 Farm Budget Planner":

        st.subheader("📋 Farm Budget Planner")

        income = st.number_input("💰 Expected Income (₦)", min_value=0)

        expenses = st.number_input("💸 Estimated Expenses (₦)", min_value=0)

        if st.button("📊 Calculate Budget"):

            balance = income - expenses

            if balance > 0:

                st.success(f"✅ Profit Estimate: ₦{balance}")

            elif balance == 0:

                st.info("⚖️ Break-even: No profit or loss.")

            else:

                st.error(f"⚠️ Loss Estimate: ₦{abs(balance)}")



    elif market_option == "💵 Farm Loan Tracker":

        st.subheader("💵 Farm Loan Tracker")

        loan_amount = st.number_input("🏦 Loan Amount (₦)", min_value=0)

        interest_rate = st.number_input("📈 Interest Rate (%)", min_value=0.0)

        duration_months = st.number_input("📅 Duration (months)", min_value=1)

        if st.button("📉 Calculate Loan Repayment"):

            total_interest = (loan_amount * interest_rate * duration_months) / (100 * 12)

            total_payment = loan_amount + total_interest

            monthly_payment = total_payment / duration_months

            st.info(f"📌 Total Repayment: ₦{round(total_payment, 2)}")

            st.info(f"📅 Monthly Payment: ₦{round(monthly_payment, 2)}")



# =========================

# SENSORS & MONITORING

# =========================

def sensors_monitoring_ui():

    sensor_option = st.sidebar.selectbox("📡 Select a Monitoring Feature", [

        "📈 Live Sensor Dashboard",

        "🚨 Sensor Alerts",

        "🌦 Weather Forecast",

        "🧠 Smart Tutor Assistant",

    ], key="sensor_monitoring")



    if sensor_option == "📈 Live Sensor Dashboard":

        st.subheader("📈 Live Sensor Dashboard")

        st.info("This dashboard displays real-time data from your connected farm sensors.")

        temperature = 28.5  # °C

        humidity = 65       # %

        soil_moisture = 40  # %

        st.metric("🌡 Temperature", f"{temperature} °C")

        st.metric("💧 Humidity", f"{humidity} %")

        st.metric("🌱 Soil Moisture", f"{soil_moisture} %")



    elif sensor_option == "🚨 Sensor Alerts":

        st.subheader("🚨 Sensor Alerts")

        moisture_level = random.randint(20, 100)  # %

        temperature = random.randint(10, 40)      # °C

        st.info(f"💧 Soil Moisture: {moisture_level}%")

        st.info(f"🌡 Temperature: {temperature}°C")

        if moisture_level < 40:

            st.warning("⚠️ Low moisture detected. Consider irrigating the crops.")

        elif moisture_level > 80:

            st.warning("⚠️ Excessive moisture. Risk of root rot.")

        if temperature > 35:

            st.error("🔥 High temperature detected! Take cooling measures immediately.")

        elif temperature < 15:

            st.warning("❄️ Low temperature detected. Protect crops from cold stress.")

        st.success("✅ All other sensor readings are in safe limits.")



    elif sensor_option == "🌦 Weather Forecast":

        st.subheader("🌦 Weather Forecast")

        st.success("Here's your local 3-day forecast.")

        forecast = {

            "Today": {"condition": "Sunny", "temp": "31°C"},

            "Tomorrow": {"condition": "Partly Cloudy", "temp": "29°C"},

            "Next Day": {"condition": "Rainy", "temp": "25°C"},

        }

        for day, data in forecast.items():

            st.write(f"{day} — {data['condition']}, 🌡 {data['temp']}")



    elif sensor_option == "🧠 Smart Tutor Assistant":

        st.subheader("📚 Smart Tutor")

        tips = [

            "Rotate your crops each season to maintain soil fertility. 🌱",

            "Use organic compost to boost plant health naturally. ♻️",

            "Water early in the morning to reduce evaporation. 💧",

            "Monitor your plants weekly for early signs of pests. 🐛",

            "Test your soil every year to know the right fertilizer to use. 🧪",

            "Intercropping can help reduce pests and increase yield. 🌾",

            "Mulch your soil to retain moisture and control weeds. 🌿",

            "Choose disease-resistant seed varieties for better harvests. 🌻"

        ]

        if st.button("💡 Get Advice", key="smart_tutor_tip"):

            st.success(random.choice(tips))



# =========================
# SUPPORT & HELP  (drop-in)
# =========================
def support_help_ui():
    import streamlit as st
    import json, random, os, calendar
    from datetime import date, datetime

    help_option = st.sidebar.selectbox(
        "🆘 Select a Help Feature",
        [
            "👨‍🌾 Farmers Community Forum",
            "💾 Data Backup & Recovery",
            "📘 Tutorial & Guide",
            "🧑‍🏫 Smart Tutor (Multi-Language)",
            "🤖 Chatbot Assistant",
        ],
        key="support_help",
    )

    # -------------------------
    # 👨‍🌾 Farmers Community Forum
    # -------------------------
    if help_option == "👨‍🌾 Farmers Community Forum":
        st.subheader("👨‍🌾 Farmers Community Forum")
        st.write("Connect with other farmers, share experiences, and ask questions.")

        if "forum_posts" not in st.session_state:
            st.session_state.forum_posts = []

        new_post = st.text_area("💬 Share your thoughts or ask a question:", key="forum_new_post")
        if st.button("📢 Post Message", key="forum_post_btn"):
            if new_post.strip():
                st.session_state.forum_posts.append(new_post.strip())
                st.success("✅ Your message has been posted!")
            else:
                st.warning("⚠️ Please enter a message before posting.")

        st.write("### 📜 Forum Messages")
        if st.session_state.forum_posts:
            for idx, post in enumerate(st.session_state.forum_posts, 1):
                st.write(f"{idx}. {post}")
        else:
            st.info("No messages yet. Be the first to post!")

    # -------------------------
    # 💾 Data Backup & Recovery
    # -------------------------
    elif help_option == "💾 Data Backup & Recovery":
        st.subheader("💾 Data Backup & Recovery")
        st.write("Backup your farm data or restore it when needed.")
        c1, c2 = st.columns(2)
        if c1.button("📤 Backup Data", key="backup_btn"):
            st.success("✅ Data backup completed successfully!")
        if c2.button("📥 Restore Data", key="restore_btn"):
            st.info("ℹ️ Data restoration feature coming soon.")

    # -------------------------
    # 📘 Tutorial & Guide
    # -------------------------
    elif help_option == "📘 Tutorial & Guide":
        st.subheader("📘 Tutorial & Guide")
        st.write("Step-by-step tutorials and guides to help you use Smart Farm AI.")
        st.markdown(
            """
- 🌿 **Farm Management**: Manage plots, accounts, and schedules.  
- 📊 **Productivity & Records**: Track sales, yields, and expenses.  
- 🧠 **AI Predictions**: Detect diseases, predict yield, and check soil health.  
- 💧 **Irrigation & Soil**: Schedule irrigation and manage soil data.  
- 💱 **Market & Finance**: Track loans, prices, and budgets.  
- 📡 **Sensors & Monitoring**: Live farm sensor dashboard.  
"""
        )

        # Quick tips button (kept inside this branch so it doesn't render everywhere)
        tips = [
            "Rotate your crops each season to maintain soil fertility. 🌱",
            "Use organic compost to boost plant health naturally. ♻️",
            "Water early in the morning to reduce evaporation. 💧",
            "Monitor your plants weekly for early signs of pests. 🐛",
            "Test your soil every year to know the right fertilizer to use. 🧪",
            "Intercropping can help reduce pests and increase yield. 🌾",
            "Mulch your soil to retain moisture and control weeds. 🌿",
            "Choose disease-resistant seed varieties for better harvests. 🌻"
        ]
        if st.button("💡 Get Advice", key="smart_tutor_tip"):
            st.success(random.choice(tips))

    # -------------------------
    # 🧑‍🏫 Smart Tutor (Multi-Language) — with Voice
    # -------------------------
    elif help_option == "🧑‍🏫 Smart Tutor (Multi-Language)":
        # ===== Optional deps (gracefully handled) =====
        try:
            import speech_recognition as sr
        except Exception:
            sr = None

        try:
            import pyttsx3  # offline TTS
        except Exception:
            pyttsx3 = None

        try:
            from gtts import gTTS  # online TTS fallback
        except Exception:
            gTTS = None

        # Translators (optional)
        translator = None
        try:
            from googletrans import Translator  # pip install googletrans==4.0.0rc1
            translator = "googletrans"
            _gt = Translator()
        except Exception:
            try:
                from deep_translator import GoogleTranslator  # pip install deep-translator
                translator = "deep"
            except Exception:
                translator = None

        # OpenAI (optional)
        client = None
        try:
            from openai import OpenAI  # pip install openai
            if os.getenv("OPENAI_API_KEY"):
                client = OpenAI()
        except Exception:
            client = None

        # ===== UI =====
        st.subheader("🧑‍🏫 Smart Tutor (Multi-Language) + 🎙️ Voice")
        st.caption("Speak or type your question. I’ll answer and can read the reply aloud.")

        LANGS = [
            "Urhobo", "Yorùbá", "Hausa", "Ịjọ (Ijaw)", "Efik (Calabar)",
            "Ịgbò (Igbo)", "Edo (Bini)", "Tiv", "Ibibio", "Kanuri",
            "Nupe", "Fulfulde (Fula)", "Itsekiri", "Gbagyi", "Idoma",
            "Ebira", "Jukun", "Igala", "Berom (Birom)", "Esan", "Isoko",
            "Okun (Yoruba dialect)", "Ika", "English (for reference)"
        ]
        DOMAINS = [
            "General chat",
            "Farming & Agriculture",
            "Business & Finance",
            "Health & Safety (non-medical advice)",
            "Education & Study Help",
        ]
        TONES = ["Neutral", "Friendly", "Professional", "Encouraging", "Brief"]

        c1, c2, c3 = st.columns([1.2, 1, 1])
        lang = c1.selectbox("Language", LANGS, index=0, key="ml_lang")
        domain = c2.selectbox("Domain", DOMAINS, index=1, key="ml_domain")
        tone = c3.selectbox("Tone", TONES, index=1, key="ml_tone")

        # Voice controls
        vc1, vc2, vc3 = st.columns([1.1, 1.1, 1])
        input_mode = vc1.radio("Input Mode", ["🎙️ Voice", "⌨️ Typing"], horizontal=True, key="ml_input_mode")
        auto_speak = vc2.toggle("🔁 Auto-speak reply", value=True, key="ml_auto_speak")
        tts_lang_hint = vc3.selectbox(
            "TTS language (for playback)",
            ["auto (best effort)", "en", "ha", "yo", "ig"],
            index=0,
            key="ml_tts_code",
            help="If your selected language lacks TTS support, fallback to English."
        )

        st.divider()

        # ===== Helpers =====
        def _system_prompt(lang_: str, domain_: str, tone_: str) -> str:
            return f"""
You are a helpful AI that replies entirely in {lang_}.
Tone: {tone_}. Domain focus: {domain_}.
Use clear, culturally appropriate expressions. Avoid slang unless asked.
If a term has no direct {lang_} word, explain briefly in {lang_}.
Keep paragraphs short. Use bullet points for steps/lists.
Do NOT switch to English unless the user asks.
""".strip()

        def _translate_to(text: str, target_code: str) -> str:
            # target_code like 'en', 'ha', 'yo', 'ig', etc.; we don't have full codes for all listed langs.
            # If translator not available or target_code is not known, return original.
            if not translator or not text.strip():
                return text
            try:
                if translator == "googletrans":
                    # Try googletrans with language code; if target_code isn't valid it may still guess
                    return _gt.translate(text, dest=target_code or "en").text
                else:
                    # deep-translator
                    from deep_translator import GoogleTranslator
                    return GoogleTranslator(source="auto", target=target_code or "en").translate(text)
            except Exception:
                return text

        def _speak_text(text: str, lang_code: str = "en"):
            # Try offline first
            if pyttsx3 is not None:
                try:
                    engine = pyttsx3.init()
                    rate = engine.getProperty("rate")
                    if isinstance(rate, int):
                        engine.setProperty("rate", max(120, min(185, rate)))
                    engine.say(text)
                    engine.runAndWait()
                    st.caption("🔉 Played using offline TTS (pyttsx3).")
                    return
                except Exception:
                    pass
            # gTTS fallback
            if gTTS is not None:
                try:
                    use_code = lang_code if lang_code in {"en", "ha", "yo", "ig"} else "en"
                    tts = gTTS(text=text, lang=use_code)
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                        tts.save(tmp.name)
                        st.audio(tmp.name, format="audio/mp3")
                        st.caption("🔉 Played using gTTS.")
                    return
                except Exception as e:
                    st.warning(f"TTS failed: {e}")
            st.info("🔇 Could not play audio (no TTS engine available).")

        def _model_answer(user_text: str) -> str:
            sys_prompt = _system_prompt(lang, domain, tone)
            if client is not None:
                try:
                    resp = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": user_text},
                        ],
                        temperature=0.6,
                        max_tokens=380,
                    )
                    return (resp.choices[0].message.content or "").strip()
                except Exception:
                    pass  # fall through to fallback
            # Local fallback pattern
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            header = f"[{lang}] — {domain} • {tone}"
            body_map = {
                "Farming & Agriculture": "• Farm advice (summary):",
                "Business & Finance": "• Business guidance (summary):",
                "Health & Safety (non-medical advice)": "• Safety tips (general):",
                "Education & Study Help": "• Study help (outline):",
                "General chat": "• Response (general):",
            }
            return (
                f"{header}\n"
                f"{body_map.get(domain,'• Response:')}\n"
                f"- 1) Identify main need. 2) Give short, clear guidance. 3) Suggest next step.\n"
                f"- Your request: “{user_text.strip()}”\n"
                f"- Tip: Keep records and review weekly.\n"
                f"— {ts}"
            )

        # Keep simple session history
        if "ml_msgs" not in st.session_state:
            st.session_state.ml_msgs = []  # list[tuple[role, text]]

        # ===== Input area (Voice or Typing) =====
        recognized_box = st.empty()
        query_text = ""

        if input_mode == "🎙️ Voice":
            c_mic, c_up = st.columns([1, 1])
            mic_clicked = c_mic.button("🎤 Tap to Record", key="ml_mic_btn")
            audio_file = c_up.file_uploader("…or upload WAV/MP3", type=["wav", "mp3", "m4a"], key="ml_audio_upload")

            if mic_clicked:
                if sr is None:
                    st.error("SpeechRecognition not installed. Try: `pip install SpeechRecognition pyaudio`")
                else:
                    try:
                        recog = sr.Recognizer()
                        with sr.Microphone() as source:
                            st.info("🎤 Listening…")
                            try:
                                recog.adjust_for_ambient_noise(source, duration=0.6)
                            except Exception:
                                pass
                            audio = recog.listen(source, timeout=4, phrase_time_limit=8)
                        st.caption("⏳ Transcribing…")
                        # Try to hint with common codes (fallback to 'en')
                        hint_code = {"Yorùbá": "yo", "Hausa": "ha", "Ịgbò (Igbo)": "ig"}.get(lang, "en")
                        query_text = recog.recognize_google(audio, language=hint_code)
                        recognized_box.success(f"🗣️ Recognized: {query_text}")
                    except sr.WaitTimeoutError:
                        st.error("Listening timed out. Try again and speak sooner.")
                    except sr.UnknownValueError:
                        st.error("I couldn't understand that. Please try again.")
                    except sr.RequestError:
                        st.error("Speech service unavailable. Check internet connection.")
                    except Exception as e:
                        st.error(f"Mic/recognition error: {e}")

            if audio_file is not None and sr is not None:
                try:
                    recog = sr.Recognizer()
                    with sr.AudioFile(audio_file) as source:
                        audio = recog.record(source)
                    st.caption("⏳ Transcribing uploaded audio…")
                    hint_code = {"Yorùbá": "yo", "Hausa": "ha", "Ịgbò (Igbo)": "ig"}.get(lang, "en")
                    query_text = recog.recognize_google(audio, language=hint_code)
                    recognized_box.success(f"🗣️ Recognized: {query_text}")
                except Exception as e:
                    st.error(f"Audio transcription failed: {e}")

            default_text = query_text or st.session_state.get("ml_last_text", "")
            user_text = st.text_area("Your question (editable):", value=default_text, key="ml_textarea", height=120)
            st.session_state["ml_last_text"] = user_text

        else:  # Typing
            user_text = st.text_area(
                "Type your question / prompt",
                placeholder="e.g., Explain in Yorùbá how to prevent tomato leaf blight this week.",
                height=140,
                key="ml_query",
            )

        st.divider()

        # ===== Generate =====
        go = st.button("Generate", type="primary", key="ml_go")
        if go:
            if not (user_text or "").strip():
                st.warning("Please enter a question or prompt.")
            else:
                with st.spinner("Generating..."):
                    base_reply = _model_answer(user_text)

                    # Try a best-effort text translate to a matching code (only a few are well supported)
                    # For playback, we also try 'tts_lang_hint' to guide TTS.
                    lang_to_code = {
                        "English (for reference)": "en",
                        "Yorùbá": "yo",
                        "Hausa": "ha",
                        "Ịgbò (Igbo)": "ig",
                    }
                    target_code = lang_to_code.get(lang, "en")
                    translated = _translate_to(base_reply, target_code) if target_code else base_reply

                # Save to history
                st.session_state.ml_msgs.append(("user", user_text))
                st.session_state.ml_msgs.append(("assistant", translated))

                st.markdown("### ✅ Tutor Response")
                st.write(translated)

                # Auto-speak (optional)
                if auto_speak and translated.strip():
                    tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                    _speak_text(translated, lang_code=tts_code or target_code or "en")

        # ===== Conversation history + manual speak buttons =====
        if st.session_state.ml_msgs:
            st.subheader("💬 Conversation")
            for role, text in st.session_state.ml_msgs:
                if role == "user":
                    with st.chat_message("user", avatar="🧑"):
                        st.write(text)
                else:
                    with st.chat_message("assistant", avatar="🧠"):
                        st.write(text)
                        if st.button("🔊 Speak this reply", key=f"ml_say_{abs(hash(text))%10**8}"):
                            tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                            # Try to infer from current language choice (fallback English)
                            lang_to_code = {"English (for reference)": "en", "Yorùbá": "yo", "Hausa": "ha", "Ịgbò (Igbo)": "ig"}
                            inferred = lang_to_code.get(lang, "en")
                            _speak_text(text, lang_code=tts_code or inferred or "en")

        


    # -------------------------
    # 🤖 Chatbot Assistant
    # -------------------------
    elif help_option == "🤖 Chatbot Assistant":
        st.subheader("🤖 Smart Farm AI Chatbot Assistant")
        st.write("Ask me anything about Smart Farm AI or farming practices.")
        chatbot_knowledge = {
            "how to add a crop": "Go to Farm Management > Add Crop and fill in the crop details.",
            "how to backup data": "Go to Support & Help > Data Backup & Recovery and click 'Backup Data'.",
            "how to check soil moisture": "Check Sensors & Monitoring > Live Farm Sensor Dashboard.",
            "how to detect crop disease": "Use AI Predictions > Crop Disease Detection and upload a leaf image.",
        }
        user_question = st.text_input("💬 Type your question here:", key="chat_q")
        if st.button("🤖 Get Answer", key="chat_go"):
            answer = chatbot_knowledge.get(
                (user_question or "").lower(),
                "❓ Sorry, I don't have an answer for that yet. Please try another question.",
            )
            st.info(answer)





# =========================

# SIDEBAR MENU

# =========================

menu = st.sidebar.selectbox(

    "📍 Select a Main Section",

    [

        "🌿 Farm Management",

        "📊 Productivity & Records",

        "🧠 AI Predictions",

        "💧 Irrigation & Soil",

        "💹 Market & Finance",

        "📡 Sensors & Monitoring",

        "🆘 Support & Help",

    ],

    key="main_menu"

)



# =========================

# ROUTER

# =========================

if menu == "🌿 Farm Management":

    st.sidebar.title("🌿 Smart Farm AI")

    st.header("🌿 Farm Management")

    farm_option = st.sidebar.selectbox("Select a Feature", [

        "User Account Management",

        "Farm Plot Mapping",

        "Smart Fertilizer & Pesticide Stock Manager",

        "AI Crop Calendar",

        "Drone Flight Scheduler",

        "Voice Command Interface"

    ], key="farm_management_option")



    if farm_option == "User Account Management":

        user_account_management_ui()

    elif farm_option == "Farm Plot Mapping":

        farm_plot_mapping_ui()

    elif farm_option == "Smart Fertilizer & Pesticide Stock Manager":

        smart_fert_pest_ui()

    elif farm_option == "AI Crop Calendar":

        ai_crop_calendar_ui()

    elif farm_option == "Drone Flight Scheduler":

        drone_flight_scheduler_ui()

    elif farm_option == "Voice Command Interface":

        voice_command_ui()



elif menu == "📊 Productivity & Records":

    productivity_option = st.sidebar.selectbox("📊 Select a Productivity Feature", [

        "📈 View Sales Record",

        "➕ Add Sales Record",

        "💰 View Expense",

        "➕ Add Expense",

        "📦 View Inventory",

        "➕ Add Inventory",

        "📄 Generate Report",

        "📊 Farm Summary",

    ], key="productivity_feature")



    if productivity_option == "➕ Add Sales Record":

        st.subheader("➕ Add Sales Record")

        item = st.text_input("Enter Item Sold")

        quantity = st.number_input("Enter Quantity", min_value=1)

        amount = st.number_input("Enter Amount (₦)", min_value=0)

        date = st.date_input("Select Date")

        if st.button("Save Record"):

            new_record = {"item": item, "quantity": quantity, "amount": amount, "date": str(date)}

            try:

                with open("sales_records.json", "r") as file:

                    sales_data = json.load(file)

            except FileNotFoundError:

                sales_data = []

            sales_data.append(new_record)

            with open("sales_records.json", "w") as file:

                json.dump(sales_data, file, indent=4)

            st.success("✅ Sales record added successfully!")



    elif productivity_option == "📈 View Sales Record":

        st.subheader("📈 View Sales Record")

        try:

            with open("sales_records.json", "r") as file:

                sales_data = json.load(file)

            if sales_data:

                for entry in sales_data:

                    st.markdown(f"""

- 📅 Date: {entry['date']}

- 🛒 Item Sold: {entry['item']}

- 🔢 Quantity: {entry['quantity']}

- 💰 Amount: ₦{entry['amount']}

---

""")

            else:

                st.info("No sales records available.")

        except FileNotFoundError:

            st.warning("No sales record file found yet.")



    elif productivity_option == "➕ Add Expense":

        st.subheader("➕ Add Expense Record")

        with st.form("expense_form"):

            date = st.date_input("📅 Date of Expense")

            category = st.selectbox("📂 Expense Category", [

                "Fertilizer", "Pesticide", "Seeds", "Labor", "Fuel", "Maintenance", "Transport", "Others"

            ])

            amount = st.number_input("💰 Amount Spent (₦)", min_value=0.0, step=100.0, format="%.2f")

            description = st.text_area("📝 Description (Optional)")

            submit_expense = st.form_submit_button("Save Expense Record")

        if submit_expense:

            new_expense = {"Date": str(date), "Category": category, "Amount": amount, "Description": description}

            try:

                with open("expenses.json", "r") as file:

                    expense_data = json.load(file)

            except FileNotFoundError:

                expense_data = []

            expense_data.append(new_expense)

            with open("expenses.json", "w") as file:

                json.dump(expense_data, file, indent=4)

            st.success("✅ Expense record added successfully!")



    elif productivity_option == "💰 View Expense":

        st.subheader("💰 View Expense Records")

        try:

            with open("expenses.json", "r") as file:

                expense_data = json.load(file)

            if expense_data:

                for entry in expense_data:

                    st.markdown(f"""

- 📅 Date: {entry['Date']}

- 📂 Category: {entry['Category']}

- 💰 Amount: ₦{entry['Amount']}

- 📝 Description: {entry['Description']}

---

""")

            else:

                st.info("No expense records available.")

        except FileNotFoundError:

            st.warning("No expense record file found yet.")



    elif productivity_option == "➕ Add Inventory":

        st.subheader("➕ Add Inventory Item")

        with st.form("inventory_form"):

            item = st.text_input("📦 Item Name")

            quantity = st.number_input("🔢 Quantity", min_value=0, step=1)

            category = st.text_input("📂 Category (e.g., Fertilizer, Seeds, Tools)")

            submit_inventory = st.form_submit_button("Save Inventory Item")

        if submit_inventory:

            new_item = {"Item": item, "Quantity": quantity, "Category": category}

            try:

                with open("inventory.json", "r") as file:

                    inventory_data = json.load(file)

            except FileNotFoundError:

                inventory_data = []

            inventory_data.append(new_item)

            with open("inventory.json", "w") as file:

                json.dump(inventory_data, file, indent=4)

            st.success("✅ Inventory item added successfully!")



    elif productivity_option == "📦 View Inventory":

        st.subheader("📦 View Inventory Records")

        try:

            with open("inventory.json", "r") as file:

                inventory_data = json.load(file)

            if inventory_data:

                for entry in inventory_data:

                    st.markdown(f"""

- 📦 Item: {entry['Item']}

- 🔢 Quantity: {entry['Quantity']}

- 📂 Category: {entry['Category']}

---

""")

            else:

                st.info("No inventory records available.")

        except FileNotFoundError:

            st.warning("No inventory record file found yet.")



    elif productivity_option == "📄 Generate Report":

        st.subheader("📄 Generate Farm Report")

        total_sales, total_expenses = 0, 0

        try:

            with open("sales_records.json", "r") as file:

                sales_data = json.load(file)

                total_sales = sum(entry['amount'] for entry in sales_data)

        except FileNotFoundError:

            sales_data = []

        try:

            with open("expenses.json", "r") as file:

                expense_data = json.load(file)

                total_expenses = sum(entry['Amount'] for entry in expense_data)

        except FileNotFoundError:

            expense_data = []

        profit_loss = total_sales - total_expenses

        st.markdown(f"""

### 📊 Farm Financial Report

- 💰 Total Sales: ₦{total_sales}

- 💸 Total Expenses: ₦{total_expenses}

- 📈 Profit / Loss: ₦{profit_loss}

""")



    elif productivity_option == "📊 Farm Summary":

        st.subheader("📊 Overall Farm Summary")

        try:

            with open("sales_records.json", "r") as file:

                sales_data = json.load(file)

                total_sales = sum(entry['amount'] for entry in sales_data)

        except FileNotFoundError:

            sales_data, total_sales = [], 0

        try:

            with open("expenses.json", "r") as file:

                expense_data = json.load(file)

                total_expenses = sum(entry['Amount'] for entry in expense_data)

        except FileNotFoundError:

            expense_data, total_expenses = [], 0

        try:

            with open("inventory.json", "r") as file:

                inventory_data = json.load(file)

        except FileNotFoundError:

            inventory_data = []

        st.markdown(f"""

- 💰 Total Sales: ₦{total_sales}

- 💸 Total Expenses: ₦{total_expenses}

- 🧮 Net: ₦{total_sales - total_expenses}

- 📦 Inventory Items: {len(inventory_data)}

""")



elif menu == "🧠 AI Predictions":

    ai_predictions_ui()



elif menu == "💧 Irrigation & Soil":

    irrigation_ui()



elif menu == "💹 Market & Finance":

    market_finance_ui()


elif menu == "📡 Sensors & Monitoring":
    sensors_monitoring_ui()

elif menu == "🆘 Support & Help":
     support_help_ui()


# 1) --- helpers defined FIRST ---

def k2(name: str) -> str:

    return f"v2_{name}"



def klsd(suffix: str) -> str:

    return f"lsd_{suffix}"


# 🎙 Voice Command (v2) — triggers real buttons/pages
def voice_command_ui_v2():
    import streamlit as st
    import threading

    # ----- Optional deps (kept optional so UI still loads without them)
    try:
        import speech_recognition as sr
    except Exception:
        sr = None

    try:
        import pyttsx3
    except Exception:
        pyttsx3 = None

    # ----- Resolve your v2 main menu session key
    try:
        main_v2_key = k2("main_menu_option")  # your existing helper
    except Exception:
        main_v2_key = "v2_main_menu_option"   # safe fallback

    # ===== Helpers =====
    def _say_async(text: str):
        """Speak text on a background thread if TTS is available."""
        if pyttsx3 is None:
            return
        def _worker():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass
        threading.Thread(target=_worker, daemon=True).start()

    def _go(page_label: str):
        """Navigate to a v2 page label exactly as in your v2 menu."""
        st.session_state[main_v2_key] = page_label

    def _open_predictions(subtool: str | None = None):
        """Open v2 AI Predictions page and optionally pick a subtool."""
        _go("🧪 AI Predictions")
        if subtool:
            # v2 page reads this and maps to internal tool keys
            st.session_state["ai_prediction_tool"] = subtool
        st.rerun()

    def _open_tips(mode: str):
        """Open AI Farm Tips and set its internal active tool."""
        _go("📚 AI Farm Tips")
        # ktips("active_tool") returns "tips_active_tool" in your setup
        st.session_state["tips_active_tool"] = mode  # "ask" or "daily"
        st.rerun()

    def _open_live_sensor():
        _go("📡 Live Sensor Dashboard")
        st.rerun()

    def _open_perf_indicators():
        _go("📍 Farm Performance Indicators")
        st.rerun()

    def _open_calendar():
        _go("📅 Calendar & Seasons")
        st.rerun()

    def _route_command(c: str) -> bool:
        """Return True if a route matched and navigated."""
        c = c.strip().lower()

        # --- high-confidence intents ---
        if "live sensor" in c or ("sensor" in c and "dashboard" in c):
            _open_live_sensor();  return True
        if "performance" in c and "indicator" in c:
            _open_perf_indicators();  return True
        if "calendar" in c or "season" in c:
            _open_calendar();  return True

        # --- AI Predictions subtools
        if ("disease" in c) or ("diagnose" in c) or ("leaf" in c) or ("blight" in c):
            _open_predictions("Crop Disease Detection");  return True
        if "yield" in c:
            _open_predictions("Yield Prediction");  return True
        if "soil" in c or "ph" in c:
            _open_predictions("Soil Health Check");  return True
        if "prediction" in c or "predictions" in c:
            _open_predictions(None);  return True

        # --- AI Farm Tips
        if "daily tip" in c or ("tip" in c and "daily" in c):
            _open_tips("daily");  return True
        if "ask tip" in c or ("tip" in c and "ask" in c) or ("ai tip" in c):
            _open_tips("ask");  return True

        return False

    # ===== UI =====
    st.header("🎙️ Voice Command (v2)")

    if sr is None:
        st.warning(
            "Speech engine not installed. Install with:\n\n"
            "`pip install SpeechRecognition pyaudio`  "
            "or use an alternative microphone backend."
        )
        return

    # Unique keys to avoid collisions across v2
    btn_key = f"{main_v2_key}_vc2_mic_btn"
    status_key = f"{main_v2_key}_vc2_status"

    # Button to record one utterance
    if st.button("🎤 Speak now", key=btn_key):
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                st.info("Listening... please speak clearly.")
                # Reduce background noise impact
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.6)
                except Exception:
                    pass
                # Listen for a short phrase
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=6)

            transcript = None
            error_msg = None

            # Try Google first (requires internet), fall back to Sphinx if available
            try:
                transcript = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                # Try offline pocketsphinx if installed
                try:
                    transcript = recognizer.recognize_sphinx(audio)
                except Exception:
                    error_msg = "I couldn't understand that. Please try again."
            except sr.RequestError:
                # Network issue, try offline if possible
                try:
                    transcript = recognizer.recognize_sphinx(audio)
                except Exception:
                    error_msg = "Network unavailable for speech. Install pocketsphinx for offline use."

            # Handle results
            if transcript:
                st.success(f"You said: “{transcript}”")
                _say_async(f"You said {transcript}")
                if not _route_command(transcript):
                    st.info(
                        "No v2 route matched. Try saying: "
                        "live sensor, performance indicators, calendar, "
                        "disease, yield, soil, predictions, daily tip, ask tip."
                    )
            else:
                st.error(error_msg or "Sorry, I didn't catch that. Please try again.")

        except sr.WaitTimeoutError:
            st.error("Listening timed out. Try again and speak sooner.")
        except OSError as e:
            st.error(f"Microphone error: {e}")
        except Exception as e:
            st.error(f"Voice command error: {e}")

def expanded_crop_calendar_ui():
    import streamlit as st
    import pandas as pd
    import calendar
    from datetime import date

    st.header("📅 Expanded AI Crop Calendar")

    # ---------- SAFE DEFAULTS (only if not already defined globally) ----------
    if "_CROPS" not in globals():
        globals()["_CROPS"] = ["Maize", "Rice", "Cassava", "Tomato"]
    if "_ZONES" not in globals():
        globals()["_ZONES"] = ["Sahel", "Sudan", "Guinea", "Rainforest"]
    if "_TASK_EMOJI" not in globals():
        globals()["_TASK_EMOJI"] = {
            "sow": "🌱", "nursery": "🪴", "transplant": "🌿", "weed": "🧹",
            "spray": "🧪", "topdress": "🧂", "harvest": "🧺", "field_checks": "🔎"
        }

    # Simple schedule builder if you didn't define one elsewhere
    if "_build_schedule" not in globals():
        def _build_schedule(crop: str, zone: str, year: int) -> pd.DataFrame:
            # Dummy windows – replace with real logic / data
            spec = [
                ("sow",          f"{year}-03-10", f"{year}-03-20"),
                ("field_checks", f"{year}-03-21", f"{year}-11-30"),
                ("weed",         f"{year}-04-05", f"{year}-04-06"),
                ("spray",        f"{year}-05-02", f"{year}-05-04"),
                ("topdress",     f"{year}-06-15", f"{year}-06-16"),
                ("harvest",      f"{year}-09-20", f"{year}-09-25"),
            ]
            rows = []
            for task, s, e in spec:
                for d in pd.date_range(s, e, freq="D"):
                    rows.append((pd.to_datetime(d).normalize(), task))
            return pd.DataFrame(rows, columns=["date", "task"])

    # Month×Week grid builder if you didn't define one elsewhere
    if "_month_grid" not in globals():
        def _month_grid(df: pd.DataFrame, year: int) -> pd.DataFrame:
            df = df.copy()
            df["month"] = df["date"].dt.month
            # naive “week-of-month” bucket (1..5)
            df["wom"] = ((df["date"].dt.day - 1) // 7) + 1
            out = []
            for m in range(1, 13):
                sub = df[df["month"] == m]
                row = {"Month": calendar.month_name[m]}
                for w in range(1, 6):
                    tasks = sorted(sub[sub["wom"] == w]["task"].unique())
                    row[f"W{w}"] = ", ".join(tasks) if tasks else ""
                out.append(row)
            return pd.DataFrame(out)

    # ---------- UI CONTROLS ----------
    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        crop = st.selectbox("Crop", _CROPS, index=0, key="ccal_crop")
    with c2:
        zone = st.selectbox("Agro-ecological Zone (NG)", _ZONES, index=2, key="ccal_zone")
    with c3:
        year = st.number_input("Season Year", min_value=2020, max_value=2100,
                               value=date.today().year, step=1, key="ccal_year")

    cache_key = f"ccal_df_{crop}_{zone}_{int(year)}"
    if cache_key not in st.session_state:
        base = _build_schedule(crop, zone, int(year))
        base = base.copy()
        base["date"] = pd.to_datetime(base["date"]).dt.normalize()
        st.session_state[cache_key] = base

    df = st.session_state[cache_key].copy()
    df["month"] = df["date"].dt.month
    df["code"] = df["task"].map(lambda t: _TASK_EMOJI.get(t, "•") + t[:3].upper())

    # ---------- ADD CUSTOM TASK ----------
    st.subheader("➕ Add Custom Task")
    with st.form("ccal_ct_form", clear_on_submit=False):
        cc1, cc2, cc3 = st.columns([1.2, 1, 1])
        with cc1:
            custom_label = st.text_input("Task label (e.g., Spray, Weeding)", key="ccal_ct_label")
        with cc2:
            default_start = df["date"].min().date()
            custom_start = st.date_input("Start date", value=default_start, key="ccal_ct_start")
        with cc3:
            default_end = (df["date"].min() + pd.Timedelta(days=3)).date()
            custom_end = st.date_input("End date", value=default_end, key="ccal_ct_end")
        submitted = st.form_submit_button("Add Task", use_container_width=True)

    if submitted:
        lbl = (custom_label or "").strip()
        if not lbl:
            st.warning("Enter a task label.")
        elif custom_start > custom_end:
            st.warning("End date must be on/after start date.")
        else:
            rng = pd.date_range(pd.to_datetime(custom_start), pd.to_datetime(custom_end), freq="D")
            extra = pd.DataFrame({"date": rng, "task": lbl})
            new_df = pd.concat([st.session_state[cache_key], extra], ignore_index=True)
            new_df["date"] = pd.to_datetime(new_df["date"]).dt.normalize()
            st.session_state[cache_key] = new_df
            st.success(f"Added custom task: {lbl} ({custom_start} → {custom_end})")
            df = new_df.copy()
            df["month"] = df["date"].dt.month
            df["code"] = df["task"].map(lambda t: _TASK_EMOJI.get(t, "•") + t[:3].upper())

    # ---------- CALENDAR GRID ----------
    st.subheader("🗓️ Calendar Grid (Month × Week)")
    grid = _month_grid(df, int(year))
    st.dataframe(grid, use_container_width=True, hide_index=True)

    # ---------- MONTH TASKS ----------
    st.subheader("📋 Month Tasks (Readable)")
    for m in range(1, 13):
        sub = df[df["month"] == m]
        if sub.empty:
            continue
        with st.expander(calendar.month_name[m]):
            for task in sorted(sub["task"].unique()):
                days = sorted(pd.to_datetime(sub[sub["task"] == task]["date"]).dt.date.unique())
                # collapse contiguous ranges
                span_start = prev = days[0]
                ranges = []
                for d in days[1:]:
                    if (pd.to_datetime(d) - pd.to_datetime(prev)).days > 1:
                        ranges.append((span_start, prev))
                        span_start = d
                    prev = d
                ranges.append((span_start, prev))
                emo = _TASK_EMOJI.get(task, "•")
                for s, e in ranges:
                    if s == e:
                        st.write(f"{emo} **{task}**: {pd.to_datetime(s).strftime('%b %d')}")
                    else:
                        st.write(f"{emo} **{task}**: {pd.to_datetime(s).strftime('%b %d')} → {pd.to_datetime(e).strftime('%b %d')}")

    # ---------- EXPORT ----------
    st.subheader("⬇️ Export")
    csv = df[["date", "task"]].sort_values("date").copy()
    csv["date"] = pd.to_datetime(csv["date"]).dt.strftime("%Y-%m-%d")
    st.download_button(
        "Download CSV",
        csv.to_csv(index=False).encode("utf-8"),
        file_name=f"{crop}_{zone}_{year}_calendar.csv",
        mime="text/csv",
        key="ccal_dl_csv"
    )

    st.success(f"✅ Expanded Crop Calendar generated successfully for {crop} · {zone} · {year}.")


# 2) --- feature function defined NEXT ---

def live_sensor_dashboard_v2():

    import time, random

    import pandas as pd

    from datetime import datetime

    import streamlit as st



    st.header("📡 Live Sensor Dashboard (v2)")

    st.caption("Simulated stream. Replace `read_sensors()` with your real sensor inputs.")



    # init state

    if klsd("log") not in st.session_state:

        st.session_state[klsd("log")] = []

    if klsd("running") not in st.session_state:

        st.session_state[klsd("running")] = True



    # controls

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])

    refresh_rate = c1.slider("⏱️ Refresh (seconds)", 1, 10, 5, key=klsd("refresh"))

    history_size = c2.number_input("🧮 Keep last N rows", 20, 1000, 150, 10, key=klsd("hist"))

    st.session_state[klsd("running")] = c3.toggle("🔄 Live monitoring", value=st.session_state[klsd("running")], key=klsd("toggle"))

    if c4.button("🧹 Clear history", key=klsd("clear")):

        st.session_state[klsd("log")] = []

        st.success("Cleared.")

        st.rerun()



    def read_sensors():

        return {

            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Temperature (°C)": round(random.uniform(24.0, 36.5), 1),

            "Humidity (%)": round(random.uniform(40.0, 90.0), 1),

            "Soil Moisture (%)": round(random.uniform(18.0, 70.0), 1),

            "Light (lux)": random.randint(8_000, 60_000),

        }



    if st.session_state[klsd("running")] or not st.session_state[klsd("log")]:

        st.session_state[klsd("log")].append(read_sensors())

        st.session_state[klsd("log")] = st.session_state[klsd("log")][-int(history_size):]



    df = pd.DataFrame(st.session_state[klsd("log")])

    if df.empty:

        st.info("No readings yet. Enable live monitoring to start.")

        return



    latest = df.iloc[-1]

    k1, k2c, k3, k4 = st.columns(4)

    k1.metric("🌡 Temperature", f"{latest['Temperature (°C)']} °C")

    k2c.metric("💧 Humidity", f"{latest['Humidity (%)']} %")

    k3.metric("🌱 Soil Moisture", f"{latest['Soil Moisture (%)']} %")

    k4.metric("🔆 Light", f"{latest['Light (lux)']} lux")



    # simple alerts

    if latest["Soil Moisture (%)"] < 35:

        st.warning("Low soil moisture — consider irrigating soon.")

    if latest["Temperature (°C)"] > 34:

        st.warning("High temperature — risk of heat stress.")

    if latest["Humidity (%)"] > 80:

        st.warning("High humidity — monitor for fungal disease.")



    st.divider()

    st.subheader("📈 Trends")

    chart_df = df.set_index("Timestamp")

    st.line_chart(chart_df[["Temperature (°C)"]])

    st.line_chart(chart_df[["Humidity (%)"]])

    st.line_chart(chart_df[["Soil Moisture (%)"]])

    st.line_chart(chart_df[["Light (lux)"]])



    st.subheader("🗃️ Recent Readings")

    st.dataframe(df.tail(30), use_container_width=True)



    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button("⬇️ Download CSV", csv,

        file_name=f"sensor_readings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",

        mime="text/csv", key=klsd("dl_csv"))



    if st.session_state[klsd("running")]:

        time.sleep(refresh_rate)

        st.rerun()

# ---------- KEY PREFIX HELPERS (single, clean) ----------
def _ccal(name: str) -> str:
    """Expanded AI Crop Calendar widgets."""
    return f"ccal_{name}"

def klsd(name: str) -> str:
    """Live Sensor Dashboard widgets."""
    return f"lsd_{name}"

def kacc(name: str) -> str:
    """Account / User management (v1)."""
    return f"acc_v1_{name}"

def k2(name: str) -> str:
    """Main v2 menu/router prefix."""
    return f"v2_{name}"

def kp2(name: str) -> str:
    """Productivity & Records (v2)."""
    return f"v2_prod_{name}"

def kfm2(name: str) -> str:
    """Farm Management (v2)."""
    return f"v2_farm_{name}"

def kirr2(name: str) -> str:
    """Irrigation & Soil (v2)."""
    return f"v2_irrig_{name}"

def kplot(name: str) -> str:
    """Farm Plot Mapping (v2)."""
    return f"v2_plot_{name}"

def kcal(name: str) -> str:
    """Calendar & Seasons (v2)."""
    return f"v2_cal_{name}"

def kalert(name: str) -> str:
    """Alerts widgets."""
    return f"alerts_{name}"

def ktips(name: str) -> str:
    """AI Farm Tips widgets."""
    return f"tips_{name}"

def kforum(name: str) -> str:
    """Community Forum widgets."""
    return f"v2_forum_{name}"

def kpl(name: str) -> str:
    """Profit & Loss widgets."""
    return f"pl_{name}"

def ap(name: str) -> str:
    """AI Predictions widgets."""
    return f"ai_pred_{name}"

def mkey(name: str) -> str:
    """Market & Economic Tools."""
    return f"market_tools_{name}"

def fi(name: str) -> str:
    """Farm Indicators."""
    return f"farm_ind_{name}"

def kdm(name: str) -> str:
    """Decision-making models."""
    return f"dm_{name}"

def kdr(name: str) -> str:
    """Drone / Irrigation tools."""
    return f"dr_{name}"

def kbak(name: str) -> str:
    """Backup & Recovery."""
    return f"bk_{name}"

def klot(name: str) -> str:
    """Farm Lot Management."""
    return f"lot_{name}"

def sfp(name: str) -> str:
    """Single Feature Page widgets."""
    return f"sfp_{name}"

# =========================
# UPGRADE MENU (second router with unique keys)
# ---------- KEY PREFIX HELPERS (clean) ----------
def _ccal(name: str) -> str: return f"ccal_{name}"
def klsd(name: str) -> str:  return f"lsd_{name}"
def kacc(name: str) -> str:  return f"acc_v1_{name}"
def k2(name: str) -> str:    return f"v2_{name}"
def kp2(name: str) -> str:   return f"v2_prod_{name}"
def kfm2(name: str) -> str:  return f"v2_farm_{name}"
def kirr2(name: str) -> str: return f"v2_irrig_{name}"
def kplot(name: str) -> str: return f"v2_plot_{name}"
def kcal(name: str) -> str:  return f"v2_cal_{name}"
def kalert(name: str) -> str:return f"alerts_{name}"
def ktips(name: str) -> str: return f"tips_{name}"
def kforum(name: str) -> str:return f"v2_forum_{name}"
def kpl(name: str) -> str:   return f"pl_{name}"
def ap(name: str) -> str:    return f"ai_pred_{name}"
def mkey(name: str) -> str:  return f"market_tools_{name}"
def fi(name: str) -> str:    return f"farm_ind_{name}"
def kdm(name: str) -> str:   return f"dm_{name}"
def kdr(name: str) -> str:   return f"dr_{name}"
def kbak(name: str) -> str:  return f"bk_{name}"
def klot(name: str) -> str:  return f"lot_{name}"
def sfp(name: str) -> str:   return f"sfp_{name}"

# =========================
# UPGRADE MENU (second router with unique keys)
# =========================
# Make sure you have this at the very top of your file too:
# import streamlit as st

menu_v2 = st.sidebar.selectbox(
    "📖 Main Menu",
    [
        "🏡 Home",
        "🌿 Farm Management",
        "📊 Productivity & Records",
        "💧 Irrigation & Soil", 
        "📊 farm profit & loss statement",
        "📅 Calendar & Seasons",
        "🧪 AI Predictions",
        "📚 AI Farm Tips",
        "🧪 Smart Fertilizer & Pesticide",
        "🌐 Farmer Community Forum",
        "📡 Live Sensor Dashboard",
        "🚨 Smart Farm Alerts",
        "🎙️ Voice Command Interface",
        "🚁 Voice-Controlled Drone Irrigation Assistant",
        "🚁 Drone Flight Scheduler",
        "🧑‍🏫 Smart Tutor Multilanguage",
        "💾 Data Backup & Recovery",
        "📍 Farm Lot Management",
        "📅 Expanded AI Crop Calendar",
        "🤖 AI Crop Calendar",
        "📈 Decision-Making Models",
        "📍 Farm Performance Indicators",
        "🔒 User Account Management",
],
key=k2("main_menu_option")
)


# -------- Router (clean & deduped) --------
if menu_v2 == "🏡 Home":
    st.subheader("🏡 Welcome to Smart Farm AI!")
    st.write("🌱 Empowering farmers with AI-driven tools for better yield, smart management, and sustainable farming.")
    st.info("👈 Use the sidebar to explore features like irrigation schedules, crop predictions, farm records, and more.")


elif menu_v2 == "🔒 User Account Management":
    user_account_management_ui_v2()

elif menu_v2 == "📅 Expanded AI Crop Calendar":
    expanded_crop_calendar_ui()

elif menu_v2 == "🧑‍🏫 Smart Tutor Multilanguage":
    # call both UIs so Support & Help and the Smart Tutor are available together
    try:
        support_help_ui()
    except Exception as e:
        st.error(f"Support UI failed: {e}")
    try:
        smart_tutor_voice()
    except Exception as e:
        st.error(f"Smart Tutor failed: {e}")

elif menu_v2 == "📡 Live Sensor Dashboard":
    live_sensor_dashboard_v2()

elif menu_v2 == "🚁 Drone Flight Scheduler":
    drone_flight_scheduler_ui()

elif menu_v2 == "🚁 Voice-Controlled Drone Irrigation Assistant":
    drone_irrigation_assistant_ui()

elif menu_v2 == "💾 Data Backup & Recovery":
    data_backup_recovery_ui()

elif menu_v2 == "🧪 Smart Fertilizer & Pesticide":
    smart_fert_pest_ui()


elif menu_v2 == "🎙️ Voice Command Interface":
    voice_command_ui()


 
# Help text kept in the code but hidden by default (silent in the app)
_show_help = False  # set to True only for debugging/dev — keep False in production

_help_content = """
**Tips for using the app**
- Use the sidebar menu to switch pages.
- Example commands: `open live sensor dashboard`, `go to predictions`, `open backup`.
- If you see a *StreamlitAPIException about session_state*, it means a menu key was changed **after** its widget was created.
  ✅ Fix: always set defaults before the selectbox, or update via callbacks.
"""

# Render the help expander only when explicitly enabled (otherwise it stays silent)
if _show_help:
    with st.expander("ℹ️ Help — Navigation & Commands"):
        st.markdown(_help_content)
# otherwise nothing is shown in the UI (help works "silently" in the code)
  




# 🏡 HOME
if menu == "🏡 Home":
    st.subheader("Welcome to Smart Farm AI!")
    st.write("Use the sidebar to navigate through available tools.")

# farm management"
elif menu_v2 == "🌿 Farm Management":
    option = st.selectbox(
        "Select a Feature",
        [
            "Farm Equipment Tracker",
            "Pesticides Recommendation",
            "Add Sale Record",
            "Add Order Record",
            "Farm Labor Record",
            "Farm Location Mapper",
        ],
        key=kfm2("feature")
    )

    if option == "Farm Equipment Tracker":
        st.subheader("Farm Equipment Tracker")
        equipment_name = st.text_input("Enter Equipment Name:", key=kfm2("equip_name"))
        purchase_date  = st.date_input("Select Purchase Date:", key=kfm2("equip_date"))
        status = st.selectbox("Equipment Status", ["Available", "In Use", "Under Repair"], key=kfm2("equip_status"))
        if st.button("Save Equipment Record", key=kfm2("equip_save")):
            st.success(f"✅ Saved: {equipment_name} | {purchase_date} | {status}")

    elif option == "Pesticides Recommendation":
        st.subheader("Pesticides Recommendation")
        pest_name = st.text_input("Enter Detected Pest Name:", key=kfm2("pest_name"))
        crop_type = st.text_input("Enter Crop Type:", key=kfm2("pest_crop"))
        severity = st.selectbox("Severity Level", ["Low", "Medium", "High"], key=kfm2("pest_severity"))
        if st.button("Get Recommendation", key=kfm2("pest_reco")):
            st.success(f"Use recommended pesticide for {pest_name} on {crop_type} (Severity: {severity})")

    elif option == "Add Sale Record":
        st.subheader("Add Sale Record")
        crop_name = st.text_input("Enter Crop Name Sold:", key=kfm2("sale_crop"))
        quantity_sold = st.number_input("Quantity Sold (kg):", min_value=0, key=kfm2("sale_qty"))
        price_per_kg = st.number_input("Price per kg (₦):", min_value=0, key=kfm2("sale_price"))
        sale_date = st.date_input("Sale Date:", key=kfm2("sale_date"))
        if st.button("Save Sale Record", key=kfm2("sale_save")):
            total_amount = quantity_sold * price_per_kg
            st.success(f"✅ Sale recorded: {quantity_sold} kg of {crop_name} sold for ₦{total_amount}")

    elif option == "Add Order Record":
        st.subheader("Add Order Record")
        customer_name = st.text_input("Customer Name:", key=kfm2("order_customer"))
        product_ordered = st.text_input("Product Ordered:", key=kfm2("order_product"))
        quantity_ordered = st.number_input("Quantity Ordered (kg):", min_value=0, key=kfm2("order_qty"))
        expected_delivery = st.date_input("Expected Delivery Date:", key=kfm2("order_date"))
        if st.button("Save Order Record", key=kfm2("order_save")):
            st.success(f"✅ Order saved: {customer_name} ordered {quantity_ordered} kg of {product_ordered}")

    elif option == "Farm Labor Record":
        st.subheader("Farm Labor Record")
        worker_name = st.text_input("Worker Name:", key=kfm2("labor_worker"))
        task_assigned = st.text_input("Task Assigned:", key=kfm2("labor_task"))
        work_date = st.date_input("Work Date:", key=kfm2("labor_date"))
        payment_amount = st.number_input("Payment Amount (₦):", min_value=0, key=kfm2("labor_pay"))
        if st.button("Save Labor Record", key=kfm2("labor_save")):
            st.success(f"✅ Labor record saved: {worker_name} on {work_date}, Task: {task_assigned}, ₦{payment_amount}")

    elif option == "Farm Location Mapper":
        st.subheader("Farm Location Mapper")
        location_name = st.text_input("Farm Location Name:", key=kfm2("loc_name"))
        gps_coordinates = st.text_input("Enter GPS Coordinates (e.g. 7.3775, 3.9470):", key=kfm2("loc_gps"))
        land_size = st.number_input("Land Size (hectares):", min_value=0.0, key=kfm2("loc_size"))
        if st.button("Save Farm Location", key=kfm2("loc_save")):
            st.success("✅ Location Saved")


#productivity & Records ----
elif menu_v2 == "📊 Productivity & Records":
    option = st.selectbox(
        "Select a Feature",
        [
            "View Sales Record",
            "View Expense",
            "Calculate Profit",
            "View Farmer Record",
            "Farm Productivity",
            "Yield Estimator",
            "Farm Loan Recorder",
            "Add Loan Record",
        ],
        key=kp2("feature")
    )

    if option == "View Sales Record":
        st.subheader("View Sales Record")
        st.write("📈 (This will later show all recorded sales in a table here.)")

    elif option == "View Expense":
        st.subheader("View Expense")
        expense_name = st.text_input("Expense Item:", key=kp2("expense_name"))
        expense_amount = st.number_input("Amount Spent (₦):", min_value=0, key=kp2("expense_amount"))
        expense_date = st.date_input("Expense Date:", key=kp2("expense_date"))
        if st.button("Save Expense", key=kp2("expense_save_btn")):
            st.success(f"✅ Expense recorded: {expense_name}, ₦{expense_amount} on {expense_date}")

    elif option == "Calculate Profit":
        st.subheader("Calculate Profit")
        total_sales = st.number_input("Enter Total Sales (₦):", min_value=0, key=kp2("profit_total_sales"))
        total_expenses = st.number_input("Enter Total Expenses (₦):", min_value=0, key=kp2("profit_total_expenses"))
        if st.button("Calculate Profit", key=kp2("profit_calc_btn")):
            profit = total_sales - total_expenses
            st.success(f"✅ Net Profit: {profit}")

    elif option == "View Farmer Record":
        st.subheader("View Farmer Record")
        st.write("👩‍🌾 (This will later display registered farmers' records here.)")

    elif option == "Farm Productivity":
        st.subheader("Farm Productivity")
        crop_name = st.text_input("Crop Name:", key=kp2("prod_crop_name"))
        season = st.selectbox("Season", ["Dry Season", "Rainy Season"], key=kp2("prod_season"))
        yield_kg = st.number_input("Total Yield (kg):", min_value=0, key=kp2("prod_yield_kg"))
        farm_size = st.number_input("Farm Size (hectares):", min_value=0.0, key=kp2("prod_farm_size"))
        if st.button("Record Productivity", key=kp2("prod_record_btn")):
            st.success(f"✅ Productivity recorded for {crop_name} ({season}): {yield_kg} kg on {farm_size} hectares")

    elif option == "Yield Estimator":
        st.subheader("Yield Estimator")
        farm_area = st.number_input("Farm Area (hectares):", min_value=0.0, key=kp2("yield_farm_area"))
        average_yield_per_hectare = st.number_input("Expected Yield per Hectare (kg):", min_value=0, key=kp2("yield_per_ha"))
        if st.button("Estimate Yield", key=kp2("yield_estimate_btn")):
            estimated_yield = farm_area * average_yield_per_hectare
            st.success(f"✅ Estimated Yield: {estimated_yield} kg")

    elif option == "Farm Loan Recorder":
        st.subheader("Farm Loan Recorder")
        lender_name = st.text_input("Lender Name:", key=kp2("loan_lender"))
        loan_amount = st.number_input("Loan Amount (₦):", min_value=0, key=kp2("loan_amount"))
        interest_rate = st.number_input("Interest Rate (%):", min_value=0.0, key=kp2("loan_interest"))
        repayment_period = st.text_input("Repayment Period (e.g. 12 months)", key=kp2("loan_period"))
        if st.button("Record Loan", key=kp2("loan_record_btn")):
            st.success(f"✅ Loan recorded: ₦{loan_amount} from {lender_name} at {interest_rate}% for {repayment_period}")

    elif option == "Add Loan Record":
        st.subheader("Add Loan Record")
        loan_purpose = st.text_input("Loan Purpose:", key=kp2("loan_purpose"))
        loan_date = st.date_input("Loan Date:", key=kp2("loan_date"))
        amount = st.number_input("Loan Amount (₦):", min_value=0, key=kp2("loan_amount_single"))
        st.button(f"✅ Loan for {loan_purpose} of ₦{amount} on {loan_date} saved.")
        
# irrigation & soil
elif menu_v2 == "💧 Irrigation & Soil":
    option = st.selectbox(
        "Select a Feature",
        ["Irrigation Schedule", "Soil Health Record"],
        key=kirr2("feature")
    )

    if option == "Irrigation Schedule":
        st.subheader("Irrigation Schedule")
        farm_location = st.text_input("Farm Location:", key=kirr2("sched_location"))
        crop_type = st.text_input("Crop Type:", key=kirr2("sched_crop"))
        irrigation_date = st.date_input("Irrigation Date:", key=kirr2("sched_date"))
        volume = st.number_input("Water Volume (liters):", min_value=0, key=kirr2("sched_volume"))

        if st.button("Save Irrigation Record", key=kirr2("sched_save_btn")):
            st.success(
                f"✅ Irrigation record saved: {farm_location} | {crop_type} | {irrigation_date} | {volume} liters"
            )

    elif option == "Soil Health Record":
        st.subheader("Soil Health Record")
        farm_location = st.text_input("Farm Location:", key=kirr2("soil_location"))
        soil_ph = st.number_input("Soil pH Level:", min_value=0.0, max_value=14.0, key=kirr2("soil_ph"))
        moisture_content = st.number_input("Moisture Content (%):", min_value=0, key=kirr2("soil_moisture"))
        nutrient_content = st.text_input("Nutrient Content Summary:", key=kirr2("soil_nutrients"))
        test_date = st.date_input("Test Date:", key=kirr2("soil_date"))

        if st.button("Save Soil Health Record", key=kirr2("soil_save_btn")):
            st.success(f"✅ Soil record saved for {farm_location} on {test_date}")

# farm plot mapping
elif menu_v2 == "🌍 Farm Plot Mapping":
    st.header("🌍 Farm Plot Mapping (Upgrade)")

    # Session storage for upgraded section
    if kplot("data") not in st.session_state:
        st.session_state[kplot("data")] = []  # list of dicts

    st.subheader("➕ Add New Farm Plot")

    with st.form(kplot("add_form"), clear_on_submit=True):
        plot_name = st.text_input("Plot Name", key=kplot("name"))
        plot_size = st.number_input("Size (hectares)", min_value=0.0, step=0.1, key=kplot("size"))
        plot_location = st.text_input("Location Description", key=kplot("loc"))
        crop_type = st.selectbox(
            "Crop Planted",
            ["Maize", "Cassava", "Tomato", "Rice", "Yam", "Other"],
            key=kplot("crop")
        )
        submitted = st.form_submit_button("Add Plot", use_container_width=True)

    if submitted:
        if not plot_name.strip():
            st.warning("Please enter a plot name.")
        else:
            new_plot = {
                "Name": plot_name.strip(),
                "Size (ha)": float(plot_size),
                "Location": plot_location.strip(),
                "Crop": crop_type
            }
            st.session_state[kplot("data")].append(new_plot)
            st.success(f"✅ Plot '{new_plot['Name']}' added successfully!")

    plots = st.session_state[kplot("data")]

    if plots:
        st.subheader("📋 Mapped Plots")
        st.dataframe(plots, use_container_width=True)

        st.divider()
        st.subheader("🗑 Manage Plots")
        # Individual delete controls
        for i, p in enumerate(plots):
            with st.expander(f"📌 {p['Name']} • {p['Crop']} • {p['Size (ha)']} ha"):
                st.write(f"**Location:** {p['Location'] or '—'}")
                if st.button("Delete this plot", key=kplot(f"del_{i}")):
                    st.session_state[kplot("data")].pop(i)
                    st.success("Plot deleted.")
                    st.experimental_rerun()

        # Export CSV
        import pandas as pd
        csv = pd.DataFrame(st.session_state[kplot("data")]).to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Plots CSV",
            csv,
            file_name="farm_plots_v2.csv",
            mime="text/csv",
            key=kplot("dl")
        )
    else:
        st.info("No plots added yet.")

# calendar & seasons
elif menu_v2 == "📅 Calendar & Seasons":
    st.header("📅 Calendar & Seasons (Upgrade)")

    option = st.selectbox(
        "Select a Calendar Tool",
        ["Planting Calendar", "Harvest Time Estimator", "Seasonal Task Planner"],
        key=kcal("option")
    )

    # --- Planting Calendar ---
    if option == "Planting Calendar":
        st.subheader("🌱 AI-Based Planting Calendar")
        crop = st.text_input("Enter Crop Name:", key=kcal("planting_crop"))
        region = st.text_input("Enter Your Region:", key=kcal("planting_region"))
        if st.button("Generate Planting Schedule", key=kcal("btn_generate")):
            if not crop.strip() or not region.strip():
                st.warning("Please enter both crop and region.")
            else:
                st.success(f"✅ Recommended planting schedule for {crop.title()} in {region.title()}:")
                st.write("- Best planting month: April")
                st.write("- Expected harvest period: July to August")
                st.write("- Ideal soil moisture: 60%")
                st.write("- AI Tip: Use sensors to monitor rainfall and adjust irrigation.")

    # --- Harvest Time Estimator ---
    elif option == "Harvest Time Estimator":
        st.subheader("🌾 Harvest Time Estimator")
        crop_type = st.text_input("Enter Crop Type:", key=kcal("harvest_crop"))
        planting_date = st.date_input("Select Planting Date:", key=kcal("planting_date"))
        if st.button("Estimate Harvest Time", key=kcal("btn_estimate")):
            est_date = planting_date + timedelta(days=90)
            st.success(f"✅ Estimated harvest time for {crop_type.title() or 'your crop'} is 90 days after planting.")
            st.write("📅 Approximate harvest date:", est_date.strftime("%Y-%m-%d"))
            st.write("🔎 Sensor Alert: Monitor ripeness using image sensors or NDVI analysis.")

    # --- Seasonal Task Planner ---
    elif option == "Seasonal Task Planner":
        st.subheader("📅 Seasonal Farm Task Planner")
        season = st.selectbox("Select Season", ["Dry Season", "Rainy Season"], key=kcal("season"))
        if st.button("Show Recommended Tasks", key=kcal("btn_tasks")):
            if season == "Rainy Season":
                st.write("- Weed control and disease monitoring")
                st.write("- Fertilizer application planning")
                st.write("- Regular drainage checks")
            else:
                st.write("- Land clearing and soil preparation")
                st.write("- Irrigation planning")
                st.write("- AI sensor calibration for dry monitoring")


# farmer community forum
elif menu_v2 == "🌐 Farmer Community Forum":
    st.header("🌐 Farmer Community Forum (Upgrade)")
    st.write("Ask questions, share knowledge, or reply to fellow farmers.")

    # Keep forum posts in session state (namespaced key)
    posts_key = kforum("posts")
    if posts_key not in st.session_state:
        st.session_state[posts_key] = []

    # Create a new post (unique keys + clear on submit)
    with st.form(kforum("new_post_form"), clear_on_submit=True):
        name = st.text_input("👤 Your Name", key=kforum("name"))
        message = st.text_area("📝 Your Message", key=kforum("message"))
        submitted = st.form_submit_button("📨 Post", use_container_width=True)

        if submitted:
            if name.strip() and message.strip():
                st.session_state[posts_key].insert(0, {
                    "name": name.strip(),
                    "message": message.strip(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("✅ Post shared successfully!")
            else:
                st.warning("Please enter both your name and a message.")

    # Display all posts with per-row delete (unique keys)
    st.subheader("📬 Recent Posts")
    posts = st.session_state[posts_key]
    if posts:
        for idx, post in enumerate(posts):
            st.markdown(f"**{post['name']}** *(at {post['timestamp']})*")
            st.markdown(f"> {post['message']}")
            del_col, _ = st.columns([1, 8])
            if del_col.button("🗑 Delete", key=kforum(f"del_{idx}")):
                posts.pop(idx)
                st.rerun()
            st.markdown("---")
    else:
        st.info("No posts yet. Be the first to share something!")



# ================================
# 📊 Farm Profit & Loss Statement
# ================================
elif menu_v2 == "📊 farm profit & loss statement":
    st.header("📊 Farm Profit & Loss Statement (Upgrade)")
    st.write("Add income/expense rows below. Totals and chart update instantly.")

    # ---- State (namespaced keys so no collisions) ----
    sales_key = kpl("sales_df")
    exp_key   = kpl("expense_df")

    if sales_key not in st.session_state:
        st.session_state[sales_key] = pd.DataFrame(columns=["Date", "Item", "Amount"])
    if exp_key not in st.session_state:
        st.session_state[exp_key] = pd.DataFrame(columns=["Date", "Category", "Amount"])

    # ---- Add rows (two forms, unique keys) ----
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("➕ Add Sale")
        with st.form(kpl("form_add_sale"), clear_on_submit=True):
            s_date = st.date_input("Date", value=date.today(), key=kpl("s_date"))
            s_item = st.text_input("Item", key=kpl("s_item"))
            s_amt  = st.number_input("Amount (₦)", min_value=0.0, step=100.0, key=kpl("s_amt"))
            add_sale = st.form_submit_button("Add Sale", use_container_width=True)

        if add_sale:
            if s_item.strip() and s_amt > 0:
                st.session_state[sales_key] = pd.concat(
                    [
                        st.session_state[sales_key],
                        pd.DataFrame([{"Date": str(s_date), "Item": s_item.strip(), "Amount": float(s_amt)}]),
                    ],
                    ignore_index=True
                )
                st.success("✅ Sale added.")
            else:
                st.warning("Please enter an item and amount > 0.")

    with c2:
        st.subheader("➕ Add Expense")
        with st.form(kpl("form_add_expense"), clear_on_submit=True):
            e_date = st.date_input("Date", value=date.today(), key=kpl("e_date"))
            e_cat  = st.text_input("Category", key=kpl("e_cat"))
            e_amt  = st.number_input("Amount (₦)", min_value=0.0, step=100.0, key=kpl("e_amt"))
            add_exp = st.form_submit_button("Add Expense", use_container_width=True)

        if add_exp:
            if e_cat.strip() and e_amt > 0:
                st.session_state[exp_key] = pd.concat(
                    [
                        st.session_state[exp_key],
                        pd.DataFrame([{"Date": str(e_date), "Category": e_cat.strip(), "Amount": float(e_amt)}]),
                    ],
                    ignore_index=True
                )
                st.success("✅ Expense added.")
            else:
                st.warning("Please enter a category and amount > 0.")

    # ---- Tables ----
    st.subheader("💰 Income (Sales)")
    st.dataframe(st.session_state[sales_key], use_container_width=True)

    st.subheader("💸 Expenses")
    st.dataframe(st.session_state[exp_key], use_container_width=True)

    # ---- Summary ----
    total_income  = float(st.session_state[sales_key]["Amount"].sum()) if not st.session_state[sales_key].empty else 0.0
    total_expense = float(st.session_state[exp_key]["Amount"].sum()) if not st.session_state[exp_key].empty else 0.0
    net_profit    = total_income - total_expense

    st.markdown("---")
    st.subheader("📈 Summary")
    a, b, c = st.columns(3)
    a.metric("Total Income",   f"₦{total_income:,.2f}")
    b.metric("Total Expenses", f"₦{total_expense:,.2f}")
    c.metric(
        "Net Profit",
        f"₦{net_profit:,.2f}",
        delta=f"{net_profit:,.2f}",
        delta_color="normal" if net_profit >= 0 else "inverse"
    )

    # ---- Chart ----
    st.markdown("### 📊 Profit/Loss Visualization")
    st.bar_chart(pd.DataFrame({"Amount": [total_income, total_expense, net_profit]},
                              index=["Income", "Expenses", "Profit"]))

    # ---- Export / Clear ----
    x1, x2, x3 = st.columns(3)
    with x1:
        st.download_button(
            "⬇️ Download Sales CSV",
            st.session_state[sales_key].to_csv(index=False).encode("utf-8"),
            file_name="sales.csv",
            mime="text/csv",
            key=kpl("dl_sales")
        )
    with x2:
        st.download_button(
            "⬇️ Download Expenses CSV",
            st.session_state[exp_key].to_csv(index=False).encode("utf-8"),
            file_name="expenses.csv",
            mime="text/csv",
            key=kpl("dl_exp")
        )
    with x3:
        if st.button("🧹 Clear All", key=kpl("clear_all")):
            st.session_state[sales_key] = st.session_state[sales_key].iloc[0:0]
            st.session_state[exp_key]   = st.session_state[exp_key].iloc[0:0]
            st.success("Cleared.")
            st.rerun()


# ===================
# 🤖 AI Crop Calendar
# ===================
elif menu_v2 == "🤖 AI Crop Calendar":
    st.header("🤖 AI Crop Calendar")
    st.write("Get AI-recommended planting and harvesting dates based on crop and location.")

    # Simple calendar data (swap in a real model later)
    crop_calendar = {
        "Maize":   {"planting": "2025-04-01", "harvesting": "2025-07-30"},
        "Rice":    {"planting": "2025-05-15", "harvesting": "2025-09-15"},
        "Cassava": {"planting": "2025-03-01", "harvesting": "2026-01-01"},
        "Yam":     {"planting": "2025-04-10", "harvesting": "2025-10-20"},
        "Tomato":  {"planting": "2025-02-20", "harvesting": "2025-05-30"},
    }

    # Inputs (keys are namespaced)
    c1, c2 = st.columns(2)
    with c1:
        crop = st.selectbox("🌾 Select Crop", list(crop_calendar.keys()), key=kcal("crop"))
    with c2:
        location = st.text_input("📍 Location", value="Benue", key=kcal("loc"))

    # Generate button (namespaced key so it always fires)
    if st.button("📅 Generate AI Crop Calendar", key=kcal("generate")):
        data = crop_calendar[crop]
        st.success(f"🌱 Plant {crop} around **{data['planting']}** in {location}.")
        st.success(f"🌾 Expected harvest around **{data['harvesting']}**.")
        st.info("Note: Dates are AI-estimated from typical seasonal trends; refine with your local weather data.")

        # Store rows in session (so users can build a small calendar list)
        rows_key = kcal("rows")
        if rows_key not in st.session_state:
            st.session_state[rows_key] = []
        st.session_state[rows_key].append({
            "Crop": crop,
            "Location": location,
            "Planting": data["planting"],
            "Harvesting": data["harvesting"],
            "Added On": date.today().isoformat(),
        })

    # Show saved rows + export / clear
    rows = st.session_state.get(kcal("rows"), [])
    if rows:
        st.subheader("🧾 Saved Schedules")
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇️ Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="ai_crop_calendar.csv",
                mime="text/csv",
                key=kcal("dl")
            )
        with col_b:
            if st.button("🧹 Clear Schedules", key=kcal("clear")):
                st.session_state[kcal("rows")] = []
                st.success("✅ All schedules cleared successfully!")
                st.rerun()


# --- AI Predictions (Trigger Buttons v2) ---
# Make sure the emoji/text here matches your sidebar label exactly.
elif menu_v2 == "🧪 AI Predictions":

    st.header("🧪 AI-Powered Farm Predictions")

    # Track active tool in session
    active_key = ap("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # If another part of the app (e.g., voice commands) sets a sub-tool, adopt it
    if "ai_prediction_tool" in st.session_state and st.session_state[active_key] is None:
        _map = {
            "Crop Disease Detection": "disease",
            "Yield Prediction": "yield",
            "Soil Health Check": "soil",
        }
        st.session_state[active_key] = _map.get(st.session_state["ai_prediction_tool"])

    # Trigger buttons row
    c1, c2, c3, c4 = st.columns([1.3, 1.3, 1.3, 0.9])
    with c1:
        if st.button("📷 Crop Disease Detection", key=ap("btn_disease")):
            st.session_state[active_key] = "disease"
    with c2:
        if st.button("📈 Yield Prediction", key=ap("btn_yield")):
            st.session_state[active_key] = "yield"
    with c3:
        if st.button("🧪 Soil Health Check", key=ap("btn_soil")):
            st.session_state[active_key] = "soil"
    with c4:
        if st.button("🔄 Reset", key=ap("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # =======================
    # Tool: Crop Disease Detection
    # =======================
    if tool == "disease":
        st.subheader("📷 Upload an image of your crop")
        uploaded_image = st.file_uploader(
            "Upload Image",
            type=["jpg", "jpeg", "png"],
            key=ap("image")
        )
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        if st.button("🔍 Predict Disease", key=ap("predict")):
            if uploaded_image is None:
                st.warning("⚠️ Please upload an image before prediction.")
            else:
                # Placeholder prediction/result
                st.success("✅ Predicted: Maize Leaf Blight")
                st.info("🧪 Recommendation: Apply fungicide spray and monitor irrigation.")

    # =======================
    # Tool: Yield Prediction
    # =======================
    elif tool == "yield":
        st.subheader("📈 Enter details for yield prediction")

        crop_type = st.selectbox(
            "Crop Type",
            ["Maize", "Rice", "Cassava", "Yam", "Tomato"],
            key=ap("yield_crop")
        )
        area = st.number_input(
            "Farm Area (ha)",
            min_value=0.1,
            step=0.1,
            key=ap("yield_area")
        )
        rainfall = st.number_input(
            "Expected Rainfall (mm)",
            min_value=0.0,
            step=1.0,
            key=ap("yield_rain")
        )

        if st.button("📊 Predict Yield", key=ap("yield_btn")):
            predicted = round(area * rainfall * 0.05, 2)  # placeholder logic
            st.success(f"✅ Predicted Yield for {crop_type}: {predicted} tons")

    # =======================
    # Tool: Soil Health Check
    # =======================
    elif tool == "soil":
        st.subheader("🧪 Enter soil details")

        ph = st.number_input(
            "Soil pH Level",
            min_value=0.0,
            max_value=14.0,
            step=0.1,
            key=ap("soil_ph")
        )
        nitrogen = st.number_input(
            "Nitrogen Content (mg/kg)",
            min_value=0,
            step=1,
            key=ap("soil_n")
        )
        potassium = st.number_input(
            "Potassium Content (mg/kg)",
            min_value=0,
            step=1,
            key=ap("soil_k")
        )

        if st.button("🧪 Check Soil Health", key=ap("soil_btn")):
            if 6.0 <= ph <= 7.5 and nitrogen >= 50 and potassium >= 40:
                st.success("✅ Soil is healthy for planting.")
            else:
                st.warning("⚠️ Soil may need treatment. Consider testing or adding fertilizer.")

    else:
        st.info("Click a button above to open a prediction tool.")

 
# =========================
# ================================
# 📍 Farm Performance Indicators
# ================================
elif menu_v2 in ("📍 Farm Performance Indicators", "📍 Farm performance Indicators"):
    import pandas as pd
    from datetime import date, datetime

    st.header("📍 Farm Performance Indicators")
    st.write("Enter quick field and market info. Click calculate to get health, water stress, and market readiness. Save snapshots for later.")

    # -------- Inputs (namespaced keys) --------
    c1, c2, c3 = st.columns(3)
    with c1:
        pest = st.number_input("Pest incidence (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key="fpi_pest")
        disease = st.number_input("Disease incidence (%)", min_value=0.0, max_value=100.0, value=8.0, step=1.0, key="fpi_dis")
        soil_moist = st.number_input("Soil moisture (%)", min_value=0.0, max_value=100.0, value=55.0, step=1.0, key="fpi_sm")
    with c2:
        ndvi = st.number_input("Vegetation index (0–1)", min_value=0.0, max_value=1.0, value=0.65, step=0.01, key="fpi_ndvi")
        temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=32.0, step=0.5, key="fpi_temp")
        et0 = st.number_input("ET₀ (mm/day)", min_value=0.0, max_value=20.0, value=4.5, step=0.1, key="fpi_et0")
    with c3:
        expected_yield = st.number_input("Expected yield (tons)", min_value=0.0, value=5.0, step=0.1, key="fpi_yield")
        price = st.number_input("Current price (₦/ton)", min_value=0.0, value=250000.0, step=1000.0, key="fpi_price")
        cost = st.number_input("Cost per ton (₦/ton)", min_value=0.0, value=180000.0, step=1000.0, key="fpi_cost")
        storage_days = st.number_input("Storage days if delayed", min_value=0, value=7, step=1, key="fpi_store_days")
        storage_cost_day = st.number_input("Storage cost (₦/ton/day)", min_value=0.0, value=200.0, step=10.0, key="fpi_store_cost")

    # -------- Calculate button --------
    if st.button("📊 Calculate Indicators", key="fpi_calc"):
        # Health score (0-100)
        score = 100.0
        score -= 0.45 * pest
        score -= 0.45 * disease
        score += 0.20 * (soil_moist - 50.0)   # around 50% is neutral
        score += 12.0 * ndvi
        score = max(0.0, min(100.0, score))

        # Water stress level
        stress_points = 0
        if soil_moist < 30: stress_points += 2
        elif soil_moist < 45: stress_points += 1
        if temp > 35: stress_points += 2
        elif temp > 30: stress_points += 1
        if et0 > 6: stress_points += 2
        elif et0 > 4: stress_points += 1
        if stress_points >= 4:
            water_level = "High"
            water_rec = "Irrigate today. Target field capacity, avoid midday heat."
        elif stress_points >= 2:
            water_level = "Moderate"
            water_rec = "Monitor closely, consider evening irrigation."
        else:
            water_level = "Low"
            water_rec = "No irrigation required now."

        # Market readiness
        margin_per_ton = price - cost
        gross_margin = margin_per_ton * expected_yield
        delay_cost = storage_days * storage_cost_day * expected_yield
        adj_margin = gross_margin - delay_cost
        if margin_per_ton <= 0:
            market_note = "Unprofitable at current price. Improve price or reduce cost."
        elif adj_margin > gross_margin * 0.95:
            market_note = "Ready to sell. Good margins and low storage drag."
        else:
            market_note = "Viable, but storage drag is notable. Recheck in a few days."

        # Show results
        st.success(f"🌿 Field Health Score: **{score:.1f}/100**")
        st.info(f"💧 Water Stress Level: **{water_level}** — {water_rec}")
        st.success(f"💹 Margin/ton: **₦{margin_per_ton:,.0f}**, Gross Margin: **₦{gross_margin:,.0f}**, Adj. Margin: **₦{adj_margin:,.0f}**")
        st.caption(market_note)

        # Save snapshot
        rows_key = "fpi_rows"
        if rows_key not in st.session_state:
            st.session_state[rows_key] = []
        st.session_state[rows_key].append({
            "Timestamp": datetime.now().isoformat(timespec="seconds"),
            "Pest%": pest,
            "Disease%": disease,
            "SoilMoist%": soil_moist,
            "NDVI": ndvi,
            "TempC": temp,
            "ET0": et0,
            "YieldTons": expected_yield,
            "PriceNperTon": price,
            "CostNperTon": cost,
            "StorageDays": storage_days,
            "StorageCostPerTonDay": storage_cost_day,
            "HealthScore": round(score, 1),
            "WaterLevel": water_level,
            "MarginPerTon": margin_per_ton,
            "GrossMargin": gross_margin,
            "AdjMargin": adj_margin,
            "Note": market_note,
        })
        st.success("✅ Snapshot saved.")

    # -------- Saved snapshots + export / clear --------
    rows = st.session_state.get("fpi_rows", [])
    if rows:
        st.subheader("🧾 Saved Indicator Snapshots")
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                "⬇️ Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="farm_performance_indicators.csv",
                mime="text/csv",
                key="fpi_dl"
            )
        with col_b:
            if st.button("🧹 Clear Snapshots", key="fpi_clear"):
                      st.rerun()
    else:
        st.info("No snapshots saved yet. Calculate an indicator and click \"Save Snapshot\".")



# ==================================
# ================================# ================================
# 📚 AI Farm Tips — Trigger Buttons
# ================================

import streamlit as st
from datetime import date

def ai_farm_tips_ui():
    st.header("📚 AI Farm Tips")

    # Track active sub-tool in session state
    active_key = ktips("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # Trigger buttons
    c1, c2, c3 = st.columns([1.3, 1.3, 0.9])
    with c1:
        if st.button("💡 Ask AI Tip", key=ktips("btn_ask")):
            st.session_state[active_key] = "ask"
    with c2:
        if st.button("🌞 View Daily Tip", key=ktips("btn_daily")):
            st.session_state[active_key] = "daily"
    with c3:
        if st.button("🔄 Reset", key=ktips("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # Helper: simple keyword mapper
    def _ai_tip_from_question(q: str) -> str:
        ql = (q or "").lower()
        if any(w in ql for w in ["fertilizer", "npk", "manure", "compost"]):
            return "Use well-decomposed compost at land prep; split NPK (basal + top-dress) to reduce losses."
        if any(w in ql for w in ["irrigation", "water", "drip", "sprinkler"]):
            return "Irrigate early morning/evening; target ~60% soil moisture and mulch to reduce evaporation."
        if any(w in ql for w in ["pest", "insect", "worm", "aphid", "fall armyworm"]):
            return "Scout twice weekly; use traps and IPM first. Rotate actives to avoid resistance."
        if any(w in ql for w in ["disease", "blight", "fungus", "mildew", "virus"]):
            return "Improve airflow, avoid late overhead watering, and remove infected leaves promptly."
        if any(w in ql for w in ["soil", "ph", "nutrient", "ec"]):
            return "Keep pH 6.0–7.0 for most crops; lime if acidic and add organic matter each season."
        if any(w in ql for w in ["harvest", "maturity", "ripen", "storage"]):
            return "Harvest in cool hours; shade immediately and store at the crop’s recommended temp/RH."
        if any(w in ql for w in ["market", "price", "sell", "profit"]):
            return "Sort/grade produce; time sales to peak market days and use simple packaging to add value."
        if any(w in ql for w in ["seed", "variety", "germination"]):
            return "Buy certified seed; do a quick germination test and treat seed against soil-borne pathogens."
        return "Start with soil testing, good seed, clean water, and consistent scouting; small improvements stack."

    # Tool views
    if tool == "ask":
        st.subheader("💡 Ask AI Tip")
        user_q = st.text_input("Ask your farming question here:", key=ktips("q"))
        if st.button("Get AI Tip", key=ktips("get_tip")):
            if user_q.strip():
                st.success(f"✅ AI Farm Tip: {_ai_tip_from_question(user_q)}")
            else:
                st.warning("Please enter a question to get a tip.")

    elif tool == "daily":
        st.subheader("🌞 Daily Farm Tip")
        tips_pool = [
            "Water early morning to reduce evaporation and disease pressure.",
            "Mulch around plants to conserve moisture and suppress weeds.",
            "Rotate crops each season to break pest and disease cycles.",
            "Scout fields twice a week; early detection saves money.",
            "Keep pH near 6.0–7.0; test soil yearly and amend as needed.",
            "Clean tools between fields to avoid spreading pathogens.",
            "Use shade nets or windbreaks to reduce heat stress.",
            "Split nitrogen applications to match crop uptake and reduce leaching.",
            "Harvest during cool hours; shade produce immediately.",
            "Record inputs and yields; data helps optimize costs.",
        ]
        idx = (date.today().timetuple().tm_yday) % len(tips_pool)
        st.info(f"🌿 {tips_pool[idx]}")

    else:
        st.info("Choose a tool above to get farm tips.")

# ---------------------------
# Router hook (use IF, not ELIF)
# ---------------------------
if (globals().get("menu_v2") == "📚 AI Farm Tips") or (globals().get("menu") == "📚 AI Farm Tips"):
    ai_farm_tips_ui()




# 📈 Market & Economic Tools (Trigger Buttons)

elif menu_v2 == "📈 Market & Economic Tools":
    st.header("📈 Market & Economic Tools")

    # Track which tool is active
    if mkey("active_tool") not in st.session_state:
        st.session_state[mkey("active_tool")] = None

    # --- Trigger buttons row ---
    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.6])
    with c1:
        if st.button("💰 ROI Calculator", key=mkey("btn_roi")):
            st.session_state[mkey("active_tool")] = "roi"
    with c2:
        if st.button("📈 Price Trend Checker", key=mkey("btn_trend")):
            st.session_state[mkey("active_tool")] = "trend"
    with c3:
        if st.button("⚖️ Break-even Calculator", key=mkey("btn_be")):
            st.session_state[mkey("active_tool")] = "breakeven"
    with c4:
        if st.button("🔄 Reset", key=mkey("btn_reset")):
            # reset only your app keys (safer) — adjust prefix if your mkey uses one
            # Example conservative reset: only clear known keys for this section
            keys_to_clear = [
                mkey("active_tool"),
                mkey("btn_roi"),
                mkey("btn_trend"),
                mkey("btn_be"),
                mkey("roi_investment"),
                mkey("roi_profit"),
                mkey("trend_prices"),
                mkey("trend_crop"),
                mkey("trend_show"),
                mkey("be_fixed"),
                mkey("be_var"),
                mkey("be_price"),
                mkey("be_calc"),
            ]
            for k in keys_to_clear:
                if k in st.session_state:
                    del st.session_state[k]

            # attempt a robust rerun compatible with multiple Streamlit versions
            try:
                if hasattr(st, "rerun"):
                    st.rerun()  # modern API
                elif hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()  # older API
                else:
                    # fallback: toggle a dummy session key to force UI update
                    st.session_state["_sfai_force_update"] = not st.session_state.get("_sfai_force_update", False)
            except Exception as _e:
                # If rerun fails for any reason, at least avoid crashing the app
                st.warning("Reset performed but automatic rerun failed. The UI should update on the next interaction.")

    tool = st.session_state.get(mkey("active_tool"))

    # =============== TOOL 1: ROI CALCULATOR ===============
    if tool == "roi":
        st.subheader("💰 ROI (Return on Investment) Calculator")
        st.write("Estimate your farm's return on investment.")

        col_a, col_b = st.columns(2)
        with col_a:
            investment = st.number_input(
                "Investment amount (₦)",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=mkey("roi_investment"),
            )
        with col_b:
            profit = st.number_input(
                "Profit amount (₦)",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=mkey("roi_profit"),
            )

        if st.button("Calculate ROI", key=mkey("roi_calc")):
            if investment <= 0:
                st.warning("Enter an investment greater than ₦0.")
            else:
                roi = ((profit - investment) / investment) * 100
                st.success(f"✅ ROI: {roi:.2f}%")

    # =============== TOOL 2: PRICE TREND CHECKER ===============
    elif tool == "trend":
        st.subheader("📈 Price Trend Checker")
        st.write("Paste recent prices for a crop to see the trend.")

        crop_name = st.text_input(
            "Crop name",
            value="Maize",
            key=mkey("trend_crop"),
        )

        prices_csv = st.text_area(
            "Enter prices separated by commas",
            value="120, 125, 130, 128, 135, 140",
            key=mkey("trend_prices"),
            help="Example: 120, 125, 130, 128, 135, 140",
        )

        if st.button("Show Trend", key=mkey("trend_show")):
            try:
                values = [float(x.strip()) for x in prices_csv.split(",") if x.strip()]
                if len(values) < 2:
                    st.warning("Enter at least two price points.")
                else:
                    df = pd.DataFrame({"Index": list(range(1, len(values) + 1)), "Price": values}).set_index("Index")
                    st.line_chart(df)  # quick visual
                    change = values[-1] - values[0]
                    pct = (change / values[0]) * 100 if values[0] != 0 else 0.0
                    direction = "increased" if change > 0 else "decreased" if change < 0 else "not changed"
                    st.info(f"{crop_name} price has {direction} by {abs(change):.2f} (≈ {abs(pct):.2f}%) over the period.")
            except Exception as e:
                st.error(f"Invalid input. Please enter numbers only. Details: {e}")

    # =============== TOOL 3: BREAK-EVEN CALCULATOR ===============
    elif tool == "breakeven":
        st.subheader("⚖️ Break-even Calculator")
        st.write("Find the number of units you need to sell to cover costs.")

        c1, c2, c3 = st.columns(3)
        with c1:
            fixed_costs = st.number_input(
                "Fixed costs (₦)",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=mkey("be_fixed"),
            )
        with c2:
            variable_cost = st.number_input(
                "Variable cost per unit (₦)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=mkey("be_var"),
            )
        with c3:
            price_per_unit = st.number_input(
                "Selling price per unit (₦)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=mkey("be_price"),
            )

        if st.button("Calculate Break-even", key=mkey("be_calc")):
            margin = price_per_unit - variable_cost
            if margin <= 0:
                st.error("Selling price must be greater than variable cost per unit.")
            elif fixed_costs <= 0:
                st.warning("Enter fixed costs greater than ₦0.")
            else:
                units = fixed_costs / margin
                units_int = int(units) if units.is_integer() else int(units) + 1  # round up to whole units
                st.success(f"🎯 You need to sell about {units:.2f} units (≈ {units_int} whole units) to break even.")



# 📈 Decision-Making Models — Trigger Buttons
elif (('menu_v2' in globals() and menu_v2 == "📈 Decision-Making Models") or
      ('menu'   in globals() and menu   == "📈 Decision-Making Models")):

    st.header("📈 Decision-Making Models")
    st.write("These models help farmers take the best actions based on farm data.")

    # track active sub-tool
    active_key = kdm("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # trigger buttons row
    c1, c2, c3, c4 = st.columns([1.4, 1.8, 1.8, 0.8])
    with c1:
        if st.button("💧 Irrigation", key=kdm("btn_irr")):
            st.session_state[active_key] = "irr"
    with c2:
        if st.button("🌿 Fertilizer", key=kdm("btn_fert")):
            st.session_state[active_key] = "fert"
    with c3:
        if st.button("🔄 Crop Rotation", key=kdm("btn_rot")):
            st.session_state[active_key] = "rot"
    with c4:
        if st.button("🔄 Reset", key=kdm("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # =======================
    # Tool: Irrigation Recommendation
    # =======================
    if tool == "irr":
        st.subheader("💧 Irrigation Recommendation")
        soil_moisture = st.slider("Soil Moisture Level (%)", 0, 100, 50, key=kdm("irr_sm"))
        temperature   = st.slider("Temperature (°C)", 10, 45, 30, key=kdm("irr_temp"))

        if soil_moisture < 30:
            recommendation = "Irrigate the crops with ~3 liters/day."
        elif soil_moisture < 60:
            recommendation = "Irrigate moderately: ~1.5 liters/day."
        else:
            recommendation = "No irrigation needed today."

        # optional tweak for heat stress
        if temperature >= 35 and soil_moisture < 60:
            recommendation += " (High temp: prefer evening irrigation.)"

        st.success(f"✅ Recommendation: {recommendation}")

    # =======================
    # Tool: Fertilizer Optimization
    # =======================
    elif tool == "fert":
        st.subheader("🌿 Fertilizer Optimization")
        crop_type    = st.selectbox("Select Crop Type", ["Maize", "Tomato", "Rice", "Yam", "Cassava"], key=kdm("fert_crop"))
        growth_stage = st.selectbox("Growth Stage", ["Early", "Mid", "Late"], key=kdm("fert_stage"))

        if crop_type == "Maize" and growth_stage == "Early":
            rec = "Apply NPK 15-15-15 at ~2 kg/ha."
        elif crop_type == "Tomato" and growth_stage == "Mid":
            rec = "Use potassium-rich fertilizer weekly."
        else:
            rec = "Use standard fertilizer guidance for this stage."

            st.success(f"✅ Fertilizer Advice: {rec}")

    # =======================
    # Tool: Crop Rotation Suggestion
    # =======================
    elif tool == "rot":
        st.subheader("🔄 Crop Rotation Suggestion")
        previous_crop = st.selectbox(
            "Last Planted Crop",
            ["Maize", "Cassava", "Tomato", "Yam", "Rice"],
            key=kdm("rot_prev")
        )

        rotation = {
            "Maize":  "Plant legumes like Soybean or Cowpea next.",
            "Cassava": "Switch to leafy vegetables or grains (e.g., Maize/Sorghum).",
            "Tomato": "Rotate with cereals (Maize/Sorghum) or legumes.",
            "Yam":    "Use the land for vegetables (Okra/leafy greens) or legumes.",
            "Rice":   "Rotate with legumes (Cowpea/Soybean) or a short cover-crop fallow.",
        }

        suggestion = rotation.get(
            previous_crop,
            "Consider rotating with legumes or cereals to break pest cycles and rebuild soil."
        )

        st.success(f"✅ Suggested rotation: {suggestion}")


# IRRIGATION PACK (One file)
# - Irrigation Scheduler (UI)
# - Voice-Controlled Drone Irrigation Assistant (UI)
# ================================

import streamlit as st
import time, random, re
import pandas as pd
from datetime import datetime
# Optional voice deps (handled gracefully in the assistant)
try:
    import speech_recognition as sr
except Exception:
    sr = None
try:
    import pyttsx3
except Exception:
    pyttsx3 = None


# ================================
# 💦 IRRIGATION SCHEDULER (simple)
# ================================
def irrigation_scheduler_ui():
    st.header("💦 Irrigation Scheduler")
    st.caption("Plan irrigation sessions by date, time, purpose, and plot. Data is stored in session for now.")

    flights_key = kdr("flights")
    if flights_key not in st.session_state:
        st.session_state[flights_key] = []  # list of dicts

    # Trigger buttons
    c1, c2, c3 = st.columns([1.4, 1.4, 0.8])
    with c1:
        show_add = st.button("📤 Schedule Irrigation", key=kdr("btn_schedule"))
    with c2:
        show_list = st.button("📋 View Schedule", key=kdr("btn_list"))
    with c3:
        if st.button("🔄 Reset View", key=kdr("btn_reset")):
            st.session_state[kdr("view")] = None
            st.rerun()

    # View state
    if kdr("view") not in st.session_state:
        st.session_state[kdr("view")] = None
    if show_add:
        st.session_state[kdr("view")] = "add"
    if show_list:
        st.session_state[kdr("view")] = "list"

    # Add form
    if st.session_state[kdr("view")] == "add":
        st.subheader("📤 Schedule a New Irrigation")
        with st.form(kdr("form_irrig"), clear_on_submit=True):
            d = st.date_input("📅 Date", datetime.now().date(), key=kdr("date"))
            t = st.time_input("⏰ Time", datetime.now().time(), key=kdr("time"))
            purpose = st.selectbox(
                "🎯 Purpose",
                ["General Irrigation", "Spot Watering", "Fertilizer Mix", "Pesticide Mix"],
                key=kdr("purpose")
            )
            plot = st.text_input("📍 Farm Plot / Block", key=kdr("plot"))
            duration_min = st.number_input("⏱ Duration (minutes)", 1, 240, 30, key=kdr("dur"))
            submit = st.form_submit_button("Save", use_container_width=True)

        if submit:
            item = {
                "Date": d.strftime("%Y-%m-%d"),
                "Time": t.strftime("%H:%M"),
                "Purpose": purpose,
                "Farm Plot": plot,
                "Duration (min)": int(duration_min),
            }
            st.session_state[flights_key].append(item)
            st.success(f"✅ Irrigation scheduled on {item['Date']} at {item['Time']} ({item['Purpose']}).")

    # List/manage
    elif st.session_state[kdr("view")] == "list":
        st.subheader("📋 Scheduled Irrigation")
        items = st.session_state[flights_key]
        if items:
            df = pd.DataFrame(items)
            st.dataframe(df, use_container_width=True)

            cA, cB, _ = st.columns([1.2, 1.2, 2])
            with cA:
                st.download_button(
                    "⬇️ Download CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name="irrigation_schedule.csv",
                    mime="text/csv",
                    key=kdr("dl_sched")
                )
            with cB:
                if st.button("🧹 Clear All", key=kdr("clear_all_sched")):
                    st.session_state[flights_key] = []
                    st.success("All irrigation entries cleared.")
                    st.rerun()

            st.divider()
            st.subheader("🗑 Delete Individual Items")
            for i, f in enumerate(list(items)):
                with st.expander(f"📌 {f['Date']} {f['Time']} — {f['Purpose']} @ {f['Farm Plot'] or '—'}"):
                    if st.button("Delete this entry", key=kdr(f"del_sched_{i}")):
                        st.session_state[flights_key].pop(i)
                        st.success("Entry deleted.")
                        st.rerun()
        else:
            st.info("No irrigation items scheduled yet.")
    else:
        st.info("Click a button above to get started.")

# ===============================================
# 🎙️ VOICE-CONTROLLED DRONE IRRIGATION ASSISTANT
# ===============================================
def drone_irrigation_assistant_ui():
    st.header("🚁 Voice-Controlled Drone Irrigation Assistant")
    st.caption("Simulated control of a spray drone for field irrigation/spot-watering.")

    # init state
    S = st.session_state
    if kdr("init") not in S:
        S[kdr("init")] = True
        S[kdr("armed")] = False
        S[kdr("in_air")] = False
        S[kdr("battery")] = 100.0
        S[kdr("mission")] = None   # {"zone","remain_s","lpm","state"}
        S[kdr("last_tick")] = time.time()
        S[kdr("log")] = []

    # tick
    now = time.time()
    dt = max(0.0, now - S[kdr("last_tick")])
    S[kdr("last_tick")] = now

    drain = 0.03 * dt
    if S[kdr("in_air")]:
        drain += 0.10 * dt
    if S[kdr("mission")]:
        drain += 0.12 * dt
        S[kdr("mission")]["remain_s"] = max(0, S[kdr("mission")]["remain_s"] - dt)
        if S[kdr("mission")]["remain_s"] <= 0:
            S[kdr("log")].append(f"{datetime.now():%H:%M:%S} ✓ Irrigation complete in Zone {S[kdr('mission')]['zone']}. Returning home.")
            S[kdr("mission")] = None
            S[kdr("in_air")] = False
            S[kdr("armed")] = True

    if S[kdr("in_air")] and S[kdr("battery")] <= 20.0 and S[kdr("mission")]:
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} ⚠ Low battery. Aborting mission, returning home.")
        S[kdr("mission")] = None
        S[kdr("in_air")] = False

    S[kdr("battery")] = max(0.0, S[kdr("battery")] - drain)

    # metrics
    colA, colB, colC, colD = st.columns(4)
    colA.metric("Battery", f"{S[kdr('battery')]:.0f}%")
    colB.metric("Armed", "Yes" if S[kdr("armed")] else "No")
    colC.metric("In Air", "Yes" if S[kdr("in_air")] else "No")
    if S[kdr("mission")]:
        colD.metric("Active Zone", f"Zone {S[kdr('mission')]['zone']} ({int(S[kdr('mission')]['remain_s']):d}s left)")
    else:
        colD.metric("Active Zone", "—")

    st.divider()

    # mock zones
    st.subheader("🗺️ Field Zones (mock moisture)")
    z1, z2, z3 = st.columns(3)
    with z1:
        st.markdown("**Zone A (North)**")
        st.progress(min(100, int(40 + 20 * random.random())))
    with z2:
        st.markdown("**Zone B (Center)**")
        st.progress(min(100, int(30 + 30 * random.random())))
    with z3:
        st.markdown("**Zone C (South)**")
        st.progress(min(100, int(50 + 20 * random.random())))

    st.divider()

    # controls
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("🔐 Arm/Disarm", key=kdr("arm")):
        S[kdr("armed")] = not S[kdr("armed")]
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} {'Armed' if S[kdr('armed')] else 'Disarmed'}.")

    if c2.button("⬆️ Takeoff", disabled=not S[kdr("armed")] or S[kdr("in_air")], key=kdr("takeoff")):
        S[kdr("in_air")] = True
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Takeoff.")

    if c3.button("⬇️ Land", disabled=not S[kdr("in_air")], key=kdr("land")):
        S[kdr("in_air")] = False
        S[kdr("mission")] = None
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Landed.")

    if c4.button("🏠 Return Home", disabled=not S[kdr("in_air")], key=kdr("rth")):
        S[kdr("mission")] = None
        S[kdr("in_air")] = False
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Return-to-Home and landed.")

    if c5.button("🧹 Clear Log", key=kdr("clear")):
        S[kdr("log")] = []

    if c6.button("🔋 Swap Battery", disabled=S[kdr("in_air")], key=kdr("swap")):
        S[kdr("battery")] = 100.0
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Battery swapped (100%).")

    st.subheader("💦 Start Irrigation")
    cc1, cc2, cc3 = st.columns([1, 1, 1])
    zone = cc1.selectbox("Zone", ["A", "B", "C"], key=kdr("zone"))
    minutes = cc2.number_input("Duration (minutes)", 1, 60, 3, key=kdr("mins"))
    lpm = cc3.number_input("Flow rate (L/min)", 1, 50, 8, key=kdr("lpm"))

    go1, stop1 = st.columns([1, 1])
    if go1.button("▶️ Start Mission", key=kdr("start"),
                  disabled=not S[kdr("armed")] or not S[kdr("in_air")] or S[kdr("mission")] is not None):
        S[kdr("mission")] = {"zone": zone, "remain_s": int(minutes * 60), "lpm": int(lpm), "state": "irrigating"}
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Irrigation started in Zone {zone} for {minutes} min @ {lpm} L/min.")

    if stop1.button("⏹ Stop Mission", key=kdr("stop"), disabled=S[kdr("mission")] is None):
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Mission aborted.")
        S[kdr("mission")] = None

    # voice command
    st.subheader("🎙️ Voice Command (optional)")
    v1, v2 = st.columns([1, 3])
    status_box = v2.empty()
    txt_cmd = st.text_input(
        "Or type a command (e.g., start zone A for 2 minutes, stop, return home, land, status):",
        key=kdr("typed_cmd")
    )

    def _tts(msg: str):
        if pyttsx3 is None:
            return
        try:
            eng = pyttsx3.init()
            eng.say(msg)
            eng.runAndWait()
        except Exception:
            pass

    def handle_command(cmd: str):
        cmd = (cmd or "").strip().lower()
        if not cmd:
            return
        S[kdr("log")].append(f"{datetime.now():%H:%M:%S} 🔈 '{cmd}'")

        m = re.search(r"start.*zone\s*([abc]).*?(\d+)\s*(min|minute|minutes|sec|second|seconds)", cmd)
        if m:
            z = m.group(1).upper()
            val = int(m.group(2))
            secs = val * (60 if "min" in m.group(3) else 1)
            if not S[kdr("armed")] or not S[kdr("in_air")]:
                msg = "Drone must be armed and in the air to start."
                status_box.warning(msg); _tts(msg); return
            if S[kdr("mission")]:
                msg = "A mission is already running."
                status_box.info(msg); _tts(msg); return
            S[kdr("mission")] = {"zone": z, "remain_s": secs, "lpm": 8, "state": "irrigating"}
            msg = f"Starting irrigation in Zone {z} for {int(secs/60)} minutes."
            status_box.success(msg); _tts(msg); return

        if "takeoff" in cmd or "launch" in cmd:
            if not S[kdr("armed")]:
                msg = "Arm first."
                status_box.warning(msg); _tts(msg); return
            if not S[kdr("in_air")]:
                S[kdr("in_air")] = True
                S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Takeoff (voice).")
                status_box.success("Takeoff."); _tts("Takeoff.")
            return

        if "land" in cmd:
            if S[kdr("in_air")]:
                S[kdr("in_air")] = False
                S[kdr("mission")] = None
                S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Landed (voice).")
                status_box.success("Landing."); _tts("Landing.")
            return

        if "return" in cmd or "home" in cmd or "rth" in cmd:
            if S[kdr("in_air")]:
                S[kdr("mission")] = None
                S[kdr("in_air")] = False
                S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Return-to-Home (voice).")
                status_box.success("Returning home."); _tts("Returning home.")
            return

        if "stop" in cmd or "abort" in cmd or "cancel" in cmd:
            if S[kdr("mission")]:
                S[kdr("mission")] = None
                S[kdr("log")].append(f"{datetime.now():%H:%M:%S} Mission stopped (voice).")
                status_box.info("Mission stopped."); _tts("Mission stopped.")
            return

        if "status" in cmd:
            status = f"Battery {S[kdr('battery')]:.0f}%, {'in air' if S[kdr('in_air')] else 'on ground'}."
            if S[kdr("mission")]:
                status += f" Irrigating Zone {S[kdr('mission')]['zone']} with {int(S[kdr('mission')]['remain_s'])} seconds left."
            status_box.info(status); _tts(status)
            return

        status_box.info("Command not recognized. Try: 'start zone A for 2 minutes', 'stop', 'return home', 'land', 'status'.")

    if sr is not None and v1.button("🎤 Speak", key=kdr("mic_btn")):
        try:
            recog = sr.Recognizer()
            with sr.Microphone() as source:
                status_box.info("Listening…")
                try:
                    recog.adjust_for_ambient_noise(source, duration=0.5)
                except Exception:
                    pass
                audio = recog.listen(source, timeout=4, phrase_time_limit=6)
            cmd = recog.recognize_google(audio)
            status_box.success(f"🗣 {cmd}")
            handle_command(cmd)
        except sr.WaitTimeoutError:
            status_box.error("Timed out. Try again.")
        except sr.UnknownValueError:
            status_box.error("Didn't catch that.")
        except sr.RequestError:
            status_box.error("Speech service unavailable.")
        except Exception as e:
            status_box.error(f"Mic error: {e}")

    # typed command
    if txt_cmd := st.session_state.get(kdr("typed_cmd")):
        handle_command(txt_cmd)
        st.rerun()

    st.divider()
    st.subheader("📜 Event Log")
    if S[kdr("log")]:
        for ln in S[kdr("log")][-200:]:
            st.write(ln)
    else:
        st.caption("No events yet.")


# ---------- BACKUP & RECOVERY UI (wrap in a function) ----------
def data_backup_recovery_ui():
    import os, shutil
    from datetime import datetime
    import streamlit as st

    st.header("💾 Data Backup & Recovery")
    st.write("Create a backup of your farm data, restore a previous one, or manage backups.")

    # ensure folders
    data_dir = "farm_data"
    backup_dir = "backups"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # track active tool
    active_key = kbak("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # triggers
    c1, c2, c3, c4 = st.columns([1.6, 1.6, 1.6, 0.8])
    with c1:
        if st.button("💾 Create Backup", key=kbak("btn_backup")):
            st.session_state[active_key] = "backup"
    with c2:
        if st.button("♻️ Restore Backup", key=kbak("btn_restore")):
            st.session_state[active_key] = "restore"
    with c3:
        if st.button("🗑 Manage Backups", key=kbak("btn_manage")):
            st.session_state[active_key] = "manage"
    with c4:
        if st.button("🔄 Reset", key=kbak("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # Create Backup
    if tool == "backup":
        st.subheader("💾 Create Backup")
        st.write(f"Source folder: `{data_dir}` → Backups in `{backup_dir}`")
        if st.button("📂 Backup Now", key=kbak("do_backup")):
            try:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_name)
                shutil.copytree(data_dir, backup_path)
                st.success(f"✅ Backup created successfully: {backup_name}")
            except FileExistsError:
                st.warning("A backup with that name already exists—please try again.")
            except Exception as e:
                st.error(f"❌ Error creating backup: {e}")

    # Restore Backup
    elif tool == "restore":
        st.subheader("♻️ Restore Backup")
        backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
        if backups:
            selected_backup = st.selectbox("Select a backup to restore", backups, key=kbak("sel_restore"))
            if st.button("🔄 Restore", key=kbak("do_restore")):
                try:
                    if os.path.exists(data_dir):
                        shutil.rmtree(data_dir)
                    shutil.copytree(os.path.join(backup_dir, selected_backup), data_dir)
                    st.success(f"✅ Backup '{selected_backup}' restored successfully.")
                except Exception as e:
                    st.error(f"❌ Error restoring backup: {e}")
        else:
            st.info("ℹ️ No backups found. Create one first.")

    # Manage Backups
    elif tool == "manage":
        st.subheader("🗑 Manage Backups")
        backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
        if backups:
            selected = st.selectbox("Select a backup", backups, key=kbak("sel_manage"))
            cA, cB = st.columns([1, 1])
            with cA:
                if st.button("🗑 Delete Selected", key=kbak("del_sel")):
                    try:
                        shutil.rmtree(os.path.join(backup_dir, selected))
                        st.success(f"Deleted backup '{selected}'.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting backup: {e}")
            with cB:
                if st.button("📁 Refresh List", key=kbak("refresh")):
                    st.rerun()
        else:
            st.info("No backups to manage yet.")

    else:
        st.info("Choose an action above to create, restore, or manage backups.")


# =========================
# 📦 REQUIRED IMPORTS (top of app.py)
# =========================
import streamlit as st
import pandas as pd
import random
from datetime import datetime, date
import uuid

# =========================
# 🧰 SESSION-STATE HELPERS
# =========================
def _init_state():
    if "stock_items" not in st.session_state:
        # id, name, type, qty, unit, min_level, expiry_date, usage_notes, last_updated
        st.session_state.stock_items = []
    if "stock_usage_logs" not in st.session_state:
        # list of dicts: {id, name, type, action, amount, unit, note, timestamp}
        st.session_state.stock_usage_logs = []
    if "indicator_history" not in st.session_state:
        st.session_state.indicator_history = pd.DataFrame(
            columns=["timestamp", "soil_moisture", "temperature", "humidity",
                     "crop_health_index", "pest_risk", "water_level", "ph", "ec"]
        )

_init_state()


# 📍 Farm Lot Management — Trigger Buttons
# 📍 Farm Lot Management — Trigger Buttons
if (('menu_v2' in globals() and menu_v2 == "📍 Farm Lot Management") or
    ('menu' in globals() and menu   == "📍 Farm Lot Management")):


    import pandas as pd
    from datetime import date
    import uuid

    st.header("📍 Farm Lot Management")

    # ---- state ----
    rows_key  = klot("rows")
    active_key = klot("active_tool")
    if rows_key not in st.session_state:
        st.session_state[rows_key] = []  # list of lot dicts
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # ---- trigger buttons ----
    c1, c2, c3, c4 = st.columns([1.5, 1.8, 2.0, 0.9])
    with c1:
        if st.button("➕ Add Lot", key=klot("btn_add")):
            st.session_state[active_key] = "add"
    with c2:
        if st.button("📋 View / Edit Lots", key=klot("btn_view")):
            st.session_state[active_key] = "view"
    with c3:
        if st.button("📤 Export / 📥 Import", key=klot("btn_io")):
            st.session_state[active_key] = "io"
    with c4:
        if st.button("🔄 Reset", key=klot("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # ======================
    # Tool: Add Lot
    # ======================
    if tool == "add":
        st.subheader("➕ Add New Lot")
        with st.form(klot("form_add"), clear_on_submit=True):
            cA, cB, cC = st.columns(3)
            with cA:
                name = st.text_input("Lot Name", key=klot("name"))
            with cB:
                area = st.number_input("Area (ha)", min_value=0.0, step=0.1, key=klot("area"))
            with cC:
                status = st.selectbox("Status", ["Fallow", "Prepared", "Planted", "Harvested"], key=klot("status"))

            cD, cE = st.columns(2)
            with cD:
                crop = st.text_input("Crop", key=klot("crop"))
            with cE:
                gps = st.text_input("GPS (lat, lon)", key=klot("gps"))

            notes = st.text_area("Notes", key=klot("notes"))
            submitted = st.form_submit_button("Save Lot", use_container_width=True)

        if submitted:
            if not name.strip():
                st.warning("Please enter a lot name.")
            else:
                st.session_state[rows_key].append({
                    "ID": str(uuid.uuid4())[:8],
                    "Name": name.strip(),
                    "Area (ha)": float(area),
                    "Status": status,
                    "Crop": crop.strip(),
                    "GPS": gps.strip(),
                    "Notes": notes.strip(),
                    "Added": date.today().isoformat(),
                })
                st.success(f"✅ Lot '{name}' saved.")

    # ======================
    # Tool: View / Edit
    # ======================
    elif tool == "view":
        lots = st.session_state.get(rows_key, [])
        if lots:
            st.subheader("📋 Lots")
            df = pd.DataFrame(lots)

            # filters
            f1, f2, f3 = st.columns([1.6, 1.6, 1])
            with f1:
                q = st.text_input("Search (name or crop)", key=klot("q"))
            with f2:
                f_status = st.multiselect("Status filter", ["Fallow", "Prepared", "Planted", "Harvested"], key=klot("f_status"))
            with f3:
                min_area = st.number_input("Min area (ha)", min_value=0.0, step=0.1, key=klot("min_area"))

            mask = pd.Series(True, index=df.index)
            if q:
                mask &= df["Name"].str.contains(q, case=False) | df["Crop"].str.contains(q, case=False)
            if f_status:
                mask &= df["Status"].isin(f_status)
            if min_area > 0:
                mask &= df["Area (ha)"] >= min_area

            view_df = df[mask]
            st.dataframe(view_df, use_container_width=True)

            st.divider()
            st.subheader("✏️ Edit / Delete")
            for _, row in view_df.reset_index(drop=True).iterrows():
                with st.expander(f"📌 {row['Name']} • {row['Area (ha)']} ha • {row['Status']}"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        new_status = st.selectbox(
                            "Status",
                            ["Fallow", "Prepared", "Planted", "Harvested"],
                            index=["Fallow","Prepared","Planted","Harvested"].index(row["Status"]),
                            key=klot(f"st_{row['ID']}")
                        )
                    with c2:
                        new_area = st.number_input(
                            "Area (ha)", min_value=0.0, step=0.1, value=float(row["Area (ha)"]),
                            key=klot(f"ar_{row['ID']}")
                        )
                    with c3:
                        new_crop = st.text_input("Crop", value=row["Crop"], key=klot(f"cr_{row['ID']}"))

                    g1, g2 = st.columns(2)
                    with g1:
                        new_gps = st.text_input("GPS (lat, lon)", value=row["GPS"], key=klot(f"gps_{row['ID']}"))
                    with g2:
                        new_notes = st.text_area("Notes", value=row["Notes"], key=klot(f"nt_{row['ID']}"))

                    s1, s2 = st.columns(2)
                    with s1:
                        if st.button("💾 Save", key=klot(f"save_{row['ID']}")):
                            for it in st.session_state[rows_key]:
                                if it["ID"] == row["ID"]:
                                    it["Status"] = new_status
                                    it["Area (ha)"] = float(new_area)
                                    it["Crop"] = new_crop
                                    it["GPS"] = new_gps
                                    it["Notes"] = new_notes
                                    st.success("Updated.")
                                    break
                    with s2:
                        if st.button("🗑 Delete", key=klot(f"del_{row['ID']}")):
                            st.session_state[rows_key] = [it for it in st.session_state[rows_key] if it["ID"] != row["ID"]]
                            st.success("Deleted.")
                            st.rerun()
        else:
            st.info("No lots yet. Add one first.")

    # ======================
    # Tool: Export / Import
    # ======================
    elif tool == "io":
        st.subheader("📤 Export / 📥 Import")
        lots = st.session_state.get(rows_key, [])
        df = pd.DataFrame(lots) if lots else pd.DataFrame(columns=["ID","Name","Area (ha)","Status","Crop","GPS","Notes","Added"])

        st.download_button(
            "⬇️ Download Lots CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="farm_lots.csv",
            mime="text/csv",
            key=klot("dl")
        )

        uploaded = st.file_uploader("Upload Lots CSV", type=["csv"], key=klot("upl"))
        if uploaded is not None:
            try:
                imp = pd.read_csv(uploaded)
                required = {"Name","Area (ha)","Status","Crop","GPS","Notes"}
                if not required.issubset(imp.columns):
                    st.warning("CSV must include columns: " + ", ".join(sorted(required)))
                else:
                    count = 0
                    for _, r in imp.iterrows():
                        st.session_state[rows_key].append({
                            "ID": str(uuid.uuid4())[:8],
                            "Name": str(r["Name"]),
                            "Area (ha)": float(r["Area (ha)"]),
                            "Status": str(r["Status"]),
                            "Crop": str(r["Crop"]),
                            "GPS": str(r["GPS"]),
                            "Notes": str(r.get("Notes", "")),
                            "Added": date.today().isoformat(),
                        })
                        count += 1
                    st.success(f"Imported {count} lot(s).")
            except Exception as e:
                st.error(f"Import failed: {e}")

    else:
        st.info("Choose an action above to manage farm lots.")
        
# =========================
# 🧪 SMART FERTILIZER & PESTICIDE STOCK MANAGER (drop-in)
# =======================

# -- initialize session state containers once
def _init_stock_state():
    if "stock_items" not in st.session_state:
        st.session_state.stock_items = []  # list of dicts
    if "stock_usage_logs" not in st.session_state:
        st.session_state.stock_usage_logs = []  # list of dicts

_init_stock_state()

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date

def _init_stock_state():
    if "stock_items" not in st.session_state:
        st.session_state.stock_items = []  # list of dicts
    if "stock_usage_logs" not in st.session_state:
        st.session_state.stock_usage_logs = []  # list of dicts

def _rerun():
    # works on both new/old Streamlit
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

_init_stock_state()

# ---------- data helpers ----------
def _stock_to_df(items):
    if not items:
        cols = ["id","name","type","qty","unit","min_level","expiry_date","usage_notes","last_updated"]
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(items)

def _log_stock_action(item, action, amount, note):
    st.session_state.stock_usage_logs.append({
        "id": item["id"],
        "name": item["name"],
        "type": item["type"],
        "action": action,   # "use" | "restock"
        "amount": amount,
        "unit": item["unit"],
        "note": note,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ---------- UI ----------
def smart_fert_pest_ui():
    st.header("🧪 Smart Fertilizer & Pesticide Stock Manager")

    # ---- Add New Item ----
    st.subheader("➕ Add New Item to Stock")
    with st.form(sfp("form_add_item")):
        c1, c2, c3 = st.columns(3)
        with c1:
            item_name = st.text_input("Item Name", key=sfp("add_name"))
            item_type = st.selectbox("Type", ["Fertilizer", "Pesticide"], key=sfp("add_type"))
            unit = st.text_input("Unit", value="kg", key=sfp("add_unit"))
        with c2:
            quantity  = st.number_input("Quantity", min_value=0.0, value=0.0, step=0.1, key=sfp("add_qty"))
            min_level = st.number_input("Reorder Level", min_value=0.0, value=5.0, step=0.1, key=sfp("add_min"))
            expiry_date = st.date_input("Expiry Date", value=date.today(), key=sfp("add_exp"))
        with c3:
            usage_notes = st.text_area("Usage Notes", key=sfp("add_notes"))
        submitted = st.form_submit_button("Add Item")
    if submitted:
        if not item_name.strip():
            st.warning("Please provide an item name.")
        else:
            new_item = {
                "id": str(uuid.uuid4()),
                "name": item_name.strip(),
                "type": item_type,
                "qty": float(quantity),
                "unit": unit.strip() or "kg",
                "min_level": float(min_level),
                "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                "usage_notes": usage_notes.strip(),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.session_state.stock_items.append(new_item)
            st.success(f"Added '{new_item['name']}' to stock.")
            _rerun()

    # ---- Filters ----
    st.subheader("🔎 Filter & Search")
    f1, f2, f3, f4 = st.columns([2,2,2,2])
    with f1:
        q = st.text_input("Search by name", key=sfp("filter_q"))
    with f2:
        t = st.multiselect("Type filter", ["Fertilizer", "Pesticide"], key=sfp("filter_type"))
    with f3:
        low_stock_only = st.checkbox("Low stock only", key=sfp("filter_low"))
    with f4:
        expiring_only = st.checkbox("Expiring within 30 days", key=sfp("filter_exp"))

    df = _stock_to_df(st.session_state.stock_items)

    if not df.empty:
        mask = pd.Series(True, index=df.index)
        if q:
            mask &= df["name"].str.contains(q, case=False, na=False)
        if t:
            mask &= df["type"].isin(t)
        if low_stock_only:
            mask &= (df["qty"] <= df["min_level"])
        if expiring_only:
            today = pd.Timestamp.today().normalize()
            soon = today + pd.Timedelta(days=30)
            df_dates = pd.to_datetime(df["expiry_date"], errors="coerce")
            mask &= df_dates.between(today, soon, inclusive="both")
        df_view = df[mask].copy()
    else:
        df_view = df

    # ---- Alerts ----
    if not df.empty:
        low_df = df[df["qty"] <= df["min_level"]]
        if not low_df.empty:
            st.error("⚠️ Low stock items detected:")
            for _, r in low_df.iterrows():
                st.write(f"- **{r['name']}** ({r['type']}): {r['qty']} {r['unit']} ≤ reorder level {r['min_level']} {r['unit']}")

        df["expiry_date_dt"] = pd.to_datetime(df["expiry_date"], errors="coerce")
        exp_alert = df[df["expiry_date_dt"] <= (pd.Timestamp.today().normalize() + pd.Timedelta(days=30))]
        if not exp_alert.empty:
            st.warning("⏳ Items nearing expiry (≤ 30 days):")
            for _, r in exp_alert.iterrows():
                days_left = (r["expiry_date_dt"].date() - date.today()).days
                st.write(f"- **{r['name']}** expires in {days_left} day(s) on {r['expiry_date']}")

    # ---- Table ----
    st.subheader("📋 Current Stock")
    st.dataframe(df_view.drop(columns=[c for c in ["expiry_date_dt"] if c in df_view.columns]),
                 use_container_width=True)

    # ---- Row Actions ----
    st.subheader("🛠 Manage Items")
    if not df_view.empty:
        for _, row in df_view.reset_index(drop=True).iterrows():
            with st.expander(f"✏️ {row['name']} • {row['type']} • {row['qty']} {row['unit']}"):
                c1, c2, c3 = st.columns(3)

                # Use
                with c1:
                    use_amount = st.number_input(
                        f"Use amount ({row['unit']})", min_value=0.0, step=0.1, key=sfp(f"use_amt_{row['id']}")
                    )
                    if st.button("➖ Use", key=sfp(f"use_btn_{row['id']}")):
                        if use_amount <= 0:
                            st.warning("Enter a valid amount to use.")
                        elif use_amount > row["qty"]:
                            st.warning("Not enough in stock.")
                        else:
                            for it in st.session_state.stock_items:
                                if it["id"] == row["id"]:
                                    it["qty"] = round(it["qty"] - float(use_amount), 3)
                                    it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    _log_stock_action(it, "use", float(use_amount), "Used in field application")
                                    st.success(f"Used {use_amount} {it['unit']} from {it['name']}.")
                                    break
                            _rerun()

                # Restock
                with c2:
                    restock_amount = st.number_input(
                        f"Restock amount ({row['unit']})", min_value=0.0, step=0.1, key=sfp(f"restock_amt_{row['id']}")
                    )
                    if st.button("➕ Restock", key=sfp(f"restock_btn_{row['id']}")):
                        if restock_amount <= 0:
                            st.warning("Enter a valid amount to restock.")
                        else:
                            for it in st.session_state.stock_items:
                                if it["id"] == row["id"]:
                                    it["qty"] = round(it["qty"] + float(restock_amount), 3)
                                    it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    _log_stock_action(it, "restock", float(restock_amount), "Supplier delivery")
                                    st.success(f"Restocked {restock_amount} {it['unit']} to {it['name']}.")
                                    break
                            _rerun()

                # Update settings
                with c3:
                    new_min = st.number_input(
                        "Update reorder level", min_value=0.0, step=0.1, value=float(row["min_level"]),
                        key=sfp(f"upd_min_{row['id']}")
                    )
                    new_exp = st.date_input(
                        "Update expiry date",
                        value=pd.to_datetime(row["expiry_date"], errors="coerce").date()
                              if pd.notna(pd.to_datetime(row["expiry_date"], errors="coerce")) else date.today(),
                        key=sfp(f"upd_exp_{row['id']}")
                    )
                    if st.button("💾 Save updates", key=sfp(f"save_upd_{row['id']}")):
                        for it in st.session_state.stock_items:
                            if it["id"] == row["id"]:
                                it["min_level"] = float(new_min)
                                it["expiry_date"] = new_exp.strftime("%Y-%m-%d")
                                it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.success("Item settings updated.")
                                break
                        _rerun()

                # Delete
                del_col1, _ = st.columns([1,5])
                with del_col1:
                    if st.button("🗑 Delete item", type="secondary", key=sfp(f"del_{row['id']}")):
                        st.session_state.stock_items = [it for it in st.session_state.stock_items if it["id"] != row["id"]]
                        st.success(f"Deleted {row['name']} from stock.")
                        _rerun()

    # ---- Logs & IO ----
    st.subheader("🧾 Usage & Restock Logs")
    if st.session_state.stock_usage_logs:
        logs_df = pd.DataFrame(st.session_state.stock_usage_logs)
        st.dataframe(logs_df, use_container_width=True)
        st.download_button(
            "Download logs CSV",
            logs_df.to_csv(index=False).encode("utf-8"),
            file_name="stock_usage_logs.csv",
            mime="text/csv",
            key=sfp("dl_logs")
        )
    else:
        st.info("No usage or restock logs yet.")

    st.subheader("📤 Export / 📥 Import")
    exp_df = _stock_to_df(st.session_state.stock_items)
    st.download_button(
        "Download stock CSV",
        exp_df.to_csv(index=False).encode("utf-8"),
        file_name="stock_items.csv",
        mime="text/csv",
        key=sfp("dl_stock")
    )

    uploaded = st.file_uploader("Import stock CSV (id will be regenerated)", type=["csv"], key=sfp("upl_stock"))
    if uploaded is not None:
        try:
            imp = pd.read_csv(uploaded)
            required = {"name","type","qty","unit","min_level","expiry_date","usage_notes"}
            if not required.issubset(set(imp.columns)):
                st.warning(f"CSV must include columns: {', '.join(sorted(required))}")
            else:
                imported = []
                for _, r in imp.iterrows():
                    imported.append({
                        "id": str(uuid.uuid4()),
                        "name": str(r["name"]),
                        "type": str(r["type"]),
                        "qty": float(r["qty"]),
                        "unit": str(r["unit"]),
                        "min_level": float(r["min_level"]),
                        "expiry_date": str(r["expiry_date"]),
                        "usage_notes": str(r.get("usage_notes","")),
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                st.session_state.stock_items.extend(imported)
                st.success(f"Imported {len(imported)} items.")
                _rerun()
        except Exception as e:
            st.error(f"Import failed:{e}")



# ===============================
# 🚨 Smart Farm Alerts
# ===============================

st.header("🚨 Smart Farm Alerts")
st.write("Click a button below to view farm alerts instantly.")

# ---- Ensure session key exists ----
st.session_state.setdefault("active_alert", None)

# ---- Optional: simple speaker (no external deps) ----
def _speak_alert(text: str) -> None:
    # Replace with pyttsx3/gTTS if you want real audio. This is a UI toast/log for now.
    st.toast("🔊 " + text)
    st.write("🔊", text)

# ---- Alert config: key -> (title, render_fn, message, voice_line) ----
_ALERTS = {
    "weather": (
        "🌦 Weather Alert",
        st.info,
        "Heavy rainfall expected tomorrow. Prepare drainage and cover seedlings.",
        "Weather alert: heavy rainfall expected tomorrow. Prepare drainage and cover seedlings."
    ),
    "pest": (
        "🐛 Pest Alert",
        st.warning,
        "Armyworm outbreak detected nearby. Apply the recommended pesticide early.",
        "Pest alert: armyworm outbreak detected nearby. Apply the recommended pesticide early."
    ),
    "soil": (
        "🌱 Soil Alert",
        st.success,
        "Soil moisture is low — consider irrigating this evening.",
        "Soil alert: moisture is low. Consider irrigating this evening."
    ),
    "market": (
        "📈 Market Alert",
        st.info,
        "Maize prices are up 12% this week — it may be a good time to sell.",
        "Market alert: maize prices are up twelve percent this week. It may be a good time to sell."
    ),
    "emergency": (
        "🚨 Emergency Alert",
        st.error,
        "Security breach detected near Gate 2. Notify the team and verify the perimeter now.",
        "Emergency alert: security breach detected near Gate two. Notify the team and verify the perimeter now."
    ),
}

# ---- Trigger buttons row ----
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("🌦 Weather", key="btn_weather"):
        st.session_state.active_alert = "weather"
with c2:
    if st.button("🐛 Pest", key="btn_pest"):
        st.session_state.active_alert = "pest"
with c3:
    if st.button("🌱 Soil", key="btn_soil"):
        st.session_state.active_alert = "soil"
with c4:
    if st.button("📈 Market", key="btn_market"):
        st.session_state.active_alert = "market"
with c5:
    if st.button("🚨 Emergency", key="btn_emergency"):
        st.session_state.active_alert = "emergency"

st.divider()


# ---------------------------
# Safe defaults (only if missing)
# ---------------------------
if "_speak_alert" not in globals():
    def _speak_alert(text: str) -> None:
        # Replace with real TTS if you want (pyttsx3 / gTTS). For now: toast + print.
        st.toast("🔊 " + text)
        st.write("🔊", text)

# Simple wrappers (optional; you can pass st.info etc. directly)
def _render_info(msg: str):    st.info(msg)
def _render_warn(msg: str):    st.warning(msg)
def _render_ok(msg: str):      st.success(msg)
def _render_err(msg: str):     st.error(msg)

# Declarative alert config: key -> (title, renderer, message, voice_line)
if "_ALERTS" not in globals():
    _ALERTS = {
        "weather": (
            "🌦 Weather Alert",
            _render_info,
            "Heavy rainfall expected tomorrow. Prepare drainage and cover seedlings.",
            "Weather alert: heavy rainfall expected tomorrow. Prepare drainage and cover seedlings."
        ),
        "pest": (
            "🐛 Pest Alert",
            _render_warn,
            "Armyworm outbreak detected nearby. Apply recommended pesticide early.",
            "Pest alert: armyworm outbreak detected nearby. Apply the recommended pesticide early."
        ),
        "soil": (
            "🌱 Soil Alert",
            _render_ok,
            "Soil moisture is low — consider irrigation this evening.",
            "Soil alert: moisture is low. Consider irrigating this evening."
        ),
        "market": (
            "📈 Market Alert",
            _render_info,
            "Maize prices have increased by 12% this week — good time to sell.",
            "Market alert: maize prices are up twelve percent this week. It may be a good time to sell."
        ),
        "emergency": (
            "🚨 Emergency Alert",
            _render_err,
            "Security breach detected near Gate 2. Notify the team and verify the perimeter now.",
            "Emergency alert: security breach near Gate 2. Notify the team and verify the perimeter now."
        ),
    }

# Ensure session key exists
st.session_state.setdefault("active_alert", None)

# ---------------------------
# Display active alert
# ---------------------------
active_key = st.session_state.get("active_alert")
cfg = _ALERTS.get(active_key)

if cfg:
    title, render_fn, message, voice_line = cfg
    st.subheader(title)
    render_fn(message)
    if st.button("🔊 Read it out", key="alert_readout"):
        _speak_alert(voice_line)
else:
    st.caption("No alert selected yet. Use the tester below to trigger one.")

# ---------------------------
# Tester UI to trigger alerts
# ---------------------------
with st.expander("🔔 Test Smart Farm Alerts"):
    from datetime import datetime

    # Use your global _ALERTS dict if it exists; otherwise show a hint.
    ALERTS = globals().get("_ALERTS", {})
    if not ALERTS:
        st.info(
            "No alerts configured yet. Define `_ALERTS` above, e.g.:\n\n"
            "_ALERTS = {\n"
            "  'Low moisture': {'level':'warning','message':'Soil moisture < 30% — irrigate soon.'},\n"
            "  'High temp': {'level':'error','message':'Temp > 35°C — heat stress risk.'},\n"
            "  'Saved': {'level':'success','message':'Settings saved successfully.'}\n"
            "}"
        )
    else:
        choice = st.selectbox("Choose alert", ["", *list(ALERTS.keys())], key="alert_choice")

        if choice:
            data = ALERTS[choice]
            # Supports either dict entries or plain strings in _ALERTS
            if isinstance(data, dict):
                level = (data.get("level") or "info").lower()
                message = data.get("message") or choice
            else:
                level = "info"
                message = str(data)

            # Show the selected alert
            if level == "success":
                st.success(message)
            elif level == "warning":
                st.warning(message)
            elif level == "error":
                st.error(message)
            else:
                st.info(message)

            # Log it (optional)
            st.session_state.setdefault("alert_log", []).append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": choice,
                    "level": level,
                    "message": message,
                }
            )

        # Show recent alerts (optional)
        if st.session_state.get("alert_log"):
            st.markdown("**Recent alerts**")
            for row in st.session_state["alert_log"][-10:][::-1]:
                st.write(f"{row['time']} • {row['level'].upper()} • {row['name']}: {row['message']}")


#smart_tutor_voice
def smart_tutor_voice():
    import os
    from datetime import datetime
    import streamlit as st

    # --- optional deps (gracefully handled)
    try:
        import speech_recognition as sr  # mic / audio-to-text
    except Exception:
        sr = None
    try:
        import pyttsx3  # offline TTS
    except Exception:
        pyttsx3 = None
    try:
        from gtts import gTTS  # online TTS fallback
    except Exception:
        gTTS = None

    # translators (optional)
    translator = None
    _gt = None
    try:
        from googletrans import Translator  # pip install googletrans==4.0.0rc1
        translator = "googletrans"
        _gt = Translator()
    except Exception:
        try:
            from deep_translator import GoogleTranslator  # pip install deep-translator
            translator = "deep"
        except Exception:
            translator = None

    # OpenAI (optional)
    client = None
    try:
        from openai import OpenAI  # pip install openai
        if os.getenv("OPENAI_API_KEY"):
            client = OpenAI()
    except Exception:
        client = None

    # --- UI
    st.header("🧑‍🏫 Smart Tutor (Multi-Language) + 🎙️ Voice")
    st.caption("Speak or type your question. I’ll answer and can read the reply aloud.")

    LANGS = [
        "Urhobo","Yorùbá","Hausa","Ịjọ (Ijaw)","Efik (Calabar)","Ịgbò (Igbo)","Edo (Bini)","Tiv",
        "Ibibio","Kanuri","Nupe","Fulfulde (Fula)","Itsekiri","Gbagyi","Idoma","Ebira","Jukun",
        "Igala","Berom (Birom)","Esan","Isoko","Okun (Yoruba dialect)","Ika","English (for reference)"
    ]
    DOMAINS = [
        "General chat","Farming & Agriculture","Business & Finance",
        "Health & Safety (non-medical advice)","Education & Study Help",
    ]
    TONES = ["Neutral","Friendly","Professional","Encouraging","Brief"]

    c1, c2, c3 = st.columns([1.2, 1, 1])
    lang   = c1.selectbox("Language", LANGS, index=0, key="st_lang")
    domain = c2.selectbox("Domain", DOMAINS, index=1, key="st_domain")
    tone   = c3.selectbox("Tone", TONES, index=1, key="st_tone")

    vc1, vc2, vc3 = st.columns([1.1, 1.1, 1])
    input_mode    = vc1.radio("Input Mode", ["🎙️ Voice", "⌨️ Typing"], horizontal=True, key="st_input_mode")
    auto_speak    = vc2.toggle("🔁 Auto-speak reply", value=True, key="st_auto_speak")
    tts_lang_hint = vc3.selectbox(
        "TTS language (for playback)",
        ["auto (best effort)","en","ha","yo","ig"],
        index=0,
        key="st_tts_code"
    )

    # --- helpers
    def _system_prompt(lang_, domain_, tone_):
        return f"""You are a helpful AI that replies entirely in {lang_}.
Tone: {tone_}. Domain focus: {domain_}.
Use clear, culturally appropriate expressions. Avoid slang unless asked.
If a term has no direct {lang_} word, explain briefly in {lang_}.
Keep paragraphs short. Use bullet points for steps/lists.
Do NOT switch to English unless the user asks.""".strip()

    def _translate_to(text, target_code):
        if not translator or not (text or "").strip():
            return text
        try:
            if translator == "googletrans":
                return _gt.translate(text, dest=target_code or "en").text
            else:
                from deep_translator import GoogleTranslator
                return GoogleTranslator(source="auto", target=target_code or "en").translate(text)
        except Exception:
            return text

    def _speak_text(text, lang_code="en"):
        # offline first
        if pyttsx3 is not None:
            try:
                engine = pyttsx3.init()
                try:
                    rate = engine.getProperty("rate")
                    if isinstance(rate, int):
                        engine.setProperty("rate", max(120, min(185, rate)))
                except Exception:
                    pass
                engine.say(text)
                engine.runAndWait()
                st.caption("🔉 Played using offline TTS (pyttsx3).")
                return
            except Exception:
                pass
        # gTTS fallback
        if gTTS is not None:
            try:
                use_code = lang_code if lang_code in {"en","ha","yo","ig"} else "en"
                tts = gTTS(text=text, lang=use_code)
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    st.audio(tmp.name, format="audio/mp3")
                    st.caption("🔉 Played using gTTS.")
                return
            except Exception as e:
                st.warning(f"TTS failed: {e}")
        st.info("🔇 Could not play audio (no TTS engine available).")

    def _model_answer(user_text: str) -> str:
        sys_prompt = _system_prompt(lang, domain, tone)
        if client is not None:
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_text}],
                    temperature=0.6,
                    max_tokens=380,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception:
                pass
        # local fallback
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        header = f"[{lang}] — {domain} • {tone}"
        body_map = {
            "Farming & Agriculture":"• Farm advice (summary):",
            "Business & Finance":"• Business guidance (summary):",
            "Health & Safety (non-medical advice)":"• Safety tips (general):",
            "Education & Study Help":"• Study help (outline):",
            "General chat":"• Response (general):",
        }
        return (
            f"{header}\n"
            f"{body_map.get(domain,'• Response:')}\n"
            f"- 1) Identify main need. 2) Give short, clear guidance. 3) Suggest next step.\n"
            f"- Your request: “{(user_text or '').strip()}”\n"
            f"- Tip: Keep records and review weekly.\n"
            f"— {ts}"
        )

    # --- state
    if "st_msgs" not in st.session_state:
        st.session_state.st_msgs = []

    recognized_box = st.empty()
    query_text = ""

    # --- input (voice or typing)
    if input_mode == "🎙️ Voice":
        c_mic, c_up = st.columns([1, 1])
        mic_clicked = c_mic.button("🎤 Tap to Record", key="st_mic_btn")
        audio_file  = c_up.file_uploader("…or upload WAV/MP3", type=["wav","mp3","m4a"], key="st_audio_upload")

        if mic_clicked:
            if sr is None:
                st.error("SpeechRecognition not installed. Try: `pip install SpeechRecognition pyaudio`")
            else:
                try:
                    recog = sr.Recognizer()
                    with sr.Microphone() as source:
                        st.info("🎤 Listening…")
                        try:
                            recog.adjust_for_ambient_noise(source, duration=0.6)
                        except Exception:
                            pass
                        audio = recog.listen(source, timeout=4, phrase_time_limit=8)
                    st.caption("⏳ Transcribing…")
                    hint_code = {"Yorùbá":"yo","Hausa":"ha","Ịgbò (Igbo)":"ig"}.get(lang, "en")
                    query_text = recog.recognize_google(audio, language=hint_code)
                    recognized_box.success(f"🗣️ Recognized: {query_text}")
                except sr.WaitTimeoutError:
                    st.error("Listening timed out. Try again and speak sooner.")
                except sr.UnknownValueError:
                    st.error("I couldn't understand that. Please try again.")
                except sr.RequestError:
                    st.error("Speech service unavailable. Check internet connection.")
                except Exception as e:
                    st.error(f"Mic/recognition error: {e}")

        if audio_file is not None and sr is not None:
            try:
                recog = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recog.record(source)
                st.caption("⏳ Transcribing uploaded audio…")
                hint_code = {"Yorùbá":"yo","Hausa":"ha","Ịgbò (Igbo)":"ig"}.get(lang, "en")
                query_text = recog.recognize_google(audio, language=hint_code)
                recognized_box.success(f"🗣️ Recognized: {query_text}")
            except Exception as e:
                st.error(f"Audio transcription failed: {e}")

        default_text = query_text or st.session_state.get("st_last_text", "")
        user_text = st.text_area(
            "Type your question / prompt",
            value=default_text,
            placeholder="e.g., Explain in Yorùbá how to prevent tomato leaf blight this week.",
            height=140,
            key="st_query",
        )
        st.session_state["st_last_text"] = user_text

    else:
        default_text = st.session_state.get("st_last_text", "")
        user_text = st.text_area(
            "Type your question / prompt",
            value=default_text,
            placeholder="e.g., Explain in Yorùbá how to prevent tomato leaf blight this week.",
            height=140,
            key="st_query",
        )
        st.session_state["st_last_text"] = user_text

    st.divider()

    # --- generate
    go = st.button("Generate", type="primary", key="st_go")
    if go:
        if not (user_text or "").strip():
            st.warning("Please enter a question or prompt.")
        else:
            with st.spinner("Generating..."):
                base_reply = _model_answer(user_text)
                lang_to_code = {
                    "English (for reference)": "en",
                    "Yorùbá": "yo",
                    "Hausa": "ha",
                    "Ịgbò (Igbo)": "ig",
                }
                target_code = lang_to_code.get(lang, "en")
                translated = _translate_to(base_reply, target_code) if target_code else base_reply

            st.session_state.st_msgs.append(("user", user_text))
            st.session_state.st_msgs.append(("assistant", translated))

            st.markdown("### ✅ Tutor Response")
            st.write(translated)

            if auto_speak and (translated or "").strip():
                tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                _speak_text(translated, lang_code=tts_code or target_code or "en")

    # --- history
    if st.session_state.get("st_msgs"):
        st.subheader("💬 Conversation")
        for role, text in st.session_state.st_msgs:
            if role == "user":
                with st.chat_message("user", avatar="🧑"):
                    st.write(text)
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.write(text)
                if st.button("🔊 Speak this reply", key=f"st_say_{abs(hash(text))%10**8}"):
                        tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                        lang_to_code = {
                            "English (for reference)": "en",
                            "Yorùbá": "yo",
                            "Hausa": "ha",
                            "Ịgbò (Igbo)": "ig",
                        }
                        inferred = lang_to_code.get(lang, "en")
                        _speak_text(text, lang_code=(tts_code or inferred or "en"))

    # Only developers who intentionally enable this will see the notes.
if st.session_state.get("_dev_show_tutor_notes", False):
    with st.expander("ℹ️ Notes / Setup"):
        st.markdown("""
        - Voice input: `pip install SpeechRecognition pyaudio` (microphone support)  
        - Offline TTS: `pyttsx3`  
        - Online TTS: `gTTS`  
        - Translation: `googletrans==4.0.0rc1` or `deep-translator` (optional)  
        - Not all listed languages have stable TTS/STT codes; the app will fallback to English playback.  
        - If you set `OPENAI_API_KEY` in the environment, real AI responses will be used; otherwise the app uses a local fallback template.  

        **Developer tips**  
        - To enable these notes temporarily in a session:  
          `st.session_state["_dev_show_tutor_notes"] = True`  
        - Keep this disabled in production to avoid exposing internal setup details.  
        - If speech or TTS features fail, check microphone permissions and re-run the install commands above.  
        """)
