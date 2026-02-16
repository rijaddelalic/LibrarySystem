const API_URL = "http://127.0.0.1:8000";
let currentUser = null, isAdmin = false, allBooks = [], activeLoansIds = [];

// --- TOAST SISTEM ---
function notify(msg, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-times-circle'}"></i> <span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 400); }, 3000);
}

// --- INIT ---
document.addEventListener("DOMContentLoaded", () => {
    if(localStorage.getItem('theme') === 'light') document.body.classList.add('light-theme');
});

function toggleTheme() {
    const isLight = document.body.classList.toggle('light-theme');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    notify("Tema ažurirana");
}

// --- AUTH ---
function switchAuth(mode) {
    document.getElementById('f-login').style.display = mode === 'login' ? 'block' : 'none';
    document.getElementById('f-register').style.display = mode === 'register' ? 'block' : 'none';
    document.getElementById('t-login').className = mode === 'login' ? 'active' : '';
    document.getElementById('t-register').className = mode === 'register' ? 'active' : '';
}

async function handleLogin() {
    const fd = new FormData();
    fd.append("email", document.getElementById("l-email").value);
    fd.append("password", document.getElementById("l-pass").value);
    const res = await fetch(`${API_URL}/users/login`, { method: "POST", body: fd });
    if (res.ok) {
        currentUser = await res.json();
        isAdmin = currentUser.email.endsWith("@libroflow.admin");
        initApp();
        notify(`Dobrodošli, ${currentUser.name}!`);
    } else notify("Podaci nisu tačni", "error");
}

async function handleRegister() {
    const fd = new FormData();
    fd.append("name", document.getElementById("r-name").value);
    fd.append("lastname", document.getElementById("r-last").value);
    fd.append("email", document.getElementById("r-email").value);
    fd.append("password", document.getElementById("r-pass").value);
    const img = document.getElementById("r-img").files[0];
    if(img) fd.append("image", img);
    const res = await fetch(`${API_URL}/users/`, { method: "POST", body: fd });
    if(res.ok) {
        const data = await res.json();
        notify("Uspješno! Vaš ID: " + data.membershipId);
        switchAuth('login');
    } else notify("Greška pri registraciji", "error");
}

// --- RESET PASSWORD MODAL ---
function openResetModal() { document.getElementById('reset-modal').style.display = 'flex'; }
function closeResetModal() { document.getElementById('reset-modal').style.display = 'none'; }

async function confirmReset() {
    const fd = new FormData();
    fd.append("email", document.getElementById("res-email").value);
    fd.append("mid", document.getElementById("res-mid").value);
    fd.append("new_pw", document.getElementById("res-new-pw").value);

    const res = await fetch(`${API_URL}/users/reset-password-external`, { method: "PUT", body: fd });
    if(res.ok) {
        notify("Lozinka uspješno resetovana!");
        closeResetModal();
    } else notify("Podaci se ne podudaraju", "error");
}

function initApp() {
    document.getElementById("auth-screen").style.display = "none";
    document.getElementById("app-screen").style.display = "flex";
    document.getElementById("u-display").innerText = currentUser.name + " " + currentUser.lastname;
    document.getElementById("u-id").innerText = currentUser.membershipId;
    const avatar = document.getElementById("u-avatar");
    avatar.src = currentUser.profile_image ? `${API_URL}/${currentUser.profile_image}` : `https://ui-avatars.com/api/?name=${currentUser.name}&background=6366f1&color=fff&bold=true`;
    document.querySelectorAll('.admin-only').forEach(el => el.style.display = isAdmin ? "flex" : "none");
    if(isAdmin) updateStats();
    fetchBooks();
}

async function updateStats() {
    const res = await fetch(`${API_URL}/stats/`);
    const data = await res.json();
    document.getElementById("st-books").innerText = data.books;
    document.getElementById("st-users").innerText = data.users;
    document.getElementById("st-loans").innerText = data.loans;
}

async function fetchBooks() {
    const [bRes, lRes] = await Promise.all([fetch(`${API_URL}/books/`), fetch(`${API_URL}/loans/history`)]);
    allBooks = await bRes.json();
    const loans = await lRes.json();
    activeLoansIds = loans.filter(l => !l.return_date).map(l => l.book_id);
    renderBooks(allBooks);
}

function renderBooks(books) {
    const grid = document.getElementById("book-grid");
    if(!grid) return;
    grid.innerHTML = books.map(b => {
        const busy = activeLoansIds.includes(b.id);
        const img = b.image_filename ? `${API_URL}/${b.image_filename}` : 'https://via.placeholder.com/240x320';
        return `
            <div class="book-card">
                <img src="${img}">
                <h4>${b.title}</h4><p style="color:var(--muted); font-size:0.8rem">${b.author}</p>
                <div class="flex-between" style="margin-top:15px">
                    <span class="status-badge ${busy ? 'tag-busy' : 'tag-free'}">${busy ? 'Zauzeta' : 'Slobodna'}</span>
                    ${isAdmin ? `<i class="fas fa-trash-alt" onclick="delBook(${b.id})" style="color:var(--danger);cursor:pointer"></i>` :
            (!busy ? `<button onclick="rent(${b.id})" class="btn-main" style="padding:6px 12px;font-size:0.7rem;width:auto">Zaduži</button>` : '')}
                </div>
            </div>`;
    }).join("");
}

async function fetchHistory() {
    const [lRes, uRes, bRes] = await Promise.all([fetch(`${API_URL}/loans/history`), fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const loans = await lRes.json(); const users = await uRes.json(); const books = await bRes.json();
    const show = isAdmin ? loans : loans.filter(l => l.user_id === currentUser.id);
    document.getElementById("history-table").innerHTML = show.map(l => {
        const u = users.find(user => user.id === l.user_id);
        const b = books.find(book => book.id === l.book_id);
        const status = l.return_date ? `<span class="status-badge tag-free">VRAĆENO</span>` : `<span class="status-badge tag-busy">AKTIVNO</span>`;
        return `<tr><td>${u ? u.name + ' ' + u.lastname : 'Nepoznat'}</td><td>${b ? b.title : 'Nepoznata'}</td><td>${new Date(l.timestamp).toLocaleDateString()}</td><td>${status}</td></tr>`;
    }).reverse().join("");
}

async function fetchLoans() {
    const [lRes, uRes, bRes] = await Promise.all([fetch(`${API_URL}/loans/history`), fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const loans = await lRes.json(); const users = await uRes.json(); const books = await bRes.json();
    const active = loans.filter(l => !l.return_date && (isAdmin || l.user_id === currentUser.id));
    document.getElementById("loan-table").innerHTML = active.map(l => {
        const u = users.find(user => user.id === l.user_id);
        const b = books.find(book => book.id === l.book_id);
        return `<tr><td>${u ? u.name : 'Nepoznat'}</td><td>${b ? b.title : 'Nepoznata'}</td><td>${new Date(l.timestamp).toLocaleDateString()}</td><td style="text-align:right"><button onclick="returnBook(${l.id})" class="btn-main" style="background:var(--danger);width:auto;padding:8px 15px">Vrati</button></td></tr>`;
    }).join("");
}

// --- ACTIONS ---
async function addBook() {
    const fd = new FormData();
    fd.append("title", document.getElementById("b-title").value);
    fd.append("author", document.getElementById("b-author").value);
    fd.append("year", document.getElementById("b-year").value);
    const img = document.getElementById("b-img").files[0];
    if(img) fd.append("image", img);
    await fetch(`${API_URL}/books/`, { method: "POST", body: fd });
    notify("Knjiga dodana"); fetchBooks(); if(isAdmin) updateStats(); document.getElementById("add-box").style.display = 'none';
}

async function rent(id) { await fetch(`${API_URL}/loans/`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({user_id: currentUser.id, book_id: id})}); notify("Zaduženo!"); fetchBooks(); }
async function returnBook(id) { await fetch(`${API_URL}/loans/${id}`, { method: "DELETE" }); notify("Vraćeno!"); fetchLoans(); fetchBooks(); if(isAdmin) updateStats(); }
async function changePass() {
    const fd = new FormData();
    fd.append("old_pw", document.getElementById("s-old").value);
    fd.append("new_pw", document.getElementById("s-new").value);
    const res = await fetch(`${API_URL}/users/${currentUser.id}/change-password`, { method: "PUT", body: fd });
    if(res.ok) notify("Lozinka promijenjena!"); else notify("Stara lozinka netačna", "error");
}

function filterBooks() { const q = document.getElementById("q").value.toLowerCase(); renderBooks(allBooks.filter(b => b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q))); }
function toggleAddBox() { const b = document.getElementById("add-box"); b.style.display = b.style.display === "none" ? "flex" : "none"; }
async function fetchUsers() {
    const res = await fetch(`${API_URL}/users/`); const users = await res.json();
    document.getElementById("user-table").innerHTML = users.map(u => `<tr><td><b>${u.name} ${u.lastname}</b></td><td>${u.email}</td><td><code>${u.membershipId}</code></td><td style="text-align:right"><i class="fas fa-trash-alt" onclick="delUser(${u.id})" style="color:var(--danger);cursor:pointer"></i></td></tr>`).join("");
}
async function showSection(name, btn) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById(name + '-section').style.display = 'block';
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    btn.classList.add('active');
    if(name === 'users') fetchUsers();
    if(name === 'loans') { fetchLoans(); if(isAdmin) fillSelectors(); }
    if(name === 'history') fetchHistory();
    if(name === 'books') fetchBooks();
}
async function fillSelectors() {
    const [uRes, bRes] = await Promise.all([fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const users = await uRes.json(), books = await bRes.json();
    document.getElementById("loanUserSelect").innerHTML = users.map(u => `<option value="${u.id}">${u.name} ${u.lastname}</option>`).join("");
    document.getElementById("loanBookSelect").innerHTML = books.filter(b => !activeLoansIds.includes(b.id)).map(b => `<option value="${b.id}">${b.title}</option>`).join("");
}