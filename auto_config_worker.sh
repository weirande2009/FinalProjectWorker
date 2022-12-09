sudo apt update
sudo apt -y install python3-pip
python3 -m pip install virtualenv
python3 -m virtualenv worker
source worker/bin/activate
pip install opencv-python-headless
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
cd worker
git clone https://github.com/weirande2009/FinalProjectWorker.git
cd FinalProjectWorker


