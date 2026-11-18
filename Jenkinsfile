// Тот же пайплайн, но зависимости ставятся через uv строго по uv.lock.

pipeline {
    agent {
        docker { image 'python:3.12-slim' }
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    parameters {
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Запускать линтер ruff')
    }

    environment {
        // Как и раньше: у uid 1000 нет домашней папки, поэтому все кэши — в workspace
        UV_CACHE_DIR = '.uv-cache'
        PIP_CACHE_DIR = '.pip-cache'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        // Брать Python из образа, а не скачивать свой
        UV_PYTHON_DOWNLOADS = 'never'
        UV_VERSION = '0.11.32'
        NOTIFY_TO = 'me@lab.local'
    }

    stages {
        stage('Setup') {
            steps {
                // 1. Ставим сам uv (зафиксированной версии) в отдельное служебное окружение .tools:
                //    в системный Python пользователю uid 1000 писать нельзя.
                // 2. uv sync --locked создаёт .venv строго по uv.lock и падает,
                //    если uv.lock не соответствует pyproject.toml.
                sh '''
                    pwd
                    ls -la
                    python --version
                '''
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
