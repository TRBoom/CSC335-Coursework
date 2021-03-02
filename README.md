# aplus - SCSU Wishlist

# Instructions for testing 

http://34.66.96.51:8080/index

# Login Credentials

- Student login

  - username: student1@gmail.com

  - password: s


- Faculty login

  - username: imad.antonios@gmail.com

  - password: f


- Admin login

  - username: admin

  - password: a

# Tips

- Use real email accounts for sign up
- Emails may take up to 5 minutes to send
- Emails will likely appear in junk/spam folder
- Recommended faculty lookup: ART 260 01

# Instructions for pull the repository and starting it.

git clone https://github.com/scsu-csc330-fa19/aplus.git

cd aplus

git remote add project https://github.com/scsu-csc330-fa19/aplus.git

export FLASK_APP=routes.py 

export FLASK_DEBUG=1

python3 -m flask run --host=0.0.0.0 --port=8080

