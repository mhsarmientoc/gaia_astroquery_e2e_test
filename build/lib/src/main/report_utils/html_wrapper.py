class HTMLWrapper:
    """
    Super simple HTML wrapper
    """

    def __init__(self, table_data, report_title, software_version):
        self.table_data = table_data
        self.title = f'{report_title}-{software_version}'

    def make(self):

        return """<!DOCTYPE HTML>
<html lang="en">     
    <head>
        <style>
        #more {display: none;}
        </style>

        <meta charset="UTF-8">
        <meta name ="author" content="ESA ESDC archives">
        <title>GAIA E2E TEST RESULTS FOR ASTROQUERY</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body> 
    <h1>"""+self.title+"""
    </h1>
    <br/><br/>
    <div class="center">
    """+self.table_data+"""
    </div>
    </body>
</html>"""
