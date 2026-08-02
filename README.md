# Mindset Bots — Render Deployment

This folder contains two Telegram bots that run together 24/7 on Render's free tier:

- **bot1**: `@this_marketing_copy_bot` (YouTube channel recommender) — `main_bot1.py`
- **bot2**: `@MindsetLibraryBot` (book library) — `bot2/main.py`

`main_cloud.py` is the supervisor: it starts both bots as separate processes,
restarts any bot that crashes after 15 seconds, and exposes an HTTP health
endpoint (`/health`) on the `$PORT` that Render provides.

## Deploy steps

1. Create a new repository on GitHub (Public or Private — either works).
2. Upload **all files and folders in this directory** to that repo (upload the
   *contents*, not the folder itself). Keep the `bot2/` folder structure.
3. Open [render.com](https://render.com) → sign in with your GitHub account.
4. Click **New → Blueprint**, choose your repository, and click **Apply**.
5. When Render asks for environment values, paste:
   - `BOT_TOKEN` = your bot1 token
   - `BOT_TOKEN_2` = your bot2 token
6. Wait for the deploy to finish (2–3 minutes), then open the **Logs** tab.
   You should see:
   ```
   [bot1_channels] started
   [bot2_library] started
   ```
7. Test both bots in Telegram with `/start`.

## Keep it awake (free tier)

Render's free tier sleeps after 15 minutes of inactivity. To keep both bots
online 24/7 for free:

1. Open [uptimerobot.com](https://uptimerobot.com) and create a free account.
2. **Add New Monitor** → type **HTTP(s)** → interval **5 minutes**.
3. URL: your Render service URL, e.g. `https://mindset-bots.onrender.com/health`
4. Save. UptimeRobot will ping the health endpoint every 5 minutes, which keeps
   the service running continuously.

## Environment variables

| Variable     | Used by       | Description             |
|--------------|---------------|-------------------------|
| `BOT_TOKEN`  | main_bot1.py  | Token of bot1 (channels)|
| `BOT_TOKEN_2`| bot2/main.py  | Token of bot2 (library) |

Tokens are read from the environment only — never hardcode them in code.
