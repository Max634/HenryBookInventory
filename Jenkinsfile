pipeline
{
  agent any
  stages{
    stage('Checkout'){
      steps{
        git branch: 'main', url: 'https://github.com/Max634/HenryBookInventory'
      }
    }
    stage('Login to ECR'){
      steps{
        withAWS(region: 'us-east-1',credentials: 'aws-creds'){
          powershell '''
          $password = aws ecr get-login-password --region us-east-1
          docker login --username AWS --password $password 842112866380.dkr.ecr.us-east-1.amazonaws.com
          '''
        }
      }
    }
    stage('Build Docker Image'){
      steps{
        powershell '''
        docker build -t HenryBookInventory:django .
        docker tag HenryBookInventory:django 842112866380.dkr.ecr.us-east-1.amazonaws.com/henrybookstore
        '''
      }
    }
    stage('Push Docker Image'){
      steps{
        powershell '''
        docker push 842112866380.dkr.ecr.us-east-1.amazonaws.com/henrybookstore
        '''
      }
    }
  }
}