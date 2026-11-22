pipeline {
    agent any
    parameters {
        string(name: 'BUILD_NUMBER', defaultValue: '1.0.0-dev', description: 'Номер билда')
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Запускать линтер ruff')
    }
    stages {
        stage('Get Commit') {
            steps {
                script {
                    def scmVars = checkout scm
                    env.GIT_COMMIT_HASH = scmVars.GIT_COMMIT
                }
                echo "тэг: ${params.BUILD_NUMBER}_${env.GIT_COMMIT_HASH}"
            }
        }
    }
}
    
