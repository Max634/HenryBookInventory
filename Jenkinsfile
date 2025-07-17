pipeline {
    agent any
    
    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '842112866380'
        ECR_REPOSITORY = 'test'                  // Back to your original name
        IMAGE_TAG = 'django'                     // Back to your original tag
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Max634/HenryBookInventory'
            }
        }
        
        stage('Login to ECR') {
            steps {
                withAWS(region: "${AWS_REGION}", credentials: 'aws-creds') {
                    powershell '''
                        $password = aws ecr get-login-password --region $env:AWS_REGION
                        docker login --username AWS --password $password $env:ECR_URI
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                powershell '''
                    docker build -t $env:ECR_REPOSITORY:$env:IMAGE_TAG .
                    docker tag $env:ECR_REPOSITORY:$env:IMAGE_TAG $env:ECR_URI/$env:ECR_REPOSITORY:$env:IMAGE_TAG
                '''
            }
        }
        
        stage('Push Docker Image') {
            steps {
                powershell '''
                    docker push $env:ECR_URI/$env:ECR_REPOSITORY:$env:IMAGE_TAG
                '''
            }
        }
    }
    
    post {
        always {
            powershell '''
                docker rmi $env:ECR_REPOSITORY:$env:IMAGE_TAG -f
                docker rmi $env:ECR_URI/$env:ECR_REPOSITORY:$env:IMAGE_TAG -f
            '''
        }
    }
}