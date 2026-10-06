
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
let obj = item;
                    
                    
                    let visual = obj.has_image ? `<img src="${obj.image_url}" style="width:100%; height:200px; object-fit:cover; border-radius:4px; margin-bottom:15px; border:1px solid #EFEADD;">` : `<div class="item-card-emoji" style="background:#F1ECE1; border-radius:4px;">${emoji}</div>`;
                    let rewardBadge = obj.reward !== "" ? `<p style="color:#C92A2A; font-weight:bold; font-family:'Fraunces', serif; margin:10px 0;"><span style="font-size:18px;">💰</span> Reward: ${obj.reward}</p>` : "";
                    
                    html += `<div class="item-card">
                        ${visual}
                        <h4>${obj.item_name} <span class="${typeClass}">${obj.type}</span></h4>
                        <p><strong>📍</strong> ${obj.location}</p>
                        <p><strong>🕒</strong> ${obj.date_reported}</p>
                        ${rewardBadge}
                        <div class="action-bar" style="margin-top:15px;">
                            <a href="item-details.jsp?id=${obj.id}" class="btn" style="padding: 8px 16px;">View</a>
                            <button onclick="copyShareLink(${obj.id})" class="share-btn" style="background:transparent; border:1px solid #7A6F66; padding:6px 12px; border-radius:4px; cursor:pointer;">🔗 Share</button>
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
