pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        GCP_PROJECT_ID = "mlops-learn-478120"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning GitHub repo') {
            steps {
                echo 'Cloning the GitHub repo...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/SasanDilanthaSTD/ml-ops-project-01-with-gcp.git']])
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Training Pipeline') {
            steps {
                // withCredentials must be INSIDE steps
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        export PYTHONPATH=$PYTHONPATH:.
                        python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Build and Push Docker') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    // Use script block only if you need Groovy logic (if/else, loops)
                    script {
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT_ID}
                            gcloud auth configure-docker --quiet
                            docker build -t gcr.io/${GCP_PROJECT_ID}/mlops-project-01:latest .
                            export DOCKER_CLIENT_TIMEOUT=300
                            export COMPOSE_HTTP_TIMEOUT=300
                            docker push gcr.io/${GCP_PROJECT_ID}/mlops-project-01:latest
                        '''
                    }
                }
            }
        }

        
        
        stage('Deploy to Google cloud run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    // Use script block only if you need Groovy logic (if/else, loops)
                    script {
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT_ID}

                            gcloud run deploy mlops-project-01 \
                                --image gcr.io/${GCP_PROJECT_ID}/mlops-project-01:latest \
                                --platform managed \
                                --region us-central1 \
                                --allow-unauthenticated \
                                --memory 1Gi
                                --timeout 300
                        '''
                    }
                }
            }
        }
    }
}