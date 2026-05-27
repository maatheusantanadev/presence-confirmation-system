from pyngrok import ngrok

# troque pelo seu token atual
ngrok.set_auth_token("35dBwf8KUl5IKp4TkNCTOA8l3Z3_48johR8gnKv2fPu1pWGXf")

public_url = ngrok.connect(8000)

print("Acesse seu backend em:", public_url)

input("Pressione Enter para fechar...")