pipeline{
    agent any

    stages{
        stage('Cloning GitHub repo to Jenkins'){
            steps{
                echo 'Cloning the GitHub repo...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/SasanDilanthaSTD/ml-ops-project-01-with-gcp.git']])
            }
        }
    }
}