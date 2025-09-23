
import streamlit as st
from datetime import datetime, date
from io import BytesIO
from PIL import Image
import json
from pathlib import Path
import hashlib

# ---------- Config ----------
USERS_FILE = Path("users.json")
MIN_REQUIRED = 10000.00

st.set_page_config(
    page_title="Landbank — International ATM Card Request",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Styles ----------
st.markdown(
    """
    <style>
    .big-title { font-size:28px; font-weight:700; }
    .muted { color: #6c757d; }
    .card { padding: 18px; border-radius: 12px; background: #ffffff; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
    .warning { background: #fff3cd; padding: 10px; border-radius: 8px; border: 1px solid #ffe8a1; }
    .demo-badge { background:#c62828; color:white; padding:6px 10px; border-radius:8px; font-weight:700; }
    .success-box { background: #e9f7ef; padding:10px; border-radius:8px; border:1px solid #c6efd6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helper functions ----------
def init_state():
    if "balance" not in st.session_state:
        st.session_state.balance = 0.0
    if "submitted_requests" not in st.session_state:
        st.session_state.submitted_requests = []
    if "logged_in_user" not in st.session_state:
        st.session_state.logged_in_user = None
    if "users" not in st.session_state:
        st.session_state.users = load_users()

def hash_password(password: str) -> str:
    """Return a hex SHA256 hash of the given password (simple demo hashing)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def load_users():
    if USERS_FILE.exists():
        try:
            with USERS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            return {}
    return {}

def save_users():
    try:
        with USERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(st.session_state.users, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save users.json: {e}")

def file_preview(file) -> BytesIO:
    """Return a small preview thumbnail (BytesIO) for image files; else None."""
    try:
        img = Image.open(file)
        img.thumbnail((300, 300))
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf
    except Exception:
        return None

def format_currency(x):
    return f"${x:,.2f}"

# ---------- Initialize ----------
init_state()

# ---------- Header ----------
colA, colB = st.columns([8, 2])
with colA:
    st.markdown('<div class="big-title">Landbank — International ATM Card Request</div>', unsafe_allow_html=True)
    st.markdown('<div class="muted">Apply for your International ATM Saving Card.</div>', unsafe_allow_html=True)
with colB:
    st.markdown('<div class="demo-badge">DEMO</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- Honest Notice ----------
st.info(
    "This app can simulate the full application flow. It is not connected to Landbank or any banking backend unless you integrate a real API.\n\n"
    "Estimated delivery shown below is simulated (example: within 2 business days) unless you connect real logistics/fulfillment APIs.",
    icon="⚠️"
)

# ---------- Authentication UI (Register / Login) ----------
st.sidebar.header("Account")

if st.session_state.logged_in_user:
    st.sidebar.write(f"Signed in as: **{st.session_state.logged_in_user.get('name','') or st.session_state.logged_in_user['email']}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.success("Logged out.")
else:
    auth_mode = st.sidebar.radio("Choose action", ["Login", "Register"])
    if auth_mode == "Register":
        st.sidebar.subheader("Register")
        reg_name = st.sidebar.text_input("Full name", key="reg_name")
        reg_email = st.sidebar.text_input("Email", key="reg_email")
        reg_password = st.sidebar.text_input("Password", type="password", key="reg_password")
        reg_password2 = st.sidebar.text_input("Confirm password", type="password", key="reg_password2")
        if st.sidebar.button("Create account"):
            if not reg_email or not reg_password:
                st.sidebar.error("Email and password are required.")
            elif reg_password != reg_password2:
                st.sidebar.error("Passwords do not match.")
            elif reg_email in st.session_state.users:
                st.sidebar.error("An account with that email already exists.")
            else:
                st.session_state.users[reg_email] = {
                    "name": reg_name,
                    "email": reg_email,
                    "password_hash": hash_password(reg_password),
                    "created_at": datetime.utcnow().isoformat()
                }
                save_users()
                st.sidebar.success("Account created. You can now log in.")
    else:
        st.sidebar.subheader("Login")
        login_email = st.sidebar.text_input("Email", key="login_email")
        login_password = st.sidebar.text_input("Password", type="password", key="login_password")
        if st.sidebar.button("Sign in"):
            user = st.session_state.users.get(login_email)
            if not user:
                st.sidebar.error("No account found for that email.")
            else:
                if user["password_hash"] == hash_password(login_password):
                    st.session_state.logged_in_user = user
                    st.sidebar.success("Logged in.")
                else:
                    st.sidebar.error("Incorrect password.")

st.markdown("---")

# ---------- Two-column layout: Form | Account summary ----------
left, right = st.columns([2, 1])

with left:
    if not st.session_state.logged_in_user:
        st.warning("You must register or log in from the sidebar to apply for a card.")
        st.stop()  # stop the page rendering here unless user is authenticated

    with st.form("application_form", clear_on_submit=False):
        st.subheader("Applicant Information")
        # Pre-fill name/email from account if available
        default_name = st.session_state.logged_in_user.get("name") or ""
        default_email = st.session_state.logged_in_user.get("email") or ""
        full_name = st.text_input("Full Name", value=default_name, placeholder="e.g., John Doe")
        dob = st.date_input("Date of Birth", value=date(1990, 1, 1))
        phone = st.text_input("Phone Number", placeholder="+234 80X XXX XXXX")
        email = st.text_input("Email Address", value=default_email)
        employed = st.radio("Are you currently employed?", ["Yes", "No"], index=1)
        tin = st.text_input("Tax Identification Number (TIN) — required if employed")

        st.markdown("### Required Documents (upload)")
        st.write("Upload clear photos or PDFs. Files are kept in your session and not transmitted to any bank unless you connect a real API.")
        id_1 = st.file_uploader("Valid Photo ID #1 (passport / national ID / driver's license)", type=["png", "jpg", "jpeg", "pdf"], key="id1")
        id_2 = st.file_uploader("Valid Photo ID #2 (passport / national ID / driver's license)", type=["png", "jpg", "jpeg", "pdf"], key="id2")
        proof_of_billing = st.file_uploader("Proof of Billing (utility bill / bank statement)", type=["png","jpg","jpeg","pdf"], key="proof")
        photo_1 = st.file_uploader("ID Photo #1 (passport-sized)", type=["png","jpg","jpeg"], key="p1")
        photo_2 = st.file_uploader("ID Photo #2 (passport-sized)", type=["png","jpg","jpeg"], key="p2")

        st.markdown("---")
        st.subheader("Simulated Account Balance")
        balance_input = st.number_input(
            "Enter your current available balance (simulation, USD)",
            min_value=0.0,
            step=50.0,
            value=float(st.session_state.balance),
            format="%.2f",
            key="balance_input"
        )

        submitted = st.form_submit_button("Save / Update Application")

    # After user clicks Save/Update
    if submitted:
        st.session_state.balance = float(balance_input)
        st.success("Application details saved in session. You may proceed to Request the card or Top-up your balance (simulation).")

    st.markdown("### Actions")
    col_req, col_top = st.columns(2)

    with col_req:
        if st.button("Request International ATM Card"):
            # Validate form fields & documents
            missing = []
            if not full_name:
                missing.append("Full Name")
            if employed == "Yes" and not tin:
                missing.append("TIN (required if employed)")
            # documents
            if id_1 is None:
                missing.append("Valid Photo ID #1")
            if id_2 is None:
                missing.append("Valid Photo ID #2")
            if proof_of_billing is None:
                missing.append("Proof of Billing")
            if photo_1 is None:
                missing.append("ID Photo #1")
            if photo_2 is None:
                missing.append("ID Photo #2")

            if missing:
                st.error("Missing required fields/documents: " + ", ".join(missing))
            else:
                # Check balance
                if st.session_state.balance < MIN_REQUIRED:
                    need = MIN_REQUIRED - st.session_state.balance
                    st.error(
                        f"❌ Error: You must have at least {format_currency(MIN_REQUIRED)} in your account before requesting a Landbank ATM Saving Card.\n"
                        f"Please top up your balance. You need an additional {format_currency(need)}."
                    )
                else:
                    # Simulate successful submission
                    request = {
                        "user_email": st.session_state.logged_in_user["email"],
                        "name": full_name,
                        "email": email,
                        "phone": phone,
                        "balance": st.session_state.balance,
                        "requested_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "status": "Submitted",
                        "estimated_delivery": "Within 2 business days (simulated)"
                    }
                    st.session_state.submitted_requests.append(request)
                    st.success("✅ Success! Your Landbank International ATM card request has been submitted (demo).")
                    st.info("A confirmation number has been generated for your reference below.")
                    conf_id = f"LB-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
                    st.write(f"Confirmation ID: {conf_id}")
                    st.write(f"Estimated delivery: {request['estimated_delivery']}")

    with col_top:
        st.write("Top-up (simulation)")
        topup_amount = st.number_input("Top up amount (USD):", min_value=0.0, step=50.0, value=0.0, key="topup")
        if st.button("Top up balance"):
            if topup_amount <= 0:
                st.error("Enter an amount greater than 0 to top up.")
            else:
                st.session_state.balance = float(st.session_state.balance) + float(topup_amount)
                st.success(f"Top up successful (simulation). New balance: {format_currency(st.session_state.balance)}")

    st.markdown("---")
    # Optional: Preview last uploaded images (if any)
    st.subheader("Preview uploaded images (session only)")
    preview_cols = st.columns(3)

    # Collect uploaded files that might be previewable images
    preview_files = []
    for f in (id_1, id_2, proof_of_billing, photo_1, photo_2):
        if f is not None:
            preview_files.append(f)

    if not preview_files:
        st.write("No image previews available. Upload images above to preview them here.")
    else:
        for i, file in enumerate(preview_files[:3]):
            buf = file_preview(file)
            if buf:
                preview_cols[i].image(buf, use_column_width=True)
            else:
                preview_cols[i].write("Preview not available for this file type.")

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Account Summary (simulation)")
    st.write(f"Current session balance: {format_currency(st.session_state.balance)}")
    st.write(f"Minimum required to request card: {format_currency(MIN_REQUIRED)}")
    progress = min(st.session_state.balance / MIN_REQUIRED, 1.0) if MIN_REQUIRED > 0 else 0.0
    st.progress(progress)
    if st.session_state.balance >= MIN_REQUIRED:
        st.markdown('<div class="success-box">You meet the minimum balance requirement. You may request the card.</div>', unsafe_allow_html=True)
    else:
        need = MIN_REQUIRED - st.session_state.balance
        st.markdown(f'<div class="warning">You need {format_currency(need)} more to reach the minimum required balance.</div>', unsafe_allow_html=True)

    st.markdown("### Recent (demo) Requests")
    if st.session_state.submitted_requests:
        last = st.session_state.submitted_requests[-5:][::-1]
        for r in last:
            st.write(f"- {r['name']} — {format_currency(r['balance'])} — {r['requested_at']}")
    else:
        st.write("No submitted requests in this session.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------- Submitted requests expanded ----------
st.subheader("Submitted Requests (demo)")
if st.session_state.submitted_requests:
    for i, r in enumerate(st.session_state.submitted_requests[::-1], start=1):
        with st.expander(f"{i}. {r['name']} — {format_currency(r['balance'])} — {r['requested_at']}"):
            st.write(f"Name: {r['name']}")
            st.write(f"Phone: {r['phone']}")
            st.write(f"Email: {r['email']}")
            st.write(f"Submitted at: {r['requested_at']}")
            st.write(f"Status: {r['status']}")
            st.write(f"Estimated delivery: {r.get('estimated_delivery','N/A')}")
else:
    st.write("No requests yet. Fill the form and click Request International ATM Card when ready.")

st.markdown("---")

# ---------- Footer / Honest notice ----------
st.caption(
    "This application demonstrates the UX and flow. To operate with a real bank you must integrate a bank API, implement secure credential handling, and confirm delivery/fulfillment with a logistics provider."
)
