pipeline {
    agent any

    environment {
        IMAGE = "madmax1406/pacer-app"
        TAG = "v${env.BUILD_NUMBER}"
    }

    stages {

        stage ('Checkout') {
            steps {
                checkout scm
            }
        }

        stage ('Build Docker Image'){
            steps {
                sh 'docker build -t $IMAGE:$TAG .'
            }
        }

        stage ('Push to Docker Hub Repo'){
            steps{
                withCredentials([usernamePassword(credentialsId: 'docker-creds', passwordVariable: 'PWD', usernameVariable: 'USERNAME')]) {
                  sh "echo $PWD | docker login -u $USERNAME --password-stdin"
                  sh "docker push $IMAGE:$TAG"
                }
            }
        }

        stage ('Update Helm Values'){
            steps {

                 sh """
                sed -i 's/tag:.*/tag: "$TAG"/' helm-chart/values.yaml
                """
            }
        }

        stage('Commit and Push changes to Github') {
            steps {
                sshagent(credentials: ['github-ssh']) {
                sh """
                    git checkout main || git checkout -b main
                    git pull origin main
                    
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins"

                    git add .
                    git commit -m "Auto bump tag to ${TAG}" || echo "Nothing to commit"

                    git remote set-url origin git@github.com:madmax1406/devops-project.git
                    git push origin main
                """
                }
            }
        }

    }
}