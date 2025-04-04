# Table of Contents

- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Problem Description](#problem-description)
- [Proposed solution](#proposed-solution)
- [System diagram](#system-diagram)
- [Video demo](#video-demo)
- [Installation](#installation)
- [Environment Variables](#environment-variables)

# Introduction
- **Winner💫** of the First Kenyare AI4I Hackathon
- KBS AI bot that automates Kenyare's PI facultative underwriting

# Problem Description

The current process of handling Professional Indemnity Insurance (PII) quotation requests is largely manual, involving the analysis of proposal forms and associated documents. This approach is time-consuming and labor-intensive, resulting in significant delays in the submission of quotes to our business partners. Presently, we rely on an Excel template for data entry and quote generation, which not only increases the likelihood of errors but also hampers efficiency and responsiveness.

As the insurance industry evolves and the demand for timely and accurate quotes grows, our manual processes are becoming a bottleneck. The inability to quickly analyze and process requests undermines our operational effectiveness and customer satisfaction. To maintain our competitive edge and ensure optimal service delivery, there is an urgent need to automate the reinsurance underwriting quotation process. This transition aims to enhance efficiency, accuracy, and overall value for our business partners, ultimately driving better outcomes for all stakeholders involved.

# Proposed solution

The proposed solution is an AI-powered bot designed to automate the processing of Professional Indemnity Insurance (PII) quotation requests. This bot will autonomously handle the majority of the process, minimizing the need for manual input and significantly reducing time delays.

# System diagram

![System schema](https://github.com/SenZmaKi/Kenyare/blob/master/docs/schema.png)

# Video demo

https://github.com/user-attachments/assets/f03b57d6-a5b2-4c38-9d59-d19778864a8f

# Installation

- Clone the repository using [Git](https://github.com/git-guides/install-git)

  ```bash
  git clone https://github.com/SenZmaKi/Kenyare.git
  cd Kenyare
  ```

- Install Poppler 24.08.0 or higher and add it to PATH

  - Linux/Mac

    - Install Poppler using your package manager

  - Windows
    - Download Poppler from [this link](https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip)
    - Extract the downloaded file
    - Add the bin folder `Release-24.08.0-0\poppler-24.08.0\Library\bin\` to PATH

- Install [Python 3.12.4](https://www.python.org/downloads/release/python-3124/) or higher then run

  - Create virtual environment
    ```bash
    python -m venv .venv
    ```
  - Activate virtual environment

    - Linux/Mac
      ```bash
      source .venv/bin/activate
      ```
    - Windows

      ```bash
      .venv\Scripts\activate
      ```

  - Install dependencies
    ```bash
    pip install -r kenyare/requirements.txt
    ```
  - Run the backend api server

    ```bash
    python -m kenyare.server
    ```

    By default the server will run on port `5000`. You can change the port by setting the `FLASK_PORT` environment variable.
    By default the server will run on host `127.0.0.1`. You can change the host by setting the `FLASK_HOST` environment variable.

- Install [Node.js 22.9.0](https://nodejs.org/en/download/package-manager) or higher then run

  - Install dependencies

    ```bash
    npm install
    ```

  - Run the frontend server

    - Development

      ```bash
      npm run dev
      ```

      Navigate to [localhost:5173](http://127.0.0.1:5173) on your browser. You can change the port and host by setting the `VITE_DEV_PORT` and `VITE_DEV_HOST` environment variables.

    - Production

      ```bash
      npm run build
      npm run preview
      ```

      Navigate to [localhost:4173](http://127.0.0.1:4173) on your browser. You can change the port and host by setting the `VITE_PROD_PORT` and `VITE_PROD_PORT` environment variables.

    By default the frontend server will make backend api requests to [localhost:5000](http://127.0.0.1:5000) set the `FLASK_PORT` and `FLASK_HOST` environment variables to change the port and host.

# Environment Variables

- Create a `.env` in the root project directory. The environment variables will be automatically loaded.

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxx # Required
FLASK_PORT=5000
FLASK_HOST=127.0.0.1
FLASK_DEBUG=1 # Set to 0 to disable flask debug mode
VITE_DEV_HOST=127.0.0.1
VITE_DEV_PORT=5173
VITE_PROD_HOST=127.0.0.1
VITE_PROD_PORT=4173
CLEAR_UPLOADS_DIR=0 # Set to 1 to clear upload directory on first quotation input run
CLEAR_QUOTATATIONS_DIR=0 # Set to 1 to clear quotations directory on backend server start
DELETE_UPLOADS=0 # Set to 1 to delete uploaded files after extracting quotation input
```
