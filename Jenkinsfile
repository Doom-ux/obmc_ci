pipeline {
  agent none
  options {
    buildDiscarder(logRotator(numToKeepStr:'10', artifactNumToKeepStr:'10', daysToKeepStr:'20', artifactDaysToKeepStr:'20'))
  }
  stages {
    stage("Test") {
      agent any
      steps {
        sh """
        . /venv_obmc/bin/activate
        qemu-system-arm -m 256 -M romulus-bmc -nographic -serial none -monitor none -drive file=/home/dima/agent/workspace/obmc_webui/romulus/obmc-phosphor-image-romulus-20250214213550.static.mtd,format=raw,if=mtd -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu
      """
      }
    }
  }
}
