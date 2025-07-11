# Google Docs Credentials Setup

To enable this application to write to a Google Doc, you must provide it with a digital identity known as a **Service Account**. This setup involves downloading a special JSON key file from Google Cloud.

Think of this JSON file as the application's **ID card** — it identifies the application to Google’s servers.

> **Note:** If you have Microsoft Word installed on your system and prefer saving transcripts locally to Word documents, you can skip this setup entirely.

---

## One-Time Setup Instructions

### Part 1: Create the Service Account and Download the JSON Key

1. **Go to the Google Cloud Console**

   * Create a **new project** (e.g., “My Scraper Project”).

2. **Enable Required APIs**

   * In your project, go to **APIs & Services > Library**.
   * Enable the following:

     * **Google Docs API**
     * **Google Drive API**

3. **Create a Service Account**

   * Navigate to **IAM & Admin > Service Accounts**.
   * Click **+ CREATE SERVICE ACCOUNT**.
   * Enter a name like `docs-writer`.
   * Click **CREATE AND CONTINUE**.
   * Skip the next two optional steps by clicking **CONTINUE**, then **DONE**.

4. **Download the JSON Key File**

   * In the list of service accounts, select the one you just created.
   * Go to the **KEYS** tab.
   * Click **ADD KEY > Create new key**.
   * Choose **JSON**, then click **CREATE**. This downloads the key file.

5. **Rename and Move the File**

   * Rename the file to `Google-Docs-API-credentials.json`.
   * Move it into the `credentials/` directory of this project.

At this point, the application has its digital credentials.

---

### Part 2: Grant Document Access via Share Link

The easiest way to allow the application to edit a document is to make the document editable by anyone with the link.

1. **Create a new Google Doc.**
2. Click the **Share** button.
3. Under **General access**, change "Restricted" to **"Anyone with the link"**.
4. Change the role from "Viewer" to **"Editor"**.
5. Click **Copy link**, then **Done**.

You can provide this link to the application when prompted. Since the service account has credentials and the document is open to editing via link, everything should work correctly.

---

## Optional: Working with Private Google Docs

If you do not want the document to be publicly editable, follow Part 1 above and instead of using a shareable link:

1. Open your private Google Doc.
2. Click **Share**.
3. In the **Add people and groups** field, paste the **service account email address** found in the JSON key (`"client_email"`).
4. Assign **Editor** access and click **Send**.

This allows only the service account to edit the document, keeping it private to everyone else.
