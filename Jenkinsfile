pipeline {
  agent any

  environment {
    AWS_REGION    = "us-east-1"
    ECR_BACKEND   = "ai-fitness-coach_backend"
    ECR_FRONTEND  = "ai-fitness-coach_frontend"
    EKS_CLUSTER   = "ai-fitness-coach_zeks"
    NAMESPACE     = "ai-fitness-coach"
    K8S_MANIFEST_DIR = "ai-fitness-coach-mlops/K8s"
  }

  stages {

    stage('Clean Workspace') {
      steps { cleanWs() }
    }

    stage('Checkout Code') {
      steps { checkout scm }
    }

    stage('Build Docker Images') {
      steps {
        sh """
          docker build -t ${ECR_BACKEND}:${BUILD_NUMBER} ./backend
          docker build -t ${ECR_FRONTEND}:${BUILD_NUMBER} ./frontend
        """
      }
    }

    stage('Login to ECR & Push Images') {
      steps {
        withCredentials([[ $class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds' ]]) {
          script {

            // Get AWS Account ID dynamically
            def accountId = sh(
              script: "aws sts get-caller-identity --query 'Account' --output text",
              returnStdout: true
            ).trim()
            env.AWS_ACCOUNT_ID = accountId

            // Use BUILD_NUMBER as image tag
            def tag = BUILD_NUMBER
            env.BUILD_TAG = tag

            // Login to ECR
            sh """
              aws ecr get-login-password --region ${AWS_REGION} | \
                docker login --username AWS --password-stdin ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com
            """

            // Tag + Push backend image
            sh """
              docker tag ${ECR_BACKEND}:${tag} ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND}:${tag}
              docker push ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND}:${tag}
            """

            // Tag + Push frontend image
            sh """
              docker tag ${ECR_FRONTEND}:${tag} ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND}:${tag}
              docker push ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND}:${tag}
            """
          }
        }
      }
    }

    stage('Deploy to EKS') {
      steps {
        withCredentials([[ $class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds' ]]) {
          script {

            // Generate kubeconfig dynamically
            sh """
              aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER}
            """

            // Create Kubernetes secret dynamically (OpenAI KEY)
            withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
              sh """
                kubectl -n ${NAMESPACE} create secret generic openai-secret \
                  --from-literal=OPENAI_API_KEY=${OPENAI_API_KEY} \
                  --dry-run=client -o yaml | kubectl apply -f -
              """
            }

            // Apply all manifests except secret
            sh """
              kubectl apply -f ${K8S_MANIFEST_DIR}/namespace.yaml
              kubectl apply -f ${K8S_MANIFEST_DIR}/configmap.yaml
              kubectl apply -f ${K8S_MANIFEST_DIR}/backend-service.yaml
              kubectl apply -f ${K8S_MANIFEST_DIR}/frontend-service.yaml
              kubectl apply -f ${K8S_MANIFEST_DIR}/backend-deployment.yaml
              kubectl apply -f ${K8S_MANIFEST_DIR}/frontend-deployment.yaml
            """

            // Update backend image
            sh """
              kubectl -n ${NAMESPACE} set image deployment/fitness-backend \
                fitness-backend=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_BACKEND}:${BUILD_TAG} --record
              kubectl -n ${NAMESPACE} rollout status deployment/fitness-backend --timeout=180s
            """

            // Update frontend image
            sh """
              kubectl -n ${NAMESPACE} set image deployment/fitness-frontend \
                fitness-frontend=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_FRONTEND}:${BUILD_TAG} --record
              kubectl -n ${NAMESPACE} rollout status deployment/fitness-frontend --timeout=180s
            """
          }
        }
      }
    }

    stage('Docker Cleanup') {
      steps { sh "docker system prune -af" }
    }

  }

  post {
    success {
      echo "🚀 Deployment Successful for Build ${BUILD_NUMBER}"
    }
    failure {
      echo "❌ Deployment Failed"
    }
  }
}
