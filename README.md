# AI-Fitness-Coach-MLOps

This project was developed as a complete **MLOps portfolio project** demonstrating skills in:

- Backend development with FastAPI  
- Frontend development with Streamlit  
- Machine Learning model training and serving  
- Containerization using Docker  
- CI/CD automation using Jenkins  
- Kubernetes deployment using AWS EKS  
- Infrastructure provisioning using Terraform

The application predicts **daily calorie needs** using a trained ML model and generates personalized **workout and diet plans** using the **OpenAI API**.  
The primary focus of the project is the **MLOps architecture**, not the UI.

# Architecture Summary

Bootstrap Phase:

    1. jenkins-bootstraph/

    2. Uses Terraform to create an EC2 instance and configure jenkins in Docker - Local run

    3. Setup S3(for terraform state) and DynamoDB(for state locking)
    
    4. Installs essentials tools in the jenkins container via user data:
        Docker CLI, AWS CLI, Terraform, Kubectl, Git, Curl, Wget, Unzip 


Infrastructure Phase:

    1. Provision AWS resources for the application using Terraform run by jenkins
        * EKS cluster for Kubernetes
        * ECR Repositories for container images
        * VPC resources
        * IAM Roles and policies
    
CI/CD Phase( Jenkinsfile + Jenkinsfiles/)
    
    1. Jenkinsfiles/Jenkinsfile.infra : Pipeline script to create AWS resources 
       for the application using Terraform run by jenkins

    2. Jenkinsfile:
        * Fetch application code from SCM(Github)
        * Build Docker images for frontend and backend, pushes to ECR
        * Deploy the images to Kubernetes cluster

    3. Jenkinsfiles/Jenkinsfile.infra-destroy: Destroy infrastructure cleanly if needed

## Architecture Diagram - AI Fitness Coach

![Architecture Diagram - AI Fitness Coach](https://raw.githubusercontent.com/MJishere/ai-fitness-coach-mlops/master/Screenshots/Ai-Fitness-Coach-Application-Arc.drawio.png)

## Architecture Diagram - Bootstraphing Jenkins server

![Architecture Diagram - Bootstraphing Jenkins](https://raw.githubusercontent.com/MJishere/ai-fitness-coach-mlops/master/Screenshots/Bootstraphing-Jenkins-server.png)

## Architecture Diagram - Create Infrastructure

![Architecture Diagram - Bootstraphing Jenkins](https://raw.githubusercontent.com/MJishere/ai-fitness-coach-mlops/master/Screenshots/Jenkins-Create-Infrastrucure-Pipeline.png)

## Tech Stack

| Category             | Tools/Services                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Cloud | AWS(EC2, EKS, ECR, S3, DynamoDB, VPC, IAM) |
| CI/CD | Jenkins |
| IaC | Terraform |
| Container | Docker |
| Orchestration | Kubernetes |
| SCM | Git and Github |
| Language | Python, FAST API(Backend), Streamlit(Frontend) |
| API | OPENAI API ( gpt 4 mini ) |


## Deployment

Prerequisites:

    1. AWS Account
    2. OpenAI API key
    3. Terraform Installed locally

Project Flow:

    1. Run Jenkins Bootstraph Terraform locally

        * An Ec2 instance with Jenkins server and necessary tools required running
        * Remote backend for Terraform

    2. Create and Run Infra Pipeline (Jenkinsfiles/Jenkinsfile.infra)

        * Provision AWS infra ( IAM, ECR, EKS, VPC)

    3. Run Application Pipeline (Jenkinsfile)

        * Fetch Source code from github repo
        * Build Docker images and Push to ECR
        * Deploy to EKS
    
    4. Access Application

        * User Frontend Service Loadbalancer DNS to access the Application
        * The React frontend connects to the Node.js backend via LoadBalancer 
        service on EKS
        




## Environment Variables

To run this project, you will need to add the following environment variables to the jenkins credentials

`aws-creds` AWS Credentials, also requires AWS credentials Plugin to be installed in the Jenkins server

`OPENAI_API_KEY` OPEN AI API key -> https://platform.openai.com/


## Features

- Fully automated CI/CD using Jenkins
- Modular Terraform architecture
- Dockerized frontend and backend apps
- AWS-native deployment on EKS & ECR
- Infrastructure state management with S3 & DynamoDB
- Designed to mimic the real world MLops pipelines

## Authors

Manoj M - AWS Certified | Cloud & DevOps Engineer


## 🔗 Links

[![linkedin](https://img.shields.io/badge/github-808080?style=for-the-badge&logo=github&logoColor=grey)](https://github.com/MJishere)

[![github](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=github&logoColor=white)](https://www.linkedin.com/in/manoj-m-mj/)
