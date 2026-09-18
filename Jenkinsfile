pipeline {

    agent any

    environment {
        DOCKER_IMAGE = 'devhub01553/user-service'
        DOCKER_REGISTRY = 'https://index.docker.io/v1/'
        IMAGE_TAG = "${BUILD_NUMBER}"
        TEST_CONTAINER = "user-service-test-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build \
                      -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                      -t ${DOCKER_IMAGE}:latest \
                      .
                """
            }
        }

        stage('Run Tests') {
            steps {
                sh """
                    docker run -d \
                      --name ${TEST_CONTAINER} \
                      -p 5001:5000 \
                      ${DOCKER_IMAGE}:${IMAGE_TAG}
                """

                sh """
                    sleep 5
                    curl --fail http://localhost:5001/health
                    curl --fail http://localhost:5001/users
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh """
                        echo "${DOCKER_PASSWORD}" | docker login \
                          --username "${DOCKER_USERNAME}" \
                          --password-stdin

                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/ingress.yaml

                    kubectl set image deployment/user-service \
                      user-service=${DOCKER_IMAGE}:${IMAGE_TAG}

                    kubectl rollout status deployment/user-service \
                      --timeout=180s
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                    kubectl get deployment user-service
                    kubectl get pods -l app=user-service
                    kubectl get service user-service
                    kubectl get ingress my-app-ingress
                """
            }
        }
    }

    post {
        always {
            sh """
                docker rm -f ${TEST_CONTAINER} 2>/dev/null || true
                docker logout 2>/dev/null || true
            """

            cleanWs()
        }
    }
}
