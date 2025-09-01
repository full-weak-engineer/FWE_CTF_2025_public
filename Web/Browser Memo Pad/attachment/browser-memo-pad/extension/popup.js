document.addEventListener('DOMContentLoaded', function() {
    loadMemos();
    
    // Ask user to confirm before removing all saved memos
    document.getElementById('clearAll').addEventListener('click', function() {
        if (confirm('Are you sure you want to delete all memos?')) {
            chrome.storage.local.clear(function() {
                loadMemos();
            });
        }
    });
});

// Load all saved memos from local storage and show them on the page
function loadMemos() {
    chrome.storage.local.get(['memos'], function(result) {
        const memos = result.memos || [];
        const memoList = document.getElementById('memoList');
        
        if (memos.length === 0) {
            memoList.innerHTML = '<div class="no-memos">No memos saved</div>';
            return;
        }
        
        // Insert the generated HTML into the memo list element
        let html = '';
        memos.forEach((memo, index) => {
            html += `
                <div class="memo-item" data-index="${index}">
                    <div class="memo-content">${memo.text}</div>
                    <div class="memo-meta">
                        📍 <a class="memo-url" href="${memo.url}">${memo.origin}</a> |
                        🕒 <span class="memo-time">${memo.timestamp}</span>
                    </div>
                    <button class="delete-btn" data-id="${index}">🗑️</button>
                </div>
            `;
        });
        memoList.innerHTML = html;

        // Add event listeners to delete buttons to remove memos
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = Number(btn.getAttribute('data-id'));
                deleteMemo(id);

            });
        });

        // View the website from which the memo was saved
        const links = memoList.querySelectorAll('.memo-url');
        links.forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();

                const dataIndex = link.closest('.memo-item')?.dataset.index;
                if (dataIndex === undefined) return;

                chrome.storage.local.get('memos', ({ memos = [] }) => {
                    const memo = memos[+dataIndex];
                    if (!memo) return;

                    const url = link.href.split('#')[0];
                    if(!url.startsWith('http://')  && !url.startsWith('https://')) {
                        console.error('invalid url');
                        return;
                    }
                    const encodedText = encodeURIComponent(memo.text);
                    const urlWithFragment = `${url}#:~:text=${encodedText}`;

                    chrome.tabs.create({ url: urlWithFragment });
                });
            });
        });
    });
}

// Delete the selected memo
function deleteMemo(dataIndex) {
    chrome.storage.local.get('memos', ({ memos = [] }) => {
        memos.splice(dataIndex, 1);
        chrome.storage.local.set({ memos }, function() {
            loadMemos();
        });
    });
}
