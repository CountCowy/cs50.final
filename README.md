Constant's Scanner

https://youtu.be/j8f7Yo8oumQ

A full-stack web application for scanning Latin poetry in dactylic hexameter, combining a custom algorithm with optional OpenAI assistance.
This project is built with Python Flask, Jinja, Bootstrap, Supabase, and deployed on Vercel.

Features:

Latin Scansion Tool

- Uses a home-built algorithm to scan Latin lines in dactylic hexameter

- Provides an assistive OpenAI-powered explanation

- Saves scan history for logged-in users

User Accounts & Security

- User registration and login

- Email verification using Supabase Auth

- Session-based authentication

- Private scan history tied to each user

Contact / Messaging System

- Users can send questions or comments directly through a built-in form

- Messages stored in a Supabase messages table

- RLS policies ensure message security and proper authorization

Database (Supabase)

- User emails, usernames, and passwords

- Scan history storage

- User-submitted messages

- Full Row-Level Security

Frontend

- Responsive UI built with Bootstrap 5

- Templates rendered via Jinja2

- Mobile-friendly navbar

- Clean, minimal layout

Deployment

- Deployed on Vercel (supports serverless Flask via adapter)

- Uses Supabase as the backend database

Project Structure
project/
│
├── app.py
├── requirements.txt
├── README.md
├── pantheon/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── scanned.html
│   ├── instructions.html
│   ├── history.html
│   ├── hitscan.html
│   ├── contact.html
│   ├── apology.html
│   └── layout.html

│
├── static/
│   ├
│   └── favicon.png
│
├── scanner.py          # Custom scansion algorithm
├── JePeux.py           # OpenAI integration
├── labienus.py         # auth helpers (login_required, apology)
└── .env