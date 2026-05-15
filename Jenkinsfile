pipeline {
    agent any
    parameters {
        booleanParam(name: 'USE_SLIM_IMAGE', defaultValue: false, description: 'Build a slimmed image?')
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('Yaqub')
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
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
        stage('Build') {
            steps {
                sh 'docker build -t bertiekiff/flask-app .'
                sh 'docker build -t bertiekiff/nginx-proxy -f Dockerfile.nginx .'
                }
        }
        stage('Image Size Gate') {
            steps {
                script {
                    def size = sh(script: "docker image inspect bertiekiff/flask-app --format='{{.Size}}'", returnStdout: true).trim().toLong()
                    def sizeMB = size / 1024 / 1024
                    echo "Image size: ${sizeMB} MB"
                    if (sizeMB > 200) {
                        unstable("Image size ${sizeMB}MB exceeds 200MB limit")
                    }
                }
            }
        }
        stage('Slim Build') {
            when { expression { return params.USE_SLIM_IMAGE } }
            steps {
                sh 'slim build --target bertiekiff/flask-app --tag bertiekiff/flask-app:slim --http-probe=false'
                script {
                    def size = sh(script: "docker image inspect bertiekiff/flask-app:slim --format='{{.Size}}'", returnStdout: true).trim().toLong()
                    echo "Slim image size: ${size / 1024 / 1024} MB"
                }
            }
        }
        stage('Unit Test') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                        python3 unit_test.py
                    '''
                }
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
                sh 'docker run -d --name flask-app --network new-network bertiekiff/flask-app'
                sh 'docker run -d -p 80:80 --name nginx-proxy --network new-network bertiekiff/nginx-proxy'
                sh 'sleep 10'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 test_app.py'
            }
        }
        stage('Tag and Push') {
            steps {
                sh 'echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin'
                sh "docker tag bertiekiff/flask-app bertiekiff/flask-app:${IMAGE_TAG}"
                sh "docker tag bertiekiff/flask-app bertiekiff/flask-app:latest"
                sh "docker push bertiekiff/flask-app:${IMAGE_TAG}"
                sh "docker push bertiekiff/flask-app:latest"
            }
        }
        stage('Collect Metadata') {
            steps {
                sh "docker image inspect bertiekiff/flask-app:${IMAGE_TAG} > image-inspect.json"
                sh "docker image ls bertiekiff/flask-app --format '{{.Repository}}:{{.Tag}} {{.Size}} {{.ID}}' > image-list.txt"
                sh "docker history bertiekiff/flask-app:${IMAGE_TAG} > image-history.txt"
            }
        }
    }
    post {
        always {
            sh 'docker logout'
            archiveArtifacts artifacts: 'trivy-results.json, image-inspect.json, image-list.txt, image-history.txt', allowEmptyArchive: true
        }
    }
}
