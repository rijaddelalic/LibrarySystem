# 📚 LibroFlow 

LibroFlow is a modern, secure, and visually stunning full-stack library management application. It provides a comprehensive solution for managing book inventories, member registrations, and loan tracking with an integrated history archive.



## ✨ Key Features

- **🔐 Secure Authentication**: Full registration and login system featuring **Bcrypt** password hashing for enterprise-grade security.
- **👨‍💼 Role-Based Access Control (RBAC)**: The system automatically detects user roles (Admin vs. User) based on the email domain provided during registration.
- **🖼️ Visual Inventory**: Support for real-time image uploads for both book covers and user profile avatars.
- **🔍 Live Search & Filtering**: Instant search functionality to filter the book catalog by title or author.
- **🔄 Smart Loan Management**: A streamlined process for borrowing and returning books with automatic status updates (Available/Rented).
- **📂 Global History Archive**: A permanent log of all transactions. Admins can monitor the entire library's history, while users have access to their personal reading logs.
- **🌓 Dynamic UI**: A premium Dashboard design featuring a sleek Sidebar and a **Dark/Light Mode** toggle saved in local storage.
- **📊 Admin Analytics**: Real-time statistics displayed on the admin dashboard (Total Books, Members, and Active Loans).

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI (Asynchronous API), SQLAlchemy (ORM), Bcrypt (Security), SQLite (Database).
- **Frontend**: HTML5, CSS3 (Custom Modern UI), Vanilla JavaScript (Fetch API, DOM Manipulation).
- **Icons**: FontAwesome 6.5.
- **Avatars**: Integrated UI-Avatars for users without profile pictures.

## ⚙️ Installation & Setup

### 1. Backend Setup
1. Navigate to the Backend directory:
   ```bash
   cd Backend
Install the required Python dependencies:
code
Bash
pip install -r ../requirements.txt
Start the FastAPI server:
code
Bash
python -m uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000
2. Frontend Setup
Simply open Frontend/index.html in any modern web browser (Chrome, Firefox, Edge).
🔑 Testing Credentials (Roles)
The application assigns permissions based on the email address used during registration:
ADMIN ACCESS: Use an email ending with @libroflow.admin (e.g., admin@libroflow.admin).
Capabilities: Add/Delete books, Manage members, View global statistics, View full history.
USER ACCESS: Use any standard email address.
Capabilities: Browse catalog, Rent books, View personal loan history, Update password.
