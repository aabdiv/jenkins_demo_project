pipeline {
    agent {
        label '!windows'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }
    }

    post {
        success {
            mail to: 'vadios008@gmail.com',
                subject: "success Pipeline: ${currentBuild.fullDisplayName}",
                body: "Something is good with ${env.BUILD_URL}"
        }
    }

}
