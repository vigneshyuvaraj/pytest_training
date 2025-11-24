pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh """
                    python3 -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then
                        python3 -m pip install -r requirements.txt
                    fi
                """
            }
        }

        stage('Run pytest') {
            steps {
                sh """
                    pytest -m "smoke" --junitxml=test-results/pytest-results.xml
                """
            }
        }
    }

    post {
        always {
            junit 'test-results/pytest-results.xml'
        }
    }
}