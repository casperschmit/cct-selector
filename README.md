# CCT Selector

## Description
This web application serves as a proof-of-concept of the CCT selector tool as described in the accompanied thesis. 
The aim of this tool is to assist dApp developers in the selection of cross-chain technologies (CCT). 
In order to account for the continuously evolving CCTs in the field of blockchain interoperability, 
the application is linked to an open database where new information on CCTs can be appended. 
New information will first be judged by curators before it is considered by the system.

When first visiting this web application we suggest you register an account and browse to the 'wizard' tab afterwards. 
This Wizard will aks you several questions. The answers to these questions are used to construct a relative ranking of the CCTs, 
where the highest ranked ones may fit your cross-chain scenario best.


## Installation
In order to install and run the system locally you may clone
this repository and install requirements by: `pip3 install -r requirements.txt`.

After all requirements have been successfully installed you can run the
`application.py` script in order to host the flask web app. In this same script you
are able to change the hosting port and whether or not you would like to deploy the app in debug mode.

## License
MIT License referenced in the `LICENSE.md` file.
