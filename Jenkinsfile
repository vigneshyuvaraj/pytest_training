pipeline {

    /******************************
     *     DOCKER AGENT
     *****************************/
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    /******************************
     *     BUILD PARAMETERS
     *****************************/
    parameters {

        choice(
            name: 'TEST_PRIORITY',
            choices: ['P0', 'P1', 'P2', 'ALL'],
            description: 'Choose pytest marker to run'
        )

        string(
            name: 'TEST_PATH',
            defaultValue: '',
            description: 'Test file or directory (e.g., tests/test_login.py). Leave empty to run entire suite.'
        )

        booleanParam(
            name: 'VERBOSE',
            defaultValue: false,
            description: 'Run pytest in verbose mode (-v)'
        )

        string(
            name: 'EXTRA_ARGS',
            defaultValue: '',
            description: 'Any additional pytest arguments (e.g., -k "login" or --lf)'
        )
    }

    /******************************
     *        PIPELINE STAGES
     *****************************/
    stages {

        stage('Install dependencies') {
            steps {
                sh """
                    pip install --upgrade pip
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                """
            }
        }

        stage('Build pytest command') {
            steps {
                script {

                    // base command
                    env.PYTEST_CMD = "pytest"

                    // add test path if user provided
                    if (params.TEST_PATH?.trim()) {
                        env.PYTEST_CMD += " ${params.TEST_PATH}"
                    }

                    // add marker (skip if ALL)
                    if (params.TEST_PRIORITY != "ALL") {
                        env.PYTEST_CMD += " -m ${params.TEST_PRIORITY}"
                    }

                    // verbose flag
                    if (params.VERBOSE == true) {
                        env.PYTEST_CMD += " -v"
                    }

                    // additional args
                    if (params.EXTRA_ARGS?.trim()) {
                        env.PYTEST_CMD += " ${params.EXTRA_ARGS}"
                    }

                    // always add junit export
                    env.PYTEST_CMD += " --junitxml=test-results/results.xml"

                    echo "Final Pytest Command: ${env.PYTEST_CMD}"
                }
            }
        }

        stage('Run pytest inside Docker') {
            steps {
                sh """
                    ${env.PYTEST_CMD}
                """
            }
        }
    }

    /******************************
     *         POST STEPS
     *****************************/
    post {
        always {
            junit 'test-results/results.xml'
            archiveArtifacts artifacts: 'test-results/**', fingerprint: true
        }
    }
}