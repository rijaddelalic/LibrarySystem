const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    fetchBooks();
});

// NAVIGACIJA
function showSection(sectionName, btnElement) {
    // Sakrij sve sekcije
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');

    // Prikaži traženu
    document.getElementById(sectionName + '-section').style.display = 'block';

    // Update aktivnog taba
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');

    // Učitaj podatke za tu sekciju
    if (sectionName === 'books') fetchBooks();
    if (sectionName === 'users') fetchUsers();
    if (sectionName === 'loans') {
        fetchLoans();
        prepareLoanSelectors();
    }
}

// LOGIKA ZA KNJIGE
async function fetchBooks() {
    try {
        const res = await fetch(`${API_URL}/books/`);
        const books = await res.json();
        const table = document.getElementById("book-table");
        table.innerHTML = "";
        books.forEach(book => {
            table.innerHTML += `
                <tr>
                    <td><strong>${book.title}</strong></td>
                    <td>${book.author}</td>
                    <td>${book.year}</td>
                    <td style="text-align: right;">
                        <button onclick="deleteBook(${book.id})" class="btn-danger"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { console.error("Greška kod knjiga:", e); }
}

async function addBook() {
    const title = document.getElementById("title").value;
    const author = document.getElementById("author").value;
    const year = document.getElementById("year").value;
    if (!title || !author || !year) return alert("Popuni sva polja!");

    await fetch(`${API_URL}/books/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, author, year: parseInt(year) })
    });
    location.reload(); // Najsigurniji način da se podaci osvježe
}

async function deleteBook(id) {
    if (confirm("Obrisati knjigu?")) {
        await fetch(`${API_URL}/books/${id}`, { method: "DELETE" });
        fetchBooks();
    }
}

// LOGIKA ZA ČLANOVE
async function fetchUsers() {
    try {
        const res = await fetch(`${API_URL}/users/`);
        const users = await res.json();
        const table = document.getElementById("user-table");
        table.innerHTML = "";
        users.forEach(user => {
            table.innerHTML += `
                <tr>
                    <td><strong>${user.name} ${user.lastname}</strong></td>
                    <td>${user.membershipId}</td>
                    <td style="text-align: right;">
                        <button onclick="deleteUser(${user.id})" class="btn-danger"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { console.error("Greška kod korisnika:", e); }
}

async function addUser() {
    const name = document.getElementById("userName").value;
    const lastname = document.getElementById("userLastname").value;
    const mId = document.getElementById("membershipId").value;
    if (!name || !lastname || !mId) return alert("Popuni sva polja!");

    await fetch(`${API_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, lastname, membershipId: mId })
    });
    fetchUsers();
}

async function deleteUser(id) {
    if (confirm("Obrisati člana?")) {
        await fetch(`${API_URL}/users/${id}`, { method: "DELETE" });
        fetchUsers();
    }
}

// LOGIKA ZA IZNAJMLJIVANJA (LOANS)
async function prepareLoanSelectors() {
    // Napuni korisnike
    const userRes = await fetch(`${API_URL}/users/`);
    const users = await userRes.json();
    const userSelect = document.getElementById("loanUserSelect");
    userSelect.innerHTML = '<option value="">Izaberi člana...</option>';
    users.forEach(u => userSelect.innerHTML += `<option value="${u.id}">${u.name} ${u.lastname}</option>`);

    // Napuni knjige
    const bookRes = await fetch(`${API_URL}/books/`);
    const books = await bookRes.json();
    const bookSelect = document.getElementById("loanBookSelect");
    bookSelect.innerHTML = '<option value="">Izaberi knjigu...</option>';
    books.forEach(b => bookSelect.innerHTML += `<option value="${b.id}">${b.title}</option>`);
}

async function fetchLoans() {
    try {
        const res = await fetch(`${API_URL}/loans/`);
        const loans = await res.json();
        const table = document.getElementById("loan-table");
        table.innerHTML = "";
        loans.forEach(loan => {
            table.innerHTML += `
                <tr>
                    <td>Član ID: ${loan.user_id}</td>
                    <td>Knjiga ID: ${loan.book_id}</td>
                    <td style="text-align: right;">
                        <button onclick="deleteLoan(${loan.id})" class="btn-danger">Vrati knjigu</button>
                    </td>
                </tr>`;
        });
    } catch (e) { console.error("Greška kod loans:", e); }
}

async function addLoan() {
    const uId = document.getElementById("loanUserSelect").value;
    const bId = document.getElementById("loanBookSelect").value;
    if (!uId || !bId) return alert("Izaberi člana i knjigu!");

    await fetch(`${API_URL}/loans/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: parseInt(uId), book_id: parseInt(bId) })
    });
    fetchLoans();
}

async function deleteLoan(id) {
    await fetch(`${API_URL}/loans/${id}`, { method: "DELETE" });
    fetchLoans();
}