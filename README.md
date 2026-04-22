git clone https://github.com/maatheusantanadev/presence-confirmation-system.git

cd presence-confirmation-system

python -m venv venv
source venv/bin/activate
    
pip freeze > requirements.txt      
pip install -r requirements.txt
pip install 'pydantic[email]'

uvicorn main:app --reload
    

python -m unittest <caminho do arquivo>


docker compose down -v # Se já existir o container
docker compose up --build

    
