pipeline {
    agent any

    tools {
        git 'Git(Default)'
    }

    environment {
        PYTHON_VERSION = '3.12.5'
        PYTHON_EXE = 'C:\\Users\\ANGE\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [[$class: 'CleanCheckout']],
                    userRemoteConfigs: [[
                        credentialsId: 'ange',
                        url: 'https://github.com/At-an/Software-Quality-Tools-Project.git'
                    ]]
                ])
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    bat """
                        ${PYTHON_EXE} -m pip install --user ^
                            bcrypt==4.2.1 ^
                            blinker==1.9.0 ^
                            click==8.1.7 ^
                            coverage==7.6.8 ^
                            dnspython==2.7.0 ^
                            flake8==7.1.1 ^
                            Flask==3.1.0 ^
                            Flask-Bcrypt==1.0.1 ^
                            Flask-Login==0.6.3 ^
                            Flask-PyMongo==2.3.0 ^
                            Flask-SQLAlchemy==3.1.1 ^
                            greenlet==3.1.1 ^
                            iniconfig==2.0.0 ^
                            itsdangerous==2.2.0 ^
                            Jinja2==3.1.4 ^
                            MarkupSafe==3.0.2 ^
                            mccabe==0.7.0 ^
                            packaging==24.2 ^
                            pluggy==1.5.0 ^
                            pycodestyle==2.12.1 ^
                            pyflakes==3.2.0 ^
                            pymongo==4.10.1 ^
                            pytest==8.3.4 ^
                            pytest-cov==6.0.0 ^
                            python-dotenv==1.0.1 ^
                            SQLAlchemy==2.0.36 ^
                            typing_extensions==4.12.2 ^
                            Werkzeug==3.1.3
                    """
                }
            }
        }

        stage('Code Quality Check') {
            steps {
                script {
                    dir('C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\Integration_test') {
                        bat """
                            ${PYTHON_EXE} -m flake8 . --max-line-length=120
                        """
                    }
                }
            }
        }

        stage('Run Integration Tests') {
            steps {
                script {
                    bat """
                        REM Create directories for test results
                        mkdir test-results
                        mkdir coverage-reports
                        
                        REM Run tests with coverage
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

        stage('Generate Requirements') {
            steps {
                script {
                    bat """
                        ${PYTHON_EXE} -m pip freeze > requirements.txt
                    """
                }
            }
        }
    }

    post {
        always {
            bat 'powershell -Command "Get-ChildItem -Path . -Filter TEST-*.xml -Recurse | Format-Table"'
            junit 'test-results/*.xml'
            recordIssues enabledForFailure: true, tools: [flake8()]
            publishCoverage adapters: [coberturaAdapter('coverage-reports/coverage.xml')]
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
            echo 'Integration tests completed successfully!'
            archiveArtifacts artifacts: 'requirements.txt', fingerprint: true
            mail to: 'natanahelatankeu@gmail.com',
                 subject: 'Integration Tests Successful',
                 body: 'Integration tests have completed successfully.',
                 from: 'DESKTOP-AV1D9BH@local',
                 smtpServer: 'smtp.gmail.com',
                 smtpPort: 465,
                 useSsl: true,
                 credentialsId: 'Atan#2005'
        }
        failure {
            echo 'Integration tests failed!'
            mail to: 'natanahelatankeu@gmail.com',
                 subject: 'Integration Tests Failed',
                 body: 'Integration tests have failed. Please check the logs for more information.',
                 from: 'DESKTOP-AV1D9BH@local',
                 smtpServer: 'smtp.gmail.com',
                 smtpPort: 465,
                 useSsl: true,
                 credentialsId: 'Atan#2005'
        }
        cleanup {
            cleanWs()
        }
    }
}
