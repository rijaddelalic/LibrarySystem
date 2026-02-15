const API_URL = "http://127.0.0.1:8000";
let currentUser = null;
let isAdmin = false;
let allBooks = [];
let activeLoansIds = []; // Ovdje ćemo čuvati ID-eve iznajmljenih knjiga

// --- AUTH LOGIKA ---

function switchAuth(mode) {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');

    if (mode === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        tabLogin.classList.remove('active');
        tabRegister.classList.add('active');
    }
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

            // Prikaz aplikacije
            document.getElementById("auth-screen").style.display = "none";
            document.getElementById("app-screen").style.display = "flex";
            document.getElementById("user-display").innerText = currentUser.name;

            // UI DOZVOLE ZA ADMINA
            if (isAdmin) {
                document.querySelectorAll('.admin-only').forEach(el => el.style.display = "block");
                document.querySelectorAll('.add-form-inline').forEach(el => el.style.display = "flex");
                document.getElementById("admin-stats").style.display = "flex"; // Prikazi statistiku
                updateStats();
            } else {
                document.querySelectorAll('.admin-only').forEach(el => el.style.display = "none");
                document.getElementById("admin-stats").style.display = "none"; // Sakrij statistiku
            }

            fetchBooks(); // Ovo sada automatski provjerava statuse
        } else { alert("Greška pri prijavi!"); }
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
    if(res.ok) { alert("Uspješno! Prijavite se."); switchAuth('login'); }
    else { const e = await res.json(); alert(e.detail); }
}

function showSection(name, btn) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById(name + '-section').style.display = 'block';
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Uvijek osvježi podatke kad mijenjaš tab
    if(name === 'books') fetchBooks();
    if(name === 'users' && isAdmin) fetchUsers();
    if(name === 'loans') { fetchLoans(); fillSelectors(); }
}

// --- LOGIKA ZA KNJIGE (SA STATUSOM) ---

async function fetchBooks() {
    // 1. Povuci knjige
    const booksRes = await fetch(`${API_URL}/books/`);
    allBooks = await booksRes.json();

    // 2. Povuci posudbe da vidimo šta je zauzeto
    const loansRes = await fetch(`${API_URL}/loans/`);
    const loans = await loansRes.json();

    // Napravi listu samo ID-eva knjiga koje su iznajmljene
    activeLoansIds = loans.map(loan => loan.book_id);

    renderBooks(allBooks);
}
function renderBooks(books) {
    const table = document.getElementById("book-table");
    if(!table) return;
    table.innerHTML = "";

    books.forEach(b => {
        const img = b.image_filename ? `${API_URL}/${b.image_filename}` : 'https://via.placeholder.com/40x55?text=No+Cover';
        const isRented = activeLoansIds.includes(b.id);

        let actionContent;

        if (isAdmin) {
            // ADMIN POGLED: Vidi status i kantu za brisanje
            const badge = isRented
                ? `<span class="status-badge status-rented">IZNAJMLJENO</span>`
                : `<span class="status-badge status-available">DOSTUPNO</span>`;

            actionContent = `<div style="display:flex; gap:10px; justify-content:flex-end; align-items:center;">
                 ${badge} <button onclick="deleteBook(${b.id})" class="btn-icon"><i class="fas fa-trash"></i></button>
               </div>`;
        } else {
            // USER POGLED:
            if (isRented) {
                // Ako je iznajmljena, samo piše da nije dostupna
                actionContent = `<span class="status-badge status-rented" style="opacity: 0.7;">NEDOSTUPNO</span>`;
            } else {
                // Ako je slobodna -> DUGME ZA IZNAJMLJIVANJE
                actionContent = `<button onclick="userRentBook(${b.id})" class="btn-primary" style="padding: 6px 15px; font-size: 0.8rem;">
                    <i class="fas fa-plus"></i> Zaduži
                </button>`;
            }
        }

        table.innerHTML += `<tr>
            <td><img src="${img}" class="book-thumb"></td>
            <td><strong>${b.title}</strong></td>
            <td>${b.author}</td>
            <td>${b.year}</td>
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
    fetchBooks();
    if(isAdmin) updateStats();
}

async function deleteBook(id) {
    // Ne daj brisanje ako je iznajmljena
    if (activeLoansIds.includes(id)) {
        alert("Ne možete obrisati knjigu koja je trenutno iznajmljena!");
        return;
    }
    if(confirm("Obrisati?")) {
        await fetch(`${API_URL}/books/${id}`, {method:"DELETE"});
        fetchBooks();
        if(isAdmin) updateStats();
    }
}

// --- KORISNICI ---
async function fetchUsers() {
    const res = await fetch(`${API_URL}/users/`);
    const users = await res.json();
    document.getElementById("user-table").innerHTML = users.map(u => `<tr><td>${u.name} ${u.lastname}</td><td>${u.email}</td><td>${u.membershipId}</td><td class="text-right"><button onclick="deleteUser(${u.id})" class="btn-icon"><i class="fas fa-trash"></i></button></td></tr>`).join("");
}

async function deleteUser(id) { if(confirm("Obrisati korisnika?")) { await fetch(`${API_URL}/users/${id}`, {method:"DELETE"}); fetchUsers(); updateStats(); } }

// --- POSUDBE ---
async function fillSelectors() {
    // Učitaj SAMO dostupne knjige u dropdown za iznajmljivanje
    const bRes = await fetch(`${API_URL}/books/`);
    const books = await bRes.json();
    const lRes = await fetch(`${API_URL}/loans/`);
    const loans = await lRes.json();
    const rentedIds = loans.map(l => l.book_id);

    // Filtriraj: Prikazuj samo one koje NISU u listi iznajmljenih
    const availableBooks = books.filter(b => !rentedIds.includes(b.id));

    document.getElementById("loanBookSelect").innerHTML = availableBooks.length > 0
        ? availableBooks.map(b => `<option value="${b.id}">${b.title}</option>`).join("")
        : `<option disabled>Sve knjige su iznajmljene</option>`;

    const uRes = await fetch(`${API_URL}/users/`);
    const users = await uRes.json();
    document.getElementById("loanUserSelect").innerHTML = users.map(u => `<option value="${u.id}">${u.name} ${u.lastname}</option>`).join("");

    document.getElementById("loanUserSelect").style.display = isAdmin ? "inline-block" : "none";
}

async function addLoan() {
    const uId = isAdmin ? document.getElementById("loanUserSelect").value : currentUser.id;
    const bId = document.getElementById("loanBookSelect").value;

    if(!bId) return alert("Nema dostupne knjige!");

    const res = await fetch(`${API_URL}/loans/`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({user_id: uId, book_id: bId})});
    if(res.ok) {
        alert("Zaduženo!");
        fetchLoans();
        if(isAdmin) updateStats();
    } else {
        const e = await res.json(); alert(e.detail);
    }
}

async function fetchLoans() {
    const res = await fetch(`${API_URL}/loans/`);
    const loans = await res.json();
    const table = document.getElementById("loan-table");
    if(!table) return;

    table.innerHTML = "";

    // Filtriranje: Admin vidi sve, User vidi SAMO SVOJE
    const loansToShow = isAdmin ? loans : loans.filter(l => l.user_id === currentUser.id);

    if (loansToShow.length === 0) {
        table.innerHTML = `<tr><td colspan="3" style="text-align:center; color:#888;">Nemate zaduženih knjiga.</td></tr>`;
        return;
    }

    loansToShow.forEach(l => {
        // I admin i vlasnik knjige mogu kliknuti "Vrati"
        const returnBtn = `<button onclick="deleteLoan(${l.id})" class="btn-danger" style="padding: 5px 10px; font-size: 0.8rem;">
            <i class="fas fa-undo"></i> Vrati knjigu
        </button>`;

        table.innerHTML += `<tr>
            <td>ID Korisnika: ${l.user_id}</td>
            <td>ID Knjige: ${l.book_id}</td>
            <td class="text-right">${returnBtn}</td>
        </tr>`;
    });
}

async function deleteLoan(id) {
    await fetch(`${API_URL}/loans/${id}`, {method:"DELETE"});
    fetchLoans();
    if(isAdmin) updateStats();
}

async function updateStats() {
    try {
        const res = await fetch(`${API_URL}/stats/`);
        const s = await res.json();
        document.getElementById("stat-books").innerText = s.books;
        document.getElementById("stat-users").innerText = s.users;
        document.getElementById("stat-loans").innerText = s.loans;
    } catch(e){}
}
async function userRentBook(bookId) {
    if (!currentUser) return alert("Morate biti prijavljeni!");

    const data = {
        user_id: currentUser.id,
        book_id: parseInt(bookId)
    };

    try {
        const res = await fetch(`${API_URL}/loans/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        if (res.ok) {
            alert("Knjiga uspješno zadužena! Nalazi se u tabu 'Iznajmljivanja'.");
            fetchBooks(); // Osvježi katalog da se knjiga označi kao zauzeta
        } else {
            const err = await res.json();
            alert("Greška: " + err.detail);
        }
    } catch (e) {
        console.error(e);
        alert("Greška na serveru.");
    }
}
