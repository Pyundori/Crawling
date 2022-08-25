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
    thead = initThead()
    tbody = initTbody() 

    index = 1
    for legend, legend_datas in vender.items():
        for product_name, product_data in legend_datas.items():
            tbody.insert(-1, "<tr>")

            tbody.insert(-1, setTbodyTag("td", index))
            index += 1
            tbody.insert(-1, setTbodyTag("td", legend))
            tbody.insert(-1, setTbodyTag("td", product_name))

            tbody.insert(-1, setTbodyTag("td", product_data['price']))
            tbody.insert(-1, setTbodyTag("td", setImgTag(product_data['img'])))

            if product_data['gift'] != None:                
                for gift_name, gift_data in product_data['gift'].items():
                    tbody.insert(-1, setTbodyTag("td", gift_name))
                    
                    tbody.insert(-1, setTbodyTag("td", gift_data['price']))
                    tbody.insert(-1, setTbodyTag("td", setImgTag(gift_data['img'])))

            tbody.insert(-1, "</tr>")

    table = thead + tbody
    table.insert(0, "<table>")
    table.append("</table>")

    return table