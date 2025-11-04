# 📘 Asset Ally

**Asset Ally** is a Chromebook & device management app built for schools to track devices, students, and staff.  
It allows authorized users to assign, return, and monitor device checkouts with accountability.

---

## 🚀 Live Demo
🔗 [Deployed on Render](https://asset-ally.onrender.com)  
🔗 [GitHub Repo](https://github.com/davolajohnson/Asset--Ally-App)

---

## 💡 Inspiration
Managing hundreds of Chromebooks for students and teachers has been a logistical challenge.  
Asset Ally simplifies this process — making it easy to assign, track, and report on school technology assets.

---

## 🧠 Features

✅  Dashboard Overview
✅  Displays total students, available devices, and            checked-out devices
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

## 📸 Screenshot
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

 Future Enhancements
 Email notifications for upcoming due dates
 Barcode scanning for asset tags
 Bulk CSV import/export for students and devices
 Role-based admin/staff permissions

Developed by:
Davola Stagg-Johnson
🎓 Software Engineering Student @ General Assembly
📍 Houston, TX
📧 Email davolastagg@gmail.com
🔗 GitHub: davolajohnson