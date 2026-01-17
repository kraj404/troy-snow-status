"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const sectionInput = document.getElementById('sectionInput');
const checkBtn = document.getElementById('checkBtn');
const notifyBtn = document.getElementById('notifyBtn');
const statusArea = document.getElementById('statusArea');
const statusText = document.getElementById('statusText');
const lastUpdated = document.getElementById('lastUpdated');
const checkLoader = document.getElementById('checkLoader');
let pollingInterval = null;
// Load saved section
const savedSection = localStorage.getItem('troy_snow_section');
if (savedSection && sectionInput) {
    sectionInput.value = savedSection;
}
function fetchStatus(sectionId) {
    return __awaiter(this, void 0, void 0, function* () {
        const url = `https://gis1.troymi.gov/server/rest/services/Snow_Plow/MapServer/2/query?where=SECTIONNUMBER='${sectionId}'&outFields=STATUS,SECTIONNUMBER&f=json`;
        try {
            const response = yield fetch(url);
            if (!response.ok)
                throw new Error('Network response was not ok');
            const data = yield response.json();
            if (data.features && data.features.length > 0) {
                return data.features[0].attributes.STATUS;
            }
            else {
                return 'NOT FOUND';
            }
        }
        catch (error) {
            console.error('Error fetching status:', error);
            return 'ERROR';
        }
    });
}
function updateUI(status) {
    if (!statusArea || !statusText || !lastUpdated)
        return;
    statusArea.style.display = 'block';
    statusText.textContent = status;
    statusArea.className = ''; // Reset classes
    if (status === 'COMPLETED' || status === 'Completed') {
        statusArea.classList.add('status-completed');
    }
    else if (status === 'ERROR' || status === 'NOT FOUND') {
        statusArea.classList.add('status-error');
    }
    else {
        statusArea.classList.add('status-pending');
    }
    const now = new Date();
    lastUpdated.textContent = `Last updated: ${now.toLocaleTimeString()}`;
}
function checkStatus() {
    return __awaiter(this, void 0, void 0, function* () {
        if (!sectionInput || !checkBtn || !checkLoader)
            return;
        const sectionId = sectionInput.value.trim();
        if (!sectionId) {
            alert('Please enter a section number');
            return;
        }
        localStorage.setItem('troy_snow_section', sectionId);
        checkBtn.disabled = true;
        checkLoader.style.display = 'inline-block';
        const status = yield fetchStatus(sectionId);
        checkBtn.disabled = false;
        checkLoader.style.display = 'none';
        updateUI(status);
        if (pollingInterval && (status === 'COMPLETED' || status === 'Completed')) {
            // If we are polling and it's done, notify and stop
            sendNotification(sectionId);
            stopPolling();
        }
        return status;
    });
}
function startPolling() {
    if (pollingInterval)
        return;
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
    pollingInterval = window.setInterval(() => __awaiter(this, void 0, void 0, function* () {
        yield checkStatus();
    }), 60000); // Check every minute
}
function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    if (notifyBtn) {
        notifyBtn.textContent = 'Notify Me';
        notifyBtn.classList.remove('active');
    }
}
function sendNotification(sectionId) {
    if (Notification.permission === "granted") {
        new Notification("Snow Cleaning Complete!", {
            body: `Section ${sectionId} has been completed.`,
            icon: "https://cityoftroy.maps.arcgis.com/sharing/rest/content/items/0b0cce9de97c42f3bd1ce8b46dd30f84/info/thumbnail/ago_downloaded.png"
        });
    }
    else {
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
        }
        else {
            startPolling();
        }
    });
}
// Allow Enter key to check
if (sectionInput) {
    sectionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            checkStatus();
        }
    });
}
