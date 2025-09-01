let saveButton = null;

function create(value) {
    const currentUrl = location.href;
    const memo = {
        text: value,
        url: currentUrl,
        origin: location.origin,
        timestamp: new Date().toLocaleString(),
    };
    
    chrome.storage.local.get(["memos"], function (result) {
        const memos = result.memos || [];
        memos.push(memo);
        chrome.storage.local.set({ memos: memos }, function () {
            if(saveButton) {
                saveButton.innerHTML = "✓ Saved successfully";
                setTimeout(() => {
                    if (saveButton) {
                        saveButton.remove();
                        saveButton = null;
                    }
                }, 1500);
            }
        });
    });
}

// Listen for mouseup events to detect text selection
document.addEventListener('mouseup', function(e) {
    setTimeout(() => {
        const selection = window.getSelection();

        if (selection.rangeCount === 0) {
            return;
        }

        const selectedText = selection.toString().trim();
        if (saveButton) {
            saveButton.remove();
            saveButton = null;
        }

        // If some text is selected, show a save button
        if (selectedText.length > 0) {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            saveButton = document.createElement('div');
            saveButton.className = 'memo-save-button';
            saveButton.innerHTML = '💾 Save';
            saveButton.style.cssText = `
                all: initial;
                position: fixed;
                top: ${rect.bottom + 5}px;
                left: ${rect.left}px;
                background: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
                z-index: 10000;
                font-size: 12px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            `;

            document.body.appendChild(saveButton);
            
            // When the save button is clicked, store the memo
            saveButton.addEventListener("click", () => create(selectedText));
        }
    }, 10);
});

document.addEventListener('click', function(e) {
    if (saveButton && !saveButton.contains(e.target)) {
        saveButton.remove();
        saveButton = null;
    }
});

if (!document.querySelector("meta[memopad-extensionId]")) {
    const meta = document.createElement("meta");
    meta.setAttribute('memopad-extensionId', chrome.runtime.id)
    document.head.appendChild(meta);
}

// API for the bot
window.addEventListener("message", (event) => {
    if (event.source !== window) return;
    if (event.data?.type === "create") {
        create(event.data.payload);
    }
});