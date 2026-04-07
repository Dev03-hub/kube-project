pipeline {
    agent any
    
    environment {
        // Docker configuration
        DOCKER_IMAGE = "devhub01553/user-service"
        DOCKER_REGISTRY = "https://index.docker.io/v1/"
        DOCKER_CREDENTIALS = "dockerhub-credentials"  // You'll create this in Jenkins
        
        // Build configuration
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // GitHub configuration
        GIT_REPO = "https://github.com/Dev03-hub/kube-project.git"
        GIT_BRANCH = "main"
    }
    
    stages {
        stage('🔍 Checkout Code') {
            steps {
                echo "📥 Cloning repository from GitHub..."
                git branch: "${GIT_BRANCH}", 
                    url: "${GIT_REPO}"
                
                sh 'ls -la'
                echo "✅ Code checkout complete!"
            }
        }
        
        stage('🔨 Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    
                    // Build the Docker image
                    dockerImage = docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}")
                    
                    echo "✅ Docker image built successfully!"
                }
            }
        }
        
        stage('🧪 Test Application') {
            steps {
                script {
                    echo "🧪 Running basic container tests..."
                    
                    // Run container to test if it starts
                    sh """
                        docker run -d --name flask-test-${BUILD_NUMBER} -p 5001:5000 ${DOCKER_IMAGE}:${IMAGE_TAG}
                        sleep 5
                        
                        # Test if Flask app is responding
                        curl -f http://localhost:5001/users || exit 1
                        
                        echo "Test passed! Flask app is running."
                        
                        # Cleanup test container
                        docker stop flask-test-${BUILD_NUMBER}
                        docker rm flask-test-${BUILD_NUMBER}
                    """
                    
                    echo "✅ Tests passed!"
                }
            }
        }
        
        stage('📤 Push to Docker Hub') {
            steps {
                script {
                    echo "📤 Pushing image to Docker Hub..."
                    
                    docker.withRegistry("${DOCKER_REGISTRY}", "${DOCKER_CREDENTIALS}") {
                        // Push with build number tag
                        dockerImage.push("${IMAGE_TAG}")
                        
                        // Also push as 'latest'
                        dockerImage.push("latest")
                    }
                    
                    echo "✅ Image pushed: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    echo "✅ Image pushed: ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('🚀 Deploy to Kubernetes') {
            steps {
                script {
                    echo "🚀 Deploying to Kubernetes cluster..."
                    
                    // Update the image in deployment
                    sh """
                        # Update deployment with new image
                        kubectl set image deployment/user-service \
                            user-service=${DOCKER_IMAGE}:${IMAGE_TAG} \
                            --record
                        
                        # Apply all K8s manifests (in case of any changes)
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        
                        # Wait for rollout to complete
                        kubectl rollout status deployment/user-service
                        
                        # Show deployment status
                        kubectl get pods -l app=user-service
                        kubectl get svc user-service
                    """
                    
                    echo "✅ Deployment complete!"
                }
            }
        }
        
        stage('✅ Verify Deployment') {
            steps {
                script {
                    echo "✅ Verifying deployment health..."
                    
                    sh """
                        # Check if pods are running
                        kubectl get pods -l app=user-service
                        
                        # Get service endpoint
                        kubectl get svc user-service
                        
                        echo "Deployment verification complete!"
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo """
            ✅✅✅ Pipeline Success! ✅✅✅
            
            🐳 Docker Image: ${DOCKER_IMAGE}:${IMAGE_TAG}
            🚀 Deployment: user-service
            📊 Build Number: ${BUILD_NUMBER}
            
            Your Flask app is now live! 🎉
            """
        }
        
        failure {
            echo """
            ❌❌❌ Pipeline Failed! ❌❌❌
            
            Build Number: ${BUILD_NUMBER}
            Check logs above for details.
            """
        }
        
        always {
            echo "🧹 Cleaning up workspace..."
            cleanWs()
        }
    }
}
