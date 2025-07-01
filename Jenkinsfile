pipeline {
    agent any

    // Define input parameters
    parameters {
        string(name: 'USERNAME', defaultValue: 'admin', description: 'Enter your username')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run the tests?')
        booleanParam(name: 'RUN_DEPLOY', defaultValue: true, description: 'Run the deploy stage?')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Choose the environment')
    }

    // Define environment variables
    environment {
        APP_NAME = 'TrustBot'
        VERSION = '1.0.0'
    }

    stages {
        stage('Init') {
            steps {
                echo " Username: ${params.USERNAME}"
                echo " Environment: ${params.ENVIRONMENT}"
                echo " App: ${env.APP_NAME} v${env.VERSION}"
            }
        }

        stage('Build') {
            steps {
                echo '🔧 Building the application...'
                // Add your build commands here
            }
        }

        stage('Test') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                echo ' Running tests...'
                // Add test commands here
            }
        }

        stage('Deploy') {
            when {
                expression { return params.RUN_DEPLOY }
            }
            steps {
                echo " Deploying ${env.APP_NAME} to ${params.ENVIRONMENT}..."
                // Add deploy commands here
            }
        }

        stage('Done') {
            steps {
                echo ' Pipeline completed successfully!'
            }
        }
    }

    post {
        success {
            echo ' Job finished with SUCCESS!'
        }
        failure {
            echo ' Job FAILED. Check the logs.'
        }
    }
}
