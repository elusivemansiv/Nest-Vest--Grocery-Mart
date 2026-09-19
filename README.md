# Nest Vest : Grocery & Mart — Multi-Vendor Django E-Commerce Platform

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-4.2.2-green.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![PayPal](https://img.shields.io/badge/Payment-PayPal-00457C.svg?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.com/)

**Nest Vest : Grocery & Mart** is a full-featured, modern, and responsive multi-vendor e-commerce web application built using **Django** and **Python**. Designed with an intuitive supermarket and grocery store UI, it provides a seamless shopping experience for customers, a dedicated management dashboard for vendors, and a powerful administrative control panel for store owners.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
  - [Customer Experience](#customer-experience)
  - [Cart & Checkout](#cart--checkout)
  - [Vendor Dashboard & Multi-Vendor Management](#vendor-dashboard--multi-vendor-management)
  - [Site Administration & CMS](#site-administration--cms)
  - [Authentication & User Profiles](#authentication--user-profiles)
- [Technology Stack](#-technology-stack)
  - [Backend](#backend)
  - [Frontend & UI](#frontend--ui)
  - [Database & Storage](#database--storage)
  - [Integrations & Third-Party Packages](#integrations--third-party-packages)
- [Project Directory Structure](#-project-directory-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Environment Variables Configuration](#environment-variables-configuration)
  - [Database Migration & Superuser](#database-migration--superuser)
  - [Running the Application](#running-the-application)
- [Application Portals & URLs](#-application-portals--urls)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Project Overview

**Nest Vest : Grocery & Mart** bridges the gap between buyers and multiple independent vendors. Customers can browse a catalog of organic and supermarket products, filter by price and tags, add items to cart via asynchronous AJAX without page reloads, leave verified reviews, and pay securely via PayPal. Meanwhile, vendors and store managers have their own analytics suite to manage orders, inventory, and track revenues in real time.

---

## ✨ Key Features

### Customer Experience
- **Interactive Storefront**: Homepage with dynamic hero sliders, promotional banners, deals of the day with countdown timers, top-selling, trending, and top-rated product sections.
- **Product Catalog & Details**: Multi-angle image galleries with interactive image zoom (ElevateZoom), rich text product descriptions and specifications, stock tracking, and manufacturer dates.
- **Advanced AJAX Product Filtering**: Real-time filtering by category, vendor, price slider range, and tag system without reloading the page.
- **Search Engine**: Instant product search by query and category matching.
- **Reviews & Ratings**: Five-star rating system and customer feedback with instant AJAX submission.
- **Wishlist**: Quick add-to-wishlist and removal system for registered shoppers.

### Cart & Checkout
- **Asynchronous Cart (AJAX)**: Add products to cart, increment/decrement quantities, and delete items with instant subtotal and tax recalculation.
- **Mini-Cart Dropdown**: Real-time cart overlay accessible from the navigation bar on any page.
- **Address Book**: Save and select multiple shipping addresses, with one-click default address selection.
- **PayPal Payment Gateway**: Integrated PayPal Standard IPN (Instant Payment Notification) workflow with automatic invoice generation and order status updates upon successful transaction.

### Vendor Dashboard & Multi-Vendor Management
- **Vendor Storefronts**: Dedicated public vendor profile pages highlighting vendor contact info, address, return policy, warranty terms, and product collection.
- **Vendor Admin Portal (`/useradmin/`)**:
  - Revenue analytics (total earnings and current month's sales) powered by **Chart.js**.
  - Order overview with customer info and order items.
  - Full product CRUD (Add new product with image uploads, edit prices, descriptions, specifications via CKEditor 5, and delete items).
  - Order status management (update between *Processing*, *Shipped*, and *Delivered*).
  - Store profile customization (logo, banner, return policies, response time).

### Site Administration & CMS
- **Custom Modern Admin Interface**: Styled with **Django Jazzmin** for an elegant, responsive backend admin experience.
- **Dynamic Site Settings (`site_settings` app)**:
  - Configure site title, logos, favicon, and copyright info from the database.
  - Manage homepage sliders, banners, and call-to-action (CTA) blocks.
  - Dynamically build footer columns and links.
  - Manage contact details and social media profile URLs.

### Authentication & User Profiles
- **Custom User Model**: Uses `email` as the primary login identifier instead of username.
- **User Authentication**: Secure user registration, login, logout, and password management.
- **Customer Dashboard**: Track past orders, view invoices, view saved items, and update profile credentials.

---

## 🛠 Technology Stack

### Backend
| Technology | Description |
|---|---|
| **Python** (3.9+) | Primary programming language |
| **Django** (4.2.2) | High-level Python Web framework |
| **Gunicorn** | Production WSGI HTTP server |
| **Asgiref** | ASGI specification implementation |
| **Python-Decouple** | Strict separation of settings from code (environment variables) |
| **ShortUUID** | Compact, URL-friendly unique identifier generation for models |

### Frontend & UI
| Technology | Description |
|---|---|
| **HTML5 / CSS3 / SCSS** | Semantic markup and customized stylesheets |
| **Bootstrap 5 & 4** | Responsive grid system and base UI components |
| **JavaScript (ES6+) & jQuery 3.6** | Client-side scripting and asynchronous DOM manipulation |
| **Chart.js** | Interactive chart visualizations in the vendor dashboard |
| **Slick Slider & Owl Carousel** | Smooth touch-enabled product carousels and hero banners |
| **ElevateZoom** | High-definition product image magnification on hover |
| **FontAwesome 5 & 6 / Material Icons** | Vector icons across storefront and management portals |

### Database & Storage
| Technology | Description |
|---|---|
| **SQLite** | Out-of-the-box local development database (`db.sqlite3`) |
| **PostgreSQL / MySQL** | Fully compatible for staging and production deployments |
| **Pillow (>= 10.0.0)** | Python imaging library for handling media and file uploads |

### Integrations & Third-Party Packages
- **`django-paypal` (2.0)**: PayPal Instant Payment Notification (IPN) integration.
- **`django-ckeditor-5` (0.2.10)**: Modern rich-text WYSIWYG editor for product descriptions and specs.
- **`django-jazzmin` (2.6.0)**: Modern admin interface customization for Django.
- **`django-crispy-forms` & `crispy-bootstrap5`**: Elegant, accessible Bootstrap form rendering.
- **`django-taggit` (3.0.0)**: Tagging support for products and search categorisation.

---

## 📂 Project Directory Structure

```text
Nest-E-commerce-Platform-Using-Django-Source-Code-Files/
├── README.md                      # Project documentation (root)
└── V1-Backend/                    # Main Django project directory
    ├── README.md                  # Project documentation (backend)
    ├── core/                      # Core e-commerce app (Catalog, Cart, Orders, Reviews, Wishlist)
    │   ├── forms.py               # Customer forms (Reviews, etc.)
    │   ├── models.py              # Models: Category, Vendor, Product, CartOrder, Review, etc.
    │   ├── urls.py                # Core routing paths
    │   ├── views.py               # Views for store operations, cart, checkout, and payments
    │   └── context_processor.py   # Global template context (cart, categories, site settings)
    │
    ├── userauths/                 # Authentication app
    │   ├── models.py              # Custom User model, Profile, ContactUs
    │   ├── urls.py                # Auth routes: sign-in, sign-up, sign-out, profile-update
    │   └── views.py               # Auth logic and session handling
    │
    ├── useradmin/                 # Multi-Vendor / Staff Dashboard
    │   ├── forms.py               # Product creation and Vendor settings forms
    │   ├── urls.py                # Dashboard URLs (analytics, products, orders, settings)
    │   └── views.py               # Vendor dashboard metrics, order and product management
    │
    ├── site_settings/             # Dynamic CMS and site configuration
    │   ├── models.py              # Sliders, Banners, CTA, Footer links, Social Links, Site config
    │   └── admin.py               # Admin registry for site customizations
    │
    ├── ecomprj/                   # Project configuration directory
    │   ├── settings.py            # Main Django configuration file
    │   ├── urls.py                # Root URL dispatcher
    │   └── wsgi.py                # WSGI entry point for web servers
    │
    ├── templates/                 # Global Django HTML templates
    │   ├── core/                  # Storefront templates (index, shop, cart, checkout)
    │   ├── userauths/             # Login, register, profile update templates
    │   ├── useradmin/             # Vendor dashboard templates
    │   └── partials/              # Base layout, navbar, headers, and footer components
    │
    ├── static/                    # Static assets (CSS, JS, Fonts, Images)
    │   ├── assets/                # Storefront styles, scripts, and plugin libraries
    │   └── assets2/               # Vendor Dashboard styles and Chart.js scripts
    │
    ├── media/                     # Uploaded user content (product images, vendor logos, etc.)
    ├── .env                       # Environment variables (secret key, debug status, hosts)
    ├── manage.py                  # Django CLI management script
    ├── Procfile                   # Process file for Heroku/PaaS deployment (Gunicorn)
    ├── passenger_wsgi.py          # WSGI configuration for cPanel / shared hosting
    ├── requirements.txt           # Python dependency specifications
    └── runtime.txt                # Target Python runtime version
```

---

## 🚀 Getting Started

Follow these step-by-step instructions to set up and run the project on your local machine.

### Prerequisites
Make sure you have installed:
- **Python 3.9+** ([Download Python](https://www.python.org/downloads/))
- **Git** ([Download Git](https://git-scm.com/))
- **pip** (Python package installer)

---

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/himanshudash132/Nest-E-commerce-Platform-Using-Django-Source-Code-Files.git
cd Nest-E-commerce-Platform-Using-Django-Source-Code-Files/V1-Backend
```

#### 2. Create and Activate a Virtual Environment

- **On Windows (PowerShell / CMD)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```

- **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Environment Variables Configuration

Create a `.env` file inside the `V1-Backend/` directory (or verify the existing one):

```ini
SECRET_KEY=your-secure-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*
```

> **Note**: For production deployments, always set `DEBUG=False` and specify your domain names or server IPs in `ALLOWED_HOSTS`.

---

### Database Migration & Superuser

1. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser (Administrator)**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter an email address, username, and password.

---

### Running the Application

Start the Django local development server:
```bash
python manage.py runserver
```

Once running, access the application in your browser at:
`http://127.0.0.1:8000/`

---

## 🔗 Application Portals & URLs

| Section | URL Pattern | Description |
|---|---|---|
| **Storefront** | `http://127.0.0.1:8000/` | Main shopping portal, categories, deals, & products |
| **Product Catalog** | `http://127.0.0.1:8000/products/` | Filterable product list view |
| **Shopping Cart** | `http://127.0.0.1:8000/cart/` | Cart management page |
| **Wishlist** | `http://127.0.0.1:8000/wishlist/` | Customer saved wishlist items |
| **Customer Dashboard**| `http://127.0.0.1:8000/dashboard/` | Order history and customer profile |
| **Vendor Dashboard** | `http://127.0.0.1:8000/useradmin/` | Vendor management dashboard (products, orders, analytics) |
| **Superuser Admin** | `http://127.0.0.1:8000/admin/` | Django Jazzmin backend administration |
| **Sign In / Sign Up** | `http://127.0.0.1:8000/user/sign-in/` | Customer/Vendor authentication portals |

---

## 🚢 Deployment

The project is pre-configured for multiple hosting environments:

- **Heroku / Render / Railway / PaaS**:
  A `Procfile` is included:
  ```text
  web: gunicorn ecomprj.wsgi --log-file -
  ```
  Specify Python version via `runtime.txt` (default `python-3.9.1`).

- **cPanel / Shared Hosting**:
  A `passenger_wsgi.py` file is included for cPanel Phusion Passenger environments.

- **Static Files Collection**:
  Before hosting on production, collect all static assets:
  ```bash
  python manage.py collectstatic --noinput
  ```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the terms of the **MIT License**.
