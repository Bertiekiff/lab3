pipeline {
    agent any
    stages {
        stage('Build'){
            steps {
                sh 'rm -f helloWorld.sh'
                sh 'ls'
                sh 'touch helloWorld.sh'
                sh 'echo "#!/bin/bash" > helloWorld.sh'
                sh 'echo "echo Hello World!" >> helloWorld.sh'
                sh 'chmod +x helloWorld.sh'
                sh 'ls -l'
            }
        }
        stage('Test'){
            steps {
                sh './helloWorld.sh'
                sh 'pwd'
            }
        }
        stage('Deploy'){
            steps {
                sh 'ls'
            }
        }
    }
}
