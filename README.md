fabic-git-deploy
==========

Deploy git source code using fabric
--------------------
It works like [Mina](https://github.com/mina-deploy/mina) but using [Fabric](https://github.com/fabric/fabric) and also works with [Fabric-bolt](https://github.com/worthwhile/fabric-bolt).

Features:
* Fast fetching and cloning source code from git repository and parallel deployment to servers
* Fast reverting git commit or rollback source code version
* Executing post-deploy commands
* Logging the deployments and support email notification to sysadmin and developer

Notes:
* Offline hosts will be ignored and warned only instead aborted
* Simple file locking, the deployment will be cancelled if there is any failures with any servers
