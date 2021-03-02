# aplus - SCSU Wishlist
This is a course project from 2019. None of it is supported online anymore, but the code is still functional and can be deployed via google cloud infrastructure. The original intent of the project was to create a course wish list or waiting list for students who wanted to get into full courses. The website was fully functional and was well recieved. My only issue with it is that it did not include enough data sanitation. 

My role in the project was project leader, github coordinator, project design, and python programmer. I worked with 4 other people on this project, all of whom I would work with again. 
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

