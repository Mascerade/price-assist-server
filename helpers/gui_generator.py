
base_html = """
<nav id="nav" class="navbar fixed-top navbar-dark bg-dark" style="margin-bottom: 13px;">
    <a class="navbar-brand" href="https://binarywiz.github.io/Timeless-Apps-Website/home.html" target="_blank">
        <img src="https://dl.dropboxusercontent.com/s/7vleowye5psd2mj/only_logo_transparent_white.png?dl=0" style="max-height: 46px; max-width: 46px;">
        <span style="font-size: 18px; color: white; margin-left: 12px;"> Price Assist </span>
    </a>
    <button id="close-button" style="background-color: Transparent; background-repeat: no-repeat; border: none; outline: none;">
        <i class="material-icons pb-close" id="close-icon" style="color: white; font-size: 24px;">close</i>
    </button>
</nav>

<div id="card-container" style="margin-top: 17px;">

    <div id="card" class="card mb-3" style="max-width: 325px;">
        <div class="card-body" style="font-color: black;">
            <h4 id="retailer" class="card-title text-dark">Amazon</h4>
            <p id="base-price" class="card-text text-dark">Base Price: $549.94</p>
        </div>
        <a href="#" id="link-button" class="btn btn-primary" target="_blank">Product</a>
    </div>


"""

ending = """
</div>
"""


def gui_generator(retailers):
    global base_html
    new_html = ""
    new_html += base_html
    for retailer in retailers:
        if retailer[1].lower() == "could not find price" or retailer[1] == "undefined" or len(retailer[1]) == 0:
            pass

        else:
            new_html += card_generator(retailer[0], retailer[1], retailer[2])
    new_html += ending
    return new_html


def card_generator(retailer, price, product_address):
    card_template = """
    <div id="card" class="card mb-3" style="max-width: 325px;">
        <div class="card-body" style="font-color: black;">
            <h4 id="retailer" class="card-title text-dark">%s</h4>
            <p id="base-price" class="card-text text-dark">Base Price: %s</p>
        </div>
        <a href="%s" id="link-button" class="btn btn-primary" target="_blank">Product</a>
    </div>
    """ % (retailer, price, product_address)
    return card_template
