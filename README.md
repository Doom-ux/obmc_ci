# obmc_ci
Ознакомиться с принципами CI/CD (Continuous Integretion/Continuous Delivery) в контексте разработки и тестирования OpenBMC

## Перечисление автотестов
В набор входят следующие тесты:
- WebUI тесты OpenBMC
- Автотесты для API Redfish в системе OpenBMC
- Нагрузочные тесты OpenBMC

## Результат тестирования

### Установка и настройка Jenkins

Для автоматизирования процесса тестирования был создан Pipeline внутри системы Jenkins, которая была развернута с помощью Docker-контейнера.
Ниже описан процесс установки системы Jenkins.

1. Создание виртуальной сети и томов для хранения данных контейнера:
   ```
   docker network create jenkins
   docker volume create jenkins-docker-certs
   docker volume create jenkins-data
   ```
   
2. Создание и запуск контейнера с установленной системой Jenkins:
   ```
   docker container run \
    --name jenkins-docker \
    --detach \
    --privileged \
    --network jenkins \
    --network-alias docker \
    --env DOCKER_TLS_CERTDIR=/certs \
    --volume jenkins-docker-certs:/certs/client \
    --volume jenkins-data:/var/jenkins_home \
    --publish 2376:2376 \
    docker:dind

   docker container run \
    --name jenkins-myocean \
    --detach \
    --network jenkins \
    --env DOCKER_HOST=tcp://docker:2376 \
    --env DOCKER_CERT_PATH=/certs/client \
    --env DOCKER_TLS_VERIFY=1 \
    --publish 8080:8080 \
    --publish 50000:50000 \
    --volume jenkins-data:/var/jenkins_home \
    --volume jenkins-docker-certs:/certs/client:ro \
    jenkins/jenkins:lts-jdk17
   ```
   
3. После создания контейнера необходимо перейти в веб-интерфейс по ссылке:
   ```
   http://localhost:8080
   ```

## Настройка CI/CD
Для выполнения автоматизации также потребовалось выполнить следующую шаги:

1. Создать с помощью веб-интерфеса системы Jenkins нового объекта Pipeline.
   
2. Определить репозиторий в GitHub с необходимым набором тестов.
   
3. Создать в репозитории файл Jenkinsfile, включающий:
   - Запуск qemu с OpenBMC в Pipeline
   - Запуск автотестов для OpenBMC
   - Запуск WebUI тестов для OpenBMC
   - Запуск нагрузочного тестирования OpenBMC
   
4. Реализовать сохранение отчетов для каждого вида тестов.  

## Отчеты тестов

- Содержимое отчета для набора WebUI тестов:
   ![test_redfish_run](https://github.com/Doom-ux/obmc_ci/blob/media/media/Output_test_obmc1.png)
  
- Содержимое отчета для набора тестов API Redfish:
   ![test_redfish_run](https://github.com/Doom-ux/obmc_ci/blob/media/media/Output_test_redfish.png)
  
- Содержание отчета для набора нагрузочных тестов (количество пользователей - 10):
  - Статистические таблицы нагрузочного тестирования.
    <br><br>
    ![test_redfish_run](https://github.com/Doom-ux/obmc_ci/blob/media/media/obmc_load_tabs.png)
    
  - Статистические графики нагрузочного тестирования.
    <br><br>
    ![test_redfish_run](https://github.com/Doom-ux/obmc_ci/blob/media/media/obmc_load_charts.png)


## Структура каталогов

```
obmc_ci/
    reports/
        obmc_load.html
        test_obmc.xml
        test_redfish.xml
    romulus/
        obmc-phosphor-image-romulus-20250214213550.static.mtd
        ...
    tests/
        test_obmc1.py
        test_redfish.py
        locustfile.py
```
  

