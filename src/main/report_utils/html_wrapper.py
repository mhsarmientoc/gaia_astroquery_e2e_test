class HTMLWrapper:
    """
    Super simple HTML wrapper
    """

    def __init__(self, table_data, report_title, software_version, current_env):
        self.table_data = table_data
        self.title = f'{report_title}-{software_version} ({current_env})'

    def make(self):

        return """<!DOCTYPE HTML>
<HTML lang="en">     
    <HEAD>
        <style>
        #more {display: none;}
        </style>

        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <META CHARSET="UTF-8">
        <META NAME ="author" content="ESA ESDC archives">
        <title>GAIA E2E TEST RESULTS FOR ASTROQUERY</title>
        <link rel="icon" href="https://www.cosmos.esa.int/o/CosmosTheme-theme/images/favicon.ico"/>
        <link rel="stylesheet" href="css/style_gacs.css">
    </head>
    <body> 
        <h1 style="width: auto;">""" + self.title + """</h1>
        <div class="mission-logo-container">
            <div class="mission-logo">
                <center><img src="./img/Gaia_logo.png"  width="250px"  alt="Gaia Mission Logo"/><br></center>
            </div>
        </div>
    """ + self.table_data + """
    </body>
</html>"""
# __end_of_class_HTMLWrapper
