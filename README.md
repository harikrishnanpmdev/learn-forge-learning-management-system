# LearnForge | Learning Management System

A full-stack **Learning Management System (LMS)** built with **Python and Django**, designed to provide a complete online learning experience for students and instructors.

LearnForge allows students to discover and enroll in courses, purchase courses through Razorpay, access structured lessons, track learning progress, take quizzes, and earn certificates. Instructors can create and manage courses, curriculum, lessons, quizzes, questions, and options through dedicated instructor dashboards.

---

## 📌 Overview

**LearnForge** is a web-based Learning Management System developed using Django.

The application provides separate workflows for **students and instructors**, with role-based access to learning and course-management features.

### Students can

* Register and verify their account using OTP
* Browse and search courses
* View detailed course information
* Add courses to cart
* Purchase courses using Razorpay
* Access enrolled courses
* Complete lessons
* Track course progress
* Take quizzes
* View quiz results
* Earn certificates
* Manage enrolled courses and certificates

### Instructors can

* Create and manage courses
* Add course descriptions
* Define learning points and requirements
* Manage curriculum
* Create chapters and lessons
* Create and manage quizzes
* Add questions and answer options
* Set correct answers
* Manage course content through an instructor dashboard

---

# ✨ Features

## 👤 User Authentication

* Custom Django user model
* Student and instructor registration
* Login and logout
* OTP verification
* Password reset functionality
* Role-based authentication
* Login protection for restricted pages
* Instructor and student-specific dashboards

---

## 📚 Course Management

* Course categories
* Course listing
* Course details
* Course descriptions
* Learning points
* Course requirements
* Course tags
* Course level
* Course language
* Course duration
* Course pricing
* Instructor information
* Course ratings and reviews
* Instructor course management

---

## 🎓 Learning Management

* Structured course curriculum
* Chapters and sections
* Lessons
* Lesson ordering
* Lesson completion tracking
* Course progress tracking
* Enrolled course dashboard
* Student learning interface
* Resume learning functionality

---

## 🛒 Cart & Enrollment

* Add courses to cart
* Remove courses from cart
* Cart management
* Dynamic cart totals
* Course enrollment
* Prevention of duplicate enrollment
* Student-only purchasing restrictions
* Automatic enrollment after successful payment

---

## 💳 Razorpay Payment Integration

LearnForge integrates **Razorpay** for online course payments.

The payment workflow includes:

1. Course selection
2. Add course to cart
3. Checkout
4. Razorpay order creation
5. Razorpay payment
6. Payment verification
7. Order status update
8. Course enrollment
9. Cart cleanup

### Security

Razorpay credentials are **not stored directly in the source code**.

They are loaded using environment variables:

```env
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

---

## 📝 Quiz Management

### Instructor Features

* Create quizzes
* Edit quizzes
* Delete quizzes
* Activate/deactivate quizzes
* Set quiz duration
* Set passing percentage
* Manage questions
* Add multiple options
* Edit options
* Delete options
* Configure correct answers

### Student Features

* Attempt quizzes
* Time-limited quizzes
* Automatic score calculation
* Percentage calculation
* Pass/fail evaluation
* Quiz result display
* Quiz attempt tracking

---

## 🏆 Certificate System

Students who successfully complete the required course and quiz conditions can receive certificates.

Certificate functionality includes:

* Certificate generation
* Unique certificate ID
* Issue date
* Certificate details
* Certificate dashboard
* Certificate PDF generation/download

---

## 🔎 Course Search

The search functionality allows users to find courses based on different course attributes.

Search can be performed using:

* Course title
* Category
* Language
* Level
* Tags
* Instructor name

---

## 📊 Student Dashboard

The student dashboard provides an overview of the learner's activity.

It includes:

* Enrolled courses
* Course progress
* Completed lessons
* Quiz attempts
* Quiz scores
* Certificates
* Learning statistics

---

## 👨‍🏫 Instructor Dashboard

The instructor dashboard provides tools for managing educational content.

It includes:

* Instructor profile
* Course management
* Course creation
* Course editing
* Curriculum management
* Lesson management
* Quiz management
* Question management
* Option management
* Course statistics

---

# 🛠️ Tech Stack

| Technology          | Usage                           |
| ------------------- | ------------------------------- |
| Python              | Backend programming             |
| Django 6.0.5        | Web framework                   |
| SQLite              | Database                        |
| HTML5               | Frontend structure              |
| CSS3                | Styling                         |
| JavaScript          | Client-side functionality       |
| Bootstrap 5         | Responsive UI                   |
| Django Crispy Forms | Form rendering                  |
| Crispy Bootstrap 5  | Bootstrap form integration      |
| Razorpay            | Payment gateway                 |
| python-dotenv       | Environment variable management |
| Git                 | Version control                 |
| GitHub              | Source code hosting             |

---

# 🏗️ Project Structure

```text
LMS/
│
├── LMS/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── cart/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── search/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── student_dashboard.html
│   ├── instructor_dashboard.html
│   ├── course_learning.html
│   ├── quiz.html
│   ├── quiz_result.html
│   ├── manage_quiz.html
│   ├── create_quiz.html
│   ├── manage_questions.html
│   ├── manage_options.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── includes/
│
├── manage.py
├── .gitignore
└── README.md
```

---

# 📦 Django Applications

## `accounts`

Responsible for:

* User authentication
* User roles
* Categories
* Courses
* Instructors
* Course content
* Curriculum
* Reviews
* Quizzes
* Questions
* Options
* Quiz attempts

### Main Models

```text
CustomUser
Category
Instructor
Course
LearnPoint
Requirement
Tag
Section
ChapterTopics
Review
Quiz
Question
Option
QuizAttempt
```

---

## `cart`

Responsible for:

* Shopping cart
* Orders
* Payments
* Course enrollment
* Lessons
* Lesson completion
* Certificates

### Main Models

```text
Cart
Order
OrderItem
Enrollment
Lesson
LessonCompletion
Certificate
```

---

## `search`

Responsible for:

* Course search
* Filtering courses using Django ORM queries
* Searching across multiple course-related fields

---

# 🗄️ Database Models

The application uses Django ORM with SQLite during development.

### User & Course Management

```text
CustomUser
    │
    ├── Instructor
    │
    └── Course
           │
           ├── Category
           ├── Tag
           ├── LearnPoint
           ├── Requirement
           ├── Section
           ├── Review
           └── Quiz
```

### Learning & Assessment

```text
Course
   │
   ├── Section
   │     └── Lessons
   │
   └── Quiz
         │
         ├── Questions
         │     └── Options
         │
         └── QuizAttempt
```

### Shopping & Enrollment

```text
User
 │
 ├── Cart
 │
 ├── Order
 │     └── OrderItem
 │
 └── Enrollment
        │
        ├── LessonCompletion
        └── Certificate
```

---

# 🔄 Application Workflows

## Student Workflow

```text
Register
   ↓
OTP Verification
   ↓
Login
   ↓
Browse Courses
   ↓
View Course Details
   ↓
Add Course to Cart
   ↓
Checkout
   ↓
Razorpay Payment
   ↓
Payment Verification
   ↓
Course Enrollment
   ↓
Start Learning
   ↓
Complete Lessons
   ↓
Take Quiz
   ↓
View Result
   ↓
Earn Certificate
```

---

## Instructor Workflow

```text
Register / Login
       ↓
Instructor Dashboard
       ↓
Create Course
       ↓
Add Course Details
       ↓
Add Learning Points
       ↓
Add Requirements
       ↓
Create Curriculum
       ↓
Add Lessons
       ↓
Create Quiz
       ↓
Add Questions
       ↓
Add Options
       ↓
Set Correct Answers
       ↓
Manage Course
```

---

# 💰 Payment Workflow

```text
Course
  ↓
Add to Cart
  ↓
Checkout
  ↓
Create Razorpay Order
  ↓
Razorpay Checkout
  ↓
Payment
  ↓
Signature Verification
  ↓
Update Order
  ↓
Create Order Items
  ↓
Create Enrollment
  ↓
Clear Cart
```

---

# 📝 Quiz Workflow

### Instructor

```text
Instructor
    ↓
Create Quiz
    ↓
Set Time Limit
    ↓
Set Passing Percentage
    ↓
Add Questions
    ↓
Add Options
    ↓
Set Correct Answer
    ↓
Publish / Activate Quiz
```

### Student

```text
Student
   ↓
Open Course
   ↓
Start Quiz
   ↓
Answer Questions
   ↓
Submit Quiz
   ↓
Calculate Score
   ↓
Calculate Percentage
   ↓
Pass / Fail
   ↓
Store Quiz Attempt
```

---

# 📌 Main Routes

| Route                   | Purpose                  |
| ----------------------- | ------------------------ |
| `/`                     | Home / course categories |
| `/register`             | User registration        |
| `/login`                | User login               |
| `/logout`               | User logout              |
| `/adminhome`            | Admin dashboard          |
| `/userhome`             | User home                |
| `/products/<id>`        | Course/product listing   |
| `/productdetail/<id>`   | Course/product details   |
| `/addcategory`          | Add category             |
| `/addproduct`           | Add course/product       |
| `/cart/addtocart/<id>`  | Add course to cart       |
| `/cart/cartview`        | View cart                |
| `/cart/cartremove/<id>` | Remove cart quantity     |
| `/cart/cartdelete/<id>` | Delete cart item         |
| `/cart/checkout`        | Checkout                 |
| `/cart/success`         | Payment success          |
| `/cart/myorder`         | View orders              |
| `/search/`              | Search courses           |

> Routes may evolve as new application features are added.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/harikrishnanpmdev/learn-forge-learning-management-system.git
```

## 2. Navigate to the Project

```bash
cd learn-forge-learning-management-system
```

## 3. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependencies

If `requirements.txt` is available:

```bash
python -m pip install -r requirements.txt
```

If dependencies need to be installed individually:

```bash
python -m pip install django
python -m pip install django-crispy-forms
python -m pip install crispy-bootstrap5
python -m pip install razorpay
python -m pip install python-dotenv
```

---

## 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password
```

**Never commit `.env` to GitHub.**

---

## 6. Apply Migrations

```bash
python manage.py migrate
```

---

## 7. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

---

## 8. Run the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Security

Sensitive information is managed using environment variables.

The following are **not stored directly in the source code**:

* Django `SECRET_KEY`
* Razorpay Key ID
* Razorpay Secret
* Email password

The `.gitignore` file excludes:

```text
.env
db.sqlite3
.venv/
__pycache__/
*.pyc
media/
staticfiles/
.idea/
.vscode/
```

Before deployment, configure:

```python
DEBUG = False
```

and configure production:

* `ALLOWED_HOSTS`
* HTTPS
* Secure cookies
* CSRF settings
* Production database
* Proper environment variables

---

# 🧪 Testing & Validation

Django configuration can be checked using:

```bash
python manage.py check
```

Expected result:

```text
System check identified no issues (0 silenced).
```

Database migrations can be checked using:

```bash
python manage.py showmigrations
```

---

# 🖥️ Frontend

The frontend uses:

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Django Template Language
* Crispy Forms

The interface includes responsive pages for:

* Authentication
* Course browsing
* Course details
* Cart
* Checkout
* Student dashboard
* Instructor dashboard
* Course learning
* Quiz management
* Quiz attempts
* Quiz results
* Certificates

---

# 📁 Static & Media Files

## Static Files

Static assets include:

```text
static/
├── css/
├── js/
├── images/
└── includes/
```

## Media Files

User-uploaded content is stored in:

```text
media/
```

The `media/` directory is excluded from Git.

---

# 🚀 Future Improvements

Possible future enhancements:

* Instructor analytics
* Advanced student analytics
* Course wishlist
* Course reviews and ratings improvements
* Payment webhooks
* Email notifications
* Certificate verification
* REST API
* PostgreSQL support
* Cloud media storage
* Production deployment
* CI/CD integration
* Automated test coverage
* Mobile application

---

# 📄 License

This project is currently developed as a **learning and portfolio project**.

A formal open-source license can be added in the future if the project is distributed publicly under specific licensing terms.

---

# 👨‍💻 Author

**HARIKRISHNAN P M**

Python Full Stack Developer

GitHub:
https://github.com/harikrishnanpmdev

---

# 🔗 Repository

**LearnForge — Learning Management System**

https://github.com/harikrishnanpmdev/learn-forge-learning-management-system
