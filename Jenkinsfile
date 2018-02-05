pipeline {
    agent any

    triggers {
        pollSCM('* * * * *')
    }

    stages {

        stage('dev') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                DEV_SECURITY = credentials('DEV_SECURITY')
                CF_USER = credentials('CF_USER')
                JWT_SECRET = credentials('JWT_SECRET')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s dev"
                sh 'cf push --no-start ras-backstage-service-dev'
                sh 'cf set-env ras-backstage-service--dev ONS_ENV dev'
                sh "cf set-env ras-backstage-service--dev SECURITY_USER_NAME ${env.DEV_SECURITY_USR}"
                sh "cf set-env ras-backstage-service--dev SECURITY_USER_PASSWORD ${env.DEV_SECURITY_PSW}"
                sh "cf set-env ras-backstage-service--dev DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-backstage-service--dev DJANGO_CLIENT_SECRET password"
                sh "cf set-env ras-backstage-service--dev JWT_SECRET ${env.JWT_SECRET}"

                sh "cf set-env ras-backstage-service--dev RAS_OAUTH_SERVICE_HOST ras-django-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service--dev RAS_SECURE_MESSAGING_SERVICE_HOST ras-secure-messaging-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RAS_SECURE_MESSAGING_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service--dev RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service--dev RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service--dev RAS_SURVEY_SERVICE_HOST surveysvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RAS_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service--dev RM_SAMPLE_SERVICE_HOST samplesvc-dev.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service--dev RM_SAMPLE_SERVICE_PORT 80"

                sh 'cf start ras-backstage-service-dev'
            }
        }

        stage('ci?') {
            agent none
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            script {
                                env.deploy_ci = input message: 'Deploy to CI?', id: 'deploy_ci', parameters: [choice(name: 'Deploy to CI', choices: 'no\nyes', description: 'Choose "yes" if you want to deploy to CI')]
                            }
                        }
                    } catch (ignored) {
                        echo 'Skipping ci deployment'
                    }
                }
            }
        }

        stage('ci') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }

            }
            when {
                environment name: 'deploy_ci', value: 'yes'
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                CI_SECURITY = credentials('CI_SECURITY')
                CF_USER = credentials('CF_USER')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s ci"
                sh 'cf push --no-start ras-backstage-service-ci'
                sh 'cf set-env ras-backstage-service-ci ONS_ENV ci'
                sh "cf set-env ras-backstage-service-ci SECURITY_USER_NAME ${env.CI_SECURITY_USR}"
                sh "cf set-env ras-backstage-service-ci SECURITY_USER_PASSWORD ${env.CI_SECURITY_PSW}"
                sh "cf set-env ras-backstage-service-ci DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-backstage-service-ci DJANGO_CLIENT_SECRET password"
                sh "cf set-env ras-backstage-service-ci JWT_SECRET ${env.JWT_SECRET}"

                sh "cf set-env ras-backstage-service-ci RAS_OAUTH_SERVICE_HOST ras-django-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-ci RAS_SECURE_MESSAGING_SERVICE_HOST ras-secure-messaging-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RAS_SECURE_MESSAGING_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-ci RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-ci RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-ci RAS_SURVEY_SERVICE_HOST surveysvc-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RAS_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-ci RM_SAMPLE_SERVICE_HOST samplesvc-ci.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-ci RM_SAMPLE_SERVICE_PORT 80"
                sh 'cf start ras-backstage-service-ci'
            }
        }

        stage('test?') {
            agent none
            steps {
                script {
                    try {
                        timeout(time: 60, unit: 'SECONDS') {
                            script {
                                env.deploy_test = input message: 'Deploy to test?', id: 'deploy_test', parameters: [choice(name: 'Deploy to test', choices: 'no\nyes', description: 'Choose "yes" if you want to deploy to test')]
                            }
                        }
                    } catch (ignored) {
                        echo 'Skipping test deployment'
                    }
                }
            }
        }

        stage('test') {
            agent {
                docker {
                    image 'governmentpaas/cf-cli'
                    args '-u root'
                }

            }
            when {
                environment name: 'deploy_test', value: 'yes'
            }

            environment {
                CLOUDFOUNDRY_API = credentials('CLOUDFOUNDRY_API')
                CF_DOMAIN = credentials('CF_DOMAIN')
                TEST_SECURITY = credentials('TEST_SECURITY')
                CF_USER = credentials('CF_USER')
            }
            steps {
                sh "cf login -a https://${env.CLOUDFOUNDRY_API} --skip-ssl-validation -u ${CF_USER_USR} -p ${CF_USER_PSW} -o rmras -s test"
                sh 'cf push --no-start ras-backstage-service-test'
                sh 'cf set-env ras-backstage-service-test ONS_ENV test'
                sh "cf set-env ras-backstage-service-test SECURITY_USER_NAME ${env.TEST_SECURITY_USR}"
                sh "cf set-env ras-backstage-service-test SECURITY_USER_PASSWORD ${env.TEST_SECURITY_PSW}"
                sh "cf set-env ras-backstage-service-test DJANGO_CLIENT_ID ons@ons.gov"
                sh "cf set-env ras-backstage-service-test DJANGO_CLIENT_SECRET password"
                sh "cf set-env ras-backstage-service-test JWT_SECRET ${env.JWT_SECRET}"

                sh "cf set-env ras-backstage-service-test RAS_OAUTH_SERVICE_HOST ras-django-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RAS_OAUTH_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-test RAS_SECURE_MESSAGING_SERVICE_HOST ras-secure-messaging-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RAS_SECURE_MESSAGING_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-test RM_COLLECTION_EXERCISE_SERVICE_HOST collectionexercisesvc-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RM_COLLECTION_EXERCISE_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-test RAS_COLLECTION_INSTRUMENT_SERVICE_HOST ras-collection-instrument-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RAS_COLLECTION_INSTRUMENT_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-test RAS_SURVEY_SERVICE_HOST surveysvc-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RAS_SURVEY_SERVICE_PORT 80"

                sh "cf set-env ras-backstage-service-test RM_SAMPLE_SERVICE_HOST samplesvc-test.${env.CF_DOMAIN}"
                sh "cf set-env ras-backstage-service-test RM_SAMPLE_SERVICE_PORT 80"
                sh 'cf start ras-backstage-service-test'
            }
        }
    }

    post {
        always {
            cleanWs()
            dir('${env.WORKSPACE}@tmp') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script') {
                deleteDir()
            }
            dir('${env.WORKSPACE}@script@tmp') {
                deleteDir()
            }
        }
    }
}