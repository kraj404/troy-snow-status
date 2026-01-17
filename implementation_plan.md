# Implementation Plan - Troy Snow Cleaning Notification App

## Goal
Create an application that allows users to check the snow cleaning status of a specific section in Troy, MI, and receive notifications when the section is completed.

## User Review Required
> [!IMPORTANT]
> The app relies on the City of Troy's GIS API. If the API changes or goes offline, the app will stop working.
> The web app requires the browser to be open to receive notifications.

## Proposed Changes

### Web Application
I will create a single-page web application using HTML, CSS, and TypeScript.

#### [NEW] [index.html](file:///Users/I808883/.gemini/antigravity/brain/e32ba253-8e99-4635-9848-02b00fb21049/index.html)
- **UI**:
    - Input field for Section Number.
    - "Check Status" and "Notify Me" buttons.
    - Status display area (Current status, Last updated).
    - Visual indicator (Green for Completed, Yellow for In Progress/Pending).
    - References `app.js` (compiled from `app.ts`).

#### [NEW] [app.ts](file:///Users/I808883/.gemini/antigravity/brain/e32ba253-8e99-4635-9848-02b00fb21049/app.ts)
- **Logic**:
    - Fetch data from `https://gis1.troymi.gov/server/rest/services/Snow_Plow/MapServer/2/query`.
    - Query parameters: `where=SECTIONNUMBER='{section_id}'&outFields=STATUS,SECTIONNUMBER&f=json`.
    - Polling mechanism (e.g., every 60 seconds) if "Notify Me" is active.
    - Browser Notification API to alert user when status is "COMPLETED".
    - `localStorage` to save the last checked section.
    - Type definitions for API responses and DOM elements.

#### [NEW] [tsconfig.json](file:///Users/I808883/.gemini/antigravity/brain/e32ba253-8e99-4635-9848-02b00fb21049/tsconfig.json)
- TypeScript configuration file.

### Python Script (Alternative)
I will also provide a Python script for command-line usage.

#### [NEW] [check_snow_status.py](file:///Users/I808883/.gemini/antigravity/brain/e32ba253-8e99-4635-9848-02b00fb21049/check_snow_status.py)
- CLI arguments for section number and polling interval.
- Prints status to console.
- Sends desktop notification (using `plyer` or system commands) when complete.

## Deployment Strategy
Since this is a static web application, it can be deployed to any static site hosting service.

### Options
1.  **GitHub Pages**: Easy if the code is hosted on GitHub.
2.  **Netlify / Vercel**: Drag-and-drop deployment or Git integration.

### Preparation
- Ensure `dist/app.js` is up-to-date.
- Create a `DEPLOY.md` guide for the user.

## Verification Plan

### Automated Tests
- I will create a test script `test_api.py` to verify the API endpoint is reachable and returns expected data format.
- I will use `unittest.mock` to simulate API responses for the Python script logic.

### Manual Verification
- **Web App**:
    1. Open `index.html` in a browser.
    2. Enter a known section number (e.g., from the map or a random one like "14").
    3. Click "Check Status" and verify the status is displayed.
    4. Click "Notify Me".
    5. Simulate a status change (by mocking the fetch or waiting if possible, but mocking is better for verification).
    6. Verify browser notification appears.
- **Python Script**:
    1. Run `python3 check_snow_status.py --section 14`.
    2. Verify output.
