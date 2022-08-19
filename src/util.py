def initThead():
    thead = []
    thead.append("<thead>")
    thead.append("<tr>")

    thead.append(setTbodyTag("td", "index"))
    thead.append(setTbodyTag("td", "type"))
    thead.append(setTbodyTag("td", "name"))
    thead.append(setTbodyTag("td", "price"))
    thead.append(setTbodyTag("td", "img"))
    thead.append(setTbodyTag("td", "gift_name"))
    thead.append(setTbodyTag("td", "gift_price"))
    thead.append(setTbodyTag("td", "gift_img"))

    thead.append("</tr>")
    thead.append("</thead>")

    return thead

def initTbody():
    tbody = []
    tbody.append("<tbody>")
    tbody.append("</tbody>")

    return tbody


def setTbodyTag(tag, dat):
    return f"<{tag}>{dat}</{tag}>"

def setImgTag(src):
    return f"<img src='{src}' style='width: 20px; height: 20px'/>"

def makeTable(vender):
    datas = []
    thead = initThead()
    tbody = initTbody() 

    index = 1
    for legend, legend_datas in vender.items():
        for product_name, product_data in legend_datas.items():
            data = []
            tbody.insert(-1, "<tr>")

            tbody.insert(-1, setTbodyTag("td", index))
            index += 1
            tbody.insert(-1, setTbodyTag("td", legend))
            tbody.insert(-1, setTbodyTag("td", product_name))

            tbody.insert(-1, setTbodyTag("td", product_data['price']))
            tbody.insert(-1, setTbodyTag("td", setImgTag(product_data['img'])))

            data.append(legend)
            data.append(product_name)

            data.append(product_data['price'])
            data.append(product_data['img'])

            if product_data['gift'] != None:                
                for gift_name, gift_data in product_data['gift'].items():
                    tbody.insert(-1, setTbodyTag("td", gift_name))
                    
                    tbody.insert(-1, setTbodyTag("td", gift_data['price']))
                    tbody.insert(-1, setTbodyTag("td", setImgTag(gift_data['img'])))

                    data.append(gift_name)
                    data.append(gift_data['price'])
                    data.append(gift_data['img'])
            else:
                data.append('null')
                data.append(0)
                data.append('null')

            tbody.insert(-1, "</tr>")
            datas.append(data)

    table = thead + tbody
    table.insert(0, "<table>")
    table.append("</table>")

    return table, datas

def pushDataToDB(sql_conn, datas):
    sql = sql_conn.cursor()

    sql_query = "TRUNCATE crawledData"
    sql.execute(sql_query)
    sql_conn.commit()

    sql_query = "INSERT INTO crawledData (pType, pName, pPrice, pImg, gName, gPrice, gImg) VALUES "
    sql_data = []

    idx = 1
    for data in datas:
        if idx % 100 == 0:
            sql.execute(sql_query + ", ".join(sql_data) + ";")
            sql_conn.commit()
            sql_data = []
            idx = 1
            
        sql_value = "("
        sql_value += ",".join([ f'"{x}"' for x in data ])
        sql_value += ")"

        sql_data.append(sql_value)
        idx += 1

    if len(sql_data) > 0:
        sql_query += ", ".join(sql_data) + ";"
        sql.execute(sql_query)
        sql_conn.commit()