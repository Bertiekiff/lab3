pipeline {
    agent any
    stages {
        stage('Clean-up'){
            steps {
                sh 'docker rm -f flask-app nginx-proxy || true'
                sh 'docker network rm new-network || true'
            }
        }
        stage('set-up'){
            steps {
                sh 'docker network create new-network'
            }
        }       
        stage('Build'){
            steps {
                sh 'docker build -t bertiekiff/flask-app .'
            }
        }
        stage('Trivy Scan') {
            steps {
                sh 'trivy fs --format json --output trivy-results.json .'
                sh 'trivy fs --severity HIGH,CRITICAL .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d --name flask-app --network app-network bertiekiff/flask-app'
                sh 'docker run -d -p 80:80 --name nginx-proxy --network app-network -v "$(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro" nginx'
                sh 'sleep 10'
            }
        }
        stage('Test') {
            steps {
                sh 'pip install requests || pip3 install requests'
                sh 'python3 test_app.py'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'trivy-results.json', allowEmptyArchive: true
        }
    }
}
