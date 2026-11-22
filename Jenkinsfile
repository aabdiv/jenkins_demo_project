pipeline {
    agent any
    parameters {
        string(name: 'BUILD_NUMBER', defaultValue: '1.0.0-dev', description: 'Номер билда')
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Запускать линтер ruff')
    }

    stages {
        stage('Get Commit Hash') {
            steps {
                script {
                    def scmVars = checkout scm
                    env.GIT_COMMIT_HASH = scmVars.GIT_COMMIT
                }
            }
        }
        stage('Run Build') {
            steps {
                script {
                    sh '''
                    curl lab-registry:5000/v2/_catalog
                    '''
                }
            }
        }
    }
}
    
