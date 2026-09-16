# Mā-kun's 28th Birthday — Streamlit page

A two-stage birthday page:

- **Friday / choose mode:** Masaki chooses the vibe, activities, food, request, start time and duration.
- **Saturday / birthday mode:** the same URL becomes his finished birthday itinerary + your message + photos.

---

## 1. Create a new GitHub repository

Create a repository such as:

`masaki-birthday`

Upload all files from this folder, preserving the structure:

```text
masaki-birthday/
├── app.py
├── config.py
├── requirements.txt
├── assets/
│   ├── README.txt
│   ├── photo_1.jpg     <- you upload this
│   ├── photo_2.jpg     <- optional
│   └── photo_3.jpg     <- optional
└── .streamlit/
    └── secrets.toml.example
```

Do **not** upload your real Google service-account credentials to GitHub.

---

## 2. Add your photos

In GitHub:

1. Open the `assets` folder.
2. Click **Add file → Upload files**.
3. Upload your images using these exact names:
   - `photo_1.jpg`
   - `photo_2.jpg`
   - `photo_3.jpg`
4. Commit the changes.

You do not need to copy image links. Streamlit reads the files directly from the repository.

---

## 3. Create the Google Sheet that will receive Masaki's answers

1. Go to Google Sheets.
2. Create a blank spreadsheet, for example:
   `Masaki Birthday Responses`
3. Leave the first sheet as-is.
4. Copy the spreadsheet ID from its URL.

For a URL like:

`https://docs.google.com/spreadsheets/d/ABC123xyz/edit`

the Sheet ID is:

`ABC123xyz`

You do not need to create columns manually. The app creates the header row on the first submission.

---

## 4. Create a Google Cloud service account

This sounds longer than it actually is. You only do it once.

1. Open Google Cloud Console.
2. Create a project (example: `masaki-birthday`).
3. Enable:
   - Google Sheets API
   - Google Drive API
4. Go to **IAM & Admin → Service Accounts**.
5. Create a service account.
6. Open the service account → **Keys → Add key → Create new key → JSON**.
7. Download the JSON key.

Important:
- Keep this JSON private.
- Never upload it to GitHub.

---

## 5. Share the Google Sheet with the service account

Open the JSON key and copy the value of:

`client_email`

It looks something like:

`birthday-app@your-project.iam.gserviceaccount.com`

Open your Google Sheet → **Share** → paste that email → give it **Editor** access.

This is what allows the app to add Masaki's response.

---

## 6. Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud with GitHub.
2. Create a new app.
3. Select your `masaki-birthday` repository.
4. Main file path:
   `app.py`
5. Deploy.

At first, the app can load even before Google Sheets is configured, but the final Submit button will not save anything until you add the secrets in the next step.

---

## 7. Add private Streamlit secrets

Open:

**Streamlit Cloud → your app → Settings → Secrets**

Use `.streamlit/secrets.toml.example` as the template.

You need:

```toml
sheet_id = "YOUR_SHEET_ID"

[gcp_service_account]
...
```

Copy the corresponding values from the Google service-account JSON.

### Important private-key formatting

In TOML, keep it inside triple quotes:

```toml
private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
"""
```

Save the secrets and reboot the app if needed.

---

## 8. Test before sending it to Masaki

Before Friday:

1. Open the public Streamlit link on your phone.
2. Complete the page yourself.
3. Press **Confirm my birthday date ♡**
4. Check your Google Sheet.
5. Confirm a new row appears.

If it works, delete your test row from Sheets.

Tip: use an incognito/private tab for a second test because Streamlit session state can remember your current step until the session resets.

---

## 9. Friday: keep choose mode

In `config.py`:

```python
APP_MODE = "choose"
```

Send Masaki the Streamlit URL.

When he confirms, his answers will appear in your Google Sheet.

---

## 10. Friday night / Saturday: build his real itinerary

Open the Google Sheet and read his choices.

Then edit `config.py`:

```python
BIRTHDAY_PLAN = [
    {"time": "1:00 PM", "activity": "..."},
    {"time": "3:00 PM", "activity": "..."},
]
```

Also replace `BIRTHDAY_MESSAGE` with your final letter.

Commit the changes to GitHub.

Streamlit should redeploy automatically.

---

## 11. Saturday: switch the same URL to birthday mode

In `config.py`, change:

```python
APP_MODE = "choose"
```

to:

```python
APP_MODE = "birthday"
```

Commit.

The same public link now becomes his finished birthday page.

---

## What you usually edit

Almost everything is in `config.py`.

### Friday
```python
APP_MODE = "choose"
```

### Saturday
```python
APP_MODE = "birthday"
```

### Photos
Upload them to `/assets`.

### Final itinerary
Edit `BIRTHDAY_PLAN`.

### Final letter
Edit `BIRTHDAY_MESSAGE`.

---

## Privacy notes

- Your Google service account key stays only in Streamlit Secrets.
- Never paste it into `app.py`, `config.py`, README, or GitHub.
- Your photos are part of the GitHub repository. If you do not want them publicly visible in GitHub, make the repository private and ensure your Streamlit deployment supports access to that private repository.
- The Google Sheet should remain private and shared only with your own Google account and the service-account email.

---

## Optional tiny customizations

In `app.py`, search for:

- `#F7F2EA` → cream background
- `#7A263A` → burgundy accent
- `"I knew you were going to pick this."` → PUBG easter egg
- `"Correct answer."` → sleep-until-one-falls-asleep easter egg

But you should not need to touch the app code for normal use.
