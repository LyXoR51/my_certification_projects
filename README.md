# my_certification_projects
Jedha fullstack DataScience certification 

# access key
The library Dotenv is used in all my notebooks, but feel free to change it for your own configuration


# M01-Projet-Kayak:
For this project, we need several keys:
- OPENWEATHERMAP_API_KEY, available for free on : https://openweathermap.org/api
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY


# M05-Projet-GetAround:

To build the dockerfile :
docker build . -t getaround

To use it locally : 
docker run -p 8501:8501 -v $(pwd):/app getaround
