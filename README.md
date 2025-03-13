# IT AE2 - Happy Shopping Web Application

## Project Description

This is a **group assignment** for the IT course **AE2**, implementing a **full-stack web application** for a company **employee login and welfare purchasing system**, developed using **Django**. 

The platform allows employees to **log in**, browse available **welfare products**, add items to their **shopping cart**, and place **orders**. This application demonstrates end-to-end functionality including backend management, frontend rendering, and database integration.

---

## Features

- ✅ Employee registration and **login system**
- ✅ **Product browsing** with detailed product pages and image display
- ✅ **Product variants** (e.g., color, size) dynamically selectable
- ✅ **Shopping cart** with quantity updates and removal
- ✅ **Order creation and management**
- ✅ Admin backend for managing products and orders (via Django admin panel)

---

## Technologies Used

- **Backend Framework**: Django 2.1.5 (Python 3.8)
- **Database**: MySQL (accessed via PyMySQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Handling**: Media files served through Django
- **Deployment Option**: Compatible with PythonAnywhere or local server

---

## Live Demo

You can visit the deployed version of this project here:  
**https://max402.pythonanywhere.com/**

## How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/hhx-gtx/IT-AE2-Happy-Shopping.git
cd IT-AE2-Happy-Shopping
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3.Install Dependencies

```bash
pip install -r requirements.txt
```

### 4.Apply Migrations
```bash
python manage.py migrate
```

### 5.Insert Initial Product Data

```bash
python manage.py shell
>>> exec(open('scripts/insert_products.py').read())
```

### 6.Run Development Server
```bash
python manage.py runserver
```

## Account for Login
| Username | Password | Name  |
|----------|----------|-------|
| Jack111  | Jack111  | Jack111 |

## Note on Media Files

Product images are included under /media/products/ and auto-linked when running the product insertion script.

## Requirements
 - Django==2.1.5
 - PyMySQL
 - Pillow
 - pytz

## Authors
 - Haoxuan Huang and Group 111 teams members(IT AE2 Assignment)
