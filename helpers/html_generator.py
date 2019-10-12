def generate_gui(dict_data):
    base_data = """
    <link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\">
    <link rel=\"stylesheet\" href=\"https://code.getmdl.io/1.3.0/material.indigo-pink.min.css\">
    <link href='https://fonts.googleapis.com/css?family=Raleway:400,500' rel='stylesheet
    <link rel='stylesheet' href='https://raw.githack.com/BinaryWiz/Price-Assist/master/css/retailers-popup.css'>
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootswatch/4.2.1/lux/bootstrap.min.css'>
    
    <nav id="nav" class="navbar fixed-top navbar-dark bg-dark" style="margin-bottom: 13px;">
        <a class="navbar-brand" href="https://binarywiz.github.io/Timeless-Apps-Website/home.html" target="_blank">
            <img src="https://dl.dropboxusercontent.com/s/7vleowye5psd2mj/only_logo_transparent_white.png?dl=0" style="max-height: 46px; max-width: 46px;">
            <span style="font-size: 18px; color: white; margin-left: 12px;"> Price Assist </span>
        </a>
        <button id="close-button" style="background-color: Transparent; background-repeat: no-repeat; border: none; outline: none;">
            <i class="material-icons pb-close" id="close-icon" style="color: white; font-size: 24px;">close</i>
        </button>
    </nav>
        
    <div id="card-container" style="margin-top: 98px;">
                    
    
    """

    for key, value in dict_data:
        base_data += add_card(value["name"], value["price"])
    base_data += "</div>"


def add_card(name, price):

    """
    <div id="card" class="card mb-3" style="max-width: 325px;">
        <div class="card-body" style="font-color: black;">
            <h4 id="retailer" class="card-title text-dark">{}</h4>
            <p id="base-price" class="card-text text-dark">Base Price: {}</p>
        </div>
        <a href="` + link + `" id="link-button" class="btn btn-primary" target="_blank">Product</a>
    </div>
    """.format(name, price)
