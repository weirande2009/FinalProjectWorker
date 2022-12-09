Follow the instructions to run the workers:
make sure that you have reserved GENI resources by file Rspec
1. wget https://raw.githubusercontent.com/weirande2009/FinalProjectWorker/master/auto_config_worker.sh
2. chmod +x auto_config_worker.sh
3. ./auto_config_worker.sh
4. source worker/bin/activate
5. cd worker
6. cd FinalProjectWorker
7. nohup python3 main.py 10.10.x.1 35410 (where 10.10.x.1 is the ip address of the worker)

