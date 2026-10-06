
let currentCategory = "";

function setCategory(btn, category) {
    // Update active pill styling
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    
    currentCategory = category;
    triggerSearch();
}

function triggerSearch() {
    let query = document.getElementById("searchInput").value;
    searchItems(query);
}

function getEmojiForCategory(category) {
    if (category === 'Electronics') return '💻';
    if (category === 'Personal') return '🎒';
    if (category === 'Documents') return '📚';
    return '✨';
}

function copyShareLink(id) {
    const url = window.location.origin + '/CampusFind/item-details.jsp?id=' + id;
    navigator.clipboard.writeText(url).then(() => {
        alert("Link copied! Share it with your friends.");
    });
}

function searchItems(query) {
    let url = 'SearchItemServlet?q=' + encodeURIComponent(query) + '&cat=' + encodeURIComponent(currentCategory);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.length === 0) {
                html = "<p style='grid-column: 1/-1; text-align:center; color:#999;'>No items found.</p>";
            } else {
                data.forEach(item => {
                    let typeClass = item.type === 'LOST' ? 'badge-lost' : 'badge-found';
                    let emoji = getEmojiForCategory(item.category);
                    
                    html += `<div class="item-card">
                        <div class="item-card-emoji">${emoji}</div>
                        <h4>${item.item_name} <span class="${typeClass}">${item.type}</span></h4>
                        <p><strong>📍</strong> ${item.location}</p>
                        <p><strong>🕒</strong> ${item.date_reported}</p>
                        <div class="action-bar">
                            <a href="item-details.jsp?id=${item.id}" class="btn" style="padding: 8px 16px;">View</a>
                            <button onclick="copyShareLink(${item.id})" class="share-btn">🔗 Share</button>
                        </div>
                    </div>`;
                });
            }
            document.getElementById("searchResults").innerHTML = html;
        });
}

function loadGuidelines() {
    fetch('GuidelinesServlet')
        .then(response => response.text())
        .then(html => {
            document.getElementById('guidelines-list').innerHTML = html;
        });
}
