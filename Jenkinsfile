pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Login to ECR') {
      steps {
        withAWS(region: 'us-east-1', credentials: 'aws-creds') {
          powershell '''
          $password = aws ecr get-login-password --region us-east-1
          docker login --username AWS --password $password 842112866380.dkr.ecr.us-east-1.amazonaws.com
          '''
        }
      }
    }
    stage('Build Docker Image') {
      steps {
        powershell '''
        docker build -t henrybookinventory:django .
        docker tag henrybookinventory:django 842112866380.dkr.ecr.us-east-1.amazonaws.com/henrybookstore
        '''
      }
    }
    stage('Push Docker Image') {
      steps {
        powershell '''
        docker push 842112866380.dkr.ecr.us-east-1.amazonaws.com/henrybookstore
        '''
      }
    }
  }
  post {
    always {
      powershell '''
      docker rmi -f henrybookinventory:django 2>$null
      docker rmi -f 842112866380.dkr.ecr.us-east-1.amazonaws.com/henrybookstore 2>$null
      '''
    }
  }
}