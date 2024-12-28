pipeline {
    agent any

    environment {
        IMAGE_NAME            = "flask-app-image"
        CONTAINER_NAME        = "flask-app-container"
        VERSION               = "1.0.${env.BUILD_ID}"
        SSH_KEY_CREDENTIALS   = credentials('46d73930-675a-40eb-990d-f3039c8b0bf6')
        REGISTRY_URL          = "docker.io/atan04/flask-app-image"
        PYTHON_EXE           = "python3.12.5" // Specify Python version
        DOCKER_USERNAME       = "natanahel atankeu" // Docker Hub username
        DOCKER_PASSWORD       = credentials('ab2b0a39-0167-4955-bdc1-1a98fbfb34a4') // Docker Hub password
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo "Building Docker image..."
                    bat """
                        docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
                        docker build -t ${IMAGE_NAME}:${VERSION} .
                        docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY_URL}:${VERSION}
                        echo "Pushing Docker image to registry..."
                        docker push ${REGISTRY_URL}:${VERSION}
                    """
                }
            }
        }

        stage('Code Quality Check') {
            steps {
                script {
                    dir('C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Integration_test') {
                        bat """
                            ${PYTHON_EXE} -m flake8 --max-line-length=120
                        """
                    }
                }
            }
        }

        stage('Run Integration Tests') {
            steps {
                script {
                    bat """
                        mkdir test-results
                        mkdir coverage-reports
                        
                        ${PYTHON_EXE} -m pytest tests\\ ^
                            --verbose ^
                            --junitxml=test-results\\junit.xml ^
                            --cov=. ^
                            --cov-report=xml:coverage-reports\\coverage.xml ^
                            --cov-report=html:coverage-reports\\html
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent([SSH_KEY_CREDENTIALS]) {
                    script {
                        echo "Deploying to server..."
                        bat """
                            ssh -o StrictHostKeyChecking=no user@your-server-ip ^
                              "docker pull ${REGISTRY_URL}:${VERSION} && ^
                               docker stop ${CONTAINER_NAME} || true && ^
                               docker rm ${CONTAINER_NAME} || true && ^
                               docker run -d -p 8080:5000 --name ${CONTAINER_NAME} ${REGISTRY_URL}:${VERSION}"
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                echo "Deployment failed. Rolling back..."
                bat """
                    ssh -o StrictHostKeyChecking=no user@your-server-ip ^
                      "docker stop ${CONTAINER_NAME} && ^
                       docker rm ${CONTAINER_NAME}"
                """
            }
        }
        always {
            bat 'powershell -Command "Get-ChildItem -Path . -Filter TEST-*.xml -Recurse | Format-Table"'
            junit 'test-results/*.xml'
            recordIssues enabledForFailure: true, tools: [flake8()]
            publishCoverage adapters: [
               coberturaAdapter('coverage-reports/coverage.xml') 
            ]
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'coverage-reports/html',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
        success {
            echo 'Deployment completed successfully!'
        }
        cleanup {
            cleanWs()
        }
    }
}
