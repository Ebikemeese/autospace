# 🅿️ Autospace - Smart Parking & Garage Management Platform

Autospace is a modern, full-stack smart parking and garage management application built with **Django**, **TailwindCSS**, **Alpine.js**, and **Leaflet.js**. It provides a comprehensive multi-role web platform for finding, reserving, and managing parking spots, garages, and valet services.

📌 **GitHub Repository**: [https://github.com/Ebikemeese/autospace.git](https://github.com/Ebikemeese/autospace.git)

---

## ✨ Features & Capabilities

### 👥 Multi-Role User Portals
- **Customer Portal**:
  - Filter parking spots by location keyword, vehicle type (`Car`, `Bike`, `Heavy Vehicle`, `Bicycle`), and maximum hourly rate (`$/hr`).
  - Interactive split-screen view with real-time Leaflet map markers and popup details.
  - Instant spot reservation modal with booking history tracking.
- **Manager Portal**:
  - Overview of company fleet garages, valets, and total bookings.
  - **Create Garage Location**: Features an interactive map coordinate picker where clicking anywhere automatically sets latitude (`lat`) and longitude (`lng`).
- **Valet Portal**:
  - Dedicated tabs for **Pickup Trips** and **Return/Drop Trips** with vehicle assignment coordinates.
- **Admin Portal**:
  - Platform garage verification management (**Verify** / **Unlist**).
  - Real-location satellite imagery inspection matching exact garage coordinates.

### 🔢 Pagination & Fetch Limit Selector
- Every page with list data (**Search Results**, **Admin Dashboard**, **Manager Dashboard**, **My Bookings**) includes a dynamic **Fetch Limit** selector:
  - Select items limit per page: `3`, `6`, `12`, `24`, or `50` (**Maximum 50 limit enforced**).
  - Preserves all active search queries and filter parameters (`location`, `type`, `max_price`) across page transitions.

### 🗺️ Dynamic Real-Location Imagery & Maps
- **Interactive Leaflet Maps**: Custom markers, popup cards, and location coordinate picker.
- **Real-Location Satellite & Roadmap Imagery**: Dynamically generated satellite and roadmap snapshots based on `latitude` and `longitude`.
- **Google Maps Integration**: Direct **Open in Google Maps ↗** navigation links (`https://www.google.com/maps/search/?api=1&query={lat},{lng}`).

### 🎨 Modern UI & Experience
- **Single 3D WebGL Background**: Dynamic WebGL 3D car scene with camera animation for auth pages.
- **Interactive Password Visibility**: Eye icon toggles for all password input fields via Alpine.js.
- **Form Action Button Loaders**: Animated SVG spinners and disabled submit button states.
- **User Dropdown Menu**: Header user profile dropdown displaying role badges, portal links, change password, and logout.
- **Legal & Policy Pages**: Privacy Policy, Cookie Policy, Interactive Cookie Preference Settings, and Terms and Conditions.

---

## 🏗️ Domain Models & Database Architecture

The system converts Prisma domain schemas into 14 decoupled Django apps:

| App | Key Models | Description |
|---|---|---|
| `authentication` | `User`, `Admin` | Custom `AbstractUser` with `email` as `USERNAME_FIELD`, `display_name`, `role`, and `uid`. |
| `customers` | `Customer` | Profile model linked to user accounts. |
| `managers` | `Manager` | Manager profile linked to company garage fleets. |
| `valets` | `Valet` | Valet driver profile linked to vehicle assignments. |
| `companies` | `Company` | Corporate owner entity for garages. |
| `garages` | `Garage` | Parking garage entity with descriptions and location images. |
| `addresses` | `Address` | Street address, latitude (`lat`), and longitude (`lng`) coordinates. |
| `slots` | `Slot` | Individual parking slots with type (`CAR`, `BIKE`, `HEAVY`, `BICYCLE`) and hourly rates. |
| `bookings` | `Booking` | Parking reservation with vehicle registration number, time range, and total price. |
| `verification` | `Verification` | Admin verification status (`verified`, `admin`). |
| `valet_assignments` | `ValetAssignment` | Pickup and drop valet assignment tracking. |
| `reviews` | `Review` | Customer star ratings and text comments. |
| `services` | `Service` | Additional garage services (car wash, EV charging, etc.). |
| `booking_timelines` | `BookingTimeline` | Audit logs for booking status changes. |

---

## 🚀 Getting Started & Requirements

### 1. Prerequisites
- Python 3.10+
- Virtualenv

### 2. Installation & Requirements Setup
```bash
# Clone the repository
git clone https://github.com/Ebikemeese/autospace.git
cd autospace

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 3. Database Migration & Seeding
```bash
# Set Django Settings environment variable
$env:DJANGO_SETTINGS_MODULE="autospace.settings"  # On Windows PowerShell

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (Optional)
python manage.py createsuperuser
```

### 4. Running Development Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 👨‍💻 Author & Credits

Developed by **Ebikeme Ese** (2026).
- GitHub Repo: [https://github.com/Ebikemeese/autospace.git](https://github.com/Ebikemeese/autospace.git)
- Portfolio: [ebikemeese.github.io](https://ebikemeese.github.io)
