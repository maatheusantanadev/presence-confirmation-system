from Database.database import engine
try:
    with engine.connect() as conn:
        print("✅ Conectado ao Supabase!")
except Exception as e:
    print(f"❌ Erro: {e}")