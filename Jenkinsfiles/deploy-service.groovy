#!/usr/bin/env groovy
// Copyright © 2018 Province of British Columbia
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//JENKINS DEPLOY ENVIRONMENT VARIABLES:
// - JENKINS_JAVA_OVERRIDES  -Dhudson.model.DirectoryBrowserSupport.CSP= -Duser.timezone=America/Vancouver
//   -> user.timezone : set the local timezone so logfiles report correxct time
//   -> hudson.model.DirectoryBrowserSupport.CSP : removes restrictions on CSS file load, thus html pages of test reports are displayed pretty
//   See: https://docs.openshift.com/container-platform/3.9/using_images/other_images/jenkins.html for a complete list of JENKINS env vars
//
// define constants -- set from call
NAMESPACE
COMPONENT_NAME
TAG_NAME
SOURCE_TAG

// define groovy functions
import groovy.json.JsonOutput

// Get an image's hash tag
String getImageTagHash(String imageName, String tag = "") {

  if(!tag?.trim()) {
    tag = "latest"
  }

  def istag = openshift.raw("get istag ${imageName}:${tag} -o template --template='{{.image.dockerImageReference}}'")
  return istag.out.tokenize('@')[1].trim()
}

// pipeline
// define job properties - keep 10 builds only
properties([
    [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator', artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '10'
        ]
    ]
])

node {
    echo """
    Pipeline called with constants:
        - NAMESPACE: ${NAMESPACE}
        - COMPONENT_NAME: ${COMPONENT_NAME}
        - TAG_NAME: ${TAG_NAME}
        - SOURCE_TAG: ${SOURCE_TAG}
    """
    if (COMPONENT_NAME == 'auto-analyze') {
        DEPLOYMENT_NAME = "${COMPONENT_NAME}-${TAG_NAME}"
    } else {
        DEPLOYMENT_NAME = COMPONENT_NAME
    }
    def old_version
    stage("Deploy ${COMPONENT_NAME}:${TAG_NAME}") {
        script {
            openshift.withCluster() {
                openshift.withProject("${NAMESPACE}-${TAG_NAME}") {
                    old_version = openshift.selector('dc', "${DEPLOYMENT_NAME}").object().status.latestVersion
                }
            }
            openshift.withCluster() {
                openshift.withProject() {
                    echo "Updating ${COMPONENT_NAME}-previous tag..."
                    def IMAGE_HASH = getImageTagHash("${COMPONENT_NAME}", "${TAG_NAME}")
                    echo "IMAGE_HASH: ${IMAGE_HASH}"
                    openshift.tag("${COMPONENT_NAME}@${IMAGE_HASH}", "${COMPONENT_NAME}:${TAG_NAME}-previous")

                    echo "Tagging ${COMPONENT_NAME} for deployment to ${TAG_NAME}..."
                    // Don't tag with BUILD_ID so the pruner can do it's job; it won't delete tagged images.
                    // Tag the images for deployment based on the image's hash
                    IMAGE_HASH = getImageTagHash("${COMPONENT_NAME}", "${SOURCE_TAG}")
                    echo "IMAGE_HASH: ${IMAGE_HASH}"
                    openshift.tag("${COMPONENT_NAME}@${IMAGE_HASH}", "${COMPONENT_NAME}:${TAG_NAME}")
                }
            }
        }
    }
    stage("Verify deployment") {
        sleep 90
        script {
            openshift.withCluster() {
                openshift.withProject("${NAMESPACE}-${TAG_NAME}") {
                    def new_version = openshift.selector('dc', "${DEPLOYMENT_NAME}").object().status.latestVersion
                    if (new_version == old_version) {
                        echo "New deployment was not triggered."
                        currentBuild.result = "FAILURE"
                        return
                    }
                    def pod_selector = openshift.selector('pod', [ app:"${DEPLOYMENT_NAME}" ])
                    pod_selector.untilEach {
                        pod = it.objects()[0]
                        deployment = pod.metadata.labels.deployment
                        echo deployment
                        if (deployment ==  "${DEPLOYMENT_NAME}-${new_version}" && pod.status.phase == 'Running' && pod.status.containerStatuses[0].ready) {
                            return true
                        } else {
                            echo "Pod for new deployment not ready"
                            sleep 5
                            return false
                        }
                    }
                }
            }
        }
    }
}//end node
