pipeline{
    agent any

    environment{
        VENV_DIR = "venv"
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
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
    }
}