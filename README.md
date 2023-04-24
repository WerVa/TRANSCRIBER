# TRANSCRIBER

Python and Flask application focused on building a platform to analyze and transcribe any Audio File uploaded to the website.

This application take an Audio File as input in Flask to create both a GET and POST request on the same route and finally render the transcribed results of the speech file to the user.

Update Docker 

How to run: 
> docker build --tag transcriber .  

> docker run --publish 80:5000 transcriber 