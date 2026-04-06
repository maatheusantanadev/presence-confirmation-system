git clone https://github.com/maatheusantanadev/presence-confirmation-system.git
cd presence-confirmation-system

python -m venv venv
source venv/bin/activate
    
pip install -r requirements.txt
uvicorn main:app --reload

python -m unittest <caminho do arquivo>
    