# Deployment Guide - Troy Snow Cleaning Notification App

This guide explains how to deploy the Troy Snow Cleaning Notification App so you can access it from anywhere. Since this is a static web application (HTML, CSS, and JavaScript), you can host it for free on several platforms.

## Prerequisites

-   A [GitHub](https://github.com/) account.
-   Git installed on your computer.

## Option 1: GitHub Pages (Recommended)

GitHub Pages is the easiest way to host this project if you already use GitHub.

1.  **Create a Repository**:
    -   Go to GitHub and create a new public repository (e.g., `troy-snow-status`).
    -   Do not initialize with a README, .gitignore, or license (we have local files).

2.  **Push Code to GitHub**:
    Open your terminal in the project folder and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/troy-snow-status.git
    git push -u origin main
    ```
    *(Replace `YOUR_USERNAME` with your actual GitHub username)*

3.  **Enable GitHub Pages**:
    -   Go to your repository **Settings** > **Pages**.
    -   Under **Source**, select `Deploy from a branch`.
    -   Under **Branch**, select `main` and folder `/ (root)`.
    -   Click **Save**.

4.  **Access Your App**:
    -   Wait a minute or two.
    -   Your app will be live at `https://YOUR_USERNAME.github.io/troy-snow-status/`.

## Option 2: Netlify

Netlify offers easy drag-and-drop deployment.

1.  **Sign Up/Log In**: Go to [Netlify](https://www.netlify.com/) and sign up.
2.  **Drag and Drop**:
    -   Go to the **Sites** tab.
    -   Drag your project folder (the one containing `index.html` and `dist/`) into the "Drag and drop your site output folder here" area.
3.  **Access Your App**:
    -   Netlify will deploy it instantly and give you a URL (e.g., `https://random-name.netlify.app`).
    -   You can change the site name in **Site settings** > **Change site name**.

## Important Notes

-   **API Access**: The app connects to `gis1.troymi.gov`. This API supports CORS (Cross-Origin Resource Sharing), so it should work fine from any domain (localhost, github.io, netlify.app).
-   **Notifications**: Browser notifications require a secure context (HTTPS). Both GitHub Pages and Netlify provide HTTPS automatically.
-   **Updates**: If you make changes to the code (e.g., in `src/app.ts`), remember to run `npm install` and `npx tsc` to recompile the JavaScript before deploying.
