pipeline {
    // На учебном узле Jenkins уже есть Docker CLI с доступом к jenkins-docker.
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Запускать линтер ruff')
        string(name: 'IMAGE_VERSION', defaultValue: '1.0.0-dev', trim: true,
               description: 'Необязательный префикс тега, например 1.0.0-dev')
    }

    environment {
        REGISTRY_HOST = 'lab-registry:5000'
        NOTIFY_TO = 'me@lab.local'
    }

    stages {
        stage('Python CI') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }

            environment {
                // Кэши лежат в общем workspace, доступном на запись.
                UV_CACHE_DIR = '.uv-cache'
                PIP_CACHE_DIR = '.pip-cache'
                PIP_DISABLE_PIP_VERSION_CHECK = '1'
                UV_PYTHON_DOWNLOADS = 'never'
                UV_VERSION = '0.11.32'
            }

            stages {
                stage('Setup') {
                    steps {
                        sh '''
                            python --version
                            python -m venv .tools
                            .tools/bin/pip install "uv==${UV_VERSION}"
                            .tools/bin/uv sync --locked
                        '''
                    }
                }

                stage('Checks') {
                    parallel {
                        stage('Lint') {
                            when { expression { params.RUN_LINT != false } }
                            steps {
                                sh '.tools/bin/uv run --locked ruff check .'
                            }
                        }
                        stage('Test') {
                            steps {
                                sh '.tools/bin/uv run --locked pytest -v --junitxml=reports/junit.xml'
                            }
                        }
                    }
                }
            }
        }

        stage('Build and Push') {
            steps {
                // Шаг выполняется на узле Jenkins, с тем же workspace и доступом к DinD.
                sh '''
                    set -eu
                    short_sha="$(git rev-parse --short=7 HEAD)"
                    image_tag="${BUILD_NUMBER}-${short_sha}"
                    if [ -n "${IMAGE_VERSION:-}" ]; then
                        image_tag="${IMAGE_VERSION}-${image_tag}"
                    fi
                    image_ref="${REGISTRY_HOST}/demo-service:${image_tag}"

                    docker build -t "$image_ref" .
                    docker push "$image_ref"
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
        }
        failure {
            mail to: "${env.NOTIFY_TO}",
                 subject: "Упала сборка ${currentBuild.fullDisplayName}",
                 body: "Лог: ${env.BUILD_URL}console"
        }
        fixed {
            mail to: "${env.NOTIFY_TO}",
                 subject: "Сборка снова зелёная: ${currentBuild.fullDisplayName}",
                 body: "${env.BUILD_URL}"
        }
    }
}
