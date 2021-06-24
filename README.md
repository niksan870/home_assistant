<p align="center">
  <h3 align="center">Flask Home Assistant</h3>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The purpose of this web app is to ease our daily life by easily accessing and manipualting the state of different electrical devies around and in your home. It has a simple and intuitive UI, which leads to the betterment of the user.

### Built With

The main frameworks I've chosen for the project are as follows.
* [Bootstrap](https://getbootstrap.com)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)


<!-- GETTING STARTED -->
## Getting Started

In order to run the project in your local machine you would need several libraries, wich are located in the requirements.txt

### Prerequisites

Before intalling the libraries you should have pip already installed

* pip

### Installation

1. Clone the repo
 ```sh
   git clone https://github.com/niksan870/home_assistant.git
   ```
2. Create a virtual environment 
3. Install packages from requirements.txt
```sh
   pip install -r requirements.txt
   ```
4. Initialize the flask app and set the app to a development state (optional)
```
   export FLASK_APP=__init__
   export FLASK_ENV=development
   ```
5. Run the flask app with the following command
```
   flask run
   ```
