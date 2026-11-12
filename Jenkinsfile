// Учебный пайплайн: Checkout → Setup → Lint → Test для маленького FastAPI-сервиса.
// Все шаги выполняются внутри контейнера python:3.12-slim, который Jenkins поднимает в dind.

pipeline {
    agent {
        docker {
            // slim (Debian, glibc), а не alpine: для библиотек вроде pydantic-core
            // есть готовые сборки (wheels) под glibc, а на alpine (musl) их может не быть,
            // и pip полезет компилировать Rust-код прямо в сборке.
            image 'python:3.12-slim'
        }
    }

    options {
        timeout(time: 15, unit: 'MINUTES')               // сборка не висит бесконечно
        timestamps()                                      // время у каждой строки лога (плагин Timestamper)
        buildDiscarder(logRotator(numToKeepStr: '20'))   // хранить только 20 последних сборок
    }

    parameters {
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Запускать линтер ruff')
    }

    environment {
        // Контейнер работает от uid 1000, у которого нет своей домашней папки,
        // поэтому кэш pip кладём в workspace — туда писать можно.
        PIP_CACHE_DIR = '.pip-cache'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        NOTIFY_TO = 'me@lab.local'
    }

    stages {
        stage('Setup') {
            steps {
                // Каждый sh — отдельный процесс оболочки, поэтому venv не «активируем»,
                // а вызываем программы из него по полному пути: .venv/bin/...
                sh '''
                    python --version
                    python -m venv .venv
                    .venv/bin/pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Lint') {
            when {
                // != false, а не просто params.RUN_LINT: на самой первой сборке
                // параметр может быть ещё не зарегистрирован и прийти как null
                expression { params.RUN_LINT != false }
            }
            steps {
                sh '.venv/bin/ruff check .'
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/python -m pytest -v --junitxml=reports/junit.xml'
            }
        }
    }

    post {
        always {
            // Отчёт о тестах: в интерфейсе сборки появится раздел Test Result
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
