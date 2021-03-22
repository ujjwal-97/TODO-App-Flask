# TODO-App-Flask using flask, docker and kubernetes

To use app locally or directly with containers change app.py with
app.config[“MONGO_URI”] = “mongodb://localhost:27017/dev”

To use just docker without kubernetes use following commands:
  Build the image 
    docker build -t tasksapp .
  Create Network
    docker network create tasksapp-net
  Create mongo container and attach with the network
    docker run --name=mongo -d --network=taskapp-net mongo
  Create the docker container app and attach it to the mongo container along with exposing the ports
    docekr run --name=todoapp --rm -p 5000:5000 -d --network=tasksapp-net tasksapp
    
To use with the kubernetes just create the objects with all the different yaml files in order
1. tasksapp.yaml
2. tasksapp-svc.yaml
3. mongo-pv.yaml
4. mongo-pvc.yaml
5. mongo.yaml
6. mongo-svc.yaml
