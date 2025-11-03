# 📘 Asset Ally

**Asset Ally** is a Chromebook & device management app built for schools to track devices, students, and staff.  
It allows authorized users to assign, return, and monitor device checkouts with accountability.

---

## 🚀 Live Demo
🔗 [Deployed on Render](https://asset-ally.onrender.com)  
🔗 [GitHub Repo](https://github.com/davolajohnson/Asset--Ally-App)

---

## 💡 Inspiration
Managing hundreds of Chromebooks for students and teachers can be a logistical challenge.  
Asset Ally simplifies this process — making it easy to assign, track, and report on school technology assets.

---

## 🧠 Features
✅ User authentication (login/logout)  
✅ Device CRUD (create, read, update, delete)  
✅ Owner-only permissions — only the creator can edit/delete  
✅ Track Students, Staff, and Checkouts  
✅ Enforce one active checkout per device  
✅ Django Admin for backend control  
✅ PostgreSQL integration for deployment  
✅ Accessible, consistent UI with Flexbox/Grid  

---

## 🧩 Models Overview
| Model | Description |
|-------|--------------|
| **Device** | Represents Chromebooks or other devices |
| **Student** | Student borrowers (grade, guardian info) |
| **Staff** | Staff borrowers or approvers |
| **Checkout** | Tracks device checkouts & returns |
| **User (Auth)** | Built-in Django user linked to created devices |

---

## 🖼️ Screenshot
*(Add your screenshot once deployed)*
![App Screenshot](docs/screenshot.png)

---

## ⚙️ Tech Stack
- **Backend:** Django 5.2  
- **Database:** PostgreSQL  
- **Frontend:** Django Templates + CSS (Flex/Grid)  
- **Auth:** Django session-based login/logout  
- **Deployment:** Render (via `render.yaml`)  
- **Env Management:** python-dotenv  

---

## 🧭 Getting Started (Local Development)

### 1️⃣ Clone & Install
```bash
git clone https://github.com/davolajohnson/Asset--Ally-App.git
cd Asset--Ally-App
pip install -r requirements.txt


