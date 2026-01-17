interface Feature {
    attributes: {
        STATUS: string;
        SECTIONNUMBER: string;
    };
}

interface ApiResponse {
    features: Feature[];
}

const sectionInput = document.getElementById('sectionInput') as HTMLInputElement;
const checkBtn = document.getElementById('checkBtn') as HTMLButtonElement;
const notifyBtn = document.getElementById('notifyBtn') as HTMLButtonElement;
const statusArea = document.getElementById('statusArea') as HTMLDivElement;
const statusText = document.getElementById('statusText') as HTMLDivElement;
const lastUpdated = document.getElementById('lastUpdated') as HTMLDivElement;
const checkLoader = document.getElementById('checkLoader') as HTMLDivElement;

let pollingInterval: number | null = null;

// Load saved section
const savedSection = localStorage.getItem('troy_snow_section');
if (savedSection && sectionInput) {
    sectionInput.value = savedSection;
}

async function fetchStatus(sectionId: string): Promise<string> {
    const url = `https://gis1.troymi.gov/server/rest/services/Snow_Plow/MapServer/2/query?where=SECTIONNUMBER='${sectionId}'&outFields=STATUS,SECTIONNUMBER&f=json`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        const data: ApiResponse = await response.json();

        if (data.features && data.features.length > 0) {
            return data.features[0].attributes.STATUS;
        } else {
            return 'NOT FOUND';
        }
    } catch (error) {
        console.error('Error fetching status:', error);
        return 'ERROR';
    }
}

function updateUI(status: string): void {
    if (!statusArea || !statusText || !lastUpdated) return;

    statusArea.style.display = 'block';
    statusText.textContent = status;

    statusArea.className = ''; // Reset classes
    if (status === 'COMPLETED' || status === 'Completed') {
        statusArea.classList.add('status-completed');
    } else if (status === 'ERROR' || status === 'NOT FOUND') {
        statusArea.classList.add('status-error');
    } else {
        statusArea.classList.add('status-pending');
    }

    const now = new Date();
    lastUpdated.textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

async function checkStatus(): Promise<string | void> {
    if (!sectionInput || !checkBtn || !checkLoader) return;

    const sectionId = sectionInput.value.trim();
    if (!sectionId) {
        alert('Please enter a section number');
        return;
    }

    localStorage.setItem('troy_snow_section', sectionId);

    checkBtn.disabled = true;
    checkLoader.style.display = 'inline-block';

    const status = await fetchStatus(sectionId);

    checkBtn.disabled = false;
    checkLoader.style.display = 'none';

    updateUI(status);

    if (pollingInterval && (status === 'COMPLETED' || status === 'Completed')) {
        // If we are polling and it's done, notify and stop
        sendNotification(sectionId);
        stopPolling();
    }

    return status;
}

function startPolling(): void {
    if (pollingInterval) return;

    // Request permission
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

    if (notifyBtn) {
        notifyBtn.textContent = 'Monitoring...';
        notifyBtn.classList.add('active');
    }

    // Check immediately
    checkStatus();

    pollingInterval = window.setInterval(async () => {
        await checkStatus();
    }, 60000); // Check every minute
}

function stopPolling(): void {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    if (notifyBtn) {
        notifyBtn.textContent = 'Notify Me';
        notifyBtn.classList.remove('active');
    }
}

function sendNotification(sectionId: string): void {
    if (Notification.permission === "granted") {
        new Notification("Snow Cleaning Complete!", {
            body: `Section ${sectionId} has been completed.`,
            icon: "https://cityoftroy.maps.arcgis.com/sharing/rest/content/items/0b0cce9de97c42f3bd1ce8b46dd30f84/info/thumbnail/ago_downloaded.png"
        });
    } else {
        alert(`Section ${sectionId} is Complete!`);
    }
}

if (checkBtn) {
    checkBtn.addEventListener('click', () => { checkStatus(); });
}

if (notifyBtn) {
    notifyBtn.addEventListener('click', () => {
        if (pollingInterval) {
            stopPolling();
        } else {
            startPolling();
        }
    });
}

// Allow Enter key to check
if (sectionInput) {
    sectionInput.addEventListener('keypress', (e: KeyboardEvent) => {
        if (e.key === 'Enter') {
            checkStatus();
        }
    });
}
