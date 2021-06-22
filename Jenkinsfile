pipeline {
    agent any

    triggers {
        pollSCM('*/5 * * * 1-5')
    }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    environment {
      PATH="/home/satops/miniconda3/bin:$PATH"
      scannerHome = tool 'SonarQube Scanner'
    }

    stages {

        stage ("Code pull"){
            steps{
                checkout scm
            }
        }
        stage('Build environment') {
            steps {
                // ${BUILD_TAG} is jenkins-${JOB_NAME}-${BUILD_NUMBER}
                sh '''source /home/satops/bin/conda_init.sh
                      conda env create --name ${BUILD_TAG} --file environment.yml
                      source activate ${BUILD_TAG}
                    '''
            }
        }
        stage('Test environment') {
            steps {
                sh '''source activate ${BUILD_TAG}
                      pytest --junitxml=junit.xml --cov-report xml:coverage.xml --cov-report term --cov-branch --cov
                    '''
            }
        }
        stage('Sonar') { 

            steps {
                withSonarQubeEnv('sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dsonar.login=46691cdd23be42045c4582f68c89f7f8ce847424"
                    
                }
            }
        }
    }
    post {
        always {
            sh '''conda remove --yes -n ${BUILD_TAG} --all
                 '''
        }
        failure {
            echo "Send e-mail, when failed"
        }
    }
}
