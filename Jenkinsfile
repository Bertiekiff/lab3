pipeline {
    agent any
    stages {
        stage('Clean-up'){
            steps {
                sh 'rm -f helloWorld.sh'
                sh 'ls'
                sh 'docker rm -f $(docker ps -a -q)'
            }
        }
        stage('set-up'){
            steps {
                sh 'docker network create new-network'
            }
        }       
        stage('Build'){
            steps {
                sh 'docker build -t bertiekiff/flask-app'
            }
        }
        stage('Deploy'){
            steps {
                sh 'docker run -d --name flask-app --network app-network bertiekiff/flask-app'
                sh 'docker run -d -p 80:80 --name nginx-proxy --network app-network -v \$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro nginx'
            }
        }
        stage('Test'){
            steps {
                sh 'sleep 5'
                sh 'curl localhost'
            }
        }
        }
    }
}
