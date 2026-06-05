import datetime
from random import randint
import requests
from xml.etree import ElementTree


ke = "Личный кабинет сотрудника. Оборудование"


def add(prob_name, host, model, sn, ip, contact, adr, br, rl):
    print('ЗАПУСК')
    url = "http://hd-integration.beeline.ru:9080/remedy_ws/RemedyOut?wsdl"  # prod
    # url = "https://yd-hd-int-tst.beeline.ru/remedy_ws/RemedyOut?wsdl" #test
    data = datetime.datetime.now()
    # дата создания ТТ (системное время сервера)
    IDtt = randint(4134512443, 8934512443)
    ke = "Print\Zabbix_PRNoffline"
    text_tt = f"""Полное описание: {prob_name}\n имя: {host}\n модель: {model} \n IP: {ip}\n sn: {sn}\n не доступно по сети.\n Необходим выезд специалиста."""
    body = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
          <soap:Header/>\
          <soap:Body>\
          <CreateTT xmlns="urn:gf-trouble-ticket-management">\
          <request xmlns="">\
          <activity xmlns="urn:gf-trouble-ticket-management:xsd">\
          <operationDate>2023-3-04</operationDate>\
          <systemID>15</systemID>\
          <operationId>{9}</operationId>\
          <comment>Автоматическое заведение ТТ по недоступности устройства печати  </comment>\
          <operator>tech_zbxvdi_ms</operator>\
          </activity>\
          <TTID xmlns="urn:gf-trouble-ticket-management:xsd">\
          <systemID>7</systemID>\
          <internalTTID>limon-5778353</internalTTID>\
          </TTID>\
          <generalTTInfo xmlns="urn:gf-trouble-ticket-management:xsd">\
          <creationDate>{10}</creationDate>\
          <initiatorEmployee>tech_zbxvdi_ms</initiatorEmployee>\
          <initiatorType>0</initiatorType>\
          <fullDescription>{12} </fullDescription>\
          <troubleType>{11}</troubleType>\
          <responsibleOrganizationalStructure>{8}</responsibleOrganizationalStructure>\
          <coordinatorOrganizationalStructure>ROL000000000153</coordinatorOrganizationalStructure>\
          <priority>PRI000000000006</priority>\
          <ownerSystem>0</ownerSystem>\
          <registrationSystem>0</registrationSystem>\
          <solutionState>TOPEN</solutionState>\
          <serviceState>SNAV</serviceState>\
          <responsibilityZone_Active>BEE</responsibilityZone_Active>\
          <clientType>EMPL</clientType>\
          <dependenceType>0</dependenceType>\
          <branch>{7}</branch>\
          <requestType>1</requestType>\
          <occurrenceTime>{10}</occurrenceTime>\
          </generalTTInfo>\
          <monitoringTT xmlns="urn:gf-trouble-ticket-management:xsd">\
          <objectType>EQUIP</objectType>\
          <degradationLevel>2</degradationLevel>\
          <configurationItem>WPU</configurationItem>\
          </monitoringTT>\
          <InternalUserTT xmlns="urn:gf-trouble-ticket-management:xsd">\
          <registrationMethod>SRC000000000003</registrationMethod>\
          </InternalUserTT>\
          </request>\
          </CreateTT>\
          </soap:Body>\
          </soap:Envelope>'.format(prob_name, host, model, sn, ip, contact, adr, br, rl, IDtt, data, ke, text_tt)

    body = body.encode('utf-8')
    session = requests.session()
    session.headers = {"Content-Type": "text/xml; charset=utf-8"}
#    session.headers.update({"Content-Length": str(len(body))})
    response = session.post(url=url, data=body, verify=False)
    print(response.status_code)  # код ошибки
    print(response.content)  # ответ
    root = ElementTree.fromstring(response.content)
    for child in root.iter('{urn:gf-trouble-ticket-management:xsd}internalTTID'):
        return child.text

# </soap:Envelope>'.format(city,dt,tb,fn,pf,rol,fil,coment,data,IDtt,dtt,cc)
# print(add(host,count,prob_name,dat,ke))
