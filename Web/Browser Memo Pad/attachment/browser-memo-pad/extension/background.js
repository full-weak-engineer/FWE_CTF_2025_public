// Initialize memos
chrome.runtime.onInstalled.addListener(() => {    
    chrome.storage.local.get(['memos'], (result) => {
        if (!result.memos) {
            chrome.storage.local.set({ memos: [] });
        }
    });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'saveMemo') {
        handleSaveMemo(request.memo);
    }
});

// Save a memo to local storage
async function handleSaveMemo(memo) {
    try {
        const result = await chrome.storage.local.get(['memos']);
        const memos = result.memos || [];
        memos.unshift(memo);
        await chrome.storage.local.set({ memos: memos });
    } catch (error) {
        console.error('Failed to save memo to local storage:', error);

    }
}