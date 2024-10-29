import mysql.connector
config = {
    'user': 'avnadmin',
    'password': 'AVNS_Jw69kwe1u00p9FJrgAH',
    'host': 'mysql-38e489bf-bunnyhemasaireddy-8196.b.aivencloud.com',
    'port': 13610,
    'database': 'defaultdb', 
    'auth_plugin': 'mysql_native_password'
}
con = mysql.connector.connect(**config)
cor=con.cursor()
# up="delete from secret;"
# cor.execute(up)
# ins="insert into secret values('--------------------------','------------------------------','-----------------','hsr.bunny.2004@gmail.com');"
# cor.execute(ins)
# con.commit()
cor.execute("select * from secret;")
r=cor.fetchone()
con.close()
# api_key=r[0]+'FzBzcZX'
# access_id= r[1]+'VKZLQISHY'
# app_pass=r[2]+' fpvu uwlr'
#app_email=r[3]
api_key=r[0]
api_gem=r[1]
access_id= 'AKIAQIJRRWVLLQUNDOMV'
app_pass=r[2]
app_email=r[3]


