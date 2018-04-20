import pymysql.cursors
import requests

# Connect to the DB
connection = pymysql.connect(host='us-cdbr-iron-east-05.cleardb.net',
                             user='b86f6ebcaa83e4',
                             password='bdd635b7',
                             db='heroku_177a4544d35b1a6',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
  with connection.cursor() as cursor:
    sql = "SELECT `id`, `bankId` FROM `product`"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    for item in result:
      itemId = item["id"]
      dbItemBankId = item['bankId']
      jsonurl = 'https://www.finansportalen.no/services/bank/boliglan/' + str(itemId) + '/json'
      jsonresponse = requests.get(jsonurl).json()
      jsonleverandorId = jsonresponse["leverandor"]["id"]
      print('=====================')
      print('Bank ID: ' + str(dbItemBankId))
      print('leverandor ID: '+ str(jsonleverandorId))
      if jsonleverandorId != dbItemBankId:
        print('Mismatch found, updating DB entry')
        updateSQL = """UPDATE product SET bankId={0} WHERE id={1}""".format(jsonleverandorId, itemId)
        cursor.execute(updateSQL)
        connection.commit()
        print("Database Updated")
      else:
        print('Nothing to update')
finally:
    connection.close()