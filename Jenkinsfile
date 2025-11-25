pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_PRIORITY',
            choices: ['P0', 'P1', 'P2'],
            description: 'Choose which priority tests to run'
        )
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh """
                    /opt/homebrew/bin/python3.11 -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then
                        /opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
                    fi
                """
            }
        }

        stage('Run pytest') {
            steps {
                sh """
                    /opt/homebrew/bin/python3.11 -m pytest -m "${params.TEST_PRIORITY}" --junitxml=test-results/pytest-results.xml
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