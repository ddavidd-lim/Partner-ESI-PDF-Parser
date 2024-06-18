# Partner Engineering & Science - ESI Report AI PDF Parser
[![python](https://img.shields.io/badge/Python-3.8-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Description
This project is a capstone project for UCI ICS CS180. This project works with Partner ESI to produce and deliver a system that can parse PDFs with Large Language Models (LLMs) to extract data from ESA Reports.

### Process
The user is able to submit an PDF ESA Report to extract data from. This PDF is converted to text using PyMuPDF and sorted into sections (eg. 1.2.4, 4.1.2). Each section of text is associated with a group of questions that can be seen in BlueLynx. The sections of text are passed as context to the LLM and each question serves as a prompt for the LLM to answer that question to extract the datafield. The sytem collects results and formats them into a JSON file that can be imported into BlueLynx.

## Getting Started
### Environment Setup
- **Clone the Repository**: 
```bash
git clone https://github.com/ddavidd-lim/Partner-ESI-PDF-Parser.git
```
- **Navigate to Project Directory**: 
```bash
cd Partner-ESI-PDF-Parser
```
- **Create a Virtual Environment using Python 3.8**: 
```bash
pip install virtualenv
```
```bash
virtualenv venv --python=3.8
```
- **Activate the Virtual Environment***: 
```bash
.\venv\Scripts\activate
```
- **Download required packages**: 
```bash
pip install -r requirements.txt
```
** Note: On Mac devices, the process to activate a virtual environment is different. **
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Deployment
Change directory to client:
```
cd client
```

### Deploy the frontend:
Install dependencies: ```npm install```

Launch frontend: ```npm start```

### Deploy the backend:
In a separate terminal in the client directory: ```node server.js```

## Contributions and Acknowledgements
**Laura Valko**
* Parsing ground truth results
* Cleaning datafields and questions
* Preprocessing datafields
* Manual Scraping of BlueLynx

**Natalie Perrochon**
* LLM model file fine-tuning
* Iterative prompting of fields using LLM
* Model Memory
* Cleaning results into JSON

**David Lim**
* PDF Parsing
* Organization of text into sections
* LLM model file fine-tuning
* Iterative prompting of fields using LLM
* Sorting JSON results into sections
* Document-wide testing metric
* Integrating backend logic into frontend
* Displaying PDF and JSON in frontend

**Visa Touch**
* Single sentence testing metric
* Hosting frontend on AWS

**Mitsutoshi Sato**
* Frontend file upload
* Frontend CSS
