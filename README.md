# Relocation RecSys

## Goal of the project
We offer a service based on a location recommendation system for those who decide to move from their hometown.

## Target audience
In addition to people who for some reason want to move to another place, the target audience of the project are also tourists, travelers and digital nomads.

## Motivation
Sometimes it is difficult for people to choose one thing from several options. Even the question of what kind of coffee to drink in the morning causes difficulties for many. Needless to say, how difficult it is to choose a place to travel or to move for a long time. Moreover, if a trip or relocation is planned with the family, then the analysis of options and the choice of the only one become much more difficult. This is where our project appears, designed to help with the choice of a place for relocation, recommending cities according to their key parameters. Using our service, it will be much easier for the user to choose a suitable city for himself, taking into account his priorities.

## Main idea
*description of user experience*

## Data used
### Numbeo data
<img src="https://user-images.githubusercontent.com/33491221/194776467-3697d807-1260-45d4-a049-18732927274e.svg" width="40"> <img src="https://user-images.githubusercontent.com/33491221/194776636-e66bfd6a-0e0c-443c-bc7a-ec5e269d1755.svg" width="160">

Link - https://www.numbeo.com

Site numbeo.com provides crowd-sourced information on the key parameters of life in the cities of the world. For the project, parameters such as cost of living, cost of housing, quality of life, as well as data on crime, health, pollution and traffic were parsed. A more detailed description of the data and the methodology for collecting them can be found on the website. The method of parsing the received data is given in the notebook "numbeo_parser.ipynb".

### WHO data

<img src="https://user-images.githubusercontent.com/33491221/194779381-9c40ca4a-0fe5-4faa-814d-cf201b00bc5f.png" width="160">

Link - https://www.who.int/data/gho/data/themes/air-pollution/who-air-quality-database#cms

The website of the World Health Organization provides a wide range of datasets related to the health of the population of the countries of the world. The project used a dataset of air quality in cities around the world. The remaining datasets provided general information about the countries of the world, which is not enough for the task.


