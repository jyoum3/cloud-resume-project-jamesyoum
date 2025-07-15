# James Youm's Cloud Resume Project

This project demonstrates a comprehensive understanding of cloud infrastructure, serverless architecture, and CI/CD pipelines by deploying a personal resume website with a dynamic visitor counter on AWS. It showcases a full-stack approach, from static website hosting to a robust serverless API.

## Live Demo

* **View Live Resume:** [https://resumejamesyoum.com](https://resumejamesyoum.com)
* **GitHub Repository:** [https://github.com/jyoum3/cloud-resume-project-jamesyoum](https://github.com/jyoum3/cloud-resume-project-jamesyoum)

## Features

* **Static Website Hosting:** Professional resume served globally.
* **Dynamic Visitor Counter:** Increments and displays the number of unique visits.
* **HTTPS Security:** Ensures secure communication.
* **Content Delivery Network (CDN):** Fast content delivery worldwide.
* **Serverless Backend:** Cost-effective and scalable API for the counter.
* **Infrastructure as Code (IaC):** Backend defined and deployed via AWS SAM.
* **Continuous Integration/Continuous Delivery (CI/CD):** Automated deployments using GitHub Actions.

## Architecture

The project's architecture is divided into a static frontend and a serverless backend:

### Frontend:

The resume's static files (HTML, CSS, JavaScript) are hosted on **Amazon S3**. This content is distributed globally and securely via **Amazon CloudFront**, which also handles HTTPS using a certificate from **AWS Certificate Manager (ACM)**. **Amazon Route 53** manages the custom domain name, directing traffic to the CloudFront distribution.

### Backend (Serverless Visitor Counter):

The dynamic visitor counter is powered by a **Python AWS Lambda function**. This function interacts with **Amazon DynamoDB** to store and retrieve the visitor count. The Lambda function is exposed to the internet via **Amazon API Gateway**, which acts as a secure, scalable HTTP endpoint and handles **CORS (Cross-Origin Resource Sharing)**.

### CI/CD:

**GitHub Actions** pipelines automate the deployment process. One pipeline synchronizes frontend changes to S3 and invalidates CloudFront cache. Another pipeline builds and deploys the serverless backend (Lambda, API Gateway) using AWS SAM CLI.

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript
* **AWS Services:** Amazon S3, Amazon CloudFront, Amazon Route 53, AWS Certificate Manager (ACM), AWS Lambda, Amazon API Gateway, Amazon DynamoDB, AWS IAM
* **Development Tools:** Python, AWS SAM (Serverless Application Model) CLI, Git, GitHub, GitHub Actions
* **Libraries:** `boto3` (Python SDK for AWS), `Flask-CORS` (for initial Flask testing, though replaced by API Gateway CORS)

## The Journey: A Cloud Resume Evolution

This project wasn't just about deploying a resume; it was a hands-on journey through various cloud deployment strategies and troubleshooting challenges.

### 1. Initial Frontend Setup:

* The foundation began with setting up the static resume in HTML/CSS.
* It was then hosted on **Amazon S3**, delivered through **CloudFront**, and secured with **HTTPS via ACM and Route 53**. This established the robust and scalable frontend.

### 2. Backend Iteration 1: Local Kubernetes (Minikube)

* Initially, the dynamic visitor counter (a Python Flask application) was containerized with **Docker** and deployed to a **local Kubernetes cluster (Minikube)**.

* **Challenge:** While great for learning Kubernetes, this setup proved impractical for a live, publicly accessible website due to:
    * **Cost:** Running a full Kubernetes cluster (even locally simulated) and potentially transitioning to AWS EKS would incur significant, continuous costs.
    * **Accessibility:** A local Minikube cluster is not directly accessible from the public internet, meaning the live website's counter wouldn't work.
    * **Complexity:** Managing a Kubernetes cluster for a simple counter was overkill.

### 3. Backend Iteration 2: Serverless Transformation (AWS Lambda & API Gateway)

* Recognizing the limitations, the backend was re-architected to a **serverless model**.
* The Flask application logic was refactored into an **AWS Lambda function** (Python).
* **Amazon API Gateway** was introduced to provide a public, scalable HTTP endpoint for the Lambda function.
* **Amazon DynamoDB** remained the persistent data store for the counter.
* **Benefit:** This approach significantly reduced operational overhead and cost, aligning with best practices for simple, event-driven APIs.

### 4. Deployment Automation (CI/CD with GitHub Actions):

* To streamline updates, **GitHub Actions** workflows were implemented:
    * A **Frontend Workflow** automates syncing `index.html`, `style.css` to S3 and invalidating CloudFront's cache on every push to the `frontend/` directory.
    * A **Backend Workflow** automates the build and deployment of the serverless Lambda and API Gateway using **AWS SAM CLI** on pushes to the `backend/` directory or `template.yaml`.

### 5. Key Debugging & Learning Points:

* **Git Stubbornness:** Overcoming issues where local Git wouldn't recognize file changes, requiring explicit staging and even repository re-creation.
* **PowerShell Syntax:** Adapting Git and AWS CLI commands for PowerShell's specific syntax (e.g., backticks for line continuation).
* **SAM CLI Errors:** Troubleshooting common SAM CLI build and deployment failures, including:
    * `NoneType` errors (due to empty `template.yaml` or incorrect `CodeUri` path).
    * Python runtime mismatches (`python3.9` vs. `python3.13`).
    * Lambda reserved environment variable conflicts (`AWS_REGION`).
    * CloudFormation stack conflicts (`resource already exists`).
* **CORS (Cross-Origin Resource Sharing):** Correctly configuring CORS headers in both the Lambda function and API Gateway to allow secure communication between the frontend (on the custom domain) and the backend API.
* **API URL Management:** Ensuring the frontend's JavaScript correctly referenced the new API Gateway endpoint URL.

This iterative process and the challenges overcome highlight practical skills in cloud architecture, serverless development, containerization (initial exploration), CI/CD, and critical troubleshooting.

## Setup & Deployment 

To replicate or set up this project:

### Frontend Deployment

1.  **Create an S3 Bucket:** For static website hosting.
2.  **Configure CloudFront:** Create a distribution pointing to the S3 bucket.
3.  **Request ACM Certificate:** For your custom domain, and attach to CloudFront.
4.  **Update Route 53:** Create Alias records pointing your custom domain to CloudFront.
5.  **GitHub Actions:** Configure `deploy-frontend.yml` with your S3 bucket name and CloudFront Distribution ID, and set up `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as GitHub Secrets.
6.  **Push `frontend/` code:** Changes to `frontend/` will automatically deploy.

### Serverless Backend Deployment

1.  **Create DynamoDB Table:** Named `ResumeVisitorCounter` with `id` as primary key (String).
2.  **Update `backend/lambda_function.py`:** Ensure `Access-Control-Allow-Origin` is set to your CloudFront domain.
3.  **Update `template.yaml`:**
    * Set `DynamoDBTableName` default to `ResumeVisitorCounter`.
    * Set `Runtime` to `python3.13`.
    * Set `AllowOrigin` in `Cors` to your CloudFront domain.
4.  **GitHub Actions:** Configure `deploy-backend.yml` with your AWS region and stack name, and ensure AWS credentials are in GitHub Secrets.
5.  **Push `backend/` code or `template.yaml`:** Changes will automatically build and deploy the Lambda and API Gateway.

## Monitoring

Key AWS services to monitor via Amazon CloudWatch for performance, cost, and errors:

* **Frontend:** S3 (storage, requests), CloudFront (requests, data transfer, cache hit ratio).
* **Backend:** Lambda (invocations, errors, duration), API Gateway (invocations, latency, errors), DynamoDB (RCU/WCU consumption, throttles).
* **Deployment:** CloudFormation (stack status).

## Future Enhancements

* Implement unit and integration tests for the Lambda function.
* Add more sophisticated logging and monitoring dashboards in CloudWatch.
* Explore custom domain setup for API Gateway (requires additional ACM certificate and Route 53 configuration).
* Expand the resume content with more dynamic sections.

## Credits

* Inspired by the original Cloud Resume Challenge by Forrest Brazeal.
