pipeline {
    agent { docker { image 'python:3.15.2-alpine3.24' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
