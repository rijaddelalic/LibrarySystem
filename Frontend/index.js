const API_URL = "http://127.0.0.1:8000";
let currentUser = null;
let isAdmin = false;
let allBooks = [];
let activeLoansIds = [];

// --- TEMA (DARK MODE) ---
function toggleTheme() {
    const isDark = document.body.classList.toggle('dark-theme');
    document.getElementById('theme-icon').className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    document.getElementById('theme-text').innerText = isDark ? 'Light Mode' : 'Dark Mode';
    localStorage.setItem('libro-theme', isDark ? 'dark' : 'light');
}

if(localStorage.getItem('libro-theme') === 'dark') {
    document.body.classList.add('dark-theme');
    document.getElementById('theme-icon').className = 'fas fa-sun';
    document.getElementById('theme-text').innerText = 'Light Mode';
}

// --- AUTH LOGIKA ---
function switchAuth(mode) {
    document.getElementById('login-form').style.display = mode === 'login' ? 'block' : 'none';
    document.getElementById('register-form').style.display = mode === 'register' ? 'block' : 'none';
    document.getElementById('tab-login').className = mode === 'login' ? 'active' : '';
    document.getElementById('tab-register').className = mode === 'register' ? 'active' : '';
}

async function handleLogin() {
    const email = document.getElementById("loginEmail").value;
    const pass = document.getElementById("loginPass").value;
    try {
        const res = await fetch(`${API_URL}/users/login`, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: pass })
        });
        if (res.ok) {
            currentUser = await res.json();
            isAdmin = currentUser.email.endsWith("@libroflow.admin");
            document.getElementById("auth-screen").style.display = "none";
            document.getElementById("app-screen").style.display = "flex";
            document.getElementById("user-display").innerText = currentUser.name;
            document.querySelectorAll('.admin-only').forEach(el => el.style.display = isAdmin ? "flex" : "none");
            if(isAdmin) { document.getElementById("admin-stats").style.display = "flex"; updateStats(); }
            fetchBooks();
        } else { alert("Pogrešni podaci!"); }
    } catch (e) { console.error(e); }
}

async function handleRegister() {
    const data = {
        name: document.getElementById("regName").value,
        lastname: document.getElementById("regLastname").value,
        membershipId: document.getElementById("regMemberId").value,
        email: document.getElementById("regEmail").value,
        password: document.getElementById("regPass").value
    };
    const res = await fetch(`${API_URL}/users/`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(data)});
    if(res.ok) { alert("Sada se prijavite!"); switchAuth('login'); } else { const e = await res.json(); alert(e.detail); }
}

// --- NAVIGACIJA ---
function showSection(name, btn) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById(name + '-section').style.display = 'block';
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    if(name === 'books') fetchBooks();
    if(name === 'users') fetchUsers();
    if(name === 'loans') { fetchLoans(); fillSelectors(); }
    if(name === 'history') fetchHistory();
}

// --- KNJIGE ---
async function fetchBooks() {
    const [bRes, lRes] = await Promise.all([fetch(`${API_URL}/books/`), fetch(`${API_URL}/loans/`)]);
    allBooks = await bRes.json();
    const loans = await lRes.json();
    activeLoansIds = loans.map(l => l.book_id);
    renderBooks(allBooks);
}

function renderBooks(books) {
    const table = document.getElementById("book-table");
    table.innerHTML = "";
    books.forEach(b => {
        const isRented = activeLoansIds.includes(b.id);
        const img = b.image_filename ? `${API_URL}/${b.image_filename}` : 'https://via.placeholder.com/40x58';
        const status = isRented ? '<span class="status-badge status-rented">ZAUZETO</span>' : '<span class="status-badge status-available">SLOBODNO</span>';

        let actionContent = status;
        if (!isAdmin && !isRented) {
            actionContent = `<button onclick="addLoanDirect(${b.id})" class="btn-primary" style="padding:5px 12px; font-size:0.75rem;">Zaduži</button>`;
        } else if (isAdmin) {
            actionContent = `<div style="display:flex; gap:10px; align-items:center; justify-content:flex-end;">${status} <button onclick="deleteBook(${b.id})" class="btn-icon"><i class="fas fa-trash"></i></button></div>`;
        }

        table.innerHTML += `<tr>
            <td><img src="${img}" class="book-thumb"></td>
            <td><strong>${b.title}</strong></td><td>${b.author}</td><td>${b.year}</td>
            <td class="text-right">${actionContent}</td>
        </tr>`;
    });
}

function filterBooks() {
    const term = document.getElementById("searchInput").value.toLowerCase();
    renderBooks(allBooks.filter(b => b.title.toLowerCase().includes(term) || b.author.toLowerCase().includes(term)));
}

async function addBook() {
    const fd = new FormData();
    fd.append("title", document.getElementById("title").value);
    fd.append("author", document.getElementById("author").value);
    fd.append("year", document.getElementById("year").value);
    const img = document.getElementById("bookImage").files[0];
    if(img) fd.append("image", img);
    await fetch(`${API_URL}/books/`, {method:"POST", body:fd});
    fetchBooks(); updateStats();
}

async function deleteBook(id) {
    if(confirm("Obrisati knjigu?")) { await fetch(`${API_URL}/books/${id}/`, {method:"DELETE"}); fetchBooks(); updateStats(); }
}

// --- LOANS & HISTORY ---
async function fetchLoans() {
    const [lRes, uRes, bRes] = await Promise.all([fetch(`${API_URL}/loans/`), fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const loans = await lRes.json(); const users = await uRes.json(); const books = await bRes.json();
    const table = document.getElementById("loan-table");
    table.innerHTML = "";

    const show = isAdmin ? loans : loans.filter(l => l.user_id === currentUser.id);
    show.forEach(l => {
        const u = users.find(user => user.id === l.user_id);
        const b = books.find(book => book.id === l.book_id);
        table.innerHTML += `<tr>
            <td>${u ? u.name : 'Nepoznat'}</td>
            <td>${b ? b.title : 'Nepoznata'}</td>
            <td class="text-right"><button onclick="deleteLoan(${l.id})" class="btn-primary" style="background:var(--danger)">Vrati</button></td>
        </tr>`;
    });
}

async function addLoan() {
    const uId = isAdmin ? document.getElementById("loanUserSelect").value : currentUser.id;
    const bId = document.getElementById("loanBookSelect").value;
    await fetch(`${API_URL}/loans/`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({user_id: uId, book_id: bId})});
    fetchLoans(); updateStats();
}

async function addLoanDirect(bookId) {
    await fetch(`${API_URL}/loans/`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({user_id: currentUser.id, book_id: bookId})});
    fetchBooks(); updateStats(); alert("Zaduženo!");
}

async function deleteLoan(id) { await fetch(`${API_URL}/loans/${id}`, {method:"DELETE"}); fetchLoans(); fetchBooks(); updateStats(); }

async function fetchHistory() {
    const [lRes, uRes, bRes] = await Promise.all([fetch(`${API_URL}/loans/`), fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const loans = await lRes.json(); const users = await uRes.json(); const books = await bRes.json();
    const table = document.getElementById("history-table");
    table.innerHTML = loans.map(l => {
        const u = users.find(user => user.id === l.user_id);
        const b = books.find(book => book.id === l.book_id);
        return `<tr>
            <td>${u ? u.name + ' ' + u.lastname : 'ID:' + l.user_id}</td>
            <td>${b ? b.title : 'ID:' + l.book_id}</td>
            <td>${new Date(l.timestamp).toLocaleDateString()}</td>
            <td class="text-right"><span class="status-badge ${l.return_date ? 'status-available' : 'status-rented'}">${l.return_date ? 'VRAĆENO' : 'AKTIVNO'}</span></td>
        </tr>`;
    }).join("");
}

// --- OSTALO ---
async function fetchUsers() {
    const res = await fetch(`${API_URL}/users/`); const users = await res.json();
    document.getElementById("user-table").innerHTML = users.map(u => `<tr><td>${u.name} ${u.lastname}</td><td>${u.email}</td><td>${u.membershipId}</td><td class="text-right"><button onclick="deleteUser(${u.id})" class="btn-icon"><i class="fas fa-trash"></i></button></td></tr>`).join("");
}

async function deleteUser(id) { if(confirm("Obriši korisnika?")) { await fetch(`${API_URL}/users/${id}`, {method:"DELETE"}); fetchUsers(); updateStats(); } }

async function fillSelectors() {
    const [uRes, bRes] = await Promise.all([fetch(`${API_URL}/users/`), fetch(`${API_URL}/books/`)]);
    const users = await uRes.json(); const books = await bRes.json();
    document.getElementById("loanUserSelect").innerHTML = users.map(u => `<option value="${u.id}">${u.name} ${u.lastname}</option>`).join("");
    document.getElementById("loanBookSelect").innerHTML = books.filter(b => !activeLoansIds.includes(b.id)).map(b => `<option value="${b.id}">${b.title}</option>`).join("");
}

async function updateStats() {
    try { const res = await fetch(`${API_URL}/stats/`); const s = await res.json();
        document.getElementById("stat-books").innerText = s.books; document.getElementById("stat-users").innerText = s.users; document.getElementById("stat-loans").innerText = s.loans; } catch(e){}
}