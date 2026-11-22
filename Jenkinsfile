pipeline {
    agent any
    stages {
        stage('Get Commit') {
            steps {
                script {
                    def scmVars = checkout scm
                    env.GIT_COMMIT_HASH = scmVars.GIT_COMMIT
                }
                echo "Full commit hash: ${env.GIT_COMMIT_HASH}"
            }
        }
    }
}