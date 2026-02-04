pipeline{
    agent any

    environment{
        VENV_DIR = ".venv"
        GCP_PROJECT_ID = "mlops-learn-478120"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning GitHub repo to Jenkins'){
            steps{
                echo 'Cloning the GitHub repo...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/SasanDilanthaSTD/ml-ops-project-01-with-gcp.git']])
            }
        }

        stage('Setting up Python Virtual Environment and Installing Dependencies'){
            steps{
                echo 'Setting up Python Virtual Environment and Installing Dependencies...'
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GCP_APP_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR...'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GCP_APP_CREDENTIALS}

                            gcloud config set project ${GCP_PROJECT_ID}

                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT_ID}/mlops-project-01:latest .
                            docker push gcr.io/${GCP_PROJECT_ID}/mlops-project-01:latest
                        '''
                    }
                }
            }
        }
    }
}