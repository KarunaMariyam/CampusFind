
// 3. JavaScript & 4. DOM Manipulation
function validateRegistration() {
    let pwd = document.getElementById("password").value;
    let cpwd = document.getElementById("confirmPassword").value;
    if (pwd !== cpwd) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}

// 5. AJAX & 20. Fetch API
function searchItems(query) {
    if (query.length < 2 && query.length > 0) return; // Wait for at least 2 chars
    
    let url = query.length === 0 ? 'SearchItemServlet?q=' : 'SearchItemServlet?q=' + encodeURIComponent(query);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            let html = "";
            if(data.length === 0) {
                html = "<p>No items found.</p>";
            } else {
                data.forEach(item => {
                    let typeClass = item.type === 'LOST' ? 'badge-lost' : 'badge-found';
                    html += `<div class="item-card card">
                        <h4>${item.item_name} <span class="${typeClass}">${item.type}</span></h4>
                        <p><strong>Category:</strong> ${item.category}</p>
                        <p><strong>Location:</strong> ${item.location}</p>
                        <a href="item-details.jsp?id=${item.id}" class="btn">View Details</a>
                    </div>`;
                });
            }
            document.getElementById("searchResults").innerHTML = html; // DOM Manipulation
        });
}

// 20. Fetch API reading from our XML parser servlet
function loadGuidelines() {
    fetch('GuidelinesServlet')
        .then(response => response.text())
        .then(html => {
            document.getElementById('guidelines-list').innerHTML = html; // DOM Manipulation
        });
}
