from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == "PC1":
            return request.args.get('hub.challenge')
        else:
          return "Error"

    data=request.get_json()
    telefonoW=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']

    if mensaje is not None:
        from rivescript import RiveScript
        bot = RiveScript()
        bot.load_file('./bbva.rive')
        bot.sort_replies()
        respuesta1= bot.reply("localuser",mensaje)
        respuesta1=respuesta1.replace("\\n","\\\n")
        respuesta1=respuesta1.replace("\\","")

        if(respuesta1=="error"):
          # Uso de ChapGPT en Python
          import openai
          openai.api_key = "tokem"
          model_engine = "text-davinci-003"
          prompt = mensaje
          completion = openai.Completion.create(engine=model_engine,
                                              prompt=prompt,
                                              max_tokens=1024,
                                              n=1,
                                              stop=None,
                                              temperature=0.7)
          respuesta=""
          for choice in completion.choices:
              respuesta=respuesta+choice.text
              print(f"Response: %s" % choice.text)
          respuesta=respuesta.replace("\\n","\\\n")
          respuesta=respuesta.replace("\\","")
        else:
           respuesta=respuesta1
        #Nos conectamos a MySQL
        import mysql.connector
        mydb = mysql.connector.connect(
          host = "mysql-chatbotpc1bbva.alwaysdata.net",
          user = "310856",
          password = "johan2027",
          database='chatbotpc1bbva_bot'
        )
        myregistro = mydb.cursor()
        query="SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';"
        myregistro.execute(query)
        cantidad, = myregistro.fetchone()
        cantidad=str(cantidad)
        cantidad=int(cantidad)
        if cantidad==0 :
            sql = ("INSERT INTO registro"+ 
            "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
            "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoW+"');")
            myregistro.execute(sql)
            mydb.commit()
            enviar(telefonoW,respuesta)
        #RETORNAMOS EL STATUS EN UN JSON
        return jsonify({"status": "success"}, 200)
#INICIAMSO FLASK
def enviar(telefonoRecibe,respuesta):
  from heyoo import WhatsApp
  token='EAAIs3pxXvSABAHPsSOTwZAgrToHaBBSminZBpUVIIwUtn2mR27mUxSZBllt5EVoW7xDw9STi86atomZAVkd3zXz6Jde2ZCslJRQPXVSnNY12beUdMgZCyYtuHzgyFSuhmHkPlmW3ZCxJwrZBuFkzSCGcWfNMcQR73PDFzbuAxlALqmDyCtTzTOhY6ZBjZAXDq0wtR4G66HkskuMgZDZD'
  idNumeroTeléfono='111479671928276'
  mensajeWa=WhatsApp(token,idNumeroTeléfono)
  mensajeWa.send_message(respuesta,telefonoRecibe)

if __name__ == "__main__":
  app.run(debug=True)
