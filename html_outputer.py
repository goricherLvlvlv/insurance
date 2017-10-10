#coding=utf8
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def outputer_html(self):
        fout = open('output.html','w',encoding="utf-8")

        fout.write("<html>")
        fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
        fout.write("<body>")
        fout.write("<table>")

        #ascii
        for data in self.datas:
            fout.write("<tr>")
            l = data['url'].split('/')

            if l[4] != "jiankangxian":
                fout.write("<td>%s</td>" % data['url'])
                fout.write("<td>%s</td>" % data['title'])
                fout.write("<td>%s</td>" % data['on_sale'])
                fout.write("<td>%s</td>" % data['info'])
                fout.write("<td>%s</td>" % data['summary'])
                # fout.write("<td>%s</td>" % data['summary'])
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()