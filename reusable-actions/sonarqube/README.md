# sonarqube

This action runs the SonarQube workflow when given a SonarQube token and URL. These are preconfigured at the organization level as GitHub secrets but must be passed by the calling workflow. There is a pre-configured template in this directory that can be used as is, with the exception of updating branches to run the workflow on (should be at least the default branch of the repository).
