
<img width="598" alt="Screen Shot 2022-04-21 at 2 19 52 AM" src="https://user-images.githubusercontent.com/25335878/164423199-51c7fa82-82af-4ac0-9c3e-04c046066edb.png">

Data Storage:

For college data, we have set up a cloud database using Cloud Firestore to manage and store our data. Firestore allows us to take advantage of its simplicity and efficiency to manage and query our application data.
The city data is accessible through an API and will query the data on demand, therefore, we do not need any storage for it.

Backend development:

Our backend component consists of a web service developed in Flask (Python Framework) to handle data communication between our user interface and data sources. The webservice is intended to fetch and transform the data before sending it to the frontend for display.

Frontend Design:

We have completed our user interface. We decided to use Streamlit Framework to develop and design our user interface to capitalize on simplicity and the abundance of python libraries we can use in handling the data.

Machine Learning:

We worked on the college recommendation by a ML model. We used the Scikit-learn package to conduct unsupervised learning and cluster out colleges by their standard exam scores (SAT and ACT) and their acceptance rate.
