# DDAM

![Logo](ddam/static/branding/ddam-social-preview.png)

🖼 ➕ 🗃 ➕ ⚖️ **Django Digital Asset Management** (spoken as *da-miŋ*)

*Ever thought about using a spreadsheet to manage the licenses and copyrights of photos? Ditch the spreadsheet and use DDAM:*

A small, focused, feature arm, minimal, web based, work in progress system to link digial assets to licences and track their use.

## 🏆 Features

* Store digial assets. Currently only images (jpg, png, svg, webp etc.) are supported.
* Link licences to assets. 
* Track usage of assets.
* Webbased, Multiuser
* (Optional) Login via LDAP/AD

## 💪 Requirements

* Python 3
* Django 4
* Bootstrap 5
* Parcel

## 🦘 Run

```bash
cp .env.dist .env  # set your environment via .env
npm install && npm run build
pip install --requirement requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## 🐞 Tests

Pull requests welcome.

## ☄ Need help?

For support, please fill an issue or contact [Thomas Breitner via his website](https://thms.de/).
